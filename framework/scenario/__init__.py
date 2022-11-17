from dataclasses import asdict, dataclass
from framework.scenario.ad_agents import ADAgent, ADSection
from framework.scenario.pd_agents import PDAgent, PDSection
from framework.scenario.tc_config import TCSection
from deap import base

from hdmap.MapParser import MapParser
import json

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
    def from_json(json_file_path):
        with open(json_file_path, 'r') as fp:
            data = json.loads(fp.read())
            ad_section = data['ad_section']
            r_ad = ADSection([])
            for adc in ad_section['adcs']:
                r_ad.add_agent(
                    ADAgent(adc['routing'], adc['start_s'], adc['dest_s'], adc['start_t'])
                )
            pd_section = data['pd_section']
            r_pd = PDSection([])
            for pd in pd_section['pds']:
                r_pd.add_agent(
                    PDAgent(pd['cw_id'], pd['speed'], pd['start_t'])
                )
            tc_section = data['tc_section']
            r_tc = TCSection(tc_section['initial'], tc_section['final'], 
                tc_section['duration_g'], tc_section['duration_y'], tc_section['duration_b'])

            return Scenario(r_ad, r_pd, r_tc)

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
