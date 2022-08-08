
import random
from modules.map.proto.map_pb2 import Map
from map.MapAnalyzer import MapAnalyzer
from automation.Chromosome import Chromosome
from automation.section_ad import ADSection
from automation.section_pd import PDSection
from automation.section_tc import TCSection
from apollo.ApolloContainer import ApolloContainer
from utils.config import APOLLO_ROOT

# Evaluation
# ================================================================================


def eval(ind: Chromosome):
    # closest distance between pair of ADC
    # # of unique decisions triggered during simulation
    return 0, 0

# Mutation
# ================================================================================


def mut_ad(ad: ADSection):
    return ad


def mut_pd(pd: PDSection):
    return pd


def mut_tc(tc: TCSection):
    return tc


def mut(ind: Chromosome):
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

# Crossover
# ================================================================================


def cx_ad(ad1: ADSection, ad2: ADSection):
    return ad1, ad2


def cx_pd(pd1: PDSection, pd2: PDSection):
    return pd1, pd2


def cx_tc(tc1: TCSection, tc2: TCSection):
    return tc1, tc2


def cx(ind1: Chromosome, ind2: Chromosome):
    return ind1, ind2


# Main
# ================================================================================
map = Map()
f = open('./data/maps/borregas_ave_fix/base_map.bin', 'rb')
map.ParseFromString(f.read())

ma = MapAnalyzer(map)


containers = [ApolloContainer(APOLLO_ROOT, f'ROUTE_{x}') for x in range(5)]
for ctn in containers:
    ctn.start_instance()
    ctn.start_dreamview()
    print(f'Dreamview running at http://{ctn.ip}:{ctn.port}')
