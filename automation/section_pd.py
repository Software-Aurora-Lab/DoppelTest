from dataclasses import dataclass
from typing import List
from modules.common.proto.geometry_pb2 import PointENU
from modules.map.proto.map_pb2 import Map


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
    def get_one(map: Map):
        pass
