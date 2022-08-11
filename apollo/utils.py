import math
from modules.common.proto.geometry_pb2 import Point3D
from modules.localization.proto.localization_pb2 import LocalizationEstimate
from modules.perception.proto.perception_obstacle_pb2 import PerceptionObstacle
from config import APOLLO_VEHICLE_HEIGHT, APOLLO_VEHICLE_LENGTH, APOLLO_VEHICLE_WIDTH, APOLLO_VEHICLE_back_edge_to_center
from dataclasses import dataclass
from shapely.geometry import Polygon
from typing import Set, Tuple
from modules.planning.proto.planning_pb2 import ADCTrajectory


@dataclass
class PositionEstimate:
    lane_id: str
    s: float

    def is_too_close(self, rhs):
        return self.lane_id == rhs.lane_id and abs(self.s-rhs.s) < 10


def generate_polygon(position: Point3D, theta: float, length: float, width: float):
    """
    Generate polygon for an perception obstacle

    Parameters:
        position: Point3D
            position vector of the obstacle
        theta: float
            heading of the obstacle
        length: float
            length of the obstacle
        width: float
            width of the obstacle

    Returns:
        points: List[Point3D]
            polygon points of the obstacle
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


def generate_adc_polygon(position: Point3D, theta: float):
    """
    Generate polygon for the ADC

    Parameters:
        position: Point3D
            localization pose of ADC
        theta: float
            heading of ADC

    Returns:
        points: List[Point3D]
            polygon points of the ADC
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


def obstacle_to_polygon(obs: PerceptionObstacle) -> Polygon:
    return Polygon([[p.x, p.y] for p in obs.polygon_point])


def localization_to_obstacle(_id: int, data: LocalizationEstimate) -> PerceptionObstacle:
    """
    Converts LocalizationEstimate to PerceptionObstacle

    Parameters:
        _id: int
            id used to construct obstacle
        data: LocalizationEstimate
            localization result for an Apollo instance

    Returns:
        obs: PerceptionObstacle
            prepared data which is ready to be sent as PerceptionObstacle
    """
    position = Point3D(x=data.pose.position.x,
                       y=data.pose.position.y, z=data.pose.position.z)
    velocity = Point3D(x=data.pose.linear_velocity.x,
                       y=data.pose.linear_velocity.y, z=data.pose.linear_velocity.z)
    obs = PerceptionObstacle(
        id=_id,
        position=position,
        theta=data.pose.heading,
        velocity=velocity,
        acceleration=data.pose.linear_acceleration,
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
