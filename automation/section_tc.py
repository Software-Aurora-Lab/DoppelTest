from dataclasses import dataclass
from random import shuffle
from typing import Dict
from modules.map.proto.map_pb2 import Map


@dataclass
class TCSection:
    """
    Class to represent Traffic Control Section

    Attributes:
    initial: Dict[str, str]
        the initial configuration for every traffic signal on the map
    final: Dict[str, str]
        the final configuration for every traffic signal on the map
    duration_g: float
        number of seconds for signal being green
    duration_y: float
        number of seconds for signal being yellow
    duration_b: float
        buffer period, where all signals go red
    """
    initial: Dict[str, str]
    final: Dict[str, str]
    duration_g: float
    duration_y: float
    duration_b: float

    @staticmethod
    def get_one(map: Map):
        initial = dict()
        # retrieve all signals on the map
        signals = list()
        shuffle(signals)
        # while there is unassigned signal
        # pick one signal, assign a color
        # assign same color to equality group
        # assign opposite color to inequality group

        final = TCSection.invert_color(map, initial)
        dg = 10
        dy = 10
        db = 3
        return TCSection(
            initial,
            final,
            dg,
            dy,
            db
        )

    @staticmethod
    def invert_color(map: Map, configuration: Dict[str, str]):
        # while there is unassigned signal
        # pick one signal, invert its color
        # assign same color to equality group
        # assign opposite color to inequality group
        signals = list(configuration.keys())
        shuffle(signals)
        result = dict()
        # while there is uninverted signal
        while len(signals) > 0:
            # pick one signal
            picked = signals.pop()

            # invert its color
            original = configuration[picked]
            inverted = 'RED' if original == 'GREEN' else 'GREEN'
            result[picked] = inverted

            # assign same color to equality group

            # assign opposite color to inequality group

        return result
