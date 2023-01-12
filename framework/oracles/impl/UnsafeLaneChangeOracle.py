from itertools import groupby
from typing import List, Dict, Set, Tuple, Optional
from shapely.geometry import Polygon
from apollo.utils import generate_adc_polygon, \
    construct_lane_boundary_linestring, generate_adc_polygon
from framework.oracles.OracleInterface import OracleInterface
from hdmap.MapParser import MapParser
from datetime import datetime

class UnsafeLaneChangeOracle(OracleInterface):
    ADC_INTERSECTING_LANE_BOUNDARY_MAX_LOOK_BACK_FRAMES_IN_SECOND = 5.0

    def __init__(self) -> None:
        self.mp = MapParser.get_instance()
        self.boundaries = dict()
        self.get_boundaries()
        self.boundary_ids = sorted(self.boundaries.keys())
        self.__data = list() # [ (intersects?, timestamp, boundary_id) ]

    def get_boundaries(self):
        for lane_id in self.mp.get_lanes():
            lane = self.mp.get_lane_by_id(lane_id)
            lboundary, rboundary = construct_lane_boundary_linestring(lane)
            self.boundaries[f"{lane_id}_L"] = lboundary
            self.boundaries[f"{lane_id}_R"] = rboundary
    
    def on_new_message(self, topic: str, message, t):
        ego_pts = generate_adc_polygon(message.pose.position, message.pose.heading)
        ego_polygon = Polygon([[x.x, x.y] for x in ego_pts])
        for bid in self.boundary_ids:
            if ego_polygon.intersects(self.boundaries[bid]):
                self.__data.append((
                    True, t, bid
                ))
                break
            else:
                self.__data.append((
                    False, t, ''
                ))
        
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
