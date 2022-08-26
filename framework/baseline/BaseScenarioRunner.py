from typing import Optional
from apollo.ApolloContainer import ApolloContainer
from apollo.ApolloRunner import ApolloRunner
from apollo.CyberBridge import Topics
from apollo.utils import PositionEstimate, clean_appolo_dir
from config import SCENARIO_UPPER_LIMIT
from framework.baseline.DynamicObstacleManager import DynamicObstacleManager
from framework.scenario import Scenario
import time
from framework.scenario.PedestrianManager import PedestrianManager
from modules.common.proto.header_pb2 import Header
from modules.perception.proto.perception_obstacle_pb2 import PerceptionObstacles
from utils import get_scenario_logger, random_numeric_id, save_record_files_and_chromosome


class BaseScenarioRunner:
    container: ApolloContainer
    runner: ApolloRunner
    curr_scenario: Optional[Scenario]
    is_initialized: bool

    def __init__(self, container: ApolloContainer) -> None:
        self.container = container
        self.curr_scenario = None
        self.is_initialized = False

    def set_scenario(self, s: Scenario):
        self.curr_scenario = s
        self.is_initialized = False

    def init_scenario(self):
        adc = self.curr_scenario.ad_section.adcs[0]
        self.runner = ApolloRunner(
            nid=0,
            ctn=self.container,
            start=adc.initial_position,
            start_time=adc.start_t,
            waypoints=adc.waypoints
        )
        self.runner.initialize()
        clean_appolo_dir()
        self.is_initialized = True

    def run_scenario(self, generation_name: str, scenario_name: str, save_record=False):
        runner_time = 0
        scenario_logger = get_scenario_logger()
        nids = random_numeric_id(len(self.curr_scenario.ad_section.adcs) - 1)
        dom = DynamicObstacleManager(
            self.curr_scenario.ad_section.adcs[1:], nids)
        pm = PedestrianManager(self.curr_scenario.pd_section)
        header_sequence_num = 0

        # starting scenario
        if save_record:
            self.runner.container.start_recorder(scenario_name)

        while True:
            # run cycle
            if self.runner.should_send_routing(runner_time/1000):
                self.runner.send_routing()

            pds = pm.get_pedestrians(runner_time/1000)
            obs = dom.get_obstacles(runner_time/1000)

            header = Header(
                timestamp_sec=time.time(),
                module_name='MAGGIE',
                sequence_num=header_sequence_num
            )
            bag = PerceptionObstacles(
                header=header,
                perception_obstacle=pds + obs,
            )

            self.container.bridge.publish(
                Topics.Obstacles, bag.SerializeToString())

            # Print Scenario Time
            if runner_time % 100 == 0:
                scenario_logger.info(
                    f'Scenario time: {round(runner_time / 1000, 1)}.')
            # Check if scenario exceeded upper limit
            if runner_time / 1000 >= SCENARIO_UPPER_LIMIT:
                scenario_logger.info('\n')
                break

            time.sleep(0.1)
            runner_time += 100

        if save_record:
            self.runner.container.stop_recorder()
            # buffer period for recorders to stop
            time.sleep(2)
            save_record_files_and_chromosome(
                generation_name, scenario_name, self.curr_scenario.to_dict())

        self.runner.stop('MAIN')

        return zip(nids, self.curr_scenario.ad_section.adcs[1:])
