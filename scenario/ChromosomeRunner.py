from logging import Logger
import threading
import time
from typing import List, Optional
from apollo.ApolloContainer import ApolloContainer
from apollo.CyberBridge import Topics
from apollo.MessageBroker import MessageBroker
from automation.Chromosome import Chromosome
from modules.map.proto.map_pb2 import Map
from apollo.ApolloRunner import ApolloRunner

from utils import clean_appolo_dir, get_logger, get_scenario_logger, random_numeric_id, save_record_files_and_chromosome
from scenario.TrafficManager import TrafficControlManager


class ChromosomeRunner:
    logger: Logger
    map: Map
    containers: List[ApolloContainer]
    curr_chromosome: Optional[Chromosome]
    tm: TrafficControlManager
    is_initialized: bool
    __instance = None

    __runners: List[ApolloRunner]

    def __init__(self, map: Map, containers: List[ApolloContainer]) -> None:
        self.logger = get_logger('ChromosomeRunner')
        self.map = map
        self.containers = containers
        self.curr_chromosome = None
        self.is_initialized = False
        ChromosomeRunner.__instance = self

    @staticmethod
    def get_instance():
        return ChromosomeRunner.__instance

    def set_chromosome(self, c: Chromosome):
        self.logger.debug('Setting chromosome')
        self.curr_chromosome = c
        self.is_initialized = False

    def init_scenario(self):
        self.logger.debug('Initializing Scenario')
        nids = random_numeric_id(len(self.curr_chromosome.AD.adcs))
        self.__runners = list()
        for i, c, a in zip(nids, self.containers, self.curr_chromosome.AD.adcs):
            a.apollo_container = c.container_name
            self.__runners.append(
                ApolloRunner(
                    nid=i,
                    ctn=c,
                    map=self.map,
                    start=a.initial_position,
                    destination=a.final_position,
                    start_time=a.start_time
                )
            )
        threads = list()
        for index in range(len(self.__runners)):
            threads.append(threading.Thread(
                target=self.__runners[index].initialize
            ))
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        clean_appolo_dir()
        self.tm = TrafficControlManager(self.curr_chromosome.TC)
        self.is_initialized = True

    def run_scenario(self, generation_name: str, run_id: str, upper_limit=30, save_record=False):
        num_adc = len(self.curr_chromosome.AD.adcs)
        self.logger.info(
            f'{num_adc} agents running a scenario G{self.curr_chromosome.gid}S{self.curr_chromosome.cid}.'
        )
        if self.curr_chromosome is None or not self.is_initialized:
            return

        mbk = MessageBroker(self.__runners)
        mbk.spin()

        runner_time = 0
        scenario_logger = get_scenario_logger()
        # starting scenario
        if save_record:
            for r in self.__runners:
                r.container.start_recorder(run_id)
        while True:
            tld = self.tm.get_traffic_configuration(runner_time/1000)
            mbk.broadcast(Topics.TrafficLight, tld.SerializeToString())
            for ar in self.__runners:
                if ar.should_send_routing(runner_time/1000):
                    ar.send_routing()

            if runner_time % 100 == 0:
                scenario_logger.info(
                    f'Scenario time: {round(runner_time / 1000, 1)}.')

            if runner_time / 1000 >= upper_limit:
                scenario_logger.info('\n')
                break
            time.sleep(0.1)
            runner_time += 100

        if save_record:
            for r in self.__runners:
                r.container.stop_recorder()
            # buffer period for recorders to stop
            time.sleep(2)
            save_record_files_and_chromosome(
                generation_name,
                run_id, self.curr_chromosome.to_dict())
        # scenario ended
        for runner in self.__runners:
            runner.stop('MAIN')
        mbk.stop()

        self.logger.debug(
            f'Scenario ended. Length: {round(runner_time/1000, 2)} seconds.')

        self.is_initialized = False
        self.curr_chromosome = None
