from time import sleep
from config import APOLLO_ROOT, MAX_ADC_COUNT, RECORDS_DIR
from apollo.ApolloContainer import ApolloContainer
from framework.oracles import RecordAnalyzer
from framework.scenario import Scenario
from framework.scenario.ScenarioRunner import ScenarioRunner
from framework.scenario.tc_config import TCSection
from framework.scenario.pd_agents import PDSection
from framework.scenario.ad_agents import ADSection
from hdmap.MapParser import MapParser
from deap import base, tools, algorithms
from utils import get_logger
import os

# EVALUATION (FITNESS)


def eval_scenario(ind: Scenario):
    g_name = f'Generation_{ind.gid:05}'
    s_name = f'Scenario_{ind.cid:05}'
    srunner = ScenarioRunner.get_instance()
    srunner.set_scenario(ind)
    srunner.init_scenario()
    for a, r in srunner.run_scenario(g_name, s_name, True):
        print(a.container.container_name, r.routing_str)
        c_name = a.container.container_name
        r_name = f"{c_name}.{s_name}.00000"
        record_path = os.path.join(RECORDS_DIR, g_name, s_name, r_name)
        ra = RecordAnalyzer(record_path)
        print(record_path)
        ra.analyze()
        print(ra.get_results())
    # analyze violations
    # analyze scenario fitness
    return 0, 0, 0, 0

# MUTATION OPERATOR


def mut_ad_section(ind: ADSection):
    return ind


def mut_pd_section(ind: PDSection):
    return ind


def mut_tc_section(ind: TCSection):
    return ind


def mut_scenario(ind: Scenario):
    ind.ad_section = mut_ad_section(ind.ad_section)
    ind.pd_section = mut_pd_section(ind.pd_section)
    ind.tc_section = mut_tc_section(ind.tc_section)
    return ind,


# CROSSOVER OPERATOR

def cx_ad_section(ind1: ADSection, ind2: ADSection):
    return ind1, ind2


def cx_pd_section(ind1: PDSection, ind2: PDSection):
    return ind1, ind2


def cx_tc_section(ind1: TCSection, ind2: TCSection):
    return ind1, ind2


def cx_scenario(ind1: Scenario, ind2: Scenario):
    ind1.ad_section, ind2.ad_section = cx_ad_section(
        ind1.ad_section, ind2.ad_section
    )
    ind1.pd_section, ind2.pd_section = cx_pd_section(
        ind1.pd_section, ind2.pd_section
    )
    ind1.tc_section, ind2.tc_section = cx_tc_section(
        ind1.tc_section, ind2.tc_section
    )
    return ind1, ind2


# MAIN

def main():
    logger = get_logger('MAIN')
    mp = MapParser('./data/maps/borregas_ave/base_map.bin')

    containers = [ApolloContainer(
        APOLLO_ROOT, f'ROUTE_{x}') for x in range(MAX_ADC_COUNT)]
    for ctn in containers:
        ctn.start_instance()
        ctn.start_dreamview()
        print(f'Dreamview at http://{ctn.ip}:{ctn.port}')

    srunner = ScenarioRunner(containers)

    # GA Hyperparameters
    POP_SIZE = 5
    OFF_SIZE = 5  # number of offspring to produce
    CXPB = 0.8  # crossover probablitiy
    MUTPB = 0.2  # mutation probability

    toolbox = base.Toolbox()
    toolbox.register("evaluate", eval_scenario)
    toolbox.register("mate", cx_scenario)
    toolbox.register("mutate", mut_scenario)
    toolbox.register("select", tools.selNSGA2)

    # start GA
    population = [Scenario.get_one() for _ in range(POP_SIZE)]
    for index, c in enumerate(population):
        c.gid = 0
        c.cid = index
    hof = tools.ParetoFront()

    # Evaluate Initial Population
    logger.info(f' ====== Analyzing Initial Population ====== ')
    invalid_ind = [ind for ind in population if not ind.fitness.valid]
    fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
    for ind, fit in zip(invalid_ind, fitnesses):
        ind.fitness.values = fit
    hof.update(population)

    # begin generational process
    curr_gen = 0
    while True:
        curr_gen += 1
        logger.info(f' ====== Generation {curr_gen} ====== ')
        # Vary the population
        offspring = algorithms.varOr(
            population, toolbox, OFF_SIZE, CXPB, MUTPB)

        # update chromosome gid and cid
        for index, c in enumerate(offspring):
            c.gid = curr_gen
            c.cid = index

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        hof.update(offspring)

        # Select the next generation population
        population[:] = toolbox.select(population + offspring, POP_SIZE)

        print(f"{hof[-1].gid} - {hof[-1].cid}: {hof[-1].fitness}")

        if curr_gen - hof[-1].gid > 500:
            break


if __name__ == '__main__':
    main()
