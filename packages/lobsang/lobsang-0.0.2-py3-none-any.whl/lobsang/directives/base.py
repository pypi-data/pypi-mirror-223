from abc import ABC, abstractmethod


class Directive(ABC):
    """
    Abstract class for directives.
    """
    @abstractmethod
    def embed(self, message: str, **kwargs) -> (str, dict):
        """
        Embeds the directive's instructions in the message.

        :return: Tuple (str, dict) of the embedded message and an info dict
        """
        pass

    @abstractmethod
    def parse(self, response: str,  **kwargs) -> (str, dict):
        """
        Parses the response from the message in the context of the directive.

        :return: Tuple (str, dict) of the parsed message and an info dict
        """
        pass

    def __str__(self):
        return self.__class__.__name__

    def __repr__(self):
        return self.__str__()
