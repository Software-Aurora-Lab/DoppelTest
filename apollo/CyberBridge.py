from collections import defaultdict
from dataclasses import dataclass
import socket
from threading import Thread
from typing import Set
from modules.canbus.proto.chassis_pb2 import Chassis
from modules.common.proto.geometry_pb2 import Point3D
from modules.localization.proto.localization_pb2 import LocalizationEstimate
from modules.perception.proto.perception_obstacle_pb2 import PerceptionObstacle, PerceptionObstacles
from modules.perception.proto.traffic_light_detection_pb2 import TrafficLightDetection
from modules.planning.proto.planning_pb2 import ADCTrajectory
from modules.routing.proto.routing_pb2 import RoutingRequest


def to_bytes(s: str):
    return bytes(s, 'ascii')


class BridgeOp:
    RegisterDesc = (1).to_bytes(1, byteorder='big')
    AddReader = (2).to_bytes(1, byteorder='big')
    AddWriter = (3).to_bytes(1, byteorder='big')
    Publish = (4).to_bytes(1, byteorder='big')


@dataclass
class Channel:
    channel: str
    msg_type: str
    msg_cls: any


class Topics:
    Chassis = Channel('/apollo/canbus/chassis',
                      'apollo.canbus.Chassis', Chassis)
    Localization = Channel('/apollo/localization/pose',
                           'apollo.localization.LocalizationEstimate', LocalizationEstimate)
    Obstacles = Channel('/apollo/perception/obstacles',
                        'apollo.perception.PerceptionObstacles', PerceptionObstacles)
    TrafficLight = Channel('/apollo/perception/traffic_light',
                           'apollo.perception.TrafficLightDetection', TrafficLightDetection)
    Planning = Channel('/apollo/planning/simplified',
                       'apollo.planning.ADCTrajectory', ADCTrajectory)
    RoutingRequest = Channel('/apollo/routing_request',
                             'apollo.routing.RoutingRequest', RoutingRequest)


class CyberBridge:
    publishable_channel: Set[str]
    spinning: bool
    t: Thread

    def __init__(self, host: str, port=9090) -> None:
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect((host, port))
        self.subscribers = defaultdict(lambda: list())
        self.publishable_channel = set()
        self.spinning = False

    @staticmethod
    def __prepare_bytes(data: bytes):
        result = bytes()
        shifts = [0, 8, 16, 24]
        for s in shifts:
            result += ((len(data) >> s).to_bytes(4, byteorder='big')
                       [-1]).to_bytes(1, byteorder='big')
        result += data
        return result

    def add_subscriber(self, topic: Channel, cb):
        topic_msg_type = topic.msg_type

        data = BridgeOp.AddReader
        data += self.__prepare_bytes(to_bytes(topic.channel))
        data += self.__prepare_bytes(to_bytes(topic_msg_type))

        self.conn.send(data)

        def cb_wrapper(data):
            parsed_msg = topic.msg_cls()
            parsed_msg.ParseFromString(data)
            cb(parsed_msg)

        self.subscribers[topic.channel].append(cb_wrapper)

    def add_publisher(self, channel: Channel):
        if channel.channel in self.publishable_channel:
            return

        topic_msg_type = channel.msg_type

        data = BridgeOp.AddWriter
        data += self.__prepare_bytes(to_bytes(channel.channel))
        data += self.__prepare_bytes(to_bytes(topic_msg_type))
        self.conn.send(data)
        self.publishable_channel.add(channel.channel)

    def on_read(self, data: bytes):
        op = data[0]
        if op == int.from_bytes(BridgeOp.Publish, 'big'):
            self.receive_publish(data)
        else:
            pass

    def __get_32_le(self, b) -> int:
        assert len(b) == 4, f"Expecting 4 bytes, got {len(b)}"
        b0 = b[0]
        b1 = b[1]
        b2 = b[2]
        b3 = b[3]
        return b0 | b1 << 8 | b2 << 16 | b3 << 24

    def receive_publish(self, data: bytes):
        offset = 1
        topic_length = self.__get_32_le(data[offset:offset+4])
        offset += 4
        topic = data[offset:offset+topic_length].decode('ascii')
        offset += topic_length
        message_size = self.__get_32_le(data[offset:offset+4])
        offset += 4
        msg = data[offset:offset+message_size]

        for subscriber in self.subscribers[topic]:
            subscriber(msg)

    def publish(self, topic: Channel, data: bytes):
        assert type(data) == bytes
        msg = BridgeOp.Publish
        msg += self.__prepare_bytes(to_bytes(topic.channel))
        msg += self.__prepare_bytes(data)
        self.conn.send(msg)

    def spin(self):
        if self.spinning:
            return

        def forever():
            while self.spinning:
                data = self.conn.recv(65527)
                try:
                    self.on_read(data)
                except Exception as e:
                    # random bridge errors
                    pass
        self.spinning = True
        self.t = Thread(target=forever)
        self.t.start()

    def stop(self):
        self.spinning = False
        self.t.join(5)
