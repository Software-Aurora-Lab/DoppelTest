from collections import defaultdict
from typing import Dict, List, Tuple

from framework.oracles.OracleInterface import OracleInterface


class OracleManager:
    """
    Helper class to organize all oracles
    """
    __topic_oracle_mapping: Dict[str, List[OracleInterface]]
    __registered_oracles: List[OracleInterface]

    def __init__(self) -> None:
        """
        Constructor
        """
        self.__topic_oracle_mapping = defaultdict(lambda: list())
        self.__registered_oracles = list()

    def register_oracle(self, oracle: OracleInterface):
        """
        Register a specific oracle

        :param OracleInterface oracle: oracle to be registered
        """
        self.__registered_oracles.append(oracle)
        for topic in oracle.get_interested_topics():
            self.__topic_oracle_mapping[topic].append(oracle)

    def on_new_message(self, topic, message, t):
        """
        Calls ``on_new_message`` for each of the oracle interested in a specific topic

        :param str topic: the topic of the message
        :param any message: actual message data
        :param float t: timestamp of the message
        """
        for oracle in self.__topic_oracle_mapping[topic]:
            oracle.on_new_message(topic, message, t)

    def get_results(self) -> List[Tuple]:
        """
        Retrieve the violations analyzed from each of the oracles

        :returns: all violations detected
        :rtype: List[Tuple]
        """
        result = list()
        for oracle in self.__registered_oracles:
            result += oracle.get_result()
        return result
