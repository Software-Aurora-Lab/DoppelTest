from copy import deepcopy
from datetime import datetime
import pickle
from random import random, sample, shuffle, randint
import shutil
from config import APOLLO_ROOT, HD_MAP_PATH, MAX_ADC_COUNT, MAX_PD_COUNT, RECORDS_DIR, RUN_FOR_HOUR
from apollo.ApolloContainer import ApolloContainer
from framework.oracles import RecordAnalyzer
from framework.oracles.ViolationTracker import ViolationTracker
from framework.scenario import Scenario
from framework.scenario.ScenarioRunner import ScenarioRunner
from framework.scenario.tc_config import TCSection
from framework.scenario.pd_agents import PDAgent, PDSection
from framework.scenario.ad_agents import ADAgent, ADSection
from hdmap.MapParser import MapParser
from deap import base, tools, algorithms
from utils import get_logger, remove_record_files
import os
import numpy as np

# EVALUATION (FITNESS)


def eval_scenario(ind: Scenario):
    g_name = f'Generation_{ind.gid:05}'
    s_name = f'Scenario_{ind.cid:05}'
    srunner = ScenarioRunner.get_instance()
    srunner.set_scenario(ind)
    srunner.init_scenario()
    runners = srunner.run_scenario(g_name, s_name, True)

    obs_routing_map = dict()
    for a, r in runners:
        obs_routing_map[a.nid] = r.routing_str

    unique_violation = 0
    duplicate_violation = 0
    min_distance = list()
    decisions = set()
    for a, r in runners:
        min_distance.append(a.get_min_distance())
        decisions.update(a.get_decisions())
        c_name = a.container.container_name
        r_name = f"{c_name}.{s_name}.00000"
        record_path = os.path.join(RECORDS_DIR, g_name, s_name, r_name)
        ra = RecordAnalyzer(record_path)
        ra.analyze()
        for v in ra.get_results():
            main_type = v[0]
            sub_type = v[1]
            if main_type == 'collision':
                if sub_type < 100:
                    # pedestrian collisoin
                    related_data = frozenset(
                        [r.routing_str, ind.pd_section.pds[sub_type].cw_id])
                    sub_type = 'A&P'
                else:
                    # adc to adc collision
                    related_data = frozenset(
                        [r.routing_str, obs_routing_map[sub_type]]
                    )
                    sub_type = 'A&A'
            else:
                related_data = r.routing_str
            if ViolationTracker.get_instance().add_violation(
                gname=g_name,
                sname=s_name,
                record_file=record_path,
                mt=main_type,
                st=sub_type,
                data=related_data
            ):
                unique_violation += 1

    ma = MapParser.get_instance()
    conflict = ind.has_ad_conflict()

    if unique_violation == 0:
        # no unique violation, remove records
        remove_record_files(g_name, s_name)
        pass

    return min(min_distance), len(decisions), conflict, unique_violation

# MUTATION OPERATOR


def mut_ad_section(ind: ADSection):
    mut_pb = random()

    # remove a random 1
    if mut_pb < 0.1 and len(ind.adcs) > 2:
        shuffle(ind.adcs)
        ind.adcs.pop()
        ind.adjust_time()
        return ind

    # add a random 1
    if mut_pb < 0.4 and len(ind.adcs) < MAX_ADC_COUNT:
        while True:
            new_ad = ADAgent.get_one()
            if ind.has_conflict(new_ad) and ind.add_agent(new_ad):
                break
        ind.adjust_time()
        return ind

    # mutate a random agent
    index = randint(0, len(ind.adcs) - 1)
    routing = ind.adcs[index].routing
    original_adc = ind.adcs.pop(index)
    mut_counter = 0
    while True:
        if ind.add_agent(ADAgent.get_one_for_routing(routing)):
            break
        mut_counter += 1
        if mut_counter == 5:
            # mutation kept failing, dont mutate
            ind.add_agent(original_adc)
            pass
    ind.adjust_time()
    return ind


def mut_pd_section(ind: PDSection):

    if len(ind.pds) == 0:
        ind.add_agent(PDAgent.get_one())
        return ind

    mut_pb = random()
    # remove a random
    if mut_pb < 0.2 and len(ind.pds) > 0:
        shuffle(ind.pds)
        ind.pds.pop()
        return ind

    # add a random
    if mut_pb < 0.4 and len(ind.pds) <= MAX_PD_COUNT:
        ind.pds.append(PDAgent.get_one())
        return ind

    # mutate a random
    index = randint(0, len(ind.pds) - 1)
    ind.pds[index] = PDAgent.get_one_for_cw(ind.pds[index].cw_id)
    return ind


def mut_tc_section(ind: TCSection):
    mut_pb = random()

    if mut_pb < 0.3:
        ind.initial = TCSection.generate_config()
        return ind
    elif mut_pb < 0.6:
        ind.final = TCSection.generate_config()
    elif mut_pb < 0.9:
        ind.duration_g = TCSection.get_random_duration_g()

    return TCSection.get_one()


def mut_scenario(ind: Scenario):
    mut_pb = random()
    if mut_pb < 1/3:
        ind.ad_section = mut_ad_section(ind.ad_section)
    elif mut_pb < 2/3:
        ind.pd_section = mut_pd_section(ind.pd_section)
    else:
        ind.tc_section = mut_tc_section(ind.tc_section)
    return ind,


