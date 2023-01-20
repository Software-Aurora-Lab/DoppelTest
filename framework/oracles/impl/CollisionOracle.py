from typing import List, Optional, Tuple
from framework.oracles.OracleInterface import OracleInterface
from modules.localization.proto.localization_pb2 import LocalizationEstimate
from modules.perception.proto.perception_obstacle_pb2 import PerceptionObstacles
from apollo.utils import generate_adc_polygon, calculate_velocity
from shapely.geometry import Polygon


class CollisionOracle(OracleInterface):
    """
    The Collision Oracle is responsibe for determining whether a collision occurred
    between the ADC instance and another road traffic participants.
    """
    last_localization: Optional[LocalizationEstimate]
    last_perception: Optional[PerceptionObstacles]
    distances: List[Tuple[float, int]]

    def __init__(self) -> None:
        self.last_localization = None
        self.last_perception = None
        self.distances = list()

    def get_interested_topics(self):
        """
        The collision oracle is interested in Localization messages and Perception
        messages.
        """
        return [
            '/apollo/localization/pose',
            '/apollo/perception/obstacles'
        ]

    def on_new_message(self, topic: str, message, t):
        """
        Upon receiving a new planning/perception message, the oracle analyzes
        the position of the ADS instance and position of all obstacles to determine
        whether a collision occurred, i.e., the distance between 2 objects is 0

        :param str topic: topic of the message
        :param any message: either Planning or Localization message
        :param float t: the timestamp
        """
        if topic == '/apollo/localization/pose':
            self.last_localization = message
        else:
            self.last_perception = message

        if self.last_localization is None or self.last_perception is None:
            # cannot analyze
            return

        # begin analyze
        adc_pose = self.last_localization.pose

        if self.is_adc_completely_stopped():
            return

        adc_polygon_pts = generate_adc_polygon(
            adc_pose.position, adc_pose.heading)
        adc_polygon = Polygon([[x.x, x.y] for x in adc_polygon_pts])

        for obs in self.last_perception.perception_obstacle:
            obs_polygon = Polygon([[x.x, x.y] for x in obs.polygon_point])
            self.distances.append((adc_polygon.distance(obs_polygon), obs.id))

    def is_adc_completely_stopped(self) -> bool:
        """
        Helper function to check if the ADS instance is completely stopper or not.

        :returns: True if completely stopped
        :rtype: bool
        """
        adc_pose = self.last_localization.pose
        adc_velocity = calculate_velocity(adc_pose.linear_velocity)

        # https://github.com/ApolloAuto/apollo/blob/0789b7ea1e1356dde444452ab21b51854781e304/modules/planning/scenarios/stop_sign/unprotected/stage_pre_stop.cc#L237
        # return adc_velocity <= self.MAX_ABS_SPEED_WHEN_STOPPED
        return adc_velocity == 0

    def get_result(self) -> List[Tuple]:
        """
        Returns violations detected by this oracle, the obstacle's ID is included in
        the output to distinguish between pedestrian and vehicle

        :returns: all violations detected by this oracle
        :rtype: List[Tuple]
        """
        result = list()
        if len(self.distances) == 0:
            return result
        for dis in self.distances:
            if dis[0] == 0.0:
                violation = ('collision', dis[1])
                if violation not in result:
                    result.append(violation)
        return result
