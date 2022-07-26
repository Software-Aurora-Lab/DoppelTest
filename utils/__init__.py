import math
import os
import logging
import random

from modules.common.proto.geometry_pb2 import PointENU
from utils.config import STREAM_LOGGING_LEVEL


def get_logger(name, filename=None) -> logging.Logger:
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
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger


def zero_velocity(points: PointENU):
    return round(math.sqrt(points.x ** 2 + points.y ** 2), 2) == 0.00


def random_numeric_id(length=5):
    return random.choices(range(100000, 999999), k=length)
