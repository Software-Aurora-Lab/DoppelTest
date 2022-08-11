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


def clean_appolo_dir():
    # remove data dir
    subprocess.run(f"rm -rf {APOLLO_ROOT}/data".split())

    # remove records dir
    subprocess.run(f"rm -rf {APOLLO_ROOT}/records".split())

    # remove logs
    fileList = glob.glob(f'{APOLLO_ROOT}/*.log.*')
    for filePath in fileList:
        os.remove(filePath)

    # create data dir
    subprocess.run(f"mkdir {APOLLO_ROOT}/data".split())
    subprocess.run(f"mkdir {APOLLO_ROOT}/data/bag".split())
    subprocess.run(f"mkdir {APOLLO_ROOT}/data/log".split())
    subprocess.run(f"mkdir {APOLLO_ROOT}/data/core".split())
    subprocess.run(f"mkdir {APOLLO_ROOT}/records".split())


def save_record_files_and_chromosome(generation_name: str, run_id: str, ch: dict):
    dest = os.path.join(RECORDS_DIR, generation_name, run_id)
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
