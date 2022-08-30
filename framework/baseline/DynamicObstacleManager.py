from random import randint
from typing import List, Tuple

from apollo.utils import dynamic_obstacle_location_to_obstacle
from framework.scenario.ad_agents import ADAgent
from hdmap.MapParser import MapParser
from modules.common.proto.geometry_pb2 import PointENU


class DynamicObstacleManager:
    obstacles: List[ADAgent]
    last_time: float
    obs_driving_time: List[float]
    obs_speed: List[float]
    obs_nids: List[int]

    def __init__(self, obs: List[ADAgent], nids: List[int]) -> None:
        self.obstacles = obs
        self.obs_driving_time = [0.0 for _ in range(len(obs))]
        self.obs_speed = [randint(10, 15) for _ in range(len(obs))]
        self.obs_nids = nids
        self.last_time = 0.0

    def calculate_position(self, ad: ADAgent, speed: float, time_spent_driving: float) -> Tuple[PointENU, float]:
        ma = MapParser.get_instance()
        dist = speed * time_spent_driving
        for index, lane_id in enumerate(ad.routing):
            lane_length = ma.get_lane_length(lane_id)
            if index < len(ad.routing) - 1:
                if dist < lane_length:
                    return ma.get_coordinate_and_heading(lane_id, dist)
                else:
                    dist -= lane_length
            else:
                if dist < lane_length:
                    return ma.get_coordinate_and_heading(lane_id, dist)
                else:
                    return ma.get_coordinate_and_heading(lane_id, lane_length)

    def get_obstacles(self, curr_time: float):
        result = list()
        delta_t = curr_time - self.last_time

        for index, obs in enumerate(self.obstacles):
            if curr_time > obs.start_t:
                self.obs_driving_time[index] += delta_t

            obs_position, obs_heading = self.calculate_position(
                obs, self.obs_speed[index], self.obs_driving_time[index])
            obs_speed = 0.0 if self.obs_driving_time[index] == 0.0 else self.obs_speed[index]
            obs = dynamic_obstacle_location_to_obstacle(
                _id=self.obs_nids[index],
                speed=obs_speed,
                loc=obs_position,
                heading=obs_heading
            )
            result.append(obs)

        self.last_time = curr_time
        return result
