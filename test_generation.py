from apollo.ApolloContainer import ApolloContainer
from config import APOLLO_ROOT, MAX_ADC_COUNT
from framework.scenario import Scenario
from hdmap.MapParser import MapParser
from framework.scenario.ScenarioRunner import ScenarioRunner

ma = MapParser('./data/maps/borregas_ave/base_map.bin')

x = Scenario.get_one()
x.gid = 0
x.cid = 0

mp = MapParser('./data/maps/borregas_ave/base_map.bin')

containers = [ApolloContainer(
    APOLLO_ROOT, f'ROUTE_{x}') for x in range(MAX_ADC_COUNT)]
for ctn in containers:
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
