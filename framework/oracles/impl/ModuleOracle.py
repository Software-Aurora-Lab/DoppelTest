from typing import List, Optional, Tuple

from framework.oracles.OracleInterface import OracleInterface
from modules.localization.proto.localization_pb2 import LocalizationEstimate


class ModuleOracle(OracleInterface):
    """
    The Module Oracle is responsible for determining whether the routing module failed.
    One root cause of this violation is the HD Map missing predecessor/successor
    information so that the routing module failed to find a valid route. We have fixed
    the issue with ``borregas_ave`` by updating the HD Map. (More details in 
    `Apollo Issue #14529 <https://github.com/ApolloAuto/apollo/issues/14529>`_)
    """
    prev_: Optional[LocalizationEstimate]
    next_: Optional[LocalizationEstimate]

    def __init__(self) -> None:
        self.prev_ = None
        self.next_ = None
        self.received_routing = False

    def get_interested_topics(self):
        """
        The module oracle is interested in Routing messages only
        """
        return [
            '/apollo/routing_response',
        ]

    def on_new_message(self, topic: str, message, t):
        """
        Upon receiving 1 routing response, the scenario passes this oracle

        :param str topic: topic of the message
        :param any message: either Planning or Localization message
        :param float t: the timestamp
        """
        if topic == '/apollo/routing_response':
            self.received_routing = True

    def get_result(self) -> List[Tuple]:
        """
        Returns violations detected by this oracle
        """
        result = list()
        if not self.received_routing:
            result.append(('module', 'routing failure'))
        return result
