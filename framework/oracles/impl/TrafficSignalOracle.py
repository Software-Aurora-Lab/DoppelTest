from framework.oracles.OracleInterface import OracleInterface


class TrafficSignalOracle(OracleInterface):
    """
    Checks if signal is red when ADC crosses signal controled stop line
    """

    def get_interested_topics(self):
        return super().get_interested_topics()

    def on_new_message(self, topic: str, message, t):
        return super().on_new_message(topic, message)

    def get_result(self):
        return super().get_result()
