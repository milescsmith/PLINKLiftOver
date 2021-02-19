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
import sys
from pathlib import Path
from subprocess import check_output

from rich.console import Console

console = Console()


def map2bed(fin: Path, fout: Path) -> bool:
    console.print("Converting MAP file to UCSC BED file...")
    for ln in fin.read_text().split("\n"):
        chrom, rs, mdist, pos = ln.split()
        fout.write_text(f"chr{chrom}\t{pos-1}\t{int(pos)}\t{rs}\n")
    return True


# global var:
LIFTED_SET = set()
UNLIFTED_SET = set()


def liftBed(
    fin: Path, fout: Path, funlifted, chainFile: Path, liftOverPath: Path
) -> bool:
    console.print("Lifting BED file...")
    params = {
        "LIFTOVER_BIN": liftOverPath,
        "OLD": fin,
        "CHAIN": chainFile,
        "NEW": fout,
        "UNLIFTED": f"{fout}.unlifted",
    }
    # cmd = Template('$LIFTOVER_BIN $OLD $CHAIN $NEW $UNLIFTED')
    check_output(params.values())
    # record lifted/unliftd rs
    for ln in Path(params["UNLIFTED"]).read_text().split("\n"):
        if len(ln) == 0 or ln[0] == "#":
            continue
        UNLIFTED_SET.add(ln.strip().split()[-1])
    for ln in Path(params["NEW"]).read_text().split("\n"):
        if len(ln) == 0 or ln[0] == "#":
            continue
        LIFTED_SET.add(ln.strip().split()[-1])

    return True


def bed2map(fin: Path, fout: Path) -> bool:
    console.print("Converting lifted BED file back to MAP...")
    for ln in fin.read_text().split("\n"):
        chrom, pos0, pos1, rs = ln.split()
        chrom = chrom.replace("chr", "")
        fout.write_text(f"{chrom}\t{rs}\t0.0\t{pos1}\n")
    return True


def liftDat(fin: Path, fout: Path) -> bool:
    for ln in fin.read_text().split("\n"):
        if len(ln) == 0 or ln[0] != "M":
            fout.write_text(ln)
        else:
            t, rs = ln.strip().split()
            if rs in LIFTED_SET:
                fout.write_text(ln)
    return True


def liftPed(fin: Path, fout: Path, fOldMap: Path) -> bool:
    # two ways to do it:
    # 1. write unlifted snp list
    #    use PLINK to do this job using --exclude
    # 2. alternatively, we can write our own method
    # we will use method 2
    marker = [i.strip().split()[1] for i in fOldMap.read_text().split("\n")]
    # flag = map(lambda x: x not in UNLIFTED_SET, marker)
    flag = [_ for _ in marker not in UNLIFTED_SET]
    # print marker[:10]
    # print flag[:10]

    console.print("Updating PED file...")
    for ln in fin.read_text().split("\n"):
        f = ln.strip().split()
        l = len(f)
        f = f[:6] + [f[i * 2] + " " + f[i * 2 + 1] for i in range(3, l / 2)]
        fout.write_text("\t".join(f[:6]))
        fout.write_text("\t")
        if len(f[6:]) != len(flag):
            logging.error("Inconsistent length of ped and map files")
            sys.exit(-1)
        newMarker = [m for i, m in enumerate(f[6:]) if flag[i]]
        fout.write_text("\t".join(newMarker))
        fout.write_text("\n")
        # print marker[:10]
        # die('test')
    return True


def makesure(result: bool, succ_msg: str, fail_msg: str = "ERROR") -> None:
    if result:
        console.print(f"SUCC: {succ_msg}")
    else:
        print(f"FAIL: {fail_msg}")
        sys.exit(2)
