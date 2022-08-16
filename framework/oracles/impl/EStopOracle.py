from typing import List, Set
from framework.oracles.OracleInterface import OracleInterface


class EStopOracle(OracleInterface):
    estops: Set

    def __init__(self) -> None:
        self.estops = set()

    def get_interested_topics(self):
        return [
            '/apollo/planning'
        ]

    def on_new_message(self, topic: str, message, t):
        main_decision = message.decision.main_decision
        if main_decision.HasField('estop'):
            self.estops.add(main_decision.estop.reason_code)

    def get_result(self):
        result = list()
        for err_code in self.estops:
            result.append(('estop', err_code))
        return result
