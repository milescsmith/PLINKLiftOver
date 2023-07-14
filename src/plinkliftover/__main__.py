from distutils.spawn import find_executable
from pathlib import Path
from typing import Annotated, Optional

import typer
from loguru import logger

from plinkliftover import app, console, verbosity_level, version_callback
from plinkliftover.bed2map import bed2map
from plinkliftover.liftover import lift_bed, lift_dat, lift_ped
from plinkliftover.logger import init_logger
from plinkliftover.map2bed import map2bed


@app.command(name="liftover")
def liftover(
    mapfile: Annotated[
        Path,
        typer.Argument(help="The plink MAP file to `liftOver`."),
    ],
    chainfile: Annotated[Path, typer.Argument(help="The location of the chain files to provide to `liftOver`.")],
    pedfile: Annotated[
        Optional[Path],  # noqa UP007
        typer.Option(
            help='Optionally remove "unlifted SNPs" from the plink PED file after running `liftOver`.',
            show_default=False,
        ),
    ] = None,
    datfile: Annotated[
        Optional[Path],  # noqa UP007
        typer.Option(
            help=(
                "Optionally remove 'unlifted SNPs' from a data file containing a list of SNPs "
                "(e.g. for  --exclude or --include in `plink`)"
            ),
            show_default=False,
        ),
    ] = None,
    prefix: Annotated[
        Optional[str], typer.Option(help="The prefix to give to the output files.", show_default=False)  # noqa UP007
    ] = None,
    liftoverexecutable: Annotated[
        Optional[str], typer.Option(help="The location of the `liftOver` executable.")  # noqa UP007
    ] = None,
    version: Annotated[  # noqa ARG007
        bool,
        typer.Option(
            "-V",
            "--version",
            callback=version_callback,
            is_eager=True,
            help="Prints the version of the plinkliftover package.",
        ),
    ] = False,  # noqa FBT002
) -> None:
    """Converts genotype data stored in plink's PED+MAP format from one genome
    build to another, using liftOver.
    """
    # Show usage message if user hasn't provided any arguments, rather
    # than giving a non-descript error message with the usage()

    init_logger(verbose=verbosity_level)

    oldbed = mapfile.with_suffix(".bed")
    map2bed(mapfile, oldbed)

    # If a location is not specified for the liftOver executable.
    # assume it is in the User's $PATH.
    if liftoverexecutable is None:
        if (lop := find_executable("liftOver")) is not None:
            lift_over_path = Path(lop)
            if not lift_over_path.exists():
                msg = "The `liftOver` executable was not found.  Please make sure it is installed and in the PATH"
                logger.exception(msg)
                raise FileNotFoundError(msg)
    else:
        lift_over_path = Path(liftoverexecutable)
        if not lift_over_path.exists():
            msg = "The `liftOver` executable was not found.  Please make sure it is installed and in the PATH"
            logger.exception(msg)
            raise FileNotFoundError(msg)

    newbed = Path(f"{mapfile}.bed")
    lifted_set, unlifted_set, lb_status = lift_bed(
        fin=oldbed,
        fout=newbed,
        chainfile=chainfile,
        lift_over_path=lift_over_path,
    )

    if lb_status:
        console.print("lifting [purple]bed[/] file: [green bold]SUCCESS[/]")
        logger.info(f"lifting bed file: {newbed} - SUCCESS")
    else:
        console.print("lifting [purple]bed[/] file: [red bold]FAILED[/]")
        logger.info(f"lifting bed file: {newbed} - FAILED")

    newmap = Path(f"{prefix}.map")
    bed2map(newbed, newmap)

    if datfile is not None:
        datfile = Path(datfile)
        console.print(f"[pink]{datfile.name}[/]")
        newdat = Path(f"{prefix}.dat")

        if lift_dat(fin=datfile, fout=newdat, lifted_set=lifted_set):
            console.print("lifting [purple]dat[/] file: [green]SUCCESS[/]")
            logger.info(f"lifting map file: {newmap} - SUCCESS")
        else:
            console.print("lifting [purple]dat[/] file: [red]FAILED[/]")
            logger.info(f"lifting map file: {newmap} - FAILED")

    if pedfile is not None:
        pedfile = Path(pedfile)
        console.print(f"[pink]{pedfile.name}[/]")
        new_ped = Path(f"{prefix}.ped")

        if lift_ped(fin=pedfile, fout=new_ped, foldmap=mapfile, unlifted_set=unlifted_set):
            console.print("lifting [dark_orange3]ped[/] file: [bold green]SUCCESS[/]")
            logger.info("lifting ped file: SUCCESS")
        else:
            console.print("lifting [dark_orange3]ped[/] file: [bold red]FAILED[/]")
            logger.info("lifting ped file: FAILED")

    console.print("cleaning up BED files...")
    logger.info("cleaning up BED files...")
    newbed.unlink()
    oldbed.unlink()
