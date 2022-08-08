from dataclasses import dataclass
from mimetypes import init
from random import randint, shuffle
from typing import Dict
from modules.map.proto.map_pb2 import Map
from random import random
from map.MapAnalyzer import MapAnalyzer


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
    def calculate_transition(initial: dict, final: dict):
        result = dict()
        for k in initial:
            if initial[k] == 'GREEN' and final[k] == 'RED':
                result[k] = 'YELLOW'
            else:
                result[k] = initial[k]
        return result

    @staticmethod
    def generate_config(ma: MapAnalyzer, preference=[]):
        result = dict()
        signals = list(ma.signals.keys())
        shuffle(signals)
        while len(signals) > 0:
            if len(preference) > 0:
                curr_sig = preference.pop()
                signals.remove(curr_sig)
            else:
                curr_sig = signals.pop(0)
            result[curr_sig] = 'GREEN'
            relevant = ma.get_signals_wrt(curr_sig)
            for sig, cond in relevant:
                signals.remove(sig)
                if cond == 'EQ':
                    result[sig] = 'GREEN'
                else:
                    result[sig] = 'RED'
        return result

    @staticmethod
    def get_one(ma: MapAnalyzer):
        initial = TCSection.generate_config(ma)
        final = TCSection.generate_config(
            ma, list(k for k in initial if initial[k] == 'RED'))
        dg = randint(10, 30)
        dy = 3
        db = 2
        return TCSection(
            initial,
            final,
            dg,
            dy,
            db
        )
