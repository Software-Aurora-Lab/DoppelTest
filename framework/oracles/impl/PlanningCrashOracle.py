from typing import Set, Optional, Dict

from shapely.geometry import LineString, Point

from apollo.utils import calculate_velocity, construct_lane_polygon
from framework.oracles.OracleInterface import OracleInterface
from hdmap.MapParser import MapParser
from modules.localization.proto.localization_pb2 import LocalizationEstimate
from modules.planning.proto.planning_pb2 import ADCTrajectory


class PlanningCrashOracle(OracleInterface):
    """
        *Idea for checking if ADC planner crashed:
        ADC must have been driven for a certain distance (to make sure it's not routing failure),
        If ADC stopped at speed of 0.0 m/s, check if:
        (1) no decision/NOT_READY decision is being made
    """

    last_localization = Optional[LocalizationEstimate]
    last_planning = Optional[ADCTrajectory]
    is_adc_started_to_drive = Optional[bool]
    lane_polygon_dict: Dict[str, LineString]

    planning_crash_locations: Set[str]

    def __init__(self) -> None:
        self.planning_crash_locations = set()

        self.last_localization = None
        self.last_planning = None

        self.is_adc_started_to_drive = False

        self.parse_lane_polygon_on_map(MapParser.get_instance())

    def get_interested_topics(self):
        return [
            '/apollo/localization/pose',
            '/apollo/planning'
        ]

    def on_new_message(self, topic: str, message, t):
        if topic == '/apollo/localization/pose':
            self.last_localization = message
        else:
            self.last_planning = message
            return

        if self.last_localization is None or self.last_planning is None:
            return

        if not self.is_adc_completely_stopped:
            if not self.is_adc_started_to_drive:
                self.is_adc_started_to_drive = True
            return

        if not self.is_adc_started_to_drive:
            return

        self.check_if_adc_planning_crashed()

    @property
    def is_adc_completely_stopped(self) -> bool:
        adc_pose = self.last_localization.pose
        adc_velocity = calculate_velocity(adc_pose.linear_velocity)
        return adc_velocity == 0

    def check_if_adc_planning_crashed(self) -> None:
        if self.is_adc_planner_making_normal_decision():
            return

        adc_lane_id = self.find_current_lane_of_adc()

        self.planning_crash_locations.add(adc_lane_id)

    def is_adc_planner_making_normal_decision(self):
        planning_main_decision = self.last_planning.decision.main_decision
        if str(planning_main_decision).strip() == "":
            return False

        if str(planning_main_decision.not_ready).strip() != "":
            return False

        return True

    def parse_lane_polygon_on_map(self, map_parser: MapParser) -> None:
        self.lane_polygon_dict = dict()
        lane_ids = map_parser.get_lanes()
        for l_id in lane_ids:
            lane_polygon = construct_lane_polygon(map_parser.get_lane_by_id(l_id))
            self.lane_polygon_dict[l_id] = lane_polygon

    def find_current_lane_of_adc(self):
        last_localization = self.last_localization
        adc_pose = last_localization.pose
        adc_pose_position = adc_pose.position
        current_point = Point(adc_pose_position.x, adc_pose_position.y)
        for lane_id, lane_polygon in self.lane_polygon_dict.items():
            if current_point.within(lane_polygon):
                return lane_id
        return None

    def get_result(self):
        result = list()
        for lane_id in self.planning_crash_locations:
            result.append(('planning_crash', lane_id))
        return result
