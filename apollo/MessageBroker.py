from logging import Logger
import math
from threading import Thread
from typing import List
import time
from modules.common.proto.geometry_pb2 import Point3D
from modules.common.proto.header_pb2 import Header
from modules.localization.proto.localization_pb2 import LocalizationEstimate
from modules.perception.proto.perception_obstacle_pb2 import PerceptionObstacle, PerceptionObstacles
from scenario.ApolloRunner import ApolloRunner
from apollo.CyberBridge import Channel, Topics
from utils import get_logger
from utils.config import APOLLO_VEHICLE_HEIGHT, APOLLO_VEHICLE_LENGTH, APOLLO_VEHICLE_WIDTH, PERCEPTION_FREQUENCY


def generate_polygon(position: Point3D, theta: float, length: float, width: float):
    """
    Generate polygon for an perception obstacle

    Parameters:
        position: Point3D
            position vector of the obstacle
        theta: float
            heading of the obstacle
        length: float
            length of the obstacle
        width: float
            width of the obstacle

    Returns:
        points: List[Point3D]
            polygon points of the obstacle
    """
    points = []
    half_l = length / 2.0
    half_w = width / 2.0
    sin_h = math.sin(theta)
    cos_h = math.cos(theta)
    vectors = [(half_l * cos_h - half_w * sin_h,
                half_l * sin_h + half_w * cos_h),
               (-half_l * cos_h - half_w * sin_h,
                - half_l * sin_h + half_w * cos_h),
               (-half_l * cos_h + half_w * sin_h,
                - half_l * sin_h - half_w * cos_h),
               (half_l * cos_h + half_w * sin_h,
                half_l * sin_h - half_w * cos_h)]
    for x, y in vectors:
        p = Point3D()
        p.x = position.x + x
        p.y = position.y + y
        p.z = position.z
        points.append(p)
    return points


def localization_to_obstacle(_id: int, data: LocalizationEstimate) -> PerceptionObstacle:
    """
    Converts LocalizationEstimate to PerceptionObstacle

    Parameters:
        _id: int
            id used to construct obstacle
        data: LocalizationEstimate
            localization result for an Apollo instance

    Returns:
        obs: PerceptionObstacle
            prepared data which is ready to be sent as PerceptionObstacle
    """
    position = Point3D(x=data.pose.position.x,
                       y=data.pose.position.y, z=data.pose.position.z)
    velocity = Point3D(x=data.pose.linear_velocity.x,
                       y=data.pose.linear_velocity.y, z=data.pose.linear_velocity.z)
    obs = PerceptionObstacle(
        id=_id,
        position=position,
        theta=data.pose.heading,
        velocity=velocity,
        acceleration=data.pose.linear_acceleration,
        length=APOLLO_VEHICLE_LENGTH,
        width=APOLLO_VEHICLE_WIDTH,
        height=APOLLO_VEHICLE_HEIGHT,
        type=PerceptionObstacle.VEHICLE,
        sub_type=PerceptionObstacle.ST_CAR,
        timestamp=data.header.timestamp_sec,
        polygon_point=generate_polygon(
            position, data.pose.heading, APOLLO_VEHICLE_LENGTH, APOLLO_VEHICLE_WIDTH)
    )
    return obs


class MessageBroker:
    """
    Class to represent MessageBroker

    Attributes:
    runners: List[ApolloRunners]
        list of running Apollo instances
    spinning: bool
        whether the message broker should forward localization as obstacle
    logger: Logger
        logging the status of the message broker
    t: Thread
        background thread to forward data
    """
    runners: List[ApolloRunner]
    spinning: bool
    logger: Logger
    t: Thread

    def __init__(self, runners: List[ApolloRunner]) -> None:
        """
        Constructs all the attributes for MessageBroker

        Parameters:
            runners: List[ApolloRunner]
                list of running Apollo instances
        """
        self.runners = runners
        self.spinning = False
        self.logger = get_logger('MessageBroker')

    def broadcast(self, channel: Channel, data: bytes):
        """
        Sends data to every instance

        Parameters:
            channel: Channel
                channel to send data to
            data: bytes
                data to be sent
        """
        for runner in self.runners:
            runner.container.bridge.publish(channel, data)

    def _spin(self):
        """
        Helper function to start forwarding localization
        """
        header_sequence_num = 0
        while self.spinning:
            # retrieve localization of running instances
            locations = dict()
            for runner in self.runners:
                if runner.is_running:
                    loc = runner.localization
                    if loc and loc.header.module_name == 'SimControlStandalone':
                        locations[runner.nid] = runner.localization

            # convert localization into obstacles
            obs = dict()
            for k in locations:
                obs[k] = localization_to_obstacle(k, locations[k])

            # publish obstacle to all running instances
            for runner in self.runners:
                if runner.is_running:
                    perception_obs = [obs[x]
                                      for x in obs if x != runner.nid]
                    header = Header(
                        timestamp_sec=time.time(),
                        module_name='MAGGIE',
                        sequence_num=header_sequence_num
                    )
                    bag = PerceptionObstacles(
                        header=header,
                        perception_obstacle=perception_obs,
                    )
                    runner.container.bridge.publish(
                        Topics.Obstacles, bag.SerializeToString()
                    )
            header_sequence_num += 1
            time.sleep(1/PERCEPTION_FREQUENCY)

    def spin(self):
        """
        Starts to forward localization
        """
        self.logger.debug('Starting to spin')
        if self.spinning:
            return
        self.t = Thread(target=self._spin)
        self.spinning = True
        self.t.start()

    def stop(self):
        """
        Stops forwarding localization
        """
        self.logger.debug('Stopping')
        if not self.spinning:
            return
        self.spinning = False
        self.t.join()
