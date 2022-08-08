from dataclasses import dataclass
import dataclasses
from random import random
from deap import base
from automation.section_ad import ADSection
from automation.section_pd import PDSection
from automation.section_tc import TCSection
from modules.map.proto.map_pb2 import Map

# Problem Encoding
# ================================================================================


class ChromosomeFitness(base.Fitness):
    # closest distance between ADC and pedestrian
    # closest distance between pair of ADC
    # # of unique decisions triggered during simulation
    # # of agents not completing mission
    # # of module failure
    weights = (1.0, 1.0, -1.0, -1.0, -1.0)


@dataclass
class Chromosome:
    AD: ADSection
    PD: PDSection
    TC: TCSection
    fitness: base.Fitness = ChromosomeFitness()

    @staticmethod
    def get_one(map: Map):
        return Chromosome(
            AD=ADSection.get_one(map),
            PD=PDSection.get_one(map),
            TC=TCSection.get_one(map),
        )

    def to_dict(self):
        return {
            "AD": dataclasses.asdict(self.AD),
            "PD": dataclasses.asdict(self.PD),
            "TC": dataclasses.asdict(self.TC),
        }

# Evaluation
# ================================================================================


def eval(ind: Chromosome):
    return 0, 0, 0, 0, 0

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
