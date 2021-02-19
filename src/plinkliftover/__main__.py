# type: ignore[attr-defined]
from typing import Optional

import logging
import sys
from distutils.spawn import find_executable
from pathlib import Path

import typer
from plinkliftover import __version__, setup_logging
from plinkliftover.liftover import bed2map, liftBed, liftDat, map2bed
from rich.console import Console

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
    mapfile: str = typer.Argument(
        ..., help="The plink MAP file to `liftOver`."
    ),
    chainfile: str = typer.Argument(
        ..., help="The location of the chain files to provide to `liftOver`."
    ),
    pedfile: Optional[str] = typer.Option(
        None,
        help='Optionally remove "unlifted SNPs" from the plink PED file after running `liftOver`.',
        show_default=False,
    ),
    datfile: Optional[str] = typer.Option(
        None,
        help="Optionally remove 'unlifted SNPs' from a data file containing a list of SNPs (e.g. for  --exclude or --include in `plink`)",
        show_default=False,
    ),
    prefix: Optional[str] = typer.Option(
        None, help="The prefix to give to the output files.", show_default=False
    ),
    liftoverexecutable: Optional[str] = typer.Option(
        None, help="The location of the `liftOver` executable."
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
    """Converts genotype data stored in plink's PED+MAP format from one genome
    build to another, using liftOver.
    """
    # Show usage message if user hasn't provided any arguments, rather
    # than giving a non-descript error message with the usage()

    lifted_set = set()
    unlifted_set = set()

    setup_logging("plinkliftover")

    mapfile = Path(mapfile)
    oldbed = mapfile.with_suffix(".bed")
    map2bed(mapfile, oldbed)

    # If a location is not specified for the liftOver executable.
    # assume it is in the User's $PATH.
    if liftoverexecutable is None:
        liftOverPath = Path(find_executable("liftOver"))
    else:
        liftOverPath = Path(liftoverexecutable)

    newbed = Path(f"{mapfile}.bed")
    # unlifted = Path(f"{prefix}.unlifted")
    lifted_set, unlifted_set, lb_status = liftBed(
        fin=oldbed,
        fout=newbed,
        chainfile=chainfile,
        liftOverPath=liftOverPath,
        unlifted_set=unlifted_set,
        lifted_set=lifted_set,
    )

    if lb_status:
        console.print("lifting [purple]bed[/] file: [green bold]SUCCESS[/]")
    else:
        console.print("lifting [purple]bed[/] file: [red bold]FAILED[/]")

    newmap = Path(f"{prefix}.map")
    bed2map(newbed, newmap)

    if datfile is not None:
        datfile = Path(datfile)
        console.print(f"[pink]{datfile.name}[/]")
        newdat = Path(f"{prefix}.dat")

        ld_status = liftDat(fin=datfile, fout=newdat, lifted_set=lifted_set)

        if ld_status:
            console.print("lifting [purple]dat[/] file: [green]SUCCESS[/]")
        else:
            console.print("lifting [purple]dat[/] file: [red]FAILED[/]")

    if pedfile is not None:
        pedfile = Path(pedfile)
        console.print(f"[pink]{pedfile.name}[/]")
        newPed = Path(f"{prefix}.ped")
        lp_status = liftPed(
            fin=pedfile, fout=newPed, fOldMap=mapfile, unlifted_set=unlifted_set
        )

        if lp_status:
            console.print(
                "lifting [dark_orange3]ped[/] file: [bold green]SUCCESS[/]"
            )
        else:
            console.print(
                "lifting [dark_orange3]ped[/] file: [bold red]FAILED[/]"
            )

    console.print("cleaning up BED files...")
    newbed.unlink()
    oldbed.unlink()


if __name__ == "__main__":
    typer.run(main)
