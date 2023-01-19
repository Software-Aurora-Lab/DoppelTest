import glob
import math
import os
import subprocess
import time
from modules.common.proto.geometry_pb2 import Point3D
from modules.localization.proto.localization_pb2 import LocalizationEstimate
from modules.perception.proto.perception_obstacle_pb2 import PerceptionObstacle
from config import APOLLO_ROOT, APOLLO_VEHICLE_HEIGHT, APOLLO_VEHICLE_LENGTH, APOLLO_VEHICLE_WIDTH, \
    APOLLO_VEHICLE_back_edge_to_center
from dataclasses import dataclass
from shapely.geometry import Polygon, LineString
from typing import List, Set, Tuple
from modules.planning.proto.planning_pb2 import ADCTrajectory
from modules.map.proto.map_lane_pb2 import Lane, LaneBoundary
from hdmap.MapParser import MapParser


@dataclass
class PositionEstimate:
    """
    Class representing a location on a HD Map

    :param str lane_id: id of the lane on a HD Map
    :param float s: distance from the start of the lane
    """
    lane_id: str
    s: float

    def is_too_close(self, rhs) -> bool:
        """
        Check if 2 PositionEstimate objects are too close to each other. 
        They are too close if their distance is less than 5 meters.
        
        :param self rhs: right hand side object for comparison
        :returns:
            True if too close, False otherwise
        :rtype: bool
        """
        # 2 vehicles are too close if their distance is less than 5 meters
        ma = MapParser.get_instance()
        adc1 = generate_adc_polygon(
            *ma.get_coordinate_and_heading(self.lane_id, self.s))
        adc2 = generate_adc_polygon(
            *ma.get_coordinate_and_heading(rhs.lane_id, rhs.s))

        adc1p = Polygon([[x.x, x.y] for x in adc1])
        adc2p = Polygon([[x.x, x.y] for x in adc2])

        return adc1p.distance(adc2p) < 5


def generate_polygon(position: Point3D, theta: float, length: float, width: float) -> List[Point3D]:
    """
    Generate polygon for a perception obstacle

    :param Point3D position: the position of the obstacle
    :param float theta: the heading of the obstacle
    :param float length: the length of the obstacle
    :param float width: the width of the obstacle

    :returns:
        List with 4 Point3D objects representing the polygon of the obstacle
    :rtype: List[Point3D]
    """
    points = []
    half_l = length / 2.0
    half_w = width / 2.0
    sin_h = math.sin(theta)
    cos_h = math.cos(theta)
    vectors = [(half_l * cos_h - half_w * sin_h,
                half_l * sin_h + half_w * cos_h),
               (-half_l * cos_h - half_w * sin_h,
                - half_l * sin_h + half_w * cos_h),
               (-half_l * cos_h + half_w * sin_h,
                - half_l * sin_h - half_w * cos_h),
               (half_l * cos_h + half_w * sin_h,
                half_l * sin_h - half_w * cos_h)]
    for x, y in vectors:
        p = Point3D()
        p.x = position.x + x
        p.y = position.y + y
        p.z = position.z
        points.append(p)
    return points


def generate_adc_polygon(position: Point3D, theta: float) -> List[Point3D]:
    """
    Generate a polygon for the ADC based on its current position

    :param Point3D position: position of the ADC
    :param float theta: the heading of the ADC (in radians)

    :returns: a list consisting 4 Point3D objects to 
        represent ADC polygon
    :rtype: List[Point3D]
    """

    points = []
    half_w = APOLLO_VEHICLE_WIDTH / 2.0
    front_l = APOLLO_VEHICLE_LENGTH - APOLLO_VEHICLE_back_edge_to_center
    back_l = -1 * APOLLO_VEHICLE_back_edge_to_center
    sin_h = math.sin(theta)
    cos_h = math.cos(theta)
    vectors = [(front_l * cos_h - half_w * sin_h,
                front_l * sin_h + half_w * cos_h),
               (back_l * cos_h - half_w * sin_h,
                back_l * sin_h + half_w * cos_h),
               (back_l * cos_h + half_w * sin_h,
                back_l * sin_h - half_w * cos_h),
               (front_l * cos_h + half_w * sin_h,
                front_l * sin_h - half_w * cos_h)]
    for x, y in vectors:
        p = Point3D()
        p.x = position.x + x
        p.y = position.y + y
        p.z = position.z
        points.append(p)
    return points


def generate_adc_rear_vertices(position: Point3D, theta: float):
    """
    Generate the rear edge for the ADC

    :param Point3D position: position of the ADC
    :param float theta: heading of the ADC

    :returns: a list consisting 2 Point3D objects to represent
        the rear edge of the ADC
    :rtype: List[Point3D]
    """
    points = []
    half_w = APOLLO_VEHICLE_WIDTH / 2.0
    back_l = -1 * APOLLO_VEHICLE_back_edge_to_center
    sin_h = math.sin(theta)
    cos_h = math.cos(theta)
    vectors = [(back_l * cos_h - half_w * sin_h,
                back_l * sin_h + half_w * cos_h),
               (back_l * cos_h + half_w * sin_h,
                back_l * sin_h - half_w * cos_h)]

    for x, y in vectors:
        p = Point3D()
        p.x = position.x + x
        p.y = position.y + y
        p.z = position.z
        points.append(p)
    return points


