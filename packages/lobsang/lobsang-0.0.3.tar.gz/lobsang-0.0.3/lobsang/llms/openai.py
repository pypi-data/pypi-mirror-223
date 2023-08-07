from typing import Sequence

from openai import ChatCompletion

from lobsang.llms.base import LLM
from lobsang.messages import Message


class OpenAI(LLM):
    """Wrapper for OpenAI API"""

    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo", **kwargs):
        """
        Initialize OpenAI API wrapper.

        Wraps the ChatCompletion API:
        https://github.com/openai/openai-python/blob/main/openai/api_resources/chat_completion.py

        Supported kwargs:
        See https://platform.openai.com/docs/api-reference/chat/create for a list of valid parameters.

        :param api_key: OpenAI API key
        :param model: OpenAI model
        :param kwargs: Additional arguments (See above)
        """
        assert api_key is not None, "OpenAI API key is required."
        assert model is not None, "OpenAI model is required."

        self.args = {'model': model, 'api_key': api_key, **kwargs}

    def chat(self, messages: Sequence[Message], **kwargs) -> (str, dict):
        # Prepare messages
        messages = [{"role": m.role, "content": m.text} for m in messages]

        # Override kwargs locally
        params = self.args | kwargs

        # Call OpenAI API
        response = ChatCompletion.create(messages=messages, **params)

        return response.choices[0].message.content, {}
