from apollo.ApolloContainer import ApolloContainer
from config import APOLLO_ROOT, HD_MAP, MAX_ADC_COUNT
from framework.scenario import Scenario
from framework.scenario.ad_agents import ADAgent, ADSection
from framework.scenario.pd_agents import PDSection
from framework.scenario.ScenarioRunner import ScenarioRunner
from framework.scenario.tc_config import TCSection
from hdmap.MapParser import MapParser

ma = MapParser.get_instance(HD_MAP)

x = Scenario(
    ad_section=ADSection(
        [
            ADAgent(['lane_25', 'lane_19'], 105, 40, 0),
            ADAgent(['lane_25', 'lane_19'], 115, 40, 0),
            ADAgent(['lane_25', 'lane_19'], 125, 40, 0),
        ]
    ),
    pd_section=PDSection([]),
    tc_section=TCSection.get_one())
x.gid = 0
x.cid = 0

containers = [ApolloContainer(
    APOLLO_ROOT, f'ROUTE_{x}') for x in range(3)]
for ctn in containers:
    print(f'{ctn.container_name}: starting')
    ctn.start_instance()
    ctn.start_dreamview()
    print(f'Dreamview at http://{ctn.ip}:{ctn.port}')

srunner = ScenarioRunner(containers)
x.gid = 0
x.cid = 0

g_name = f'Generation_{x.gid:05}'
s_name = f'Scenario_{x.cid:05}'
srunner = ScenarioRunner.get_instance()
srunner.set_scenario(x)
srunner.init_scenario()
srunner.run_scenario(g_name, s_name, False)
