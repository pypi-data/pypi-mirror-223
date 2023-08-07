from typing import Sequence

from lobsang.llms.base import LLM
from lobsang.messages import Message


class FakeLLM(LLM):
    """
    A fake LLM that just returns a dummy response.
    Can be used for testing.
    """
    def chat(self, messages: Sequence[Message]) -> (str, dict):
        """
        Wraps the provided messages in a dummy response.
        For example, the message 'hello' will be responded to with 'DUMMY RESPONSE for 'hello''.
        """
        return f"DUMMY RESPONSE for '{messages[-1].text}'", {}
