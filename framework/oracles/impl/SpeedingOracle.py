
from framework.oracles.OracleInterface import OracleInterface
from typing import List
from apollo.utils import calculate_velocity
from hdmap.MapParser import MapParser
from shapely.geometry import Point


class SpeedingOracle(OracleInterface):

    def __init__(self) -> None:
        self.result = None
        self.mp = MapParser.get_instance()
        self.lanes = dict()

        for lane in self.mp.get_lanes():
            lane_obj = self.mp.get_lane_by_id(lane)
            speed_limit = lane_obj.speed_limit
            central_curve = self.mp.get_lane_central_curve(lane)
            self.lanes[lane] = (speed_limit, central_curve)

        self.cached_lanes = set()

    def get_interested_topics(self) -> List[str]:
        return ['/apollo/localization/pose']

    def on_new_message(self, topic: str, message, t):
        if self.result is not None:
            # violation already detected
            return

        p = message.pose.position
        ego_position = Point(p.x, p.y, p.z)
        ego_velocity = calculate_velocity(message.pose.linear_velocity)
        for lane_id in self.cached_lanes:
            lane_speed_limit, lane_curve = self.lanes[lane_id]
            ego_position.distance(lane_curve)
            if ego_position.distance(lane_curve) <= 1:
                if ego_velocity > lane_speed_limit:
                    self.result = ((p.x, p.y),
                        f'{ego_velocity} violates speed limit {lane_speed_limit} at {lane_id}')
                return

        for lane_id in self.lanes:
            lane_speed_limit, lane_curve = self.lanes[lane_id]
            if round(ego_position.distance(lane_curve), 1) <= 1:
                self.update_cached_lanes(lane_id)
                if ego_velocity > lane_speed_limit:
                    self.result = ((p.x, p.y),
                                   f'{ego_velocity} violates speed limit {lane_speed_limit} at {lane_id}')
                return

    def update_cached_lanes(self, lane_id:str):
        self.cached_lanes.add(lane_id)

    def get_result(self):
        if self.result is None:
            return list()
        return [
            ('speed violation', self.result)
        ]
