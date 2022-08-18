from typing import Optional
from framework.oracles.OracleInterface import OracleInterface
from modules.localization.proto.localization_pb2 import LocalizationEstimate
from shapely.geometry import Point


class ModuleOracle(OracleInterface):
    prev_: Optional[LocalizationEstimate]
    next_: Optional[LocalizationEstimate]

    distance_traveled: float

    def __init__(self) -> None:
        self.prev_ = None
        self.next_ = None
        self.distance_traveled = -1.0

    def get_interested_topics(self):
        return [
            '/apollo/localization/pose',
        ]

    def on_new_message(self, topic: str, message, t):
        if self.prev_ is None and self.next_ is None:
            self.prev_ = message
            self.distance_traveled = 0.0
            return
        self.next_ = message
        # analyze
        prev_point = Point(self.prev_.pose.position.x,
                           self.prev_.pose.position.y)
        next_point = Point(self.next_.pose.position.x,
                           self.next_.pose.position.y)
        self.distance_traveled += next_point.distance(prev_point)
        # update prev_
        self.prev_ = message

    def get_result(self):
        result = list()
        if self.distance_traveled == 0.0:
            result.append(('module', 'routing failure'))
        elif self.distance_traveled == -1.0:
            result.append(('module', 'sim control failure'))
        return result
