#!/usr/bin/python
"""
This script to be used to run liftOver on genotype data stored in
the plink format.
See: http://genome.sph.umich.edu/wiki/LiftOver
Downloaded from: http://genome.sph.umich.edu/wiki/LiftMap.py

Modified by Scott Ritchie:
 - to work with user specified chain files, rather than
   the original developer's specific chain file.
 - to not rely the original developer's path to liftOver.
 - to provide helpful usage documentation.
 - to clean up the intermediary BED files to avoid confusion.
 - to generally be slightly more PEP compliant.

Modified by Miles Smith:
 - Update to work with python >= 3.10
"""

# TODO: convert as much as possible to Rust
# TODO: Use either pyliftover or the cython-version
# TODO: maybe convert pyliftover to Rust and incorporate that?

from multiprocessing import cpu_count
from pathlib import Path
from subprocess import CalledProcessError, check_output

import numpy as np
from joblib import Parallel, delayed
from loguru import logger
from tqdm.rich import tqdm

from plinkliftover import console

DAT_LINE_LENGTH: int = 2


def lift_bed(
    fin: Path,
    fout: Path,
    chainfile: Path,
    lift_over_path: Path,
) -> tuple[set[str], set[str]]:
    """Liftover a bamfile using UCSC's LiftOver tool

    Parameters
    ----------
    fin : Path
        Location of the currect MAP file to convert
    fout : Path
        Where to save the new BED file
    chainfile : Path
        Location of the chain file to use to perform the liftover
    lift_over_path : Path
        Location of the `liftOver` executable

    Returns
    -------
    set[str]
        The names of the variants that liftOver was able to map to the new genome
    set[str]
        The names of the variants that liftOver was UNable to map
    """
    console.print(f"Lifting [green]BED[/] file [blue]{fin.name}[/]...")
    params: dict[str, str | Path] = {
        "LIFTOVER_BIN": lift_over_path.resolve(),
        "OLD": fin,
        "CHAIN": chainfile,
        "NEW": fout,
        "UNLIFTED": f"{fout}.unlifted",
    }

    try:
        check_output([str(params[_]) for _ in params])  # noqa: S603
        # record lifted/unlifted rs
        unlifted_lines = Path(params["UNLIFTED"]).read_text().split("\n")
        console.print(f"Processing [red]unlifted[/] {fout.name}.unlifted")

        unlifted_set = {ln.strip().split()[-1] for ln in tqdm(unlifted_lines) if len(ln) > 0 and ln[0] != "#"}

        console.print(f"Processing [red]new[/] {fout.name}")
        new_bed_lines = Path(params["NEW"]).read_text().split("\n")

        lifted_set = {ln.strip().split()[-1] for ln in tqdm(new_bed_lines) if len(ln) != 0 and ln[0] != "#"}

        console.print("lifting [purple]bed[/] file: [green bold]SUCCESS[/]")
        logger.info(f"lifting bed file: {fout} - SUCCESS")

        return lifted_set, unlifted_set
    except CalledProcessError as err:
        console.print("lifting [purple]bed[/] file: [red bold]FAILED[/]")
        logger.info(f"lifting bed file: {fout} - FAILED")
        msg = err.stderr
        raise RuntimeError(msg) from err


def lift_dat(fin: Path, fout: Path, lifted_set: set[str]) -> bool:
    """
    Parameters
    ----------
    fin : Path
        The original, non-uplifted DAT file
    fout : Path
        Where to place the new, uplifted and filtered DAT file
    lifted_set : set[str]
        The set of alleles `liftOver` was able to map

    Returns
    -------
    bool
        Was this successful?
    """
    console.print(f"Updating [green]DAT[/] file [pink]{fin.name}[/]...")
    dat_lines = fin.read_text().split("\n")
    output = []
    # TODO: parallellize this
    parallel = Parallel(n_jobs=cpu_count(), return_as="generator")
    output = parallel(delayed(lift_dat_loop)(line, lifted_set) for line in tqdm(dat_lines))

    console.print(f"Writing [green]new DAT[/] file [pink]{fout.name}[/]...")
    with fout.open("w") as lines_out:
        lines_out.writelines(filter(None, output))

    return True


def lift_dat_loop(line: str, lifted_set: set[str]) -> str | None:
    """
    Parameters
    ----------
    line : str
        A single line from the DAT file

    lifted_set : set[str]
        The set of alleles able to be uplifted

    Returns
    -------
    str | None
        The original line if either the allele was in the uplifted set or if it was not a
    """
    if len(line) == 0 or line[0] != "M":
        result = line
    elif len(thing := line.strip().split()) == DAT_LINE_LENGTH:
        _, rs = thing
        if rs in lifted_set:
            result = line
    else:
        result = None
    if isinstance(result, str) and (not result.endswith("\n")):
        result = f"{result}\n"
    return result


def lift_ped(fin: Path, fout: Path, foldmap: Path, unlifted_set: set[str]) -> bool:
    """
    two ways to do it:
    1. write unlifted snp list use PLINK to do this job using --exclude
    2. alternatively, we can write our own method
    we will use method 2

    Parameters
    ----------
    fin : Path
        The original, non-uplifted PED file
    fout : Path
        Where to place the new, uplifted and filtered PED file
    foldmap : Path
        The original, non-uplifted MAP file
    unlifted_set : set[str]
        The set of alleles `liftOver` was unable to map


    Returns
    -------
    bool
        Was this successful?
    """
    with open(foldmap) as f:
        marker = [i.strip().split()[1] for i in f]  # the full list of variants
    flags = [(x not in unlifted_set) for x in marker]  # boolean mask of whether items in marker are in unlifted_set

    console.print(f"Updating [green]PED[/] file [orange]{fin.resolve()}[/]...")

    # TODO: shouldn't this be a generator? or something where I don't read the entire PED file into memory
    lines = fin.read_text().split("\n")
    parallel = Parallel(n_jobs=cpu_count(), return_as="generator")
    output = parallel(delayed(lift_ped_loop)(x, flags) for line in tqdm(lines) if (x := line.strip()) != "")

    # the serial version. useful for debugging
    # output = [lift_ped_loop(line, flag) for line, flag in zip(lines, flags, strict=True) if (x := line.strip() != "")]
    console.print(f"Writing new [green]PED[/] data to [light_slate_blue]{fout.resolve()}[/]")
    with open(fout, "a") as fo:
        fo.writelines(output)
    return True


def lift_ped_loop(line: str, flags: list[bool]) -> str:
    """
    Parameters
    ----------
    line : str
        A single tab-delimited line from a PLINK PED file. The first six items should be
    flags : list[bool]
        A mask of which variant columns are not in the new BED file (i.e. "True" means remove, "False" means keep). Used to filter `line`

    Returns
    -------
    str
        A filtered version of `line` with columns removed that were unable to be lifted over.
    """
    header = line.split("\t")[:6]
    info = line.split("\t")[6:]
    evens = [x for i, x in enumerate(info) if (i % 2 == 0)]
    odds = [x for i, x in enumerate(info) if (i % 2 == 1)]
    newinfo = [f"{x}\t{y}" for x, y in zip(evens, odds, strict=True)]
    maskedinfo = np.ma.MaskedArray(newinfo, flags)
    return "\t".join(header) + "\t" + "\t".join(maskedinfo[maskedinfo.mask].data) + "\n"
