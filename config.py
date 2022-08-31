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
MAGGIE_ROOT = '/home/yuqi/ResearchWorkspace/MAGGIE'
RECORDS_DIR = f'{MAGGIE_ROOT}/data/records'
LOG_DIR = f'{MAGGIE_ROOT}/data/Logs'

# MAGGIE CONFIGS ====================================
STREAM_LOGGING_LEVEL = logging.INFO
USE_SIM_CONTROL_STANDALONE = True
FORCE_INVALID_TRAFFIC_CONTROL = False
SCENARIO_UPPER_LIMIT = 30
INSTANCE_MAX_WAIT_TIME = 15
MAX_ADC_COUNT = 5
MAX_PD_COUNT = 5
RUN_FOR_HOUR = 12
HD_MAP_PATH = f'{MAGGIE_ROOT}/data/maps/shalun/base_map.bin'
