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

import logging
from pathlib import Path
from subprocess import check_output

from rich.console import Console
from typer import progressbar

console = Console()


def map2bed(fin: Path, fout: Path) -> bool:
    logging.getLogger("plinkliftover")
    logging.info(f"fin: {fin}, fout: {fout}")
    console.print(
        f"Converting [green]MAP[/] file [yellow]{fin.name}[/] file to [green]UCSC BED[/] file [blue]{fout.name}[/]..."
    )
    lines = fin.read_text().split("\n")
    output = []
    with progressbar(lines) as map_lines:
        for ln in map_lines:
            if len(x := ln.split()) == 4:
                chrom, rs, mdist, pos = x
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
    unlifted_set: set[str],
    lifted_set: set[str],
) -> tuple[set[str]]:
    logging.getLogger("plinkliftover")
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
        for ln in unlifted:
            if len(ln) == 0 or ln[0] == "#":
                continue
            unlifted_set.add(ln.strip().split()[-1])

    console.print(f"Processing [red]new[/] {fout.name}")
    new_bed_lines = Path(params["NEW"]).read_text().split("\n")
    with progressbar(new_bed_lines) as new_bed:
        for ln in new_bed:
            if len(ln) == 0 or ln[0] == "#":
                continue
            lifted_set.add(ln.strip().split()[-1])

    return lifted_set, unlifted_set, True


def bed2map(fin: Path, fout: Path) -> bool:
    logging.getLogger("plinkliftover")
    console.print(
        f"Converting lifted [green]BED[/] [blue]{fin.name}[/] file back to [green]MAP[/] [yellow]{fout.name}[/]..."
    )
    bed_lines = fin.read_text().split("\n")
    output = list()
    with progressbar(bed_lines) as lines:
        for ln in lines:
            if len(x := ln.split()) == 4:
                chrom, pos0, pos1, rs = x
                chrom = chrom.replace("chr", "")
                output.append(f"{chrom}\t{rs}\t0.0\t{pos1}")
    fout.write_text("\n".join(output))
    return True


def liftDat(fin: Path, fout: Path, lifted_set: set[str]) -> bool:
    logging.getLogger("plinkliftover")
    console.print(f"Updating [green]DAT[/] file [pink]{fin.name}[/]...")
    lines = fin.read_text().split("\n")
    output = []
    with progressbar(lines) as dat_lines:
        for ln in dat_lines:
            if len(ln) == 0 or ln[0] != "M":
                output.append(ln)
            else:
                if len(thing := ln.strip().split()) == 2:
                    t, rs = thing
                    if rs in lifted_set:
                        output.append(ln)
    console.print(f"Writing [green]new DAT[/] file [pink]{fout.name}[/]...")

    return True


def liftPed(
    fin: Path, fout: Path, fOldMap: Path, unlifted_set: set[str]
) -> bool:
    logging.getLogger("plinkliftover")
    # two ways to do it:
    # 1. write unlifted snp list
    #    use PLINK to do this job using --exclude
    # 2. alternatively, we can write our own method
    # we will use method 2
    marker = [i.strip().split()[1] for i in open(fOldMap)]
    flag = [(x not in unlifted_set) for x in marker]

    console.print(f"Updating [green]PED[/] file [orange]{fin.name}[/]...")
    lines = fin.read_text().split("\n")
    output = []
    with progressbar(lines) as liftped_lines:
        for ln in liftped_lines:
            if ln.strip() != "":
                f = ln.strip().split()
                # l = len(f)
                f = f[:6] + [
                    f[i * 2] + " " + f[i * 2 + 1] for i in range(3, len(f) // 2)
                ]
                if len(f[6:]) != len(flag):
                    logging.error("Inconsistent length of ped and map files")
                    logging.error(f"{len(f[6:])} vs {len(flag)}")
                    return False
                newmarker = [m for i, m in enumerate(f[6:]) if flag[i]]

                a = "\t".join(f[:6])
                b = "\t".join(newmarker)
                output.append(f"{a}\t{b}\n")
            # print marker[:10]
    fout.write_text("".join(output))
    return True