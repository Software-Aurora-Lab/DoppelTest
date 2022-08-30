from config import FORCE_INVALID_TRAFFIC_CONTROL
from modules.perception.proto.traffic_light_detection_pb2 import TrafficLightDetection, TrafficLight
from time import time
from framework.scenario.tc_config import TCSection


class TrafficControlManager:
    def __init__(self, tc: TCSection) -> None:
        self.tc = tc
        self.sequence_num = 0

    def get_traffic_configuration(self, curr_t: float) -> TrafficLightDetection:

        if FORCE_INVALID_TRAFFIC_CONTROL:
            config = self.tc.get_config_with_color('GREEN')
        elif self.tc.initial == self.tc.final:
            config = self.tc.initial
        else:
            if curr_t <= self.tc.duration_g:
                # green duration
                config = self.tc.initial
                pass
            elif curr_t <= self.tc.duration_g + self.tc.duration_y:
                config = self.tc.calculate_transition()
                # yellow duration
                pass
            elif curr_t <= self.tc.duration_g + self.tc.duration_y + self.tc.duration_b:
                # buffer duration
                config = self.tc.get_config_with_color('RED')
            else:
                config = self.tc.final

        tld = TrafficLightDetection()
        tld.header.timestamp_sec = time()
        tld.header.module_name = "MAGGIE"
        tld.header.sequence_num = self.sequence_num
        self.sequence_num += 1

        for k in config:
            tl = tld.traffic_light.add()
            tl.id = k
            tl.confidence = 1

            if config[k] == 'GREEN':
                tl.color = TrafficLight.GREEN
            elif config[k] == 'YELLOW':
                tl.color = TrafficLight.YELLOW
            else:
                tl.color = TrafficLight.RED

        return tld
