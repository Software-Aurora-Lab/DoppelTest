from absl import app

from apollo.ApolloContainer import ApolloContainer
import config
from framework.scenario import Scenario
from framework.scenario.ad_agents import ADAgent, ADSection
from framework.scenario.pd_agents import PDSection
from framework.scenario.ScenarioRunner import ScenarioRunner
from framework.scenario.tc_config import TCSection
from hdmap.MapParser import MapParser


def main(_: list) -> None:
    MapParser.get_instance(config.HD_MAP)

    scenario = Scenario(
        ad_section=ADSection(
            [
                ADAgent(['lane_25', 'lane_19'], 105, 40, 0),
                ADAgent(['lane_25', 'lane_19'], 115, 40, 0),
                ADAgent(['lane_25', 'lane_19'], 125, 40, 0),
            ]
        ),
        pd_section=PDSection([]),
        tc_section=TCSection.get_one())
    scenario.gid = 0
    scenario.cid = 0

    containers = [
        ApolloContainer(config.APOLLO_ROOT, f'ROUTE_{index}')
        for index in range(3)
    ]
    for container in containers:
        print(f'{container.container_name}: starting')
        container.start_instance()
        container.start_dreamview()
        print(f'Dreamview at http://{container.ip}:{container.port}')

    ScenarioRunner(containers)
    g_name = f'Generation_{scenario.gid:05}'
    s_name = f'Scenario_{scenario.cid:05}'
    scenario_runner = ScenarioRunner.get_instance()
    scenario_runner.set_scenario(scenario)
    scenario_runner.init_scenario()
    scenario_runner.run_scenario(g_name, s_name, False)


if __name__ == '__main__':
    app.run(main)
