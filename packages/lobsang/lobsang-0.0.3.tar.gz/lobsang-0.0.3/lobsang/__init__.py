"""
Lobsang provides a simple interaction interface with a dialog-based LLM.
Please see the README for more information.

https://thelongearth.fandom.com/wiki/Lobsang
"""

import importlib.metadata

__version__ = importlib.metadata.version('lobsang')
__all__ = ["Chat", "LLM", "FakeLLM", "OpenAI", "Message", "SystemMessage", "UserMessage", "AssistantMessage"]

from lobsang.chat import Chat
from lobsang.llms import LLM, FakeLLM, OpenAI
from lobsang.messages import Message, SystemMessage, UserMessage, AssistantMessage