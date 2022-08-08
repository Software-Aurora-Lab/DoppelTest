from dataclasses import dataclass
from random import randint, shuffle
from typing import Dict
from modules.map.proto.map_pb2 import Map
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
        allowedValue: [10, 30)
    duration_y: float
        number of seconds for signal being yellow 
        allowedValue: 3
    duration_b: float
        buffer period, where all signals go red 
        allwedValue: 2
    """
    initial: Dict[str, str]
    final: Dict[str, str]
    duration_g: float
    duration_y: float
    duration_b: float

    def calculate_transition(self):
        result = dict()
        for k in self.initial:
            if self.initial[k] == 'GREEN' and self.final[k] == 'RED':
                result[k] = 'YELLOW'
            else:
                result[k] = self.initial[k]
        return result

    def get_all(self, color: str):
        result = dict()
        for k in self.initial:
            result[k] = color
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
