from enum import Enum
from typing import Optional, Tuple, Set, Dict

from cyber_record.record import Record
from shapely.geometry import LineString, Polygon

from apollo.utils import calculate_velocity, generate_adc_rear_vertices, generate_adc_polygon
from modules.localization.proto.localization_pb2 import LocalizationEstimate
from modules.perception.proto.perception_obstacle_pb2 import PerceptionObstacles


class CollisionType(Enum):
    DEFAULT = 0
    REAR_END = 1


class CollisionLiabilityChecker:
    record_obj: Record

    interesting_topics = {
        '/apollo/localization/pose',
        '/apollo/perception/obstacles'
    }

    last_localization: Optional[LocalizationEstimate]
    last_perception: Optional[PerceptionObstacles]

    collision_type_checking_result_dict = Dict[str, str]

    def __init__(self, record_path: str) -> None:
        self.record_obj = Record(record_path)

        self.last_localization = None
        self.last_perception = None

        self.collision_type_checking_result_dict = dict()

    def start(self):
        for topic, message, t in self.record_obj.read_messages():
            if topic not in self.interesting_topics:
                continue
            self.on_new_message_callback(topic, message, t)
        return self.get_results()

    def on_new_message_callback(self, topic: str, message, t):
        if topic == '/apollo/localization/pose':
            self.last_localization = message
        else:
            self.last_perception = message

        if self.last_localization is None or self.last_perception is None:
            return

        adc_pose = self.last_localization.pose

        if self.is_adc_completely_stopped():
            return

        adc_polygon_pts = generate_adc_polygon(adc_pose.position, adc_pose.heading)
        adc_polygon = Polygon([[x.x, x.y] for x in adc_polygon_pts])

        adc_rear_line_string = LineString([[x.x, x.y] for x in (adc_polygon_pts[1], adc_polygon_pts[2])])

        for obs in self.last_perception.perception_obstacle:
            # ignore this obs if it collided ego car before
            if obs.id in self.collision_type_checking_result_dict:
                continue

            obs_polygon = Polygon([[x.x, x.y] for x in obs.polygon_point])
            if adc_polygon.intersection(obs_polygon):
                if adc_rear_line_string.intersection(obs_polygon):
                    self.collision_type_checking_result_dict[obs.id] = CollisionType.REAR_END
                else:
                    self.collision_type_checking_result_dict[obs.id] = CollisionType.DEFAULT

    def is_adc_completely_stopped(self) -> bool:
        adc_pose = self.last_localization.pose
        adc_velocity = calculate_velocity(adc_pose.linear_velocity)

        # https://github.com/ApolloAuto/apollo/blob/0789b7ea1e1356dde444452ab21b51854781e304/modules/planning/scenarios/stop_sign/unprotected/stage_pre_stop.cc#L237
        # return adc_velocity <= self.MAX_ABS_SPEED_WHEN_STOPPED
        return adc_velocity == 0

    def get_results(self):
        if len(self.collision_type_checking_result_dict) > 0:
            result = list()
            for obs_id, collision_type in self.collision_type_checking_result_dict.items():
                result.append({"type": collision_type, "obstacle_id": obs_id})
            return {"collision": result}
        else:
            return {}
