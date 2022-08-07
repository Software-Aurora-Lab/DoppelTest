from itertools import combinations
from logging import Logger
from utils import get_logger
from typing import Dict, List
from modules.map.proto.map_lane_pb2 import Lane
from modules.map.proto.map_pb2 import Map
import networkx as nx
from modules.map.proto.map_signal_pb2 import Signal
from modules.map.proto.map_junction_pb2 import Junction
from modules.map.proto.map_crosswalk_pb2 import Crosswalk
from shapely.geometry import MultiLineString, LineString

from map.utils import get_distance, get_overlap_ids


class MapAnalyzer:
    logger: Logger
    map: Map
    lanes: Dict[str, Lane]
    junctions: Dict[str, Junction]
    signals: Dict[str, Signal]
    crosswalks: Dict[str, Crosswalk]
    _lanes: nx.DiGraph
    _signals: nx.DiGraph

    def __init__(self, map: Map) -> None:
        self.logger = get_logger('MapAnalyzer')
        self.logger.info('Loading map')
        self.map = map
        self.lanes = dict()
        self.junctions = dict()
        self.signals = dict()
        self.crosswalks = dict()
        self.load_lanes()
        self.load_junctions()
        self.load_signals()
        self.load_crosswalks()
        self.logger.info('Ready')

    def load_lanes(self):
        self.logger.debug('Loading lanes')
        for lane in self.map.lane:
            self.lanes[lane.id.id] = lane
        DG = nx.DiGraph()
        for lane in self.map.lane:
            line_segment = lane.central_curve.segment[0]
            lane_start = line_segment.start_position
            lane_end = line_segment.line_segment.point[-1]
            length = line_segment.length
            DG.add_node(lane.id.id, start=lane_start,
                        end=lane_end, length=length)
        for node1 in DG:
            for node2 in DG:
                if node1 == node2:
                    continue
                if DG.get_edge_data(node1, node2) or DG.get_edge_data(node2, node1):
                    continue
                s1, e1 = DG.nodes[node1]['start'], DG.nodes[node1]['end']
                s2, e2 = DG.nodes[node2]['start'], DG.nodes[node2]['end']
                if get_distance(e1, s2) < 0.001:
                    DG.add_edge(node1, node2)
                if get_distance(s1, e2) < 0.001:
                    DG.add_edge(node2, node1)
        self._lanes = DG

    def load_junctions(self):
        self.logger.debug('Loading junctions')
        for junction in self.map.junction:
            self.junctions[junction.id.id] = junction

    def load_signals(self):
        self.logger.debug('Loading signals')
        DG = nx.DiGraph()
        for signal in self.map.signal:
            DG.add_node(signal.id.id)
            self.signals[signal.id.id] = signal
        for j in self.junctions:
            junction_signals = self.get_signals_in_junction(self.junctions[j])
            for node1 in junction_signals:
                for node2 in junction_signals:
                    if node1 == node2:
                        continue
                    edge = DG.get_edge_data(node1, node2)
                    if not edge:
                        # no edge
                        signal1 = self.signals[node1]
                        signal2 = self.signals[node2]
                        if self.is_controlling_same_lanes(signal1, signal2):
                            DG.add_edge(node1, node2, value='EQ')
                            DG.add_edge(node2, node1, value='EQ')
                        elif self.is_conflict_signals(signal1, signal2):
                            DG.add_edge(node1, node2, value='NE')
                            DG.add_edge(node2, node1, value='NE')
        self._signals = DG

    def load_crosswalks(self):
        self.logger.debug('Loading crosswalks')
        for cw in self.map.crosswalk:
            self.crosswalks[cw.id.id] = cw

    def get_signals_wrt(self, signal_id: str) -> List[str]:
        assert signal_id in self.signals
        for u, v in self._signals.out_edges(signal_id):
            print(u, v, self._signals.edges[(u, v)]['value'])

    def get_lanes_controlled_by_signal(self, signal: Signal) -> List[Lane]:
        lanes = []
        signal_oids = get_overlap_ids(signal)
        for lane in self.map.lane:
            lane_oids = get_overlap_ids(lane)
            if signal_oids & lane_oids != set():
                lanes.append(lane)
        return lanes

    def get_signals_in_junction(self, junction: Junction) -> List[str]:
        result = list()
        j_oids = get_overlap_ids(junction)
        for signal in self.map.signal:
            s_oids = get_overlap_ids(signal)
            if j_oids & s_oids != set():
                result.append(signal.id.id)
        return result

    def get_crosswalk_in_junction(self, junction: Junction) -> List[str]:
        result = list()
        j_oids = get_overlap_ids(junction)
        for cw in self.map.crosswalk:
            c_oids = get_overlap_ids(cw)
            if j_oids & c_oids != set():
                result.append(cw.id.id)
        return result

    def get_cw_lanes_overlap(self, cw: Crosswalk) -> List[str]:
        pass

    def is_controlling_same_lanes(self, signal1: Signal, signal2: Signal) -> bool:
        lanes1 = self.get_lanes_controlled_by_signal(signal1)
        lanes2 = self.get_lanes_controlled_by_signal(signal2)
        if lanes1 == lanes2:
            return True
        return False

    def is_conflict_signals(self, signal1: Signal, signal2: Signal) -> bool:
        signal1_oids = get_overlap_ids(signal1)
        signal2_oids = get_overlap_ids(signal2)
        lane1_list = []
        lane2_list = []
        for lane in self.map.lane:
            if get_overlap_ids(lane) & signal1_oids != set():
                lane1_list.append(lane)
            if get_overlap_ids(lane) & signal2_oids != set():
                lane2_list.append(lane)
        if lane1_list == lane2_list:
            return False
        for lane1 in lane1_list:
            for lane2 in lane2_list:
                if lane1.id.id == lane2.id.id:
                    break
                if self.is_conflict_lanes(lane1, lane2):
                    return True
        return False

    def is_conflict_lanes(self, lane1: Lane, lane2: Lane) -> bool:
        lane1_points = []
        lane2_points = []
        for segment in lane1.central_curve.segment:
            for point in segment.line_segment.point:
                lane1_points.append((point.x, point.y))
        for segment in lane2.central_curve.segment:
            for point in segment.line_segment.point:
                lane2_points.append((point.x, point.y))
        multiline = MultiLineString([lane1_points, lane2_points])
        for line1, line2 in combinations([line for line in multiline.geoms], 2):
            if line1.intersects(line2):
                return True
        return False