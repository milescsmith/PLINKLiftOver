from pathlib import Path
from plinkliftover import map2bed

mapfile = Path("tests", "data", "gsa_chr1.map")
outfile = Path("tests", "data", "gsa_chr1.bed")

map2bed.map2bed(mapfile, outfile)