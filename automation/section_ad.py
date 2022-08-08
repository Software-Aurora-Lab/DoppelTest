
from dataclasses import dataclass
from typing import List

from scenario.ApolloRunner import PositionEstimate
from modules.map.proto.map_pb2 import Map


@dataclass
class AD:
    initial_position: PositionEstimate
    final_position: PositionEstimate
    start_time: float
    apollo_container: str = ''


@dataclass
class ADSection:
    adcs: List[AD]

    @staticmethod
    def get_one(map: Map):
        pass
