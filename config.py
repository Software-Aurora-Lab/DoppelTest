"""Command-line configurable DoppelTest settings."""

import logging
from pathlib import Path
from typing import Any, Dict

from absl import flags

FLAGS = flags.FLAGS

_DEFAULT_DT_ROOT = Path(__file__).parent

# APOLLO CONFIGURATION ==============================
flags.DEFINE_integer(
    "perception_frequency",
    25,
    "Rate at which the Message Broker publishes perception messages.",
    lower_bound=1,
)
flags.DEFINE_float(
    "apollo_vehicle_length", 4.933, "Length of the default Apollo vehicle.",
    lower_bound=0.0,
)
flags.DEFINE_float(
    "apollo_vehicle_width", 2.11, "Width of the default Apollo vehicle.",
    lower_bound=0.0,
)
flags.DEFINE_float(
    "apollo_vehicle_height", 1.48, "Height of the default Apollo vehicle.",
    lower_bound=0.0,
)
flags.DEFINE_float(
    "apollo_vehicle_back_edge_to_center",
    1.043,
    "Distance between the back edge and center of the default Apollo vehicle.",
    lower_bound=0.0,
)

# DIRECTORIES =======================================
flags.DEFINE_string("dt_root", str(_DEFAULT_DT_ROOT), "Root directory of DoppelTest.")
flags.DEFINE_string(
    "apollo_root",
    None,
    "Root directory of Apollo 7.0. Defaults to <dt_root>/apollo-doppeltest.",
)
flags.DEFINE_string(
    "records_dir",
    None,
    "Directory used to save record files. Defaults to <dt_root>/data/records.",
)
flags.DEFINE_string(
    "doppeltest_log_dir",
    None,
    "Directory used to save log files. Defaults to <dt_root>/data/Logs.",
)

# DoppelTest CONFIGS ================================
flags.DEFINE_enum(
    "stream_logging_level",
    "INFO",
    ["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"],
    "Global console logging level.",
)
flags.DEFINE_bool(
    "use_sim_control_standalone",
    True,
    "Whether to use extracted SimControl when executing a scenario.",
)
flags.DEFINE_bool(
    "force_invalid_traffic_control",
    False,
    "Whether to force invalid traffic control, such as every signal being green.",
)
flags.DEFINE_integer(
    "scenario_upper_limit", 30, "Length of each scenario in seconds.", lower_bound=10,
)
flags.DEFINE_integer(
    "instance_max_wait_time",
    15,
    "Maximum delay before the last ADS instance starts moving.",
    lower_bound=0,
)
flags.DEFINE_integer(
    "max_adc_count",
    5,
    "Maximum number of ADS instances to run simultaneously.",
    lower_bound=2,
)
flags.DEFINE_integer(
    "max_pd_count",
    5,
    "Maximum number of pedestrians to include in simulations.",
    lower_bound=0,
)
flags.DEFINE_float(
    "run_for_hour", 12.0, "Number of hours to run.", lower_bound=0.0,
)

# Also update ``apollo/modules/common/data/global_flagfile.txt`` to match the
# HD map selected here.
flags.DEFINE_string("hd_map", "borregas_ave", "HD map to use.")

_FLAG_NAMES: Dict[str, str] = {
    "PERCEPTION_FREQUENCY": "perception_frequency",
    "APOLLO_VEHICLE_LENGTH": "apollo_vehicle_length",
    "APOLLO_VEHICLE_WIDTH": "apollo_vehicle_width",
    "APOLLO_VEHICLE_HEIGHT": "apollo_vehicle_height",
    "APOLLO_VEHICLE_back_edge_to_center": "apollo_vehicle_back_edge_to_center",
    "DT_ROOT": "dt_root",
    "APOLLO_ROOT": "apollo_root",
    "RECORDS_DIR": "records_dir",
    "LOG_DIR": "doppeltest_log_dir",
    "STREAM_LOGGING_LEVEL": "stream_logging_level",
    "USE_SIM_CONTROL_STANDALONE": "use_sim_control_standalone",
    "FORCE_INVALID_TRAFFIC_CONTROL": "force_invalid_traffic_control",
    "SCENARIO_UPPER_LIMIT": "scenario_upper_limit",
    "INSTANCE_MAX_WAIT_TIME": "instance_max_wait_time",
    "MAX_ADC_COUNT": "max_adc_count",
    "MAX_PD_COUNT": "max_pd_count",
    "RUN_FOR_HOUR": "run_for_hour",
    "HD_MAP": "hd_map",
}


def __getattr__(name: str) -> Any:
    """Return the current flag-backed value for a legacy config name."""
    try:
        value = FLAGS[_FLAG_NAMES[name]].value
    except KeyError as exc:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}") from exc

    if value is None:
        relative_path = {
            "APOLLO_ROOT": ("apollo-doppeltest",),
            "RECORDS_DIR": ("data", "records"),
            "LOG_DIR": ("data", "Logs"),
        }[name]
        value = str(Path(__getattr__("DT_ROOT"), *relative_path))

    if name in {"DT_ROOT", "APOLLO_ROOT"}:
        return Path(value)
    if name == "STREAM_LOGGING_LEVEL":
        return getattr(logging, value)
    return value


def __dir__() -> list:
    """Include dynamically resolved settings in interactive discovery."""
    return sorted(set(globals()) | set(_FLAG_NAMES))
