from framework.oracles.OracleInterface import OracleInterface


class UUStopOracle(OracleInterface):
    def get_interested_topics(self):
        return super().get_interested_topics()

    def on_new_message(self, topic: str, message, t):
        return super().on_new_message(topic, message)

    def get_result(self):
        return super().get_result()