# CROSSOVER OPERATOR

def cx_ad_section(ind1: ADSection, ind2: ADSection):
    # swap entire ad section
    cx_pb = random()
    if cx_pb < 0.05:
        return ind2, ind1

    cxed = False

    for adc1 in ind1.adcs:
        for adc2 in ind2.adcs:
            if adc1.routing_str == adc2.routing_str:
                # same routing in both parents
                # swap start_s and start_t
                if random() < 0.5:
                    adc1.start_s = adc2.start_s
                else:
                    adc1.start_t = adc2.start_t
                mutated = True
    if cxed:
        ind1.adjust_time()
        return ind1, ind2

    if len(ind1.adcs) < MAX_ADC_COUNT:
        for adc in ind2.adcs:
            if ind1.has_conflict(adc) and ind1.add_agent(deepcopy(adc)):
                # add an agent from parent 2 to parent 1 if there exists a conflict
                ind1.adjust_time()
                return ind1, ind2

    # if none of the above happened, no common adc, no conflict in either
    # combine to make a new populations
    available_adcs = ind1.adcs + ind2.adcs
    shuffle(available_adcs)
    split_index = randint(2, min(len(available_adcs), MAX_ADC_COUNT))

    result1 = ADSection([])
    for x in available_adcs[:split_index]:
        result1.add_agent(deepcopy(x))

    # make sure offspring adc count is valid

    while len(result1.adcs) > MAX_ADC_COUNT:
        result1.adcs.pop()

    while len(result1.adcs) < 2:
        new_ad = ADAgent.get_one()
        if result1.has_conflict(new_ad) and result1.add_agent(new_ad):
            break
    result1.adjust_time()
    return result1, ind2


def cx_pd_section(ind1: PDSection, ind2: PDSection):
    cx_pb = random()
    if cx_pb < 0.1:
        return ind2, ind1

    available_pds = ind1.pds + ind2.pds

    result1 = PDSection(
        sample(available_pds, k=randint(0, min(MAX_PD_COUNT, len(available_pds)))))
    result2 = PDSection(
        sample(available_pds, k=randint(0, min(MAX_PD_COUNT, len(available_pds)))))
    return result1, result2


def cx_tc_section(ind1: TCSection, ind2: TCSection):
    cx_pb = random()
    if cx_pb < 0.1:
        return ind2, ind1
    elif cx_pb < 0.4:
        ind1.initial, ind2.initial = ind2.initial, ind1.initial
    elif cx_pb < 0.7:
        ind1.final, ind2.final = ind2.final, ind1.final
    else:
        ind1.duration_g, ind2.duration_g = ind2.duration_g, ind1.duration_g
    return ind1, ind2


def cx_scenario(ind1: Scenario, ind2: Scenario):
    cx_pb = random()
    if cx_pb < 0.6:
        ind1.ad_section, ind2.ad_section = cx_ad_section(
            ind1.ad_section, ind2.ad_section
        )
    elif cx_pb < 0.6 + 0.2:
        ind1.pd_section, ind2.pd_section = cx_pd_section(
            ind1.pd_section, ind2.pd_section
        )
    else:
        ind1.tc_section, ind2.tc_section = cx_tc_section(
            ind1.tc_section, ind2.tc_section
        )
    return ind1, ind2


# MAIN

def main():
    logger = get_logger('MAIN')
    mp = MapParser(HD_MAP_PATH)

    containers = [ApolloContainer(
        APOLLO_ROOT, f'ROUTE_{x}') for x in range(MAX_ADC_COUNT)]
    for ctn in containers:
        ctn.start_instance()
        ctn.start_dreamview()
        print(f'Dreamview at http://{ctn.ip}:{ctn.port}')

    srunner = ScenarioRunner(containers)
    vt = ViolationTracker()

    # GA Hyperparameters
    POP_SIZE = 10  # number of population
    OFF_SIZE = 10  # number of offspring to produce
    CXPB = 0.8  # crossover probablitiy
    MUTPB = 0.2  # mutation probability

    toolbox = base.Toolbox()
    toolbox.register("evaluate", eval_scenario)
    toolbox.register("mate", cx_scenario)
    toolbox.register("mutate", mut_scenario)
    toolbox.register("select", tools.selNSGA2)

    # start GA
    start_time = datetime.now()
    population = [Scenario.get_conflict_one() for _ in range(POP_SIZE)]
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

    stats = tools.Statistics(key=lambda ind: ind.fitness.values)
    stats.register("avg", np.mean, axis=0)
    stats.register("max", np.max, axis=0)
    stats.register("min", np.min, axis=0)
    logbook = tools.Logbook()
    logbook.header = 'gen', 'avg', 'max', 'min'

    # begin generational process
    curr_gen = 0
    while True:
        curr_gen += 1
        logger.info(f' ====== GA Generation {curr_gen} ====== ')
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

        record = stats.compile(population)
        logbook.record(gen=curr_gen, **record)
        print(logbook.stream)

        vt.save_to_file()
        with open('./data/log.bin', 'wb') as fp:
            pickle.dump(logbook, fp)
        with open('./data/hof.bin', 'wb') as fp:
            pickle.dump(hof, fp)

        curr_time = datetime.now()
        tdelta = (curr_time - start_time).total_seconds()
        if tdelta / 3600 > RUN_FOR_HOUR:
            break


if __name__ == '__main__':
    main()
