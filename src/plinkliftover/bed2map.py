from multiprocessing import cpu_count
from pathlib import Path
from typing import Annotated, Optional

import typer
from joblib import Parallel, delayed
from loguru import logger
from tqdm.rich import tqdm

from plinkliftover import app, console, verbosity_level, version_callback
from plinkliftover.logger import init_logger

BED_LINES_LENGTH: int = 4


def bed2map(fin: Path, fout: Path) -> bool:
    init_logger(verbosity_level)
    logger.info(f"fin: {fin}, fout: {fout}")
    console.print(
        f"Converting lifted [green]BED[/] [blue]{fin.name}[/] file back to [green]MAP[/] [yellow]{fout.name}[/]..."
    )
    lines = fin.read_text().split("\n")

    parallel = Parallel(n_jobs=cpu_count(), return_as="generator")
    output = parallel(delayed(bedlinesplit)(x) for line in tqdm(lines) if len(x := line.split()) == BED_LINES_LENGTH)

    with fout.open("w") as lines_out:
        lines_out.writelines(output)
    return True


def bedlinesplit(line: str) -> str:
    chrom, _, pos1, rs = line
    chrom = chrom.replace("chr", "")
    return f"{chrom}\t{rs}\t0.0\t{pos1}\n"


@app.command(name="bed2map", no_args_is_help=True)
def bed2mapapp(
    bedfile: Annotated[Path, typer.Argument(help="A BED file.")],
    output: Annotated[
        Optional[Path],  # noqa UP007
        typer.Option(
            "-o",
            "--output",
            help=(
                "Location to save MAP file to.  If one is not provided, "
                "then it will be saved to where the BED file is."
            ),
            show_default=True,
        ),
    ] = None,
    version: Annotated[  # noqa ARG001
        Optional[bool],  # noqa UP007
        typer.Option(
            "-v",
            "--version",
            callback=version_callback,
            is_eager=True,
            help="Prints the version of the plinkliftover package.",
        ),
    ] = None,
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
