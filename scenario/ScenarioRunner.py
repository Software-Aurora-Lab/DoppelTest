
from logging import Logger
import threading
import time
from typing import List, Optional
from apollo.MessageBroker import MessageBroker
from apollo.ApolloContainer import ApolloContainer

from scenario import Scenario, ScenarioGene
from scenario.ApolloRunner import ApolloRunner, PositionEstimate
from utils import get_logger, get_scenario_logger, random_numeric_id
from utils.config import APOLLO_ROOT


class ScenarioRunner:
    scenario: Scenario
    containers: List[ApolloContainer]
    runners: List[ApolloRunner]
    gene: Optional[ScenarioGene]
    logger: Logger

    def __init__(self, scenario: Scenario) -> None:
        self.scenario = scenario
        self.containers = list()
        for index, routing in enumerate(self.scenario.routings):
            ctn = ApolloContainer(APOLLO_ROOT, f'ROUTE_{index}')
            self.containers.append(ctn)
        self.gene = None
        self.logger = get_logger(f"ScenarioRunner")

    def start_instances(self):
        self.logger.info('Starting instances')
        for ctn in self.containers:
            ctn.start_instance()

        threads = list()
        for index in range(len(self.containers)):
            t = threading.Thread(
                target=self.containers[index].start_dreamview)
            t.start()
            threads.append(t)

            t = threading.Thread(
                target=self.containers[index].start_bridge)
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

    def initialize_scenario(self, gene: ScenarioGene):
        self.logger.info('Initializing scenario')
        self.runners = list()
        nids = random_numeric_id(len(self.containers))
        for index, routing in enumerate(self.scenario.routings):
            ar = ApolloRunner(
                nid=nids[index],
                ctn=self.containers[index],
                map=self.scenario.map,
                start=PositionEstimate(routing[0], gene.lane_s[index][0]),
                destination=PositionEstimate(
                    routing[1], gene.lane_s[index][1]),
                start_time=gene.start_times[index]
            )
            self.runners.append(ar)

        threads = list()
        for index in range(len(self.runners)):
            threads.append(threading.Thread(
                target=self.runners[index].initialize
            ))
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        for runner in self.runners:
            runner.container.bridge.spin()

        self.gene = gene

    def run(self, scenario_name: str, upper_limit=90):
        if not self.gene:
            self.logger.error('Gene has not been initialized.')
            return
        self.logger.info(f'Started scenario {scenario_name}')

        mbk = MessageBroker(self.runners)
        mbk.spin()

        runner_time = 0
        scenario_logger = get_scenario_logger()
        # starting scenario
        for container in self.containers:
            container.start_recorder(scenario_name)
        while True:
            exit_reasons = list()
            for ar in self.runners:
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
        # scenario ended
        for container in self.containers:
            container.stop_recorder()
        for runner in self.runners:
            runner.stop('MAIN')
        mbk.stop()

        self.logger.info(
            f'Scenario ended. Length: {round(runner_time/1000, 2)} seconds.')

        return
