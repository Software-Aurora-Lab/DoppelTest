import re
from typing import Dict, List, Optional, Set

from shapely.geometry import LineString, Polygon

from apollo.utils import generate_adc_polygon, calculate_velocity
from framework.oracles.OracleInterface import OracleInterface
from hdmap.MapParser import MapParser
from modules.localization.proto.localization_pb2 import LocalizationEstimate
from modules.perception.proto.traffic_light_detection_pb2 import TrafficLightDetection, TrafficLight
from modules.planning.proto.decision_pb2 import STOP_REASON_SIGNAL
from modules.planning.proto.planning_pb2 import ADCTrajectory


class TrafficSignalOracle(OracleInterface):
    """
        *Idea for checking if ADC had crossed the stop line when signal was RED:
        If the traffic light status is being RED and an ADC intersecting stop line at this time. Check if:
        (1) the STOP_REASON_SIGNAL decision is being made for this signal_id, and
        (2) ADC speed is 0.0 m/s at this time
    """

    last_localization = Optional[LocalizationEstimate]
    last_traffic_signal_detection = Optional[TrafficLightDetection]
    last_planning = Optional[ADCTrajectory]

    traffic_signal_stop_line_string_dict: Dict[str, LineString]
    violated_at_traffic_signal_ids: Set[str]

    TRAFFIC_LIGHT_VO_ID_PREFIX = "TL_"

    def __init__(self) -> None:
        self.violated_at_traffic_signal_ids = set()

        self.last_localization = None
        self.last_traffic_signal_detection = None
        self.last_planning = None

        self.parse_traffic_signal_stop_line_string_on_map(MapParser.get_instance())

    def get_interested_topics(self):
        return [
            '/apollo/localization/pose',
            '/apollo/perception/traffic_light',
            '/apollo/planning',
        ]

    def on_new_message(self, topic: str, message, t):
        if topic == '/apollo/localization/pose':
            self.last_localization = message
        elif topic == "/apollo/perception/traffic_light":
            self.last_traffic_signal_detection = message
            return
        else:
            self.last_planning = message
            return

        if self.last_localization is None or self.last_traffic_signal_detection is None \
                or self.last_planning is None:
            return

        last_traffic_signal_info = self.last_traffic_signal_detection.traffic_light
        if len(last_traffic_signal_info) <= 0:
            return

        last_traffic_signal_status = last_traffic_signal_info[0].color
        if last_traffic_signal_status != TrafficLight.RED:
            # todo - also handle TrafficLight.BLACK and TrafficLight.UNKNOWN
            return

        last_received_signal_id = last_traffic_signal_info[0].id
        crossing_traffic_signal_id = self.check_if_adc_intersecting_any_stop_lines()
        if last_received_signal_id != crossing_traffic_signal_id:
            return

        # now check both conditions (1) and (2)
        if self.is_planning_main_decision_to_stop_at_traffic_signal(self.last_planning,
                                                                    crossing_traffic_signal_id) is False \
                or self.is_adc_completely_stopped() is False:
            self.violated_at_traffic_signal_ids.add(crossing_traffic_signal_id)

    def get_result(self):
        result = list()
        for traffic_signal_id in self.violated_at_traffic_signal_ids:
            violation = ('traffic_signal', traffic_signal_id)
            result.append(violation)
        return result

    def parse_traffic_signal_stop_line_string_on_map(self, map_parser: MapParser) -> None:
        self.traffic_signal_stop_line_string_dict = dict()
        traffic_signal_ids = map_parser.get_signals()
        for ts_id in traffic_signal_ids:
            traffic_signal_data = map_parser.get_signal_by_id(ts_id)
            line = LineString([[p.x, p.y] for p in traffic_signal_data.stop_line[0].segment[0].line_segment.point])
            self.traffic_signal_stop_line_string_dict[ts_id] = line

    def check_if_adc_intersecting_any_stop_lines(self) -> str:
        last_localization = self.last_localization
        adc_pose = last_localization.pose
        adc_polygon_pts = generate_adc_polygon(adc_pose.position, adc_pose.heading)
        adc_polygon = Polygon([[x.x, x.y] for x in adc_polygon_pts])
        for traffic_signal_id, stop_line_string in self.traffic_signal_stop_line_string_dict.items():
            if not stop_line_string.intersection(adc_polygon).is_empty:
                return traffic_signal_id
        return ""

    def is_adc_completely_stopped(self) -> bool:
        adc_pose = self.last_localization.pose
        adc_velocity = calculate_velocity(adc_pose.linear_velocity)

        # https://github.com/ApolloAuto/apollo/blob/0789b7ea1e1356dde444452ab21b51854781e304/modules/planning/scenarios/stop_sign/unprotected/stage_pre_stop.cc#L237
        # return adc_velocity <= self.MAX_ABS_SPEED_WHEN_STOPPED
        return adc_velocity == 0

    def is_planning_main_decision_to_stop_at_traffic_signal(self, planning_message: ADCTrajectory,
                                                            traffic_signal_id: str) -> bool:
        try:
            stop_decision = planning_message.decision.main_decision.stop
        except AttributeError:
            return False

        stop_reason_code = stop_decision.reason_code
        if stop_reason_code != STOP_REASON_SIGNAL:
            return False

        stop_reason = stop_decision.reason  # e.g,  stop_reason = "stop by SS_stop_sign_0" (included stop_sign_id)
        if re.sub("^stop by ", "", stop_reason) == self.TRAFFIC_LIGHT_VO_ID_PREFIX + traffic_signal_id:
            return True

        return False
