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
    logger.propagate = False
    if logger.handlers:
        return logger
    logger.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    ch.setLevel(STREAM_LOGGING_LEVEL)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    ch.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(ch)
    return logger


def get_scenario_logger() -> logging.Logger:
    """
    Gets logger that always logs on the same line

    Returns:
        logger: Logger
    """
    logger = logging.getLogger('Scenario')
    logger.propagate = False
    if logger.handlers:
        return logger

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


def create_dir_for_scenario(generation_name: str, scenario_name: str):
    dest = os.path.join(RECORDS_DIR, generation_name, scenario_name)
    if not os.path.exists(dest):
        os.makedirs(dest)
    else:
        shutil.rmtree(dest)
        os.makedirs(dest)


def save_record_files_and_chromosome(generation_name: str, scenario_name: str, ch: dict):
    dest = os.path.join(RECORDS_DIR, generation_name, scenario_name)
    if not os.path.exists(dest):
        os.makedirs(dest)
    else:
        shutil.rmtree(dest)
        os.makedirs(dest)

    fileList = glob.glob(f'{APOLLO_ROOT}/records/*')
    for filePath in fileList:
        shutil.copy2(filePath, dest)

    dest_file = os.path.join(dest, "c.json")
    with open(dest_file, 'w') as fp:
        json.dump(ch, fp, indent=4)


def remove_record_files(generation_name: str, scenario_name: str):
    dest = os.path.join(RECORDS_DIR, generation_name, scenario_name)
    shutil.rmtree(dest)
