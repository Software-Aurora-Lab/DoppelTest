"""
Random version of the framework, used to compare as base line.
"""

from main_ga import eval_scenario
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

    # randomly generate a chromosome
    # chromosome = Scenario.get_one()

    # parse an existing chromosome (c.json)
    chromosome = Scenario.from_json('/home/sora/Desktop/yhuai/DoppelTest/data/c.json')

    # Run scenario 5 times and check printed violation.
    chromosome.gid = 0
    for i in range(5):
        chromosome.cid = i
        eval_scenario(chromosome)
        vt.print()
        vt.clear()


if __name__ == '__main__':
    main()
