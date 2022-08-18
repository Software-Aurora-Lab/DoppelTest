from dataclasses import dataclass
from random import randint, uniform
from secrets import choice
from typing import List

from config import MAX_PD_COUNT, SCENARIO_UPPER_LIMIT
from hdmap.MapParser import MapParser


@dataclass
class PDAgent:
    cw_id: str
    speed: float
    start_t: float

    @staticmethod
    def get_one():
        ma = MapParser.get_instance()
        cws = list(ma.get_crosswalks())
        cw = choice(cws)
        return PDAgent(
            cw_id=cw,
            speed=round(uniform(1.25, 3), 1),
            start_t=randint(0, SCENARIO_UPPER_LIMIT)
        )

    @staticmethod
    def get_one_for_cw(cw_id: str):
        ma = MapParser.get_instance()
        return PDAgent(
            cw_id=cw_id,
            speed=round(uniform(1.25, 3), 1),
            start_t=randint(0, SCENARIO_UPPER_LIMIT)
        )


@dataclass
class PDSection:
    pds: List[PDAgent]

    def add_agent(self, pd: PDAgent) -> bool:
        for p in self.pds:
            if p.cw_id == pd.cw_id:
                return False
        self.pds.append(pd)
        return True

    @staticmethod
    def get_one():
        ma = MapParser.get_instance()

        num = randint(0, MAX_PD_COUNT)
        num = min(len(ma.get_crosswalks()), num)
        result = PDSection([])
        while len(result.pds) < num:
            result.add_agent(PDAgent.get_one())
        return result