def obstacle_to_polygon(obs: PerceptionObstacle) -> Polygon:
    """
    Constructs a polygon for an obstacle

    :param PerceptionObstacle obs: the perception obstacle protobuf message

    :returns: a Polygon object representing the obstacle
    :rtype: Polygon
    """
    return Polygon([[p.x, p.y] for p in obs.polygon_point])


def pedestrian_location_to_obstacle(_id: int, speed: float, loc: Point3D, heading: float) -> PerceptionObstacle:
    """
    Constructs a perception obstacle message for a pedestrian

    :param int _id: ID of the obstacle
    :param float speed: speed of the obstacle
    :param Point3D loc: location of the obstacle
    :param float heading: heading of the obstacle

    :returns: a PerceptionObstacle protobuf message ready to be published to cyberRT
    :rtype: PerceptionObstacle
    """
    position = Point3D(x=loc.x,
                       y=loc.y, z=loc.z)
    velocity = Point3D(x=math.cos(heading) * speed,
                       y=math.sin(heading) * speed, z=0.0)
    obs = PerceptionObstacle(
        id=_id,
        position=position,
        theta=heading,
        velocity=velocity,
        acceleration=Point3D(x=0, y=0, z=0),
        length=0.3,
        width=0.5,
        height=1.75,
        type=PerceptionObstacle.PEDESTRIAN,
        timestamp=time.time(),
        tracking_time=1.0,
        polygon_point=generate_polygon(
            position, heading, 0.3, 0.5)
    )
    return obs


def dynamic_obstacle_location_to_obstacle(_id: int, speed: float, loc: Point3D, heading: float) -> PerceptionObstacle:
    """
    Constructs a perception obstacle message for a dynamic obstacle, used for generating a simulated Apollo instance only

    :param int _id: ID of the obstacle
    :param float speed: speed of the obstacle
    :param Point3D loc: location of the obstacle
    :param float heading: heading of the obstacle

    :returns: a PerceptionObstacle protobuf message ready to be published to cyberRT
    :rtype: PerceptionObstacle
    """
    position = Point3D(x=loc.x,
                       y=loc.y, z=loc.z)
    velocity = Point3D(x=math.cos(heading) * speed,
                       y=math.sin(heading) * speed, z=0.0)
    obs = PerceptionObstacle(
        id=_id,
        position=position,
        theta=heading,
        velocity=velocity,
        acceleration=Point3D(x=0, y=0, z=0),
        length=APOLLO_VEHICLE_LENGTH,
        width=APOLLO_VEHICLE_WIDTH,
        height=APOLLO_VEHICLE_HEIGHT,
        type=PerceptionObstacle.VEHICLE,
        timestamp=time.time(),
        tracking_time=1.0,
        polygon_point=generate_polygon(
            position, heading, APOLLO_VEHICLE_LENGTH, APOLLO_VEHICLE_WIDTH)
    )
    return obs


def to_Point3D(data: Point3D) -> Point3D:
    """
    Replaces NaN that may occur in Apollo to 0.0

    :param Point3D data: Point3D object to be cleaned

    :returns: cleaned up version of the original Point3D object
    :rtype: Point3D
    """
    return Point3D(
        x=0.0 if math.isnan(data.x) else data.x,
        y=0.0 if math.isnan(data.y) else data.y,
        z=0.0 if math.isnan(data.z) else data.z
    )


def localization_to_obstacle(_id: int, data: LocalizationEstimate) -> PerceptionObstacle:
    """
    Converts LocalizationEstimate to PerceptionObstacle. The localization message of an ADS
    instance is used as part of the perception message for other ADS instances.

    :param int _id: ID of the obstacle
    :param LocalizationEstimate data: localization message of the ADC

    :returns: PerceptionObstacle message converted from localization of an ADC
    :rtype: PerceptionObstacle
    """
    position = to_Point3D(data.pose.position)
    velocity = to_Point3D(data.pose.linear_velocity)
    acceleration = to_Point3D(data.pose.linear_acceleration)

    obs = PerceptionObstacle(
        id=_id,
        position=position,
        theta=data.pose.heading,
        velocity=velocity,
        acceleration=acceleration,
        length=APOLLO_VEHICLE_LENGTH,
        width=APOLLO_VEHICLE_WIDTH,
        height=APOLLO_VEHICLE_HEIGHT,
        type=PerceptionObstacle.VEHICLE,
        timestamp=data.header.timestamp_sec,
        tracking_time=1.0,
        polygon_point=generate_adc_polygon(
            position, data.pose.heading)
    )
    return obs


