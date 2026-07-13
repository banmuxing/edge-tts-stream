import logging
import sys


def get_logger(name="edge-tts"):

    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(

        "%(asctime)s | %(levelname)-8s | %(message)s",

        "%Y-%m-%d %H:%M:%S"

    )

    console = logging.StreamHandler(sys.stdout)

    console.setFormatter(formatter)

    logger.addHandler(console)

    logger.propagate = False

    return logger


logger = get_logger()