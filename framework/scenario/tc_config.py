from dataclasses import dataclass
from random import randint, shuffle
from typing import Dict

from config import HD_MAP, SCENARIO_UPPER_LIMIT
from hdmap.MapParser import MapParser


@dataclass
class TCSection:
    """
    Genetic representation of the traffic control section

    :param Dict[str, str] initial: the initial configuration
    :param Dict[str, str] final: the final configuration
    :param float duration_g: green signal duration
    :param float duration_y: yellow change interval duration
    :param float duration_b: red clearance interval duration
    """
    initial: Dict[str, str]
    final: Dict[str, str]
    duration_g: float
    duration_y: float
    duration_b: float

    def calculate_transition(self) -> Dict[str, str]:
        """
        Calculates the color of signals during the transition stage.

        :returns: color assignment for signals during the transition stage
        :rtype: Dict[str, str]

        :example: If a signal was green in the initial configuration,
          but is red in the final configuration, it must be yellow during
          the transition stage.
        """
        result = dict()
        for k in self.initial:
            if self.initial[k] == 'GREEN' and self.final[k] == 'RED':
                result[k] = 'YELLOW'
            else:
                result[k] = self.initial[k]
        return result

    def get_config_with_color(self, color: str) -> Dict[str, str]:
        """
        Gets a configuration where all signals have the specified color

        :param str color: color to be specified

        :returns: a configuration in which all signals have the specified color
        :rtype: Dict[str, str]

        :warning: It is reasonable if all signals are red, but all signals being green
          will definitely cause problems!
        """
        result = dict()
        for k in self.initial:
            result[k] = color
        return result

    @staticmethod
    def generate_config(preference=[]) -> Dict[str, str]:
        """
        Generate a configuration with certain signals being green

        :param List[str] preference: signals prefered to be green

        :returns: a configuration in which preferred signals are green
        :rtype: Dict[str, str]
        """
        ma = MapParser.get_instance(HD_MAP)
        result = dict()
        signals = list(ma.get_signals())
        shuffle(signals)
        while len(signals) > 0:
            if len(preference) > 0:
                curr_sig = preference.pop()
                signals.remove(curr_sig)
            else:
                curr_sig = signals.pop()

            result[curr_sig] = 'GREEN'
            relevant = ma.get_signals_wrt(curr_sig)
            for sig, cond in relevant:
                if sig in preference:
                    preference.remove(sig)
                if sig in signals:
                    signals.remove(sig)
                    if cond == 'EQ':
                        result[sig] = 'GREEN'
                    else:
                        # NE
                        result[sig] = 'RED'
        return result

    @staticmethod
    def get_one() -> 'TCSection':
        """
        Randomly generates a traffic control section

        :returns: traffic control section
        :rypte: TCSection
        """
        init = TCSection.generate_config()
        final = TCSection.generate_config(
            preference=[x for x in init if init[x] == 'RED'])
        return TCSection(
            initial=init,
            final=final,
            duration_g=randint(5, int(SCENARIO_UPPER_LIMIT/2)),
            duration_y=3,
            duration_b=2
        )

    @staticmethod
    def get_random_duration_g() -> int:
        """
        Generate a random duration for green light

        :returns: green light duration
        :rtype: int
        """
        return randint(5, int(SCENARIO_UPPER_LIMIT/2))
