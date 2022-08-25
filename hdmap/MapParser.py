from collections import defaultdict
from typing import List, Set, Tuple
from hdmap import load_hd_map
from modules.map.proto.map_pb2 import Map
import networkx as nx
from shapely.geometry import LineString, Point
from modules.common.proto.geometry_pb2 import PointENU
import math


class MapParser:
    __map: Map
    __junctions: dict
    __signals: dict
    __stop_signs: dict
    __lanes: dict
    __crosswalk: dict

    __signals_at_junction: dict
    __lanes_at_junction: dict
    __lanes_controlled_by_signal: dict

    __signal_relations: nx.Graph
    __lane_nx: nx.DiGraph

    __instance = None

    def __init__(self, filename: str) -> None:
        self.__map = load_hd_map(filename)
        self.load_junctions()
        self.load_signals()
        self.load_stop_signs()
        self.load_lanes()
        self.load_crosswalks()
        self.parse_relations()
        self.parse_signal_relations()
        self.parse_lane_relations()
        MapParser.__instance = self

    @staticmethod
    def get_instance():
        assert not MapParser.__instance is None
        return MapParser.__instance

    def load_junctions(self):
        self.__junctions = dict()
        for junc in self.__map.junction:
            self.__junctions[junc.id.id] = junc

    def load_signals(self):
        self.__signals = dict()
        for sig in self.__map.signal:
            self.__signals[sig.id.id] = sig

    def load_stop_signs(self):
        self.__stop_signs = dict()
        for ss in self.__map.stop_sign:
            self.__stop_signs[ss.id.id] = ss

    def load_lanes(self):
        self.__lanes = dict()
        for l in self.__map.lane:
            self.__lanes[l.id.id] = l

    def load_crosswalks(self):
        self.__crosswalk = dict()
        for cw in self.__map.crosswalk:
            self.__crosswalk[cw.id.id] = cw

    def parse_relations(self):
        # load signals at junction
        self.__signals_at_junction = defaultdict(lambda: list())
        for sigk, sigv in self.__signals.items():
            for junk, junv in self.__junctions.items():
                if self.__is_overlap(sigv, junv):
                    self.__signals_at_junction[junk].append(sigk)

        # load lanes at junction
        self.__lanes_at_junction = defaultdict(lambda: list())
        for lank, lanv in self.__lanes.items():
            for junk, junv in self.__junctions.items():
                if self.__is_overlap(lanv, junv):
                    self.__lanes_at_junction[junk].append(lank)

        # load lanes controlled by signal
        self.__lanes_controlled_by_signal = defaultdict(lambda: list())
        for junk, junv in self.__junctions.items():
            signal_ids = self.__signals_at_junction[junk]
            lane_ids = self.__lanes_at_junction[junk]
            for sid in signal_ids:
                for lid in lane_ids:
                    if self.__is_overlap(self.__signals[sid], self.__lanes[lid]):
                        self.__lanes_controlled_by_signal[sid].append(lid)

    def parse_signal_relations(self):
        g = nx.Graph()
        for junk, junv in self.__junctions.items():
            signal_ids = self.__signals_at_junction[junk]
            for sid1 in signal_ids:
                g.add_node(sid1)
                for sid2 in signal_ids:
                    if sid1 == sid2:
                        continue
                    lg1 = self.__lanes_controlled_by_signal[sid1]
                    lg2 = self.__lanes_controlled_by_signal[sid2]
                    if lg1 == lg2:
                        g.add_edge(sid1, sid2, v='EQ')
                    elif self.is_conflict_lanes(lg1, lg2):
                        g.add_edge(sid1, sid2, v='NE')
        self.__signal_relations = g

    def parse_lane_relations(self):
        dg = nx.DiGraph()
        for lane1 in self.__lanes:
            dg.add_node(lane1)
            for lane2 in self.__lanes:
                if lane1 == lane2:
                    continue
                line1 = self.get_lane_central_curve(lane1)
                line2 = self.get_lane_central_curve(lane2)
                s1, e1 = Point(line1.coords[0]), Point(line1.coords[-1])
                s2, e2 = Point(line2.coords[0]), Point(line2.coords[-1])

                if s1.distance(e2) < 0.001:
                    dg.add_edge(lane2, lane1)
                elif e1.distance(s2) < 0.001:
                    dg.add_edge(lane1, lane2)
        self.__lane_nx = dg

    def __is_overlap(self, obj1, obj2):
        oid1 = set([x.id for x in obj1.overlap_id])
        oid2 = set([x.id for x in obj2.overlap_id])
        return oid1 & oid2 != set()

    def get_signals_wrt(self, signal_id: str) -> Tuple[str, str]:
        result = list()
        for u, v, data in self.__signal_relations.edges(signal_id, data=True):
            result.append((v, data['v']))
        return result

    def is_conflict_lanes(self, lane_id1: List[str], lane_id2: List[str]) -> bool:
        for lid1 in lane_id1:
            for lid2 in lane_id2:
                if lid1 == lid2:
                    continue
                lane1 = self.get_lane_central_curve(lid1)
                lane2 = self.get_lane_central_curve(lid2)
                if lane1.intersects(lane2):
                    return True
        return False

    def get_lane_central_curve(self, lane_id: str) -> LineString:
        lane = self.__lanes[lane_id]
        points = lane.central_curve.segment[0].line_segment
        line = LineString([[x.x, x.y] for x in points.point])
        return line

    def get_lane_length(self, lane_id: str):
        return self.get_lane_central_curve(lane_id).length

    def get_coordinate_and_heading(self, lane_id: str, s: float):
        lst = self.get_lane_central_curve(lane_id)
        ip = lst.interpolate(s)

        segments = list(map(LineString, zip(lst.coords[:-1], lst.coords[1:])))
        segments.sort(key=lambda x: ip.distance(x))
        line = segments[0]
        x1, x2 = line.xy[0]
        y1, y2 = line.xy[1]

        return (PointENU(x=ip.x, y=ip.y), math.atan2(y2-y1, x2-x1))

    def get_junctions(self) -> List[str]:
        return list(self.__junctions.keys())

    def get_lanes(self) -> List[str]:
        return list(self.__lanes.keys())

    def get_lane_by_id(self, l_id: str):
        return self.__lanes[l_id]

    def get_crosswalks(self) -> List[str]:
        return list(self.__crosswalk.keys())

    def get_crosswalk_by_id(self, cw_id: str):
        return self.__crosswalk[cw_id]

    def get_signals(self) -> List[str]:
        return list(self.__signals.keys())

    def get_signal_by_id(self, s_id: str):
        return self.__signals[s_id]

    def get_stop_signs(self) -> List[str]:
        return list(self.__stop_signs.keys())

    def get_stop_sign_by_id(self, ss_id: str):
        return self.__stop_signs[ss_id]

    def get_lanes_not_in_junction(self) -> Set[str]:
        lanes = set(self.get_lanes())
        for junc in self.__lanes_at_junction:
            jlanes = set(self.__lanes_at_junction[junc])
            lanes = lanes - jlanes
        return lanes

    def get_path_from(self, lane_id: str) -> List[List[str]]:
        target_lanes = self.get_lanes_not_in_junction()
        reachable = self.__get_reachable_from(lane_id)
        return [p for p in reachable if p[-1] in target_lanes]

    def __get_reachable_from(self, lane_id: str, depth=5):
        if depth == 1:
            return [[lane_id]]
        result = list()
        for u, v in self.__lane_nx.edges(lane_id):
            result.append([u, v])
            for rp in self.__get_reachable_from(v, depth-1):
                result.append([u] + rp)
        return result
