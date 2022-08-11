
from dataclasses import dataclass
from random import choice, randint, random, uniform
from typing import List
from config import INSTANCE_MAX_WAIT_TIME
from map.MapAnalyzer import MapAnalyzer
from apollo.utils import PositionEstimate
from map.utils import get_length_of_lane


@dataclass
class AD:
    routing: List[str]
    start_s: float
    end_s: float
    start_time: float
    apollo_container: str = ''

    @property
    def initial_position(self):
        return PositionEstimate(self.routing[0], self.start_s)

    def get_waypoints(self):
        result = list()
        for i, r in enumerate(self.routing):
            if i == 0:
                continue
            elif i == len(self.routing) - 1:
                # destination
                result.append(PositionEstimate(r, self.end_s))
            else:
                result.append(PositionEstimate(r, 0))
        return result

    @staticmethod
    def get_one(ma: MapAnalyzer):
        allowed_start = list(ma.get_lanes_not_in_junction())
        start = None
        routing = None
        while True:
            start = choice(allowed_start)
            allowed_routing = ma.get_allowed_routing(start)
            if len(allowed_routing) > 0:
                routing = choice(allowed_routing)
                break

        print(start, routing)
        start_length = get_length_of_lane(ma.lanes[start])
        end_length = get_length_of_lane(ma.lanes[routing[-1]])

        print()

        return AD(
            routing,
            random() * (start_length - 5),
            random() * end_length,
            randint(0, INSTANCE_MAX_WAIT_TIME),
        )


@dataclass
class ADSection:
    adcs: List[AD]

    def adjust_time(self):
        self.adcs.sort(key=lambda x: x.start_time)
        start_times = [x.start_time for x in self.adcs]
        delta = round(start_times[0] - 2.0, 1)
        for i in range(len(start_times)):
            start_times[i] = round(start_times[i] - delta, 1)
            self.adcs[i].start_time = start_times[i]

    @staticmethod
    def get_one(ma: MapAnalyzer):
        num = randint(2, 5)
        result = list()
        should_add = True
        while len(result) < num:
            new_ad = AD.get_one(ma)
            # check if it overlap with any existing one
            should_add = True
            for ad in result:
                if new_ad.initial_position.is_too_close(ad.initial_position):
                    should_add = False
            if should_add:
                result.append(new_ad)
        result = ADSection(result)
        result.adjust_time()
        return result
