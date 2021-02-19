# type: ignore[attr-defined]
from pathlib import Path

import typer
from rich.console import Console

from plinkliftover import __version__
from plinkliftover.liftover import makesure, liftBed, bed2map, map2bed, liftDat, liftPed
from distutils.spawn import find_executable


app = typer.Typer(
    name="plinkliftover",
    help="Converts genotype data stored in plink's PED+MAP format from one genome build to another, using liftOver",
    add_completion=False,
)
console = Console()


def version_callback(value: bool):
    """Prints the version of the package."""
    if value:
        console.print(
            f"[yellow]plinkliftover[/] version: [bold blue]{__version__}[/]"
        )
        raise typer.Exit()


@app.command(name="")
def main(
    mapFile: str = typer.Argument(..., help="The plink MAP file to `liftOver`."),
    pedFile: str = typer.Option("", help='Optionally remove "unlifted SNPs" from the plink PED file after running `liftOver`.', show_default=False),
    datFile: str = typer.Option("", help="Optionally remove 'unlifted SNPs' from a data file containing a list of SNPs (e.g. for  --exclude or --include in `plink`)", show_default=False),
    prefix: str = typer.Option("", help="The prefix to give to the output files.", show_default=False),
    chainFile: str = typer.Argument(..., help="The location of the chain files to provide to `liftOver`."),
    liftOverExecutable: str = typer.Option(None, help="The location of the `liftOver` executable."),
    version: bool = typer.Option(
        None,
        "-v", "--version",
        callback=version_callback,
        is_eager=True,
        help="Prints the version of the plinkliftover package.",
    ),
) -> None:
    """Converts genotype data stored in plink's PED+MAP format from one genome
    build to another, using liftOver.
    """
    # Show usage message if user hasn't provided any arguments, rather
    # than giving a non-descript error message with the usage()

    oldBed = f"{mapFile}.bed"
    makesure(map2bed(mapFile, oldBed), "map->bed succ")

    # If a location is not specified for the liftOver executable.
    # assume it is in the User's $PATH.
    if liftOverExecutable is None:
        liftOverPath = find_executable("liftOver")
    else:
        liftOverPath = liftOverExecutable

    newBed = Path(f"{mapFile}.bed")
    unlifted = Path(f"{prefix}.unlifted")
    makesure(liftBed(oldBed, newBed, unlifted, chainFile, liftOverPath), "liftBed succ")

    newMap = Path(f"{prefix}.map")
    makesure(bed2map(newBed, newMap), "bed->map succ")

    if datFile:
        newDat = Path(f"{prefix}.dat")
        makesure(liftDat(datFile, newDat), "liftDat succ")

    if pedFile:
        newPed = Path(f"{prefix}.ped")
        makesure(liftPed(pedFile, newPed, mapFile), "liftPed succ")

    console.print("cleaning up BED files...")
    newBed.unlink()
    oldBed.unlink()
