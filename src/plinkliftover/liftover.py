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
 - Update to work with python >=3.7
"""

from typing import Set, Tuple

import sys
from pathlib import Path
from subprocess import check_output

from .logger import plo_logger as logger
from rich.console import Console
from typer import progressbar

console = Console()


def map2bed(fin: Path, fout: Path) -> bool:
    logger.info(f"fin: {fin}, fout: {fout}")
    console.print(
        f"Converting [green]MAP[/] file [yellow]{fin.name}[/] file to [green]UCSC BED[/] file [blue]{fout.name}[/]..."
    )
    lines = fin.read_text().split("\n")
    output = list()
    with progressbar(lines) as map_lines:
        for line in map_lines:
            if len(x := line.split()) == 4:
                chrom, rs, _, pos = x
                output.append(f"chr{chrom}\t{int(pos)-1}\t{int(pos)}\t{rs}")
            else:
                pass
    fout.write_text("\n".join(output))
    return True


def liftBed(
    fin: Path,
    fout: Path,
    chainfile: Path,
    liftOverPath: Path,
) -> Tuple[Set[str]]:
    console.print(f"Lifting [green]BED[/] file [blue]{fin.name}[/]...")
    params = {
        "LIFTOVER_BIN": liftOverPath.resolve(),
        "OLD": fin,
        "CHAIN": chainfile,
        "NEW": fout,
        "UNLIFTED": f"{fout}.unlifted",
    }

    check_output(params.values())
    # record lifted/unliftd rs
    unlifted_lines = Path(params["UNLIFTED"]).read_text().split("\n")
    console.print(f"Processing [red]unlifted[/] {fout.name}.unlifted")
    with progressbar(unlifted_lines) as unlifted:
        print("Using new set comprehension for 'unlifted_set'")
        unlifted_set = {ln.strip().split()[-1] for ln in unlifted if len(ln) > 0 and ln[0] != "#"}

    console.print(f"Processing [red]new[/] {fout.name}")
    new_bed_lines = Path(params["NEW"]).read_text().split("\n")
    with progressbar(new_bed_lines) as new_bed:
        print("Using new set comprehension for 'lifted_set'")
        lifted_set = {ln.strip().split()[-1] for ln in new_bed if len(ln) != 0 and ln[0] != "#"}

    return lifted_set, unlifted_set, True


def bed2map(fin: Path, fout: Path) -> bool:
    console.print(
        f"Converting lifted [green]BED[/] [blue]{fin.name}[/] file back to [green]MAP[/] [yellow]{fout.name}[/]..."
    )
    bed_lines = fin.read_text().split("\n")
    output = list()
    with progressbar(bed_lines) as lines:
        for ln in lines:
            if len(x := ln.split()) == 4:
                chrom, _, pos1, rs = x
                chrom = chrom.replace("chr", "")
                output.append(f"{chrom}\t{rs}\t0.0\t{pos1}")
    fout.write_text("\n".join(output))
    return True


def liftDat(fin: Path, fout: Path, lifted_set: Set[str]) -> bool:
    console.print(f"Updating [green]DAT[/] file [pink]{fin.name}[/]...")
    lines = fin.read_text().split("\n")
    output = list()
    with progressbar(lines) as dat_lines:
        for ln in dat_lines:
            if len(ln) == 0 or ln[0] != "M":
                output.append(ln)
            else:
                if len(thing := ln.strip().split()) == 2:
                    _, rs = thing
                    if rs in lifted_set:
                        output.append(ln)
    console.print(f"Writing [green]new DAT[/] file [pink]{fout.name}[/]...")

    return True


def liftPed(
    fin: Path, fout: Path, fOldMap: Path, unlifted_set: Set[str]
) -> bool:
    # two ways to do it:
    # 1. write unlifted snp list
    #    use PLINK to do this job using --exclude
    # 2. alternatively, we can write our own method
    # we will use method 2
    marker = [i.strip().split()[1] for i in open(fOldMap)]
    flag = [(x not in unlifted_set) for x in marker]

    console.print(f"Updating [green]PED[/] file [orange]{fin.resolve()}[/]...")
    lines = fin.read_text().split("\n")
    output = list()
    with progressbar(lines) as liftped_lines:
        for ln in liftped_lines:
            if ln.strip() != "":
                f = ln.strip().split()
                f = f[:6] + [
                    f[i * 2] + " " + f[i * 2 + 1] for i in range(3, len(f) // 2)
                ]
                if len(f[6:]) != len(flag):
                    logger.error("Inconsistent length of ped and map files")
                    logger.error(f"{len(f[6:])} vs {len(flag)}")
                    sys.exit(-1)
                newmarker = [m for i, m in enumerate(f[6:]) if flag[i]]

                a = "\t".join(f[:6])
                b = "\t".join(newmarker)
                output.append(f"{a}\t{b}\n")
    console.print(
        f"Writing new [green]PED[/] data to [light_slate_blue]{fout.resolve()}[/]"
    )
    with open(fout, "w") as fo:
        fo.writelines(output)
    return True
