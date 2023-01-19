import glob
import json
import shutil
import os
import logging
import random
import time
from typing import List

from config import APOLLO_ROOT, RECORDS_DIR, STREAM_LOGGING_LEVEL


def get_logger(name, filename=None, log_to_file=False) -> logging.Logger:
    """
    Gets logger from logging module

    :param str filename: filename of the log records
    :param bool log_to_file: flag to determine logging to file

    :returns: Logger object
    :rtype: Logger
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

    :returns: Logger object
    :rtype: Logger
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

    :param int length: expected length of the ID

    :returns: list of integer ids
    :rtype: List[int]
    """
    return sorted(random.sample(range(100000, 999999), k=length))


def create_dir_for_scenario(generation_name: str, scenario_name: str):
    """
    Creates directory to store scenario record files

    :param str generation_name: name of the generation
    :param str scenario_name: name of the scenario
    """
    dest = os.path.join(RECORDS_DIR, generation_name, scenario_name)
    if not os.path.exists(dest):
        os.makedirs(dest)
    else:
        shutil.rmtree(dest)
        os.makedirs(dest)


def save_record_files_and_chromosome(generation_name: str, scenario_name: str, ch: dict):
    """
    Save the record file and the genetic representation

    :param str generation_name: name of the generation
    :param str scenario_name: name of the scenario
    :param dict ch: the genetic representation
    """
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
    """
    Remove record files for the specified generation and scenario name

    :param str generation_name: name of the generation
    :param str scenario_name: name of the scenario
    """
    dest = os.path.join(RECORDS_DIR, generation_name, scenario_name)
    shutil.rmtree(dest)


def find_all_files_by_wildcard(base_dir: str, file_name: str, recursive=False) -> List[str]:
    """
    Recursively find all files in a given directory based on filename

    :param str base_dir: the root of the directory to be searched
    :param str filename: filename (wildcard) to be matched

    :returns: all files found
    :rtype: List[str]
    """
    return glob.glob(os.path.join(base_dir, file_name), recursive=recursive)


def get_current_timestamp() -> float:
    """
    Retrieve the current timestamp

    :returns: timestamp
    :rtype: float
    """
    return round(time.time())