def extract_main_decision(data: ADCTrajectory) -> Set[Tuple]:
    """
    Extracts the main decision from a Planning message

    :param ADCTrajectory data: ADC's planning module output

    :returns: a set containing the overall decision and main decision
        for each obstacle
    :rtype: Set[Tuple]
    """
    main_decision = data.decision.main_decision
    object_decisions = data.decision.object_decision.decision

    decisions = set()

    # analyze main decision
    if main_decision.HasField('cruise'):
        # FORWARD = 0, LEFT = 1, RIGHT = 2
        md = ('main', 'cruise', main_decision.cruise.change_lane_type)
    elif main_decision.HasField('stop'):
        # modules/planning/proto/decision.proto:19
        md = ('main', 'stop', main_decision.stop.reason_code,
              main_decision.stop.reason)
    elif main_decision.HasField('estop'):
        # modules/planning/proto/decision.proto:150
        md = ('main', 'estop', main_decision.estop.reason_code)
    elif main_decision.HasField('mission_complete'):
        md = ('main', 'mission_complete',)
    else:
        md = ('main', 'not_ready',)

    decisions.add(md)

    # analyze object decision
    for obj_d in object_decisions:
        object_decision = obj_d.object_decision[0]
        if object_decision.HasField('stop'):
            od = ('obj', 'stop', object_decision.stop.reason_code)
        elif object_decision.HasField('follow'):
            od = ('obj', 'follow')
        elif object_decision.HasField('yield'):
            od = ('obj', 'yield')
        elif object_decision.HasField('overtake'):
            od = ('obj', 'overtake')
        elif object_decision.HasField('nudge'):
            od = ('obj', 'nudge', object_decision.nudge.type)
        elif object_decision.HasField('avoid'):
            od = ('obj', 'avoid')
        elif object_decision.HasField('side_pass'):
            od = ('obj', 'side_pass', object_decision.side_pass.type)
        else:  # object_decision.HasField('ignore')
            od = ('obj', 'ignore')
        decisions.add(od)

    return decisions


def clean_appolo_dir():
    """
    Removes Apollo's log files to save disk space
    """
    # remove data dir
    subprocess.run(f"rm -rf {APOLLO_ROOT}/data".split())

    # remove records dir
    subprocess.run(f"rm -rf {APOLLO_ROOT}/records".split())

    # remove logs
    fileList = glob.glob(f'{APOLLO_ROOT}/*.log.*')
    for filePath in fileList:
        os.remove(filePath)

    # create data dir
    subprocess.run(f"mkdir {APOLLO_ROOT}/data".split())
    subprocess.run(f"mkdir {APOLLO_ROOT}/data/bag".split())
    subprocess.run(f"mkdir {APOLLO_ROOT}/data/log".split())
    subprocess.run(f"mkdir {APOLLO_ROOT}/data/core".split())
    subprocess.run(f"mkdir {APOLLO_ROOT}/records".split())


def calculate_velocity(linear_velocity: Point3D) -> float:
    """
    Calculate velocity based on a given vector

    :param Point3D linear_velocity: velocity in vector form

    :returns: speed calculated from the velocity
    :rtype: float
    """
    x, y, z = linear_velocity.x, linear_velocity.y, linear_velocity.z
    return round(math.sqrt(x ** 2 + y ** 2), 2)


def construct_lane_polygon(lane_msg: Lane) -> Polygon:
    '''
    Construct the lane polygon based on their boundaries

    :param Lane lane_msg: Lane protobuf message extracted from HD Map

    :returns: Polygon representing the lane
    :rtype: Polygon
    '''
    left_points = get_lane_boundary_points(lane_msg.left_boundary)
    right_points = get_lane_boundary_points(lane_msg.right_boundary)
    right_points.reverse()
    all_points = left_points + right_points
    return Polygon(all_points)


def get_lane_boundary_points(boundary: LaneBoundary) -> List[Tuple[float, float]]:
    '''
    Given a lane boundary (left/right), return a list of x, y
    coordinates of all points in the boundary

    :param LaneBoundary boundary: LaneBoundary protobuf message

    :returns: list of boundary points
    :rtype: List[Tuple[float, float]]
    '''
    boundary_points = []
    for segment in boundary.curve.segment:
        for segment_point in segment.line_segment.point:
            boundary_points.append((segment_point.x, segment_point.y))
    return boundary_points


def construct_lane_boundary_linestring(lane_msg: Lane) -> List[Tuple[LineString, LineString]]:
    """
    Construct two linestrings for the lane's left and right boundary

    :param Lane lane_msg: Lane protobuf message extracted from HD Map
    
    :returns: 2 LineString objects representing left and right boundary of the lane
    :rtype: Tuple[LaneString, LaneString]
    """
    left_boundary_points = get_lane_boundary_points(lane_msg.left_boundary)
    right_boundary_points = get_lane_boundary_points(lane_msg.right_boundary)
    return LineString(left_boundary_points), LineString(right_boundary_points)
