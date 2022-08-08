
from modules.map.proto.map_pb2 import Map
from apollo.ApolloContainer import ApolloContainer
from automation.Chromosome import Chromosome
from map.MapAnalyzer import MapAnalyzer
from scenario.ChromosomeRunner import ChromosomeRunner
from utils import make_dir_for_generation
from utils.config import APOLLO_ROOT
from uuid import uuid4
map = Map()
f = open('./data/maps/borregas_ave_fix/base_map.bin', 'rb')
map.ParseFromString(f.read())

ma = MapAnalyzer(map)

pop = [Chromosome.get_one(ma) for _ in range(10)]

containers = [ApolloContainer(APOLLO_ROOT, f'ROUTE_{x}') for x in range(5)]
for ctn in containers:
    ctn.start_instance()
    ctn.start_dreamview()
    print(f'Dreamview running at http://{ctn.ip}:{ctn.port}')

make_dir_for_generation('TestGeneration')

for chromosome in pop:

    runner = ChromosomeRunner(map, containers)
    counter = 0
    while True:
        print(counter)
        print([x.start_time for x in chromosome.AD.adcs])
        runner.set_chromosome(chromosome)
        runner.init_scenario()
        runner.run_scenario(generation_name='TestGeneration', run_id=f'{str(uuid4())}',
                            upper_limit=55, save_record=True)
        counter += 1
        break
