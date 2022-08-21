"""
Random version of the framework, used to compare as base line.
"""

from main import eval_scenario
from config import APOLLO_ROOT, MAX_ADC_COUNT
from apollo.ApolloContainer import ApolloContainer
from framework.oracles.ViolationTracker import ViolationTracker
from framework.scenario import Scenario
from framework.scenario.ScenarioRunner import ScenarioRunner
from hdmap.MapParser import MapParser


def main():
    mp = MapParser('./data/maps/borregas_ave/base_map.bin')

    containers = [ApolloContainer(
        APOLLO_ROOT, f'ROUTE_{x}') for x in range(MAX_ADC_COUNT)]
    for ctn in containers:
        ctn.start_instance()
        ctn.start_dreamview()
        print(f'Dreamview at http://{ctn.ip}:{ctn.port}')

    srunner = ScenarioRunner(containers)
    vt = ViolationTracker()
    POP_SIZE = 25

    curr_gen = 0
    while True:
        print(f'===== Generation {curr_gen} =====')
        population = [Scenario.get_one() for _ in range(POP_SIZE)]
        for index, c in enumerate(population):
            c.gid = curr_gen
            c.cid = index

        for ind in population:
            print(f'Running scenario {ind.cid} - {ind.gid}')
            eval_scenario(ind)

        curr_gen += 1


if __name__ == '__main__':
    main()