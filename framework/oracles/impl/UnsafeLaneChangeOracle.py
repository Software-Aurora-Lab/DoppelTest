from datetime import datetime
from itertools import groupby
from typing import Dict, List, Optional, Set, Tuple

from shapely.geometry import Polygon

from apollo.utils import (construct_lane_boundary_linestring,
                          generate_adc_polygon)
from config import HD_MAP
from framework.oracles.OracleInterface import OracleInterface
from hdmap.MapParser import MapParser


class UnsafeLaneChangeOracle(OracleInterface):
    ADC_INTERSECTING_LANE_BOUNDARY_MAX_LOOK_BACK_FRAMES_IN_SECOND = 5.0
    PRUNE_DISTANCE = 150

    def __init__(self) -> None:
        self.mp = MapParser.get_instance(HD_MAP)
        self.boundaries = dict()
        self.get_boundaries()
        self.boundary_ids = sorted(self.boundaries.keys())
        self.__data = list() # [ (intersects?, timestamp, boundary_id) ]

        self.searchable_boundary_ids = set(self.boundary_ids)

    def get_boundaries(self):
        for lane_id in self.mp.get_lanes():
            lane = self.mp.get_lane_by_id(lane_id)
            lboundary, rboundary = construct_lane_boundary_linestring(lane)
            self.boundaries[f"{lane_id}_L"] = lboundary
            self.boundaries[f"{lane_id}_R"] = rboundary
    
    def on_new_message(self, topic: str, message, t):
        ego_pts = generate_adc_polygon(message.pose.position, message.pose.heading)
        ego_polygon = Polygon([[x.x, x.y] for x in ego_pts])
        pending_removal_boundary_ids = set()
        for bid in self.searchable_boundary_ids:
            distance = ego_polygon.distance(self.boundaries[bid])
            if distance == 0:
                # intersection found
                self.__data.append((True, t, bid))
                return
            if distance > UnsafeLaneChangeOracle.PRUNE_DISTANCE:
                pending_removal_boundary_ids.add(bid)
        
        self.searchable_boundary_ids = self.searchable_boundary_ids - pending_removal_boundary_ids

        # no intersection
        self.__data.append((False, t, ''))
        
    def get_interested_topics(self) -> List[str]:
        return ["/apollo/localization/pose"]
    
    def get_result(self):
        violations = list()
        for k, v in groupby(self.__data, key=lambda x: (x[0], x[2])):
            intersects, b_id = k
            traces = list(v)
            if intersects and len(traces) > 1:
                start_time = datetime.fromtimestamp(traces[0][1]/1000000000)
                end_time = datetime.fromtimestamp(traces[-1][1]/1000000000)
                deltaT = (end_time - start_time).total_seconds()

                if deltaT > self.ADC_INTERSECTING_LANE_BOUNDARY_MAX_LOOK_BACK_FRAMES_IN_SECOND:
                    violations.append(('unsafe_lane_change', b_id))
        return violations
