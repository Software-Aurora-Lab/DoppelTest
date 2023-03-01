import json
from dataclasses import asdict, dataclass, field

from deap import base

from config import HD_MAP
from framework.scenario.ad_agents import ADAgent, ADSection
from framework.scenario.pd_agents import PDAgent, PDSection
from framework.scenario.tc_config import TCSection
from hdmap.MapParser import MapParser


class ScenarioFitness(base.Fitness):
    """
    Class to represent weight of each fitness function
    """
    # minimize closest distance between pair of ADC
    # maximize number of unique decisions being made
    # maximize pairs of conflict trajectory
    # maximize unique violation
    weights = (-1.0, 1.0, 1.0, 1.0)
    """
    :note: minimize closest distance, maximize number of decisions,
      maximize pairs having conflicting trajectory,
      maximize unique violation. Refer to our paper for more
      detailed explanation.
    """


@dataclass
class Scenario:
    """
    Genetic representation of a scenario (individual)

    :param ADSection ad_section: section of chromosome
      describing ADS instances
    :param PDSection pd_section: section of chromosome
      describing pedestrians
    :param TCSection tc_section: section of chromosome
      describing traffic control configuration
    """
    ad_section: ADSection
    pd_section: PDSection
    tc_section: TCSection

    gid: int = -1  # generation id
    cid: int = -1  # scenario id
    fitness: base.Fitness = field(default_factory=ScenarioFitness)

    def to_dict(self) -> dict:
        """
        Converts the chromosome to dict

        :returns: scenario in JSON format
        :rtype: dict
        """
        return {
            'ad_section': asdict(self.ad_section),
            'pd_section': asdict(self.pd_section),
            'tc_section': asdict(self.tc_section)
        }

    @staticmethod
    def from_json(json_file_path: str) -> 'Scenario':
        """
        Converts a JSON file into Scenario object

        :param str json_file_path: name of the JSON file

        :returns: Scenario object
        :rtype: Scenario
        """
        with open(json_file_path, 'r') as fp:
            data = json.loads(fp.read())
            ad_section = data['ad_section']
            r_ad = ADSection([])
            for adc in ad_section['adcs']:
                r_ad.add_agent(
                    ADAgent(adc['routing'], adc['start_s'],
                            adc['dest_s'], adc['start_t'])
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
    def get_one() -> 'Scenario':
        """
        Randomly generates a scenario using the representation

        :returns: randomlly generated scenario
        :rtype: Scenario
        """
        result = Scenario(
            ad_section=ADSection.get_one(),
            pd_section=PDSection.get_one(),
            tc_section=TCSection.get_one()
        )
        return result

    @staticmethod
    def get_conflict_one() -> 'Scenario':
        """
        Randomly generates a scenario that gurantees at least
        2 ADS instances have conflicting trajectory

        :returns: randomly generated scenario with conflict
        :rtype: Scenario
        """
        while True:
            result = Scenario(
                ad_section=ADSection.get_one(),
                pd_section=PDSection.get_one(),
                tc_section=TCSection.get_one()
            )
            if result.has_ad_conflict() > 0:
                return result

    def has_ad_conflict(self) -> int:
        """
        Check number of ADS instance pairs with conflict

        :returns: number of conflicts
        :rtype: int
        """
        ma = MapParser.get_instance(HD_MAP)
        conflict = set()
        for ad in self.ad_section.adcs:
            for bd in self.ad_section.adcs:
                if ad.routing == bd.routing:
                    continue
                if ma.is_conflict_lanes(ad.routing, bd.routing):
                    conflict.add(frozenset([ad.routing_str, bd.routing_str]))
        return len(conflict)
