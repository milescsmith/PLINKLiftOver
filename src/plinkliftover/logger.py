import datetime
from sys import stderr

from loguru import logger


def init_logger(verbose: int, msg_format: str | None = None) -> None:
    if msg_format is None:
        msg_format = "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan>·-·<level>{message}</level>"

    timezone = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo
    logger.add(f"readcounts_{datetime.datetime.now(tz=timezone).strftime('%d-%m-%Y--%H-%M-%S')}.log", level="DEBUG")

    match verbose:
        case 3:
            logger.add(stderr, format=msg_format, level="DEBUG")
        case 2:
            logger.add(stderr, format=msg_format, level="INFO")
        case 1:
            logger.add(stderr, format=msg_format, level="WARNING")
        case _:
            logger.add(stderr, format=msg_format, level="ERROR")
