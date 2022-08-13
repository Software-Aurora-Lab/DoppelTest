import glob
import json
import shutil
import subprocess
import math
import os
import logging
import random
from typing import List

from modules.common.proto.geometry_pb2 import PointENU
from config import APOLLO_ROOT, LOG_DIR, RECORDS_DIR, STREAM_LOGGING_LEVEL
from modules.map.proto.map_pb2 import Map


def get_logger(name, filename=None, log_to_file=False) -> logging.Logger:
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

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    # %(filename)s - %(lineno)d

    # stream handlers
    ch = logging.StreamHandler()
    ch.setLevel(STREAM_LOGGING_LEVEL)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    # file handler
    if log_to_file:
        if not os.path.exists(LOG_DIR):
            os.makedirs(LOG_DIR)
        fh = logging.FileHandler(
            f"{LOG_DIR}/{filename if filename else name}.log")
        fh.setLevel(logging.ERROR)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

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
    return sorted(random.sample(range(100000, 999999), k=length))
