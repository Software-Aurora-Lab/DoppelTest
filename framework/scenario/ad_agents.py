from dataclasses import dataclass
from random import randint, random
from secrets import choice
from typing import List
from apollo.utils import PositionEstimate
from config import MAX_ADC_COUNT, INSTANCE_MAX_WAIT_TIME
from hdmap.MapParser import MapParser


@dataclass
class ADAgent:
    routing: List[str]
    start_s: float
    dest_s: float
    start_t: float

    @property
    def initial_position(self):
        return PositionEstimate(self.routing[0], self.start_s)

    @property
    def waypoints(self):
        result = list()
        for i, r in enumerate(self.routing):
            if i == 0:
                continue
            elif i == len(self.routing) - 1:
                # destination
                result.append(PositionEstimate(r, self.dest_s))
            else:
                result.append(PositionEstimate(r, 0))
        return result

    @property
    def routing_str(self):
        return '->'.join(self.routing)

    @staticmethod
    def get_one():
        ma = MapParser.get_instance()
        allowed_start = list(ma.get_lanes_not_in_junction())
        start_r = ''
        routing = None
        while True:
            start_r = choice(allowed_start)
            allowed_routing = ma.get_path_from(start_r)
            if len(allowed_routing) > 0:
                routing = choice(allowed_routing)
                break

        start_length = ma.get_lane_length(start_r)
        dest_length = ma.get_lane_length(routing[-1])

        if start_length > 5:
            start_s = round(random() * (start_length - 5), 1)
        else:
            start_s = 0.0

        return ADAgent(
            routing=routing,
            start_s=start_s,
            dest_s=round(dest_length / 2, 1),
            start_t=randint(0, INSTANCE_MAX_WAIT_TIME)
        )

    @staticmethod
    def get_one_for_routing(routing: List[str]):
        start_r = routing[0]
        ma = MapParser.get_instance()
        start_length = ma.get_lane_length(start_r)
        dest_length = ma.get_lane_length(routing[-1])

        if start_length > 5:
            start_s = round(random() * (start_length - 5), 1)
        else:
            start_s = 0.0

        return ADAgent(
            routing=routing,
            start_s=start_s,
            dest_s=round(dest_length / 2, 1),
            start_t=randint(0, INSTANCE_MAX_WAIT_TIME)
        )


@dataclass
class ADSection:
    adcs: List[ADAgent]

    def adjust_time(self):
        self.adcs.sort(key=lambda x: x.start_t)
        start_times = [x.start_t for x in self.adcs]
        delta = round(start_times[0] - 2.0, 1)
        for i in range(len(start_times)):
            start_times[i] = round(start_times[i] - delta, 1)
            self.adcs[i].start_t = start_times[i]

    def add_agent(self, adc: ADAgent) -> bool:
        adc_start = PositionEstimate(adc.routing[0], adc.start_s)
        for ad in self.adcs:
            ad_start = PositionEstimate(ad.routing[0], ad.start_s)
            if ad_start.is_too_close(adc_start):
                return False
        self.adcs.append(adc)
        return True

    def has_conflict(self, adc: ADAgent) -> bool:
        ma = MapParser.get_instance()
        for ad in self.adcs:
            if ma.is_conflict_lanes(adc.routing, ad.routing):
                return True
        return False

    @staticmethod
    def get_one():
        num = randint(2, MAX_ADC_COUNT)
        result = ADSection([])

        while len(result.adcs) < num:
            result.add_agent(ADAgent.get_one())
        result.adjust_time()
        return result
