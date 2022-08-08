from collections import defaultdict
from datetime import datetime
import math
from statistics import mean
import time
from tracemalloc import start
from cyber_record.record import Record
from shapely.geometry import Point
from apollo.utils import generate_polygon
from utils import zero_velocity
from utils.config import APOLLO_VEHICLE_LENGTH, APOLLO_VEHICLE_WIDTH
from shapely.geometry import Polygon


class RecordAnalyzer:
    PERCEPTION = '/apollo/perception/obstacles'
    LOCALIZATION = '/apollo/localization/pose'
    PLANNING = '/apollo/planning'
    CHASSIS = '/apollo/canbus/chassis'

    decisions: defaultdict

    def __init__(self) -> None:
        self.initialize()

    def initialize(self):
        self.decisions = defaultdict(lambda: 0)

    def analyze_planning_message(self, message):
        main_decision = message.decision.main_decision
        object_decisions = message.decision.object_decision.decision

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
        self.decisions[md] += 1

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
            self.decisions[od] += 1

        return md, main_decision

    def analyze_stop_sign_stop(self, record, stop_sign_stop_positions) -> float:

        targets = dict()
        conversion = 1000000000
        for k in stop_sign_stop_positions:
            x = mean(stop_sign_stop_positions[k]['x'])
            y = mean(stop_sign_stop_positions[k]['y'])
            targets[(k, x, y)] = list()

        speeds = defaultdict(lambda: list())
        start_time = None

        for topic, message, t in record.read_messages():
            if not start_time:
                start_time = datetime.fromtimestamp(t/conversion)
            if topic == RecordAnalyzer.LOCALIZATION:
                curr_time = datetime.fromtimestamp(t/conversion)

                px = message.pose.position.x
                py = message.pose.position.y
                vx = message.pose.linear_velocity.x
                vy = message.pose.linear_velocity.y

                speed = Point(vx, vy).distance(Point(0, 0))

                p = Point(px, py)
                for t in targets:
                    tp = Point(t[1], t[2])
                    if tp.distance(p) < 6:
                        speeds[t[0]].append((tp.distance(p), speed))

        result = dict()

        for stop_sign in speeds:
            reversed_log = list(reversed(speeds[stop_sign]))
            for index, value in enumerate(reversed_log):
                if index == len(reversed_log) - 1:
                    break
                if value[0] > reversed_log[index+1][0]:
                    # moving away
                    continue
                if value[1] == 0.0:
                    result[stop_sign] = 'FULL_STOP'
                    break
                elif value[1] < 0.1:
                    result[stop_sign] = 'ROLLING_STOP'
            if stop_sign not in result:
                result[stop_sign] = 'VIOLATION'
        return result

    def analyze_collision(self, record):
        localization = None
        perception = None
        distances = list()
        for topic, message, t in record.read_messages():
            if topic == RecordAnalyzer.LOCALIZATION:
                localization = message
            elif topic == RecordAnalyzer.PERCEPTION:
                perception = message
            else:
                # None got updated
                continue

            if localization and perception:
                polygon_points = generate_polygon(
                    localization.pose.position, localization.pose.heading, APOLLO_VEHICLE_LENGTH, APOLLO_VEHICLE_WIDTH)
                adc_polygon = Polygon(
                    sorted([(point.x, point.y) for point in polygon_points]))

                for obs in perception.perception_obstacle:
                    obs_polygon = Polygon(
                        sorted([(point.x, point.y) for point in obs.polygon_point]))
                    distances.append(adc_polygon.distance(obs_polygon))
        if len(distances) == 0:
            # no obstacle or no perception message
            return 10000000000
        return min(distances)

    def analyze_red_light_violation(self, record):
        # For a signal,
        # if the vehicle wasn't on its controlled line before it turned red
        # but is on the lane after it turned red
        # it is a red light violation
        # definition of being on a lane is distance = 0 and heading matches
        pass

    def analyze_mission(self, record, last_main_decision):
        pass

    def is_stop_sign_decision(self, dt):
        return dt[0] == 'main' and dt[1] == 'stop' and dt[2] == 101

    def analyze_record(self, path: str):
        # analyze for # of decision
        # analyze for closest distance to another vehicle
        # complete mission or not
        # module failure
        self.initialize()
        record = Record(path)

        conversion = 1000000000

        stop_sign_stop_positions = defaultdict(
            lambda: defaultdict(lambda: list()))
        last_main_decision = None
        # analyze planning message
        for topic, message, t in record.read_messages():
            if topic == RecordAnalyzer.PLANNING:
                last_main_decision, data = self.analyze_planning_message(
                    message)
                if self.is_stop_sign_decision(last_main_decision):
                    stop_sign_stop_positions[last_main_decision]['x'].append(
                        data.stop.stop_point.x)
                    stop_sign_stop_positions[last_main_decision]['y'].append(
                        data.stop.stop_point.y)

        # analyze if stopped for stop sign
        ss_analysis = self.analyze_stop_sign_stop(
            record, stop_sign_stop_positions)
        # analysis for collision
        co_analysis = self.analyze_collision(record)
        tc_analysis = self.analyze_red_light_violation(record)
        mission_analysis = self.analyze_mission(record, last_main_decision)

        result = {
            'min_distance': co_analysis,
            'stop_sign': ss_analysis,
            'decisions': list(self.decisions.keys())
        }
        print(result)
        return result
