from typing import List, Dict, Set, Tuple, Optional

from shapely.geometry import Polygon, LineString, Point

from apollo.utils import calculate_velocity, generate_adc_polygon, construct_lane_polygon, \
    construct_lane_boundary_linestring
from framework.oracles.OracleInterface import OracleInterface
from hdmap.MapParser import MapParser
from modules.localization.proto.localization_pb2 import LocalizationEstimate


class UnsafeLaneChangeOracle(OracleInterface):
    """
    *Idea for ADC making unsafe lane change:
    Todo
    """

    past_localization_list: List[LocalizationEstimate]

    unsafe_lane_change_locations: Set[str]
    lane_polygon_dict: Dict[str, LineString]
    lane_boundaries_dict: Dict[str, Tuple[LineString, LineString]]
    is_adc_started_to_drive = Optional[bool]

    ADC_INTERSECTING_LANE_BOUNDARY_MAX_LOOK_BACK_FRAMES_IN_SECOND = 5.0

    def __init__(self):
        self.unsafe_lane_change_locations = set()
        self.past_localization_list = list()

        self.parse_lane_info_on_map(MapParser.get_instance())

    def get_interested_topics(self):
        return [
            '/apollo/localization/pose',
        ]

    def on_new_message(self, topic: str, message, t):
        self.prune_old_messages()

        if topic == '/apollo/localization/pose':
            self.past_localization_list.append(message)

        if not self.past_localization_list:
            return
        # start_time = time.time()
        self.check_if_adc_intersecting_any_lane_boundaries_for_too_long()
        # print("--- %s seconds ---" % (time.time() - start_time))

    def get_result(self):
        result = list()
        for lane_id in self.unsafe_lane_change_locations:
            violation = ('unsafe_lane_change', lane_id)
            result.append(violation)
        return result

    def parse_lane_info_on_map(self, map_parser: MapParser) -> None:
        self.lane_polygon_dict = dict()
        self.lane_boundaries_dict = dict()
        lane_ids = map_parser.get_lanes()
        for l_id in lane_ids:
            lane_data = map_parser.get_lane_by_id(l_id)
            self.lane_polygon_dict[l_id] = construct_lane_polygon(lane_data)
            self.lane_boundaries_dict[l_id] = construct_lane_boundary_linestring(lane_data)

    def check_if_adc_intersecting_any_lane_boundaries_for_too_long(self):
        last_localization_timestamp = self.past_localization_list[-1].header.timestamp_sec
        current_boundary_intersecting_lane_id = None
        is_enough_checking_time = False
        for i, past_localization in enumerate(self.past_localization_list[::-1]):
            past_localization_timestamp = past_localization.header.timestamp_sec
            if last_localization_timestamp - past_localization_timestamp > self.ADC_INTERSECTING_LANE_BOUNDARY_MAX_LOOK_BACK_FRAMES_IN_SECOND:
                is_enough_checking_time = True
                break

            if self.is_adc_completely_stopped(past_localization):
                return

            adc_pose = past_localization.pose
            adc_polygon_pts = generate_adc_polygon(adc_pose.position, adc_pose.heading)
            adc_polygon = Polygon([[x.x, x.y] for x in adc_polygon_pts])

            adc_lane_id = self.find_lane_of_adc(past_localization)

            lane_boundaries = self.lane_boundaries_dict[adc_lane_id]
            is_adc_intersecting_lane_boundary = adc_polygon.intersection(lane_boundaries[0]) or \
                                                adc_polygon.intersection(lane_boundaries[1])
            if not is_adc_intersecting_lane_boundary:
                return
            else:
                if i == 0:
                    current_boundary_intersecting_lane_id = adc_lane_id
                else:
                    if current_boundary_intersecting_lane_id != adc_lane_id:
                        return
        if current_boundary_intersecting_lane_id and is_enough_checking_time:
            self.unsafe_lane_change_locations.add(current_boundary_intersecting_lane_id)

    CACHE_FOUND_LANES = []

    def find_lane_of_adc(self, localization_message):
        adc_pose = localization_message.pose
        adc_pose_position = adc_pose.position
        current_point = Point(adc_pose_position.x, adc_pose_position.y)

        if len(self.CACHE_FOUND_LANES) >= 5:
            self.CACHE_FOUND_LANES = self.CACHE_FOUND_LANES[1::]

        checked = set()
        for lane_data in self.CACHE_FOUND_LANES[::-1]:
            lane_id, lane_polygon = lane_data
            if lane_id in checked:
                continue
            if current_point.within(lane_polygon):
                return lane_id
            checked.add(lane_id)

        for lane_id, lane_polygon in self.lane_polygon_dict.items():
            if current_point.within(lane_polygon):
                self.CACHE_FOUND_LANES.append((lane_id, lane_polygon))
                return lane_id

        return None

    def is_adc_completely_stopped(self, localization_message) -> bool:
        adc_pose = localization_message.pose
        adc_velocity = calculate_velocity(adc_pose.linear_velocity)
        return adc_velocity == 0.0

    def prune_old_messages(self) -> None:
        total_localization_message_number = len(self.past_localization_list)
        if total_localization_message_number > 200:
            # based on PERCEPTION_FREQUENCY = 25 == 125 messages sent per 5 seconds
            self.past_localization_list = self.past_localization_list[1:]
