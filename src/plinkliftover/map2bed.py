from typing import Optional

from pathlib import Path

import typer

from . import app, console, version_callback
from .logger import plo_logger as logger

# map2bedapp = typer.Typer(
#     name="map2bed",
#     help="Converts PLINK MAP files into BED format",
#     add_completion=False,
# )


def map2bed(fin: Path, fout: Path) -> bool:
    logger.info(f"fin: {fin}, fout: {fout}")
    console.print(
        f"Converting [green]MAP[/] file [yellow]{fin.name}[/] file to [green]UCSC BED[/] file [blue]{fout.name}[/]..."
    )
    lines = fin.read_text().split("\n")
    output = list()
    with typer.progressbar(lines) as map_lines:
        for line in map_lines:
            if len(x := line.split()) == 4:
                chrom, rs, _, pos = x
                output.append(f"chr{chrom}\t{int(pos)-1}\t{int(pos)}\t{rs}")
            else:
                pass
    fout.write_text("\n".join(output))
    return True


@app.command(name="map2bed")
def map2bedapp(
    mapfile: Path = typer.Argument(..., help="A PLINK MAP file."),
    output: Optional[Path] = typer.Option(
        None,
        "-o",
        "--output",
        help=f"Location to save BED file to.  If one is not provided, "
        f"then it will be saved to where the MAP file is.",
        show_default=True,
    ),
    version: bool = typer.Option(
        None,
        "-v",
        "--version",
        callback=version_callback,
        is_eager=True,
        help="Prints the version of the plinkliftover package.",
    ),
) -> None:
    """Convert genotype data stored in a PLINK MAP file into a BED file,
    allowing one to use the online version of liftOver should the local
    executable is unavailable
    """

    if output is None:
        output_bed = mapfile.with_suffix(".bed")
    else:
        output_bed = output.joinpath(f"{mapfile.stem}.bed")

    map2bed(mapfile, output_bed)
