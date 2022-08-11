
from modules.map.proto.map_pb2 import Map
from apollo.ApolloContainer import ApolloContainer
from automation.Chromosome import Chromosome
from automation.section_ad import AD, ADSection
from automation.section_pd import PDSection
from automation.section_tc import TCSection
from apollo.utils import PositionEstimate
from scenario.ChromosomeRunner import ChromosomeRunner
from config import APOLLO_ROOT

map = Map()
f = open('./data/maps/borregas_ave_fix/base_map.bin', 'rb')
map.ParseFromString(f.read())

chromosome = Chromosome(
    ADSection(
        [AD(PositionEstimate('lane_25', 55), PositionEstimate('lane_27', 50), 1),
         AD(PositionEstimate('lane_25', 65), PositionEstimate('lane_27', 50), 1),
         AD(PositionEstimate('lane_25', 75), PositionEstimate('lane_27', 50), 1),
         AD(PositionEstimate('lane_25', 85), PositionEstimate('lane_27', 50), 1),
         AD(PositionEstimate('lane_25', 95), PositionEstimate('lane_27', 50), 1)]
    ),
    PDSection([]),
    TCSection(dict(), dict(), 0, 0, 0)
)

containers = [ApolloContainer(APOLLO_ROOT, f'ROUTE_{x}') for x in range(5)]
for ctn in containers:
    ctn.start_instance()
    ctn.start_dreamview()
    print(f'Dreamview running at http://{ctn.ip}:{ctn.port}')


runner = ChromosomeRunner(map, containers)
counter = 0
while True:
    print(counter)
    runner.set_chromosome(chromosome)
    runner.init_scenario()
    runner.run_scenario(generation_name='TestGeneration',
                        run_id='benchmark', upper_limit=90, save_record=False)
    counter += 1
    break
