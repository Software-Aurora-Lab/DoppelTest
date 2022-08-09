import math
from modules.common.proto.geometry_pb2 import Point3D
from modules.localization.proto.localization_pb2 import LocalizationEstimate
from modules.perception.proto.perception_obstacle_pb2 import PerceptionObstacle
from utils.config import APOLLO_VEHICLE_HEIGHT, APOLLO_VEHICLE_LENGTH, APOLLO_VEHICLE_WIDTH


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


def generate_adc_polygon(position: Point3D, theta: float, length: float, width: float):
    """
    Generate polygon for the ADC

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
    vectors = [(length * cos_h - half_w * sin_h,
                length * sin_h + half_w * cos_h),
               (0 * cos_h - half_w * sin_h,
                0 * sin_h + half_w * cos_h),
               (0 * cos_h + half_w * sin_h,
                0 * sin_h - half_w * cos_h),
               (length * cos_h + half_w * sin_h,
                length * sin_h - half_w * cos_h)]
    for x, y in vectors:
        p = Point3D()
        p.x = position.x + x
        p.y = position.y + y
        p.z = position.z
        points.append(p)
    return points


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
        # sub_type=PerceptionObstacle.ST_CAR,
        timestamp=data.header.timestamp_sec,
        tracking_time=1.0,
        polygon_point=generate_adc_polygon(
            position, data.pose.heading, APOLLO_VEHICLE_LENGTH, APOLLO_VEHICLE_WIDTH)
    )
    return obs
