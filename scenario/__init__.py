from dataclasses import dataclass
from enum import Enum
from modules.map.proto.map_pb2 import Map
from typing import List, Tuple

from scenario.ApolloRunner import PositionEstimate
from utils import random_numeric_id


class ScenarioEventType(Enum):
    VEHICLE_ROUTING = 0
    TRAFFIC_CONTROL = 1


@dataclass
class ApolloInstance:
    uid: str
    nid: str
    start_time: int
    initial: PositionEstimate
    destination: PositionEstimate


@dataclass
class ScenarioGene:
    start_times: List[int]
    lane_s: List[Tuple[float, float]]


@dataclass
class Scenario:
    map: Map
    routings: List[Tuple[str, str]]
