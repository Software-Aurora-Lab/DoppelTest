from collections import defaultdict
from typing import Dict, List

from framework.oracles.OracleInterface import OracleInterface


class OracleManager:
    __topic_oracle_mapping: Dict[str, List[OracleInterface]]
    __registered_oracles: List[OracleInterface]

    def __init__(self) -> None:
        self.__topic_oracle_mapping = defaultdict(lambda: list())
        self.__registered_oracles = list()

    def register_oracle(self, oracle: OracleInterface):
        self.__registered_oracles.append(oracle)
        for topic in oracle.get_interested_topics():
            self.__topic_oracle_mapping[topic].append(oracle)

    def on_new_message(self, topic, message, t):
        for oracle in self.__topic_oracle_mapping[topic]:
            oracle.on_new_message(topic, message, t)

    def get_results(self):
        result = list()
        for oracle in self.__registered_oracles:
            result += oracle.get_result()
        return result
