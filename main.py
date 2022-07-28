
from modules.map.proto.map_pb2 import Map
from scenario import Scenario, ScenarioGene
from scenario.ScenarioRunner import ScenarioRunner

map = Map()
f = open('./data/maps/borregas_ave_fix/base_map.bin', 'rb')
map.ParseFromString(f.read())

scene = Scenario(map, [('lane_25', 'lane_27'), ('lane_23', 'lane_27')])
gene1 = ScenarioGene([1000, 1000], [(170, 20), (10.04, 20)])
gene2 = ScenarioGene([1000, 5000], [(190, 20), (13.04, 20)])
gene3 = ScenarioGene([1000, 1000], [(190, 20), (13.04, 20)])


scenario_runner = ScenarioRunner(scene)
scenario_runner.start_instances()

counter = 0
while True:
    print(counter)
    scenario_runner.initialize_scenario(gene1)
    scenario_runner.run(f'1.{counter}')
    scenario_runner.initialize_scenario(gene2)
    scenario_runner.run(f'2.{counter}')
    scenario_runner.initialize_scenario(gene3)
    scenario_runner.run(f'3.{counter}')
    counter += 3
