from logging import Logger
from threading import Thread
from typing import List
import time
from apollo.ApolloContainer import ApolloContainer
from modules.common.proto.geometry_pb2 import Point3D
from modules.common.proto.header_pb2 import Header
from modules.localization.proto.localization_pb2 import LocalizationEstimate
from modules.perception.proto.perception_obstacle_pb2 import PerceptionObstacle, PerceptionObstacles
from scenario.ApolloRunner import ApolloRunner
from apollo.CyberBridge import Channel, Topics
from utils import get_logger

PERCEPTION_FREQUENCY = 10

APOLLO_VEHICLE_LENGTH = 4.70
APOLLO_VEHICLE_WIDTH = 2.06
APOLLO_VEHICLE_HEIGHT = 2.05


def localization_to_obstacle(_id: int, data: LocalizationEstimate) -> PerceptionObstacle:
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
        sub_type=PerceptionObstacle.ST_CAR
    )
    return obs


class MessageBroker:
    runners: List[ApolloRunner]
    spinning: bool
    logger: Logger
    t: Thread

    def __init__(self, runners: List[ApolloRunner]) -> None:
        self.runners = runners
        self.spinning = False
        self.logger = get_logger('MessageBroker')

    def broadcast(self, channel: Channel, data: bytes):
        for runner in self.runners:
            runner.container.bridge.publish(channel, data)

    def spin(self):
        self.logger.info('Starting to spin')
        if self.spinning:
            # already spinning
            return

        def forever():
            header_sequence_num = 0
            while self.spinning:
                # retrieve localization of running instances
                locations = dict()
                for runner in self.runners:
                    if runner.is_running:
                        loc = runner.localization
                        if loc and loc.header.module_name == 'SimControl':
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

        self.t = Thread(target=forever)
        self.spinning = True
        self.t.start()

    def stop(self):
        self.logger.info('Stopping')
        if not self.spinning:
            # Not running
            return
        self.spinning = False
        self.t.join()
