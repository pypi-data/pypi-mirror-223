import textwrap
from abc import ABC, abstractmethod


class Directive(ABC):
    """
    Abstract class for directives.
    """
    instructions = None

    def __init__(self, instructions: str = None):
        """
        Initializes the directive (with the provided instructions, if any).

        :param instructions: The instructions to be used in the directive (optional).
        """
        self.instructions = instructions or self.instructions
        assert isinstance(self.instructions, str), "Instructions must be a string"

    def _info(self, original: str, **kwargs):
        """
        Creates an info dict with the original message/response, the directive and any additional arguments (kwargs).
        """
        return dict(original=original, directive=self, **kwargs)

    def embed(self, message: str, **kwargs) -> (str, dict):
        """
        Embeds the directive's instructions in the message. This also dedents the instructions to remove the
        indentation of the multiline string.

        :param message: The message to embed the instructions in.
        :param kwargs: Additional arguments to be used in the instructions.
        :return: Tuple (str, dict) of the embedded message and an info dict
        """
        dedented = textwrap.dedent(self.instructions)
        formatted = dedented.format(message=message, **kwargs)
        return formatted, self._info(message, **kwargs)

    @abstractmethod
    def parse(self, response: str, **kwargs) -> (str, dict):
        """
        Parses the response from the message in the context of the directive.

        :param response: The response to parse.
        :param kwargs: Additional arguments to be used in the parsing.
        :return: Tuple (str, dict) of the parsed message and an info dict
        """
        pass

    def __str__(self):
        return self.__class__.__name__

    def __repr__(self):
        return self.__str__()
