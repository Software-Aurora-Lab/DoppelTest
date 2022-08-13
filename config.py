"""
Global configurations for the framework
"""


import logging


# APOLLO CONFIGURATION ==============================
PERCEPTION_FREQUENCY = 25

APOLLO_VEHICLE_LENGTH = 4.933
APOLLO_VEHICLE_WIDTH = 2.11
APOLLO_VEHICLE_HEIGHT = 1.48
APOLLO_VEHICLE_back_edge_to_center = 1.043


# DIRECTORIES =======================================
APOLLO_ROOT = '/home/yuqi/ResearchWorkspace/apollo'
RECORDS_DIR = '/home/yuqi/ResearchWorkspace/MAGGIE/data/records'
LOG_DIR = '/home/yuqi/ResearchWorkspace/MAGGIE/data/Logs'

# MAGGIE CONFIGS ====================================
STREAM_LOGGING_LEVEL = logging.INFO
USE_SIM_CONTROL_STANDALONE = True
FORCE_INVALID_TRAFFIC_CONTROL = True
SCENARIO_UPPER_LIMIT = 55
INSTANCE_MAX_WAIT_TIME = 15
MAX_ADC_COUNT = 5
