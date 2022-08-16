from abc import ABC, abstractmethod
from typing import List


class OracleInterface(ABC):

    @abstractmethod
    def get_interested_topics(self) -> List[str]:
        return list()

    @abstractmethod
    def on_new_message(self, topic: str, message, t):
        pass

    @abstractmethod
    def get_result(self):
        return list()
