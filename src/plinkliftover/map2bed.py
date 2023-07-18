from multiprocessing import cpu_count
from pathlib import Path
from typing import Annotated, Optional

import typer
from joblib import Parallel, delayed
from loguru import logger
from tqdm.rich import tqdm

from plinkliftover import app, console, verbosity_level, version_callback
from plinkliftover.logger import init_logger

MAP_LINE_LENGTH: int = 4


def map2bed(fin: Path, fout: Path) -> bool:
    logger.info(f"fin: {fin}, fout: {fout}")
    console.print(
        f"Converting [green]MAP[/] file [yellow]{fin.name}[/] file to [green]UCSC BED[/] file [blue]{fout.name}[/]..."
    )
    init_logger(verbosity_level)
    lines = fin.read_text().split("\n")
    parallel = Parallel(n_jobs=cpu_count(), return_as="generator")
    output = parallel(delayed(maplinesplit)(x) for line in tqdm(lines) if len(x := line.split()) == MAP_LINE_LENGTH)

    with fout.open("w") as lines_out:
        lines_out.writelines(output)
    return True


def maplinesplit(line: str) -> str:
    chrom, rs, _, pos = line
    return f"chr{chrom}\t{int(pos)-1}\t{int(pos)}\t{rs}\n"


@app.command(name="map2bed", no_args_is_help=True)
def map2bedapp(
    mapfile: Annotated[Path, typer.Argument(help="A PLINK MAP file.")],
    output: Annotated[
        Optional[Path],  # noqa UP007
        typer.Option(
            "-o",
            "--output",
            help=(
                "Location to save BED file to.  If one is not provided, "
                "then it will be saved to where the MAP file is."
            ),
            show_default=True,
        ),
    ] = None,
    version: Annotated[  # noqa ARG001
        bool,
        typer.Option(
            "-v",
            "--version",
            callback=version_callback,
            is_eager=True,
            help="Prints the version of the plinkliftover package.",
        ),
    ] = False,  # noqa FBT007
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
