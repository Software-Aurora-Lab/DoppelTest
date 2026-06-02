"""
Random version of the framework, used to compare as base line.
"""

import pickle
from datetime import datetime

import numpy as np
from absl import app
from deap import tools

from apollo.ApolloContainer import ApolloContainer
import config
from framework.oracles.ViolationTracker import ViolationTracker
from framework.scenario import Scenario
from framework.scenario.ScenarioRunner import ScenarioRunner
from hdmap.MapParser import MapParser
from main_ga import eval_scenario


def main(_: list) -> None:
    mp = MapParser.get_instance(config.HD_MAP)

    containers = [ApolloContainer(
        config.APOLLO_ROOT, f'ROUTE_{x}') for x in range(config.MAX_ADC_COUNT)]
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
        if tdelta / 3600 > config.RUN_FOR_HOUR:
            break


if __name__ == '__main__':
    app.run(main)
