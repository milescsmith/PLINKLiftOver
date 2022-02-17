from typing import Optional

from pathlib import Path

import typer

from . import app, console, version_callback
from .logger import plo_logger as logger

# bed2mapapp = typer.Typer(
#     name="bed2map",
#     help="Converts BED files to PLINK MAP format",
#     add_completion=False,
# )


def bed2map(fin: Path, fout: Path) -> bool:
    logger.info(f"fin: {fin}, fout: {fout}")
    console.print(
        f"Converting lifted [green]BED[/] [blue]{fin.name}[/] file back to [green]MAP[/] [yellow]{fout.name}[/]..."
    )
    lines = fin.read_text().split("\n")
    output = list()
    with typer.progressbar(lines) as bed_lines:
        for line in bed_lines:
            if len(x := line.split()) == 4:
                chrom, _, pos1, rs = x
                chrom = chrom.replace("chr", "")
                output.append(f"{chrom}\t{rs}\t0.0\t{pos1}")
    fout.write_text("\n".join(output))
    return True


@app.command(name="bed2map")
def bed2mapapp(
    bedfile: Path = typer.Argument(..., help="A BED file."),
    output: Optional[Path] = typer.Option(
        None,
        "-o",
        "--output",
        help=f"Location to save MAP file to.  If one is not provided, "
        f"then it will be saved to where the BED file is.",
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
        output_map = bedfile.with_suffix(".map")
    else:
        output_map = output.joinpath(f"{bedfile.stem}.map")

    bed2map(bedfile, output_map)
