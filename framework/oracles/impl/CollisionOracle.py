from typing import List, Optional, Tuple
from framework.oracles.OracleInterface import OracleInterface
from modules.localization.proto.localization_pb2 import LocalizationEstimate
from modules.perception.proto.perception_obstacle_pb2 import PerceptionObstacles
from apollo.utils import generate_adc_polygon
from shapely.geometry import Polygon
import numpy as np


class CollisionOracle(OracleInterface):
    last_localization: Optional[LocalizationEstimate]
    last_perception: Optional[PerceptionObstacles]
    distances: List[Tuple[float, int]]

    def __init__(self) -> None:
        self.last_localization = None
        self.last_perception = None
        self.distances = list()

    def get_interested_topics(self):
        return [
            '/apollo/localization/pose',
            '/apollo/perception/obstacles'
        ]

    def on_new_message(self, topic: str, message, t):
        if topic == '/apollo/localization/pose':
            self.last_localization = message
        else:
            self.last_perception = message

        if self.last_localization is None or self.last_perception is None:
            # cannot analyze
            return

        # begin analyze
        adc_pose = self.last_localization.pose
        adc_polygon_pts = generate_adc_polygon(
            adc_pose.position, adc_pose.heading)
        adc_polygon = Polygon([[x.x, x.y] for x in adc_polygon_pts])

        for obs in self.last_perception.perception_obstacle:
            obs_polygon = Polygon([[x.x, x.y] for x in obs.polygon_point])
            self.distances.append((adc_polygon.distance(obs_polygon), obs.id))

    def get_result(self):
        result = list()
        if len(self.distances) == 0:
            return result
        for dis in self.distances:
            if dis[0] == 0.0:
                violation = ('collision', dis[1])
                if violation not in result:
                    result.append(violation)
        return result
