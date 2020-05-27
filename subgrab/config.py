from pathlib import Path

from loguru import logger


logger.remove(0)


def init_logger():
    path = Path(Path.home(), "subgrab.log")
    logger.add(path, format="{time} {level} {message}", rotation="1 MB")
    return logger
