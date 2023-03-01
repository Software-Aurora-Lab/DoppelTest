import time
from logging import Logger
from threading import Thread
from typing import List

from apollo.ApolloRunner import ApolloRunner
from apollo.CyberBridge import Channel, Topics
from apollo.utils import localization_to_obstacle, obstacle_to_polygon
from config import PERCEPTION_FREQUENCY
from framework.scenario.PedestrianManager import PedestrianManager
from modules.common.proto.header_pb2 import Header
from modules.perception.proto.perception_obstacle_pb2 import \
    PerceptionObstacles
from utils import get_logger


class MessageBroker:
    """
    Class to represent MessageBroker, it tracks location of each ADS instance and broadcasts
    perception message to all ADS instances

    :param List[ApolloRunner] runners: list of runners each controlling an ADS instance
    """

    runners: List[ApolloRunner]
    spinning: bool
    logger: Logger
    t: Thread

    def __init__(self, runners: List[ApolloRunner]) -> None:
        """
        Constructor
        """
        self.runners = runners
        self.spinning = False
        self.logger = get_logger('MessageBroker')

    def broadcast(self, channel: Channel, data: bytes):
        """
        Sends data to specified channel of every instance

        :param Channel channel: cyberRT channel to send data to
        :param bytes data: data to be sent
        """
        for runner in self.runners:
            runner.container.bridge.publish(channel, data)

    def _spin(self):
        """
        Helper function to start forwarding localization
        """
        header_sequence_num = 0
        curr_time = 0.0
        while self.spinning:
            # retrieve localization of running instances
            locations = dict()
            for runner in self.runners:
                loc = runner.localization
                if loc and loc.header.module_name == 'SimControl':
                    locations[runner.nid] = runner.localization

            # convert localization into obstacles
            obs = dict()
            obs_poly = dict()
            for k in locations:
                obs[k] = localization_to_obstacle(k, locations[k])
                obs_poly[k] = obstacle_to_polygon(obs[k])

            # pedestrian obstacles
            pm = PedestrianManager.get_instance()
            pds = pm.get_pedestrians(curr_time)

            # publish obstacle to all running instances
            for runner in self.runners:
                perception_obs = [obs[x]
                                  for x in obs if x != runner.nid] + pds
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
            # update closest distance
            for runner in self.runners:
                if runner.nid not in obs_poly:
                    continue
                _adc = obs_poly[runner.nid]
                _obs = [obs_poly[x] for x in obs_poly if x != runner.nid]
                for o in _obs:
                    runner.set_min_distance(_adc.distance(o))
            header_sequence_num += 1
            time.sleep(1/PERCEPTION_FREQUENCY)
            curr_time += 1/PERCEPTION_FREQUENCY

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
