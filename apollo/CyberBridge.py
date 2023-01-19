from collections import defaultdict
from dataclasses import dataclass
import socket
from threading import Thread
from typing import DefaultDict, List, Set

from modules.canbus.proto.chassis_pb2 import Chassis
from modules.localization.proto.localization_pb2 import LocalizationEstimate
from modules.perception.proto.perception_obstacle_pb2 import PerceptionObstacles
from modules.perception.proto.traffic_light_detection_pb2 import TrafficLightDetection
from modules.planning.proto.planning_pb2 import ADCTrajectory
from modules.routing.proto.routing_pb2 import RoutingRequest


def to_bytes(s: str) -> bytes:
    """
    Converts string to bytes using ascii

    :param str s: string to be converted
    :returns: bytes in ascii
    :rtype: bytes
    """
    return bytes(s, 'ascii')


class BridgeOp:
    """
    Class representing cyber bridge operations.
    """
    RegisterDesc = (1).to_bytes(1, byteorder='big')
    AddReader = (2).to_bytes(1, byteorder='big')
    """Register a subscriber"""
    AddWriter = (3).to_bytes(1, byteorder='big')
    """Register a publisher"""
    Publish = (4).to_bytes(1, byteorder='big')
    """Publish a message"""


@dataclass
class Channel:
    """
    Class representing information regarding cyber bridge channels

    :param str channel: the name of the channel
    :param str msg_type: the protobuf data type of messages on this channel
    :param any msg_cls: the compiled Python protobuf class
    """
    channel: str
    msg_type: str
    msg_cls: any


class Topics:
    """
    Class representing channels used
    """
    Chassis = Channel('/apollo/canbus/chassis',
                      'apollo.canbus.Chassis', Chassis)
    """Chassis channel"""
    Localization = Channel('/apollo/localization/pose',
                           'apollo.localization.LocalizationEstimate', LocalizationEstimate)
    """Localization Channel, typically includes vehicle's location, velocity, acceleration, etc."""
    Obstacles = Channel('/apollo/perception/obstacles',
                        'apollo.perception.PerceptionObstacles', PerceptionObstacles)
    """Perception Channel, typically includes obstacles perceived from sensor or ground truth."""
    TrafficLight = Channel('/apollo/perception/traffic_light',
                           'apollo.perception.TrafficLightDetection', TrafficLightDetection)
    """Traffic Light Channel, users can send color of any traffic signal to this channel"""
    Planning = Channel('/apollo/planning/simplified',
                       'apollo.planning.ADCTrajectory', ADCTrajectory)
    """Planning Channel, Apollo's planning decisions are published to this channel"""
    RoutingRequest = Channel('/apollo/routing_request',
                             'apollo.routing.RoutingRequest', RoutingRequest)
    """Routing Request Channel, users send routing request to this channel"""


class CyberBridge:
    """
    Class to represent CyberBridge

    :param str host: IP address of cyber bridge running inside docker
    :param int port: port of the cyber bridge
    """

    conn: socket
    subscribers: DefaultDict[str, List]
    publishable_channel: Set[str]
    spinning: bool
    t: Thread

    def __init__(self, host: str, port=9090) -> None:
        """
        Constructor
        """
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect((host, port))
        self.conn.setblocking(False)
        self.subscribers = defaultdict(lambda: list())
        self.publishable_channel = set()
        self.spinning = False

    @staticmethod
    def __prepare_bytes(data: bytes) -> bytes:
        """
        Transforms data into [length][data]

        :param bytes data: data to be sent

        :returns: prepared bytes ready to be sent to bridge
        :rtype: bytes
        """
        result = bytes()
        shifts = [0, 8, 16, 24]
        for s in shifts:
            result += ((len(data) >> s).to_bytes(4, byteorder='big')
                       [-1]).to_bytes(1, byteorder='big')
        result += data
        return result

    def add_subscriber(self, channel: Channel, cb):
        """
        Adds a subscriber to the bridge

        :param Channel channel: the channel to subscribe from
        :param Function cb: callback function that takes parsed data from bridge
        """
        topic_msg_type = channel.msg_type

        data = BridgeOp.AddReader
        data += self.__prepare_bytes(to_bytes(channel.channel))
        data += self.__prepare_bytes(to_bytes(topic_msg_type))

        self.conn.send(data)

        def cb_wrapper(data):
            parsed_msg = channel.msg_cls()
            parsed_msg.ParseFromString(data)
            cb(parsed_msg)

        self.subscribers[channel.channel].append(cb_wrapper)

    def add_publisher(self, channel: Channel):
        """
        Adds a publisher to the bridge

        :param Channel channel: the channel to publish message to
        """
        if channel.channel in self.publishable_channel:
            return

        topic_msg_type = channel.msg_type

        data = BridgeOp.AddWriter
        data += self.__prepare_bytes(to_bytes(channel.channel))
        data += self.__prepare_bytes(to_bytes(topic_msg_type))
        self.conn.send(data)
        self.publishable_channel.add(channel.channel)

    def on_read(self, data: bytes):
        """
        Function callback to notify bridge has published data

        :param bytes data: data received from bridge
        """
        op = data[0]
        if op == int.from_bytes(BridgeOp.Publish, 'big'):
            self.receive_publish(data)
        else:
            pass

    def __get_32_le(self, b: bytes) -> int:
        """
        Converts 32 bit le integer to int

        :param bytes b: bytes representing a 32 bit integer

        :return: converted integer
        :rtype: int
        """
        assert len(b) == 4, f"Expecting 4 bytes, got {len(b)}"
        b0 = b[0]
        b1 = b[1]
        b2 = b[2]
        b3 = b[3]
        return b0 | b1 << 8 | b2 << 16 | b3 << 24

    def receive_publish(self, data: bytes):
        """
        Receives data published by bridge and calls subscribers

        :param bytes data: data received from bridge
        """
        if not self.spinning:
            return
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

    def publish(self, channel: Channel, data: bytes):
        """
        Publish data to the bridge

        :param Channel channel: channel to publish data to
        :param bytes data: data to be published

        :note: You should register a publisher first before publishing any data
        """
        assert type(data) == bytes
        msg = BridgeOp.Publish
        msg += self.__prepare_bytes(to_bytes(channel.channel))
        msg += self.__prepare_bytes(data)
        self.conn.send(msg)

    def _spin(self):
        """
        Helper function to start receiving data from socket
        """
        while self.spinning:
            try:
                data = self.conn.recv(65527)
                self.on_read(data)
            except Exception as e:
                pass

    def spin(self):
        """
        Starts to spin the cyber bridge client
        """
        if self.spinning:
            return
        self.spinning = True
        self.t = Thread(target=self._spin)
        self.t.start()

    def stop(self):
        """
        Stops the cyber bridge client
        """
        self.spinning = False
        self.t.join()
