"""
Global configurations for the framework

PERCEPTION_FREQUENCY: number of cycles per second to publish perception

APOLLO_VEHICLE_LENGTH: length of apollo vehicle
APOLLO_VEHICLE_WIDTH: width of apollo vehicle
APOLLO_VEHICLE_HEIGHT: height of apollo vehicle

APOLLO_ROOT: root directory of Baidu Apollo

STREAM_LOGGING_LEVEL: global logging level
"""

import logging

PERCEPTION_FREQUENCY = 10

APOLLO_VEHICLE_LENGTH = 4.70
APOLLO_VEHICLE_WIDTH = 2.06
APOLLO_VEHICLE_HEIGHT = 2.05

APOLLO_ROOT = '/home/yuqi/ResearchWorkspace/apollo'

STREAM_LOGGING_LEVEL = logging.INFO

USE_SIM_CONTROL_STANDALONE = True
