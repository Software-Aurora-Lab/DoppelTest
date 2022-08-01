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

    Parameters:
        s: str
            string to be converted
    Returns:
        b: bytes
    """
    return bytes(s, 'ascii')


class BridgeOp:
    """
    Class representing cyber bridge operations
    """
    RegisterDesc = (1).to_bytes(1, byteorder='big')
    AddReader = (2).to_bytes(1, byteorder='big')
    AddWriter = (3).to_bytes(1, byteorder='big')
    Publish = (4).to_bytes(1, byteorder='big')


@dataclass
class Channel:
    """
    Class representing information regarding cyber bridge channels

    Attributes:
        channel: str
            name of the cyber_bridge channel
        msg_type: str
            name of the type of the channel
        msg_cls: any
            protobuf constructor for the specified type
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
    """
    Class to represent CyberBridge

    Attributes:
        conn: socket
            Socket connection to cyber bridge
        subscribers: DefaultDict[str, List]
            Dictionary of subscribers, key is channel name, value is list of function calls
        publishable_channel: Set[str]
            Set of registered publishers
        spinning: bool
            Controls the thread reading data from bridge to start/stop
        t: Thread
            Background thread to start reading data from bridge
    """
    conn: socket
    subscribers: DefaultDict[str, List]
    publishable_channel: Set[str]
    spinning: bool
    t: Thread

    def __init__(self, host: str, port=9090) -> None:
        """
        Construct all the attributes for CyberBridge object

        Parameters:
            host: str
                host IP address of the cyber bridge
            port: int
                host port of the cyber bridge
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

        Parameters:
            data: bytes
                data to be sent

        Returns:
            result: bytes
                Prepared bytes ready to be sent to bridge
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

        Parameters:
            channel: Channel
                the topic to subscribe from
            cb: Function
                a function that takes parsed data from bridge
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

        Parameters:
            channel: Channel
                the channel to publish to
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

        Parameters:
            data: bytes
                data received from bridge
        """
        op = data[0]
        if op == int.from_bytes(BridgeOp.Publish, 'big'):
            self.receive_publish(data)
        else:
            pass

    def __get_32_le(self, b: bytes) -> int:
        """
        Converts 32 bit le integer to int

        Parameters:
            b: bytes
                bytes representing a 32 bit integer
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

        Parameters:
            data: bytes
                data received from bridge
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

        Parameters:
            channel: Channel
                channel to publish data to
            data: bytes
                data to be published
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
