from dataclasses import asdict, dataclass
from framework.scenario.ad_agents import ADSection
from framework.scenario.pd_agents import PDSection
from framework.scenario.tc_config import TCSection
from deap import base

from hdmap.MapParser import MapParser


class ScenarioFitness(base.Fitness):
    # minimize closest distance between pair of ADC
    # maximize number of unique decisions being made
    # maximize pairs of conflict trajectory
    # maximize unique violation
    weights = (-1.0, 1.0, 1.0, 1.0)


@dataclass
class Scenario:
    ad_section: ADSection
    pd_section: PDSection
    tc_section: TCSection

    gid: int = -1  # generation id
    cid: int = -1  # scenario id
    fitness: base.Fitness = ScenarioFitness()

    def to_dict(self):
        return {
            'ad_section': asdict(self.ad_section),
            'pd_section': asdict(self.pd_section),
            'tc_section': asdict(self.tc_section)
        }

    @staticmethod
    def get_one():
        result = Scenario(
            ad_section=ADSection.get_one(),
            pd_section=PDSection.get_one(),
            tc_section=TCSection.get_one()
        )
        return result

    @staticmethod
    def get_conflict_one():
        while True:
            result = Scenario(
                ad_section=ADSection.get_one(),
                pd_section=PDSection.get_one(),
                tc_section=TCSection.get_one()
            )
            if result.has_ad_conflict() > 0:
                return result

    def has_ad_conflict(self) -> int:
        ma = MapParser.get_instance()
        conflict = set()
        for ad in self.ad_section.adcs:
            for bd in self.ad_section.adcs:
                if ad.routing == bd.routing:
                    continue
                if ma.is_conflict_lanes(ad.routing, bd.routing):
                    conflict.add(frozenset([ad.routing_str, bd.routing_str]))
        return len(conflict)
