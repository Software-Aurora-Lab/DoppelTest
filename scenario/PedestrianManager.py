from dataclasses import dataclass
import math
from typing import List, Tuple

from shapely.geometry import MultiLineString, LineString


@dataclass
class Point3D:
    x: int = 0
    y: int = 0
    z: int = 0


@dataclass
class Pedestrian:
    boundary: List[Point3D]
    speed: float
    start_time: float


class PedestrianManager:
    pedestrians: List[Pedestrian]

    def __init__(self, pedestrians: List[Pedestrian]) -> None:
        self.pedestrians = pedestrians

    def calculate_position(self, pd: Pedestrian, time_spent_walking: float) -> Tuple[Point3D, float]:
        '''
        Return the pedestrians location and heading
        '''
        # heading is calculated by which segment the pedestrian is on (from the polygon) and then using atan2
        distance = pd.speed * time_spent_walking
        line_list = []
        for i in range(len(pd.boundary) - 1):
            line_list.append(
                ((pd.boundary[i].x, pd.boundary[i].y), (pd.boundary[i + 1].x, pd.boundary[i + 1].y)))
        line_list.append(
            ((pd.boundary[-1].x, pd.boundary[-1].y), (pd.boundary[0].x, pd.boundary[0].y)))
        heading_list = []
        for line in line_list:
            heading_list.append(math.atan2(
                line[1][1]-line[0][1], line[1][0]-line[0][0]))
        lines = MultiLineString(line_list)
        boundary_length = lines.length
        curr_point = lines.interpolate(distance % boundary_length)
        for i in range(len(line_list)):
            line = LineString(line_list[i])
            if line.contains(curr_point):
                return Point3D(x=curr_point.x, y=curr_point.y), heading_list[i]
        '''
        process the boundary point
        '''
        for i in range(len(pd.boundary)):
            x = pd.boundary[i].x
            y = pd.boundary[i].y
            if x == curr_point.x and y == curr_point.y:
                return Point3D(x=curr_point.x, y=curr_point.y), heading_list[i]

    def get_pedestrians(self, curr_time: float) -> List[Tuple[Point3D, float]]:
        result = list()
        for pd in self.pedestrians:
            time_spent_walking = curr_time - pd.start_time
            if time_spent_walking > 0:
                pd_position = self.calculate_position(pd, time_spent_walking)
            else:
                pd_position = pd.boundary[0], math.atan2(
                    pd.boundary[1].y-pd.boundary[0].y, pd.boundary[1].x-pd.boundary[0].x)
            result.append(pd_position)
        return result


pd = Pedestrian(
    boundary=[Point3D(0, 0),
              Point3D(10, 0),
              Point3D(10, 10),
              Point3D(0, 10)],
    speed=1,
    start_time=5
)

pm = PedestrianManager([pd])

print(pm.get_pedestrians(0))
# [(Point3D(x=0, y=0, z=0), 0.0)] Pedestrian hasn't moved
print(pm.get_pedestrians(4))
# [(Point3D(x=0, y=0, z=0), 0.0)] again
print(pm.get_pedestrians(6))
# [(Point3D(x=1, y=0, z=0), 0.0)] # expected output, pedestrian is given 1 second to travel 1 meter around the boundary
