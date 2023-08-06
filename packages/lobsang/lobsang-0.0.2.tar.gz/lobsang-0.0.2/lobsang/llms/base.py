from abc import ABC, abstractmethod
from collections.abc import Sequence

from lobsang.messages import Message


class LLM(ABC):
    """
    Abstract base class for LLMs.
    """
    @abstractmethod
    def chat(self, messages: Sequence[Message]) -> (str, dict):
        """
        Sends the provided messages to the LLM and returns the response.

        :param messages: A sequence of messages to send to the LLM.
        :return: (response, info) where info is a dictionary that may contain additional information about the response.
        """
        pass