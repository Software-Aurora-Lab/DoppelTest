from dataclasses import dataclass
from typing import List
from modules.common.proto.geometry_pb2 import PointENU

from map.MapAnalyzer import MapAnalyzer


@dataclass
class PD:
    rule_following: bool
    boundary: bool
    initial_positon: PointENU
    final_position: PointENU
    start_time: float


@dataclass
class PDSection:
    pds: List[PD]

    @staticmethod
    def get_one(ma: MapAnalyzer):
        return PDSection(list())
