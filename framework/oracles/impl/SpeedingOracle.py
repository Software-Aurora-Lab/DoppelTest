
from framework.oracles.OracleInterface import OracleInterface
from typing import List
from apollo.utils import calculate_velocity
from hdmap.MapParser import MapParser
from shapely.geometry import Point


class SpeedingOracle(OracleInterface):

    def __init__(self) -> None:
        self.result = None
        self.mp = MapParser.get_instance()
        self.lanes = list()

        for lane in self.mp.get_lanes():
            lane_obj = self.mp.get_lane_by_id(lane)
            speed_limit = lane_obj.speed_limit
            central_curve = self.mp.get_lane_central_curve(lane)
            self.lanes.append(
                (lane, speed_limit, central_curve)
            )

        self.lanes.sort(key=lambda x: x[1])  # sort lanes by speed limit

    def get_interested_topics(self) -> List[str]:
        return ['/apollo/localization/pose']

    def on_new_message(self, topic: str, message, t):
        if self.result is not None:
            # violation already detected
            return

        p = message.pose.position
        ego_position = Point(p.x, p.y, p.z)
        ego_velocity = calculate_velocity(message.pose.linear_velocity)

        for lane in self.lanes:
            lane_id, lane_speed_limit, lane_curve = lane
            if round(ego_position.distance(lane_curve), 1) <= 0.1:
                if ego_velocity > lane_speed_limit:
                    self.result = ((p.x, p.y),
                                   f'{ego_velocity} violates speed limit {lane_speed_limit} at {lane_id}')

    def get_result(self):
        if self.result is None:
            return list()
        return [
            ('speed violation', self.result)
        ]
