from typing import List, Optional, Tuple
from modules.common.proto.geometry_pb2 import PointENU
from modules.map.proto.map_pb2 import Map
from modules.map.proto.map_lane_pb2 import Lane
from shapely.geometry import MultiLineString, LineString
import math


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
