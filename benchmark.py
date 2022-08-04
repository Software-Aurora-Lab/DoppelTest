
from modules.map.proto.map_pb2 import Map
from scenario import Scenario, ScenarioGene
from scenario.ScenarioRunner import ScenarioRunner

map = Map()
f = open('./data/maps/borregas_ave_fix/base_map.bin', 'rb')
map.ParseFromString(f.read())

scene = Scenario(map, [('lane_25', 'lane_27'), ('lane_25', 'lane_27'),
                 ('lane_25', 'lane_27'), ('lane_25', 'lane_27'), ('lane_25', 'lane_27')])
gene1 = ScenarioGene(
    [1000, 1000, 1000, 1000, 1000],
    [(5, 20), (15, 20), (25, 20), (35, 20), (45, 20)])


scenario_runner = ScenarioRunner(scene)
scenario_runner.start_instances()
counter = 0
while True:
    scenario_runner.initialize_scenario(gene1)
    scenario_runner.run('benchmark', 30)
    counter += 1
    print(counter)
    if counter % 10 == 0:
        for ctn in scenario_runner.containers:
            ctn.restart_dreamview()
