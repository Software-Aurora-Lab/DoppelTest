from itertools import combinations
from typing import List, Optional, Set, Tuple
from modules.common.proto.geometry_pb2 import PointENU, Polygon
from modules.map.proto.map_pb2 import Map
from modules.map.proto.map_lane_pb2 import Lane
from modules.map.proto.map_signal_pb2 import Signal
from modules.map.proto.map_crosswalk_pb2 import Crosswalk
from shapely.geometry import MultiLineString
import math
import networkx as nx


def get_distance(p1: PointENU, p2: PointENU):
    return abs(math.sqrt((p1.x-p2.x)**2 + (p1.y-p2.y)**2))


def points_to_segments(points: List[PointENU]):
    result = []
    for i in range(1, len(points)):
        p1 = points[i-1]
        p2 = points[i]
        result.append(((p1.x, p1.y), (p2.x, p2.y)))
    return result


def get_lane_by_id(map: Map, id: str) -> Optional[Lane]:
    for l in map.lane:
        if l.id.id == id:
            return l
    return None


def get_signal_by_id(map: Map, id: str) -> Optional[Signal]:
    for signal in map.signal:
        if signal.id.id == id:
            return signal
    return None


def get_length_of_lane(lane: Lane):
    return lane.central_curve.segment[0].length


def get_coordinate_for(lane: Lane, s: float) -> Tuple[PointENU, float]:
    central_curve = lane.central_curve

    points = central_curve.segment[0].line_segment.point
    lines = points_to_segments(points)

    mtl = MultiLineString(lines)
    ip = mtl.interpolate(s)

    indexes = list(range(len(mtl.geoms)))
    indexes.sort(key=lambda x: mtl.geoms[x].distance(ip))
    line = mtl.geoms[indexes[0]]

    x1, y1 = line.coords[0]
    x2, y2 = line.coords[1]

    return (PointENU(x=ip.x, y=ip.y), math.atan2(y2-y1, x2-x1))


def get_overlap_ids(obj: object) -> Set[str]:
    return set([x.id for x in obj.overlap_id])


def cw_to_graph(cw: Crosswalk) -> nx.Graph:
    g = nx.Graph()
    precision = 2
    for index, point in enumerate(cw.polygon.point):
        fx, fy = round(point.x, precision), round(point.y, precision)
        if index == len(cw.polygon.point)-1:
            tp = cw.polygon.point[0]
        else:
            tp = cw.polygon.point[index+1]
        tx, ty = round(tp.x, precision), round(tp.y, precision)

        g.add_edge((fx, fy), (tx, ty))
    return g


def merge_cw(cw1: Crosswalk, cw2: Crosswalk) -> Crosswalk:
    g1 = cw_to_graph(cw1)
    g2 = cw_to_graph(cw2)

    for edge in g1.edges:
        ((fx, fy), (tx, ty)) = edge
        if ((fx, fy), (tx, ty)) in g2.edges:
            g1.remove_edge((fx, fy), (tx, ty))
            g2.remove_edge((fx, fy), (tx, ty))

    F = nx.compose(g1, g2)

    coords = list(F.nodes)
    points = list()
    while len(coords) > 0:
        if len(points) == 0:
            curr = coords.pop(0)
            points.append(curr)
        for c in coords:
            if not F.get_edge_data(curr, c) is None:
                points.append(c)
                coords.remove(c)
                curr = c
                break

    result = Crosswalk()
    result.id.id = f'{cw1.id.id}+{cw2.id.id}'
    for p in points:
        a = result.polygon.point.add()
        a.x = p[0]
        a.y = p[1]
    for oid in cw1.overlap_id:
        a = result.overlap_id.add()
        a.id = oid.id
    for oid in cw2.overlap_id:
        a = result.overlap_id.add()
        a.id = oid.id

    return result


def share_edge(cw1: Crosswalk, cw2: Crosswalk) -> bool:
    g1 = cw_to_graph(cw1)
    g2 = cw_to_graph(cw2)

    for edge in g1.edges:
        ((fx, fy), (tx, ty)) = edge
        if ((fx, fy), (tx, ty)) in g2.edges:
            return True
    return False
