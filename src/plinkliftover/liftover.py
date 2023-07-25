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

from multiprocessing import cpu_count
from pathlib import Path
from subprocess import check_output

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
) -> tuple[set[str], set[str], bool]:
    console.print(f"Lifting [green]BED[/] file [blue]{fin.name}[/]...")
    params: dict[str, str | Path] = {
        "LIFTOVER_BIN": lift_over_path.resolve(),
        "OLD": fin,
        "CHAIN": chainfile,
        "NEW": fout,
        "UNLIFTED": f"{fout}.unlifted",
    }

    check_output([str(params[_]) for _ in params])  # noqa: S603
    # record lifted/unliftd rs
    unlifted_lines = Path(params["UNLIFTED"]).read_text().split("\n")
    console.print(f"Processing [red]unlifted[/] {fout.name}.unlifted")

    unlifted_set = {ln.strip().split()[-1] for ln in tqdm(unlifted_lines) if len(ln) > 0 and ln[0] != "#"}

    console.print(f"Processing [red]new[/] {fout.name}")
    new_bed_lines = Path(params["NEW"]).read_text().split("\n")

    lifted_set = {ln.strip().split()[-1] for ln in tqdm(new_bed_lines) if len(ln) != 0 and ln[0] != "#"}

    return lifted_set, unlifted_set, True


def lift_dat(fin: Path, fout: Path, lifted_set: set[str]) -> bool:
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
    if len(line) == 0 or line[0] != "M":
        result = line
    elif len(thing := line.strip().split()) == DAT_LINE_LENGTH:
        _, rs = thing
        if rs in lifted_set:
            result = line
    if not result.endswith("\n"):
        result = f"{result}\n"
    return result


def lift_ped(fin: Path, fout: Path, foldmap: Path, unlifted_set: set[str]) -> bool:
    # two ways to do it:
    # 1. write unlifted snp list
    #    use PLINK to do this job using --exclude
    # 2. alternatively, we can write our own method
    # we will use method 2
    marker = [i.strip().split()[1] for i in open(foldmap)]
    flags = [(x not in unlifted_set) for x in marker]

    console.print(f"Updating [green]PED[/] file [orange]{fin.resolve()}[/]...")
    lines = fin.read_text().split("\n")
    # TODO: parallelize
    parallel = Parallel(n_jobs=cpu_count(), return_as="generator")
    output = parallel(
        delayed(lift_ped_loop)(x, flag)
        for line, flag in tqdm(zip(lines, flags, strict=True))
        if (x := line.strip() != "")
    )

    console.print(f"Writing new [green]PED[/] data to [light_slate_blue]{fout.resolve()}[/]")
    with open(fout, "a") as fo:
        fo.writelines(output)
    return True


def lift_ped_loop(line: str, flag: bool) -> str:
    f = line.strip().split()
    f = f[:6] + [f"{f[i * 2]} {f[i * 2 + 1]}" for i in range(3, len(f) // 2)]
    if len(f[6:]) != len(flag):
        msg = f"Inconsistent length of ped and map files - {len(f[6:])} vs {len(flag)}"
        logger.error(msg)
        raise ValueError(msg)
    newmarker = [m for m in f[6:] if flag]

    a = "\t".join(f[:6])
    b = "\t".join(newmarker)
    return f"{a}\t{b}\n"
