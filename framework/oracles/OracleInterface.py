from abc import ABC, abstractmethod
from typing import List


class OracleInterface(ABC):
    """
    Interface that defines how a oracle should be implemented
    """

    @abstractmethod
    def get_interested_topics(self) -> List[str]:
        """
        Returns a list of topics this oracle is interested in. The oracle manager
        will call ``on_new_message`` for this oracle when a message from its
        interested topic is parsed

        :returns: list of topics
        :rtype: List[str]
        """
        return list()

    @abstractmethod
    def on_new_message(self, topic: str, message, t):
        """
        Called when a message from a interested topic is parsed, i.e., this function
        should define what the oracle should do for messages it is interested in
        """
        pass

    @abstractmethod
    def get_result(self) -> List:
        """
        Returns a list of violations from this oracle

        :returns: list of violations
        :rtype: List
        """
        return list()
