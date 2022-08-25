"""
Random version of the framework, used to compare as base line.
"""

from datetime import datetime
from main_ga import eval_scenario
from config import APOLLO_ROOT, MAX_ADC_COUNT, RUN_FOR_HOUR
from apollo.ApolloContainer import ApolloContainer
from framework.oracles.ViolationTracker import ViolationTracker
from framework.scenario import Scenario
from framework.scenario.ScenarioRunner import ScenarioRunner
from hdmap.MapParser import MapParser
from deap import tools
import numpy as np
import pickle


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
    POP_SIZE = 10

    hof = tools.ParetoFront()
    stats = tools.Statistics(key=lambda ind: ind.fitness.values)
    stats.register("avg", np.mean, axis=0)
    stats.register("max", np.max, axis=0)
    stats.register("min", np.min, axis=0)
    logbook = tools.Logbook()
    logbook.header = 'gen', 'avg', 'max', 'min'

    start_time = datetime.now()

    curr_gen = 0
    while True:
        print(f'===== RAND Generation {curr_gen} =====')
        population = [Scenario.get_one() for _ in range(POP_SIZE)]
        for index, c in enumerate(population):
            c.gid = curr_gen
            c.cid = index

        for ind in population:
            print(f'Running scenario {ind.cid} - {ind.gid}')
            fit = eval_scenario(ind)
            ind.fitness.values = fit
            print('Fitness', fit)

        hof.update(population)
        record = stats.compile(population)
        logbook.record(gen=curr_gen, **record)
        print(logbook.stream)

        curr_gen += 1

        vt.save_to_file()
        curr_time = datetime.now()
        tdelta = (curr_time - start_time).total_seconds()
        if tdelta / 3600 > RUN_FOR_HOUR:
            break


if __name__ == '__main__':
    main()
