from dataclasses import dataclass
import dataclasses
from random import random
from deap import base
from automation.section_ad import ADSection
from automation.section_pd import PDSection
from automation.section_tc import TCSection
from modules.map.proto.map_pb2 import Map
from map.MapAnalyzer import MapAnalyzer

# Problem Encoding
# ================================================================================


class ChromosomeFitness(base.Fitness):
    # ! closest distance between ADC and pedestrian
    # closest distance between pair of ADC
    # # of unique decisions triggered during simulation
    # ! # of agents not completing mission
    # ! # of module failure
    weights = (1.0, -1.0)


@dataclass
class Chromosome:
    AD: ADSection
    PD: PDSection
    TC: TCSection

    gid: str = ''  # generation id
    cid: str = ''  # chromosome id
    fitness: base.Fitness = ChromosomeFitness()

    @staticmethod
    def get_one(ma: MapAnalyzer):
        return Chromosome(
            AD=ADSection.get_one(ma),
            PD=PDSection.get_one(ma),
            TC=TCSection.get_one(ma),
        )

    def to_dict(self):
        return {
            "AD": dataclasses.asdict(self.AD),
            "PD": dataclasses.asdict(self.PD),
            "TC": dataclasses.asdict(self.TC),
        }