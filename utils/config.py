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

PERCEPTION_FREQUENCY = 25

APOLLO_VEHICLE_LENGTH = 4.933
APOLLO_VEHICLE_WIDTH = 2.11
APOLLO_VEHICLE_HEIGHT = 1.48
APOLLO_VEHICLE_back_edge_to_center = 1.043

APOLLO_ROOT = '/home/yuqi/ResearchWorkspace/apollo'

RECORDS_DIR = '/home/yuqi/ResearchWorkspace/MAGGIE/records'

STREAM_LOGGING_LEVEL = logging.INFO

USE_SIM_CONTROL_STANDALONE = True

FORCE_INVALID_TRAFFIC_CONTROL = True

SCENARIO_UPPER_LIMIT = 55
