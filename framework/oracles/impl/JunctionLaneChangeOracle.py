from typing import List

from shapely.geometry import Point, Polygon

from config import HD_MAP
from framework.oracles.OracleInterface import OracleInterface
from hdmap.MapParser import MapParser


class JunctionLaneChangeOracle(OracleInterface):
    def __init__(self) -> None:
        super().__init__()
        self.mp = MapParser.get_instance(HD_MAP)
        self.junctions = list()
        for j_id in self.mp.get_junctions():
            j_obj = self.mp.get_junction_by_id(j_id)
            junction_polygon = Polygon([[x.x, x.y] for x in j_obj.polygon.point])
            self.junctions.append(
                (j_id, junction_polygon)
            )
        self.last_localization = None
        self.violation = None

    def get_interested_topics(self) -> List[str]:
        return [
            '/apollo/planning',
            '/apollo/localization/pose'
        ]

    def current_junction(self):
        if self.last_localization is None:
            return ''
        p = self.last_localization.pose.position
        ego_position = Point(p.x, p.y)

        for j_id, j_poly in self.junctions:
            if ego_position.within(j_poly):
                return j_id
        return ''

    def on_planning(self, message):
        if self.last_localization is None:
            return
        main_decision = message.decision.main_decision
        change_lane_type = None
        if main_decision.HasField('cruise'):
            change_lane_type = main_decision.cruise.change_lane_type
        elif main_decision.HasField('stop'):
            change_lane_type = main_decision.stop.change_lane_type
        # modules/routing/proto/routing.proto#70
        changing_lane = change_lane_type is not None and change_lane_type in [
            1, 2]
        
        if changing_lane and self.current_junction() != '':
            self.violation = f'Lane Change at Junction {self.current_junction()}'

    def on_localization(self, message):
        self.last_localization = message

    def on_new_message(self, topic: str, message, t):
        if self.violation is not None:
            # violation already tracked
            return
        if topic == '/apollo/planning':
            self.on_planning(message)
        else:
            self.on_localization(message)

    def get_result(self):
        if self.violation is None:
            return []
        return [('Junction Violation', self.violation)]
