import math
import os
import logging
import random
from typing import List

from modules.common.proto.geometry_pb2 import PointENU
from utils.config import STREAM_LOGGING_LEVEL


def get_logger(name, filename=None) -> logging.Logger:
    """
    Gets logger from logging module

    Parameters:
        filename: str, Optional
            filename of the log records

    Returns:
        logger: Logger
    """
    logger = logging.getLogger(name)
    logger.handlers.clear()
    logger.setLevel(logging.DEBUG)
    if not os.path.exists("Logs"):
        os.makedirs("Logs")
    fh = logging.FileHandler(f"Logs/{filename if filename else name}.log")
    fh.setLevel(logging.ERROR)
    ch = logging.StreamHandler()
    ch.setLevel(STREAM_LOGGING_LEVEL)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    # %(filename)s - %(lineno)d
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger


def get_scenario_logger() -> logging.Logger:
    """
    Gets logger that always logs on the same line

    Returns:
        logger: Logger
    """
    logger = logging.getLogger('Scenario')
    logger.handlers.clear()
    logger.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    ch.terminator = '\r'
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger


def zero_velocity(velocity: PointENU) -> bool:
    """
    Checks if the given velocity vector is 0

    Parameters:
        velocity: PointENU
            velocity vector

    Returns
        result: bool
            True if velocity is 0, False otherwise
    """
    return round(math.sqrt(velocity.x ** 2 + velocity.y ** 2), 2) == 0.00


def random_numeric_id(length=5) -> List[int]:
    """
    Generates a list of random integer ids

    Parameters:
        length: int
            expected size of the output

    Returns:
        result: List[int]
            list of integer ids in range 100000, 999999
    """
    return random.choices(range(100000, 999999), k=length)
