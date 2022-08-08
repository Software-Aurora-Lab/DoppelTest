
from random import choices, random, choice, randint
from unittest import runner
from modules.map.proto.map_pb2 import Map
from map.MapAnalyzer import MapAnalyzer
from automation.Chromosome import Chromosome
from automation.section_ad import AD, ADSection
from automation.section_pd import PDSection
from automation.section_tc import TCSection
from apollo.ApolloContainer import ApolloContainer
from scenario.ChromosomeRunner import ChromosomeRunner
from utils import get_logger
from utils.config import APOLLO_ROOT
from deap import tools, creator, base, algorithms


# Mutation
# ================================================================================


def mut_ad(ad: ADSection):
    mut_pb = random()
    operation = ''
    if mut_pb < 1/3:
        # attempt to remove 1
        if len(ad.adcs) == 2:
            # cannot remove, add 1
            operation = 'ADD'
        else:
            operation = 'REMOVE'
    elif mut_pb < 2/3:
        # add 1
        if len(ad.adcs) == 5:
            operation = 'REMOVE'
        else:
            operation = 'ADD'
    else:
        # replace 1
        operation = 'REPLACE'

    if operation == 'REMOVE' or operation == 'REPLACE':
        ad.adcs.remove(choice(ad.adcs))

    if operation == 'ADD' or operation == 'REPLACE':
        added = False
        while not added:
            new_ad = AD.get_one(MapAnalyzer.get_instance())
            should_add = True
            for ex in ad.adcs:
                if ex.initial_position.is_too_close(new_ad.initial_position):
                    should_add = False
            if should_add:
                ad.adcs.append(new_ad)
                added = True

    ad.adjust_time()
    return ad


def mut_pd(pd: PDSection):
    mut_pb = random()
    operation = ''
    if mut_pb < 1/3:
        # attempt to remove 1
        if len(pd.pds) == 0:
            # cannot remove, add 1
            operation = 'ADD'
        else:
            operation = 'REMOVE'
    elif mut_pb < 2/3:
        # add 1
        if len(pd.pds) == 5:
            operation = 'REMOVE'
        else:
            operation = 'ADD'
    else:
        # replace 1
        operation = 'REPLACE'
    return pd


def mut_tc(tc: TCSection):
    mut_pb = random()
    if mut_pb < 1/3:
        tc.initial = TCSection.generate_config(MapAnalyzer.get_instance())
    elif mut_pb < 2/3:
        tc.final = TCSection.generate_config(MapAnalyzer.get_instance())
    else:
        tc.duration_g = randint(10, 30)
    return tc


def mut(ind: Chromosome):
    # mutate 1 of the 3 sections
    mut_pb = random()
    if mut_pb < 1/3:
        # mute AD section
        ind.AD = mut_ad(ad=ind.AD)
    elif mut_pb < 2/3:
        # mutate PD section
        ind.PD = mut_pd(pd=ind.PD)
    else:
        # mutate TC section
        ind.TC = mut_tc(tc=ind.TC)
    return ind,


# Crossover
# ================================================================================


def cx_ad(ad1: ADSection, ad2: ADSection):
    adcs = list()
    for a in ad1.adcs:
        adcs.append(a)

    for b in ad2.adcs:
        can_add = True
        for x in adcs:
            if x.initial_position.is_too_close(b.initial_position):
                can_add = False
        if can_add:
            adcs.append(b)

    new_ad1_length = randint(2, 5)
    new_ad2_length = randint(2, 5)

    return ADSection(choices(adcs, k=new_ad1_length)), ADSection(
        choices(adcs, k=new_ad2_length))


def cx_pd(pd1: PDSection, pd2: PDSection):
    return pd1, pd2


def cx_tc(tc1: TCSection, tc2: TCSection):
    return tc1, tc2


def cx(ind1: Chromosome, ind2: Chromosome):
    cx_pb = random()
    if cx_pb < 1/2:
        ind1.AD, ind2.AD = ind2.AD, ind1.AD
    else:
        ind1.AD, ind2.AD = cx_ad(ind1.AD, ind2.AD)
    # if cx_pb < 1/3:
    #     ind1.AD, ind2.AD = ind2.AD, ind1.AD
    # elif cx_pb < 2/3:
    #     ind1.PD, ind2.PD = ind2.PD, ind1.PD
    # else:
    #     ind1.TC, ind2.TC = ind2.TC, ind1.TC
    return ind1, ind2


# Evaluation
# ================================================================================


def eval(ind: Chromosome):
    # closest distance between pair of ADC
    # # of unique decisions triggered during simulation
    runner = ChromosomeRunner.get_instance()
    runner.set_chromosome(ind)
    runner.init_scenario()
    g_name = f'Generation_{ind.gid:05}'
    s_name = f'Scenario_{ind.cid:05}'
    runner.run_scenario(
        generation_name=g_name,
        run_id=s_name,
        upper_limit=55, save_record=True
    )
    return random(), random()


# Main
# ================================================================================


def main():
    logger = get_logger("MAIN")
    # load map
    map = Map()
    f = open('./data/maps/borregas_ave_fix/base_map.bin', 'rb')
    map.ParseFromString(f.read())

    # analyze map
    ma = MapAnalyzer(map)

    # start Apollo containers
    containers = [ApolloContainer(APOLLO_ROOT, f'ROUTE_{x}') for x in range(5)]
    for ctn in containers:
        ctn.start_instance()
        ctn.start_dreamview()
        print(f'Dreamview running at http://{ctn.ip}:{ctn.port}')

    runner = ChromosomeRunner(map, containers)

    # GA Hyperparameters
    POP_SIZE = 50
    OFF_SIZE = 50  # number of offspring to produce
    CXPB = 0.5  # crossover probablitiy
    MUTPB = 0.2  # mutation probability

    toolbox = base.Toolbox()
    toolbox.register("evaluate", eval)
    toolbox.register("mate", cx)
    toolbox.register("mutate", mut)
    toolbox.register("select", tools.selNSGA2)

    # start GA
    population = [Chromosome.get_one(ma) for _ in range(POP_SIZE)]
    for index, c in enumerate(population):
        c.gid = 0
        c.cid = index
    hof = tools.ParetoFront()

    # Evaluate Initial Population
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
