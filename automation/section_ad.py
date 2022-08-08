
from collections import defaultdict
from dataclasses import dataclass
from random import choice, randint, uniform
from typing import List
from map.MapAnalyzer import MapAnalyzer

from scenario.ApolloRunner import PositionEstimate
from modules.map.proto.map_pb2 import Map


@dataclass
class AD:
    initial_position: PositionEstimate
    final_position: PositionEstimate
    start_time: float
    apollo_container: str = ''

    @staticmethod
    def get_one(ma: MapAnalyzer):
        junction_lanes = list()
        for junction in ma.junctions:
            junction_lanes += ma.get_lanes_in_junction(ma.junctions[junction])

        chooseable = set(ma.lanes.keys()).difference(
            set(junction_lanes))

        reachable = dict()
        for k in chooseable:
            reachable[k] = [
                x for x in ma.get_reachable_lanes(k) if x in chooseable]

        for k in reachable:
            if len(reachable[k]) == 0:
                chooseable.remove(k)

        init_lane = choice(list(chooseable))

        initial = PositionEstimate(
            init_lane, uniform(5.0, ma.get_lane_data(init_lane)['length']-5)
        )

        final_lane = choice(reachable[init_lane])
        final = PositionEstimate(
            final_lane, uniform(
                ma.get_lane_data(final_lane)['length']*0.5, ma.get_lane_data(final_lane)['length'])
        )
        return AD(
            initial_position=initial,
            final_position=final,
            start_time=round(uniform(0, 15), 1)
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
                result.append(AD.get_one(ma))
        result = ADSection(result)
        result.adjust_time()
        return result
