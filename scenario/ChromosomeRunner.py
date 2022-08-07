from logging import Logger
import threading
import time
from typing import List, Optional
from apollo.ApolloContainer import ApolloContainer
from apollo.MessageBroker import MessageBroker
from automation.Chromosome import Chromosome
from modules.map.proto.map_pb2 import Map
from scenario.ApolloRunner import ApolloRunner

from utils import clean_appolo_dir, get_logger, get_scenario_logger, random_numeric_id, save_record_files


class ChromosomeRunner:
    logger: Logger
    map: Map
    containers: List[ApolloContainer]
    curr_chromosome: Optional[Chromosome]
    is_initialized: bool

    __runners: List[ApolloRunner]

    def __init__(self, map: Map, containers: List[ApolloContainer]) -> None:
        self.logger = get_logger('ChromosomeRunner')
        self.map = map
        self.containers = containers
        self.curr_chromosome = None
        self.is_initialized = False

    def set_chromosome(self, c: Chromosome):
        self.logger.info('Setting chromosome')
        self.curr_chromosome = c
        self.is_initialized = False

    def init_scenario(self):
        self.logger.info('Initializing Scenario')
        nids = random_numeric_id(len(self.curr_chromosome.AD.adcs))
        self.__runners = list()
        for i, c, a in zip(nids, self.containers, self.curr_chromosome.AD.adcs):
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
        self.is_initialized = True

    def run_scenario(self, run_id: str, upper_limit=30, save_record=False):
        self.logger.info('Running scenario')
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
            exit_reasons = list()
            for ar in self.__runners:
                if ar.should_send_routing(runner_time):
                    ar.send_routing()
                exit_reasons.append(ar.get_exit_reason())

            if runner_time % 100 == 0:
                scenario_logger.info(
                    f'Scenario time: {round(runner_time / 1000, 1)}. Status: {exit_reasons}')

            if all(exit_reasons):
                scenario_logger.info("\n")
                self.logger.info(f'Stop reasons: {exit_reasons}')
                break
            elif runner_time / 1000 > upper_limit:
                self.logger.info(
                    f'Stopped. Scenario over {upper_limit} seconds')
                break
            time.sleep(0.1)
            runner_time += 100

        if save_record:
            for r in self.__runners:
                r.container.stop_recorder()
            # buffer period for recorders to stop
            time.sleep(2)
            save_record_files()
        # scenario ended
        for runner in self.__runners:
            runner.stop('MAIN')
        mbk.stop()

        self.logger.info(
            f'Scenario ended. Length: {round(runner_time/1000, 2)} seconds.')

        self.is_initialized = False
        self.curr_chromosome = None
        self.logger.info('Scenario ended')
