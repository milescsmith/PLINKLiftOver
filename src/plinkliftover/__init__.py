"""
`plinkliftover` Converts genotype data stored in plink's PED+MAP
format from one genome build to another, using liftOver
"""
import warnings
from importlib.metadata import PackageNotFoundError, version
from os import environ
from typing import Annotated

import better_exceptions
from tqdm import TqdmExperimentalWarning

warnings.filterwarnings("ignore", category=TqdmExperimentalWarning)

from loguru import logger

try:
    __version__ = version(__name__)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"

import typer
from rich.console import Console

environ["BETTER_EXCEPTIONS"] = "1"
console = Console()
logger.disable("readcounts")

app = typer.Typer(
    name="plinkliftover",
    help="Converts genotype data stored in plink's PED+MAP format from one genome build to another, using liftOver",
    add_completion=True,
    no_args_is_help=True,
)

verbosity_level = 0


def version_callback(value: bool) -> None:  # noqa FBT001
    """Prints the version of the package."""
    if value:
        console.print(f"[yellow]plinkliftover[/] version: [bold blue]{__version__}[/]")
        raise typer.Exit()


@app.callback()
def verbosity(
    verbose: Annotated[
        int,
        typer.Option(
            "-v",
            "--verbose",
            help="Control output verbosity. Pass this argument multiple times to increase the amount of output.",
            count=True,
        ),
    ] = 0
) -> None:
    verbosity_level = verbose  # noqa: F841


if __name__ == "main":
    app()
