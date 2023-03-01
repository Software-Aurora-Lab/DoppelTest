import math
from typing import List, Optional

import numpy as np

from apollo.utils import calculate_velocity
from framework.oracles.OracleInterface import OracleInterface
from modules.localization.proto.localization_pb2 import LocalizationEstimate


class ComfortOracle(OracleInterface):
    prev_: Optional[LocalizationEstimate]
    next_: Optional[LocalizationEstimate]
    accl: List[float]

    MAX_ACCL = 4.0
    MAX_DCCL = -4.0

    def __init__(self) -> None:
        self.prev_ = None
        self.next_ = None
        self.accl = list()

    def get_interested_topics(self):
        return ['/apollo/localization/pose']

    def on_new_message(self, topic: str, message, t):
        if self.prev_ is None and self.next_ is None:
            self.prev_ = message
            return
        self.next_ = message
        # compare velocity
        accel_x = self.next_.pose.linear_acceleration.x
        accel_y = self.next_.pose.linear_acceleration.y
        accel_z = self.next_.pose.linear_acceleration.z

        accel_value = math.sqrt(accel_x ** 2 + accel_y ** 2 + accel_z ** 2)

        prev_velocity = calculate_velocity(self.prev_.pose.linear_velocity)
        next_velocity = calculate_velocity(self.next_.pose.linear_velocity)
        direction = next_velocity - prev_velocity

        if direction < 0:
            accel = accel_value * -1
        else:
            accel = accel_value

        self.accl.append(accel)

        # update prev_
        self.prev_ = message


    def get_result(self):
        result = list()
        if len(self.accl) == 0:
            return result
        max_accl = np.max(self.accl)
        min_accl = np.min(self.accl)
        # if max_accl >= ComfortOracle.MAX_ACCL:
        if max_accl > ComfortOracle.MAX_ACCL:
            result.append(('comfort', 'Acceleration exceeded max'))
        if min_accl < ComfortOracle.MAX_DCCL:
            result.append(('comfort', 'Deceleration exceeded max'))
        return result
