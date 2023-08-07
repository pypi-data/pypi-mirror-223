"""
This module contains Chat class, which is a subclass of list
and can be used to manage a conversation with a LLM.
"""

from collections.abc import Sequence
from typing import SupportsIndex

from lobsang.directives import Directive, TextDirective
from lobsang.llms.base import LLM
from lobsang.messages import Message, SystemMessage, UserMessage, AssistantMessage


class Chat(list[Message]):
    """
    A chat (subclass of list) holds a conversation between a user and an assistant which can be called with one or
    more messages, i.e. `chat(message)` or `chat([message1, message2, ...])`.

    **Disclaimer:** Not all methods of list were re-implemented, so some might not work as expected. If you need a
    specific method, please open an issue or make a pull request on GitHub. Thanks! 🙏
    """

    def __init__(self, seq: Sequence[Message] = (),
                 system_message: str | SystemMessage = "You are a helpful assistant.", llm: LLM = None) -> None:
        """
        Creates a new chat instance.

        :param seq: A sequence of messages to initialize the chat with.
        :param llm: The language model to use.
        """
        assert isinstance(seq, Sequence), f"Expected 'Sequence' but got {type(seq)} for 'seq'."
        assert all(isinstance(m, Message) for m in seq), f"Found non-Message element in 'seq'."
        assert isinstance(system_message, (str, SystemMessage)), \
            f"Expected 'str' or 'SystemMessage' but got {type(system_message)}."

        # Convert system_message to SystemMessage if necessary
        if isinstance(system_message, str):
            system_message = SystemMessage(system_message)

        # Set attributes
        super().__init__(seq)
        self.system_message = system_message
        self.llm = llm

    def __call__(self, msg: str | UserMessage, append: bool = True,
                 system_message: str | SystemMessage = None) -> AssistantMessage:
        """
        Convenience wrapper for `Chat.run()` to be able to call chat with a single message, i.e. `chat(message)`.
        Returns the response from the LLM. Internally simply calls `chat.run([message])`. See `Chat.run()` for more
        information.

        >>> from lobsang.llms import FakeLLM
        >>> chat = Chat(llm=FakeLLM())
        >>> res = chat("My name is Bark Twain")  # 👈 Internally converted to UserMessage for convenience
        >>> chat == res
        True
        >>> str(chat[-1])
        "ASSISTANT: DUMMY RESPONSE for 'My name is Bark Twain'"

        :param msg: The message to send to the LLM.
        :param append: Whether to append the conversation to the chat history.
        :param system_message: The system message to use. If None, the chat's system message is used.
        :return: The response from the LLM.
        """
        assert isinstance(msg, (str, UserMessage)), f"Expected 'str' or 'UserMessage' but got {type(msg)} for 'msg'."

        res = self.run([msg], append=append, system_message=system_message)[-1]
        assert isinstance(res, AssistantMessage), f"Expected 'AssistantMessage' but got {type(res)} for 'res'."

        return res

    def run(self, seq: Sequence[str | Message | Directive], append: bool = True,
            system_message: str | SystemMessage = None) -> list[Message]:
        """
        Calls the chat with a seq of messages and directives, i.e. `chat([user_msg, directive, ...])`.
        Returns the conversation with all messages and corresponding responses from the LLM.

        **Note:** All messages of type `str` will be implicitly converted to `UserMessage` for convenience.

        :param seq: The messages and directives to send to the LLM.
        :param append: Whether to append the conversation to the chat history.
        :param system_message: The system message to use. If None, the chat's system message is used.
        :return: The conversation with all messages and corresponding responses from the LLM.
        :raises TypeError: If data is not of correct type (see note above).
        """
        assert isinstance(seq, Sequence), f"Expected 'Sequence' but got {type(seq)} for 'seq'."
        assert len(seq) > 0, "Expected non-empty sequence for 'seq'."
        assert all(isinstance(m, (str, Message, Directive)) for m in seq), \
            "Expected only 'str', 'Message' or 'Directive' as elements of 'seq'."
        assert isinstance(self.llm, LLM), "Expected 'LLM' but got {type(self.llm)} for 'self.llm'."

        # Check if system_message is set and convert to SystemMessage if necessary
        system_message = system_message or self.system_message
        system_message = SystemMessage(system_message) if isinstance(system_message, str) else system_message
        assert isinstance(system_message, SystemMessage), \
            f"Expected 'str' or 'SystemMessage' but got {type(system_message)} for 'system_message'."

        # Convert strings to UserMessages
        seq = [UserMessage(m) if isinstance(m, str) else m for m in seq]

        # Interpolate messages (add default directives [TextDirective] after messages if necessary)
        seq = self._interpolate(seq)

        # Loop through data and invoke LLM
        conversation = []
        for elem in seq:
            if isinstance(elem, Message):
                conversation.append(elem)
            elif isinstance(elem, Directive):
                assistant_message = self._invoke_with_directive(directive=elem, context=[*self, *conversation],
                                                                system_message=system_message)
                conversation.append(assistant_message)
            else:
                raise NotImplementedError(f"Cannot handle {type(elem)}. "
                                          f"Only Message and Directive are supported for now.")

        # If flag is set, append conversation to chat
        if append:
            self.extend(conversation)

        return conversation

    @staticmethod
    def _interpolate(seq: Sequence[Message | Directive], default_directive=TextDirective()) -> list[Message]:
        """
        Interpolates the provided sequence with default directives (TextDirective) if necessary.

        **Details:** For convenience, we do not require a directive after each unanswered message, i.e. this is fine:
        `[user_msg, user_msg, directive, user_msg]`. However, the LLM is called on directives and not on messages. So we
        need a corresponding directive for each message. This is done by inserting the provided default directive after
        each user message if it is directly followed by another user message.

        **Example:** `[user_msg, user_msg, directive, user_msg]` is interpolated to `[user_msg, TextDirective, user_msg,
        directive, user_msg, TextDirective]`, i.e. 2 TextDirectives are inserted.

        :param seq: The sequence to interpolate.
        :param default_directive: The default directive to interpolate with.
        :return: The interpolated sequence.
        """
        assert isinstance(seq, Sequence), f"Expected 'Sequence' but got {type(seq)} for 'seq'."
        assert len(seq) > 0, "Expected non-empty sequence for 'seq'."
        assert all(isinstance(item, (Message, Directive)) for item in seq), \
            "Expected only 'Message' or 'Directive' as elements of 'seq'."
        assert isinstance(default_directive, Directive), \
            f"Expected 'Directive' but got {type(default_directive)} for 'default_directive'."

        # Split sequence into head and last item to avoid IndexError
        *head, last = seq
        interpolated = []

        # Loop through head and add items to interpolated if necessary
        for idx, elem in enumerate(head):
            interpolated.append(elem)

            # When two user messages directly follow each other, add a TextDirective
            if isinstance(elem, UserMessage) and isinstance(seq[idx + 1], UserMessage):
                interpolated.append(default_directive)

        # Append last item and, if necessary, a TextDirective
        interpolated.append(last)
        if isinstance(last, UserMessage):
            interpolated.append(default_directive)

        return interpolated

    def _invoke_with_directive(self, directive: Directive, context: Sequence[Message],
                               system_message: str | SystemMessage = None) -> AssistantMessage:
        """
        Invokes the LLM with a directive.

        **Details:** The directive is applied to the last message in the context (embeds the directive's instructions
        into the message). The LLM then processes all together (system message, context, directive) and returns the
        response which is parsed using the directive and returned as an AssistantMessage.

        :param directive: The directive to invoke the LLM with.
        :param context: The context to invoke the LLM with, i.e. a sequence of messages
        :param system_message: The system message to use. If None, the chat's system message is used.
        :return: The response from the LLM as an AssistantMessage.
        """
        assert isinstance(directive, Directive), f"Expected 'Directive' but got {type(directive)} for 'directive'."
        assert isinstance(context, Sequence), f"Expected 'Sequence' but got {type(context)} for 'context'."
        assert len(context) > 0, "Expected non-empty sequence for 'context'."
        assert all(isinstance(m, Message) for m in context), "Expected only 'Message' as elements of 'context'."

        # Check if system_message is set and convert to SystemMessage if necessary
        system_message = system_message or self.system_message
        system_message = SystemMessage(system_message) if isinstance(system_message, str) else system_message
        assert isinstance(system_message, SystemMessage), \
            f"Expected 'str' or 'SystemMessage' but got {type(system_message)} for 'system_message'."

        # Embed directive's instructions into query (i.e. last message in context)
        query = context[-1]
        query.text, directive_info = directive.embed(query.text)
        query.info.update(directive_info)

        # Invoke LLM with system message and context
        system_message = system_message or self.system_message
        response, llm_info = self.llm.chat([system_message, *context])

        # Parse response
        parsed_response, directive_info = directive.parse(response)

        # Create and return assistant message
        assistant_info = llm_info | directive_info
        assistant_message = AssistantMessage(parsed_response, info=assistant_info)
        return assistant_message

    def __setitem__(self, idx: SupportsIndex, item) -> None:
        """
        Sets an item at a given index in the chat.

        :param idx: The index to set the message at.
        :param item: The message to set.
        """
        # If item is a slice, check if all items are messages
        if isinstance(idx, slice):
            assert all(isinstance(msg, Message) for msg in item), \
                "Expected only 'Message' as elements of slice 'item'."
        else:
            assert isinstance(item, Message), f"Expected 'Message' but got {type(item)} for 'item'."

        super().__setitem__(idx, item)

    def __getitem__(self, item):
        """
        Gets an item from the chat.

        :param item: The item to get.
        :return: The item.
        """
        # If item is a slice, return a new chat with the sliced messages
        if isinstance(item, slice):
            return Chat(super().__getitem__(item), self.system_message, self.llm)
        else:
            return super().__getitem__(item)

    def __add__(self, other):
        # Not supported bc how to handle the system message and the LLM? 🤔
        raise NotImplementedError("Not supported. Use extend() instead.")

    def __radd__(self, other):
        # Not supported bc how to handle the system message and the LLM? 🤔
        raise NotImplementedError("Not supported. Use extend() instead.")

    def copy(self) -> "Chat":
        """
        Returns a shallow copy of the chat.

        :return: The shallow copy.
        """
        return Chat(self, self.system_message, self.llm)

    def append(self, msg: Message) -> None:
        """
        Appends a message to the chat.

        :param msg: The message to append.
        """
        assert isinstance(msg, Message), f"Expected 'Message' but got {type(msg)} for 'msg'."
        super().append(msg)

    def extend(self, seq: Sequence[Message]) -> None:
        """
        Extends the list by the given sequence of messages.

        :param seq: The sequence of messages to extend the list with.
        """
        assert isinstance(seq, Sequence), f"Expected 'Sequence' but got {type(seq)} for 'seq'."
        assert all(isinstance(m, Message) for m in seq), "Expected only 'Message' as elements of 'seq'."

        super().extend(seq)

    def insert(self, idx: SupportsIndex, msg: Message) -> None:
        """
        Inserts a message at a given index into the chat history.

        :param idx: The index to insert the message at.
        :param msg: The message to insert.
        """
        assert isinstance(msg, Message), f"Expected 'Message' but got {type(msg)} for 'msg'."
        super().insert(idx, msg)

    def sort(self, *args, **kwargs):
        # Not supported bc why the hell would you want to sort a chat? By what criterion? 🤔
        # If you try this, a magic wizard will appear and cast a spell on you to turn you into a frog
        raise NotImplementedError("🧙‍♂️ Thou shalt not sort a chat! Ribbit ribbit. 🐸")

    def validate(self):
        """
        Validates the chat, by checking if it is a sequence of alternating user and assistant messages, starting with a
        user message.

        **Examples:**
        - `[user_msg, assistant_msg, user_msg, assistant_msg]` would be valid.
        - `[user_msg, assistant_msg, user_msg]` would be invalid. (odd number of messages, missing assistant message)
        - `[assistant_msg, user_msg, assistant_msg, user_msg]` would be invalid. (not starting with user message)
        - `[user_msg, user_msg, assistant_msg, user_msg]` would be invalid. (two user messages in a row)

        :return: True if the chat is valid, otherwise raises a ValueError.
        :raises ValueError: If the chat is not valid.
        """
        if len(self) == 0:
            return True

        for i, message in enumerate(self):
            if i % 2 == 0 and not isinstance(message, UserMessage):
                raise ValueError(f"Expected a UserMessage at index {i}, but got {type(message)} instead.")
            elif i % 2 == 1 and not isinstance(message, AssistantMessage):
                raise ValueError(f"Expected a AssistantMessage at index {i}, but got {type(message)} instead.")

        # Check if the chat ends with an assistant message.
        if not isinstance(self[-1], AssistantMessage):
            raise ValueError("Chat is missing an assistant message at the end.")

        # If we got here, the chat is valid 🎉 Passing the loop above implies that the chat starts with a user message
        # and alternates between user and assistant messages. Finally, we checked that the chat ends with an assistant
        # message. Therefore, each user message is followed by an assistant message, and the chat is valid. QED.
        return True

    def __str__(self, sep='\n'):
        """
        Returns a string representation of the chat HISTORY.

        :param sep: The separator to use between messages.
        """
        return sep.join(map(str, self))

    def __repr__(self):
        """
        Returns a string representation of the chat OBJECT.
        """
        # Show only the first and last message if the chat is longer than 4 messages
        excerpt = f"[{self[0]}, ..., {self[-1]}]" if len(self) > 4 else list(map(str, self))

        return f"Chat(llm={self.llm.__class__.__name__ if isinstance(self.llm, LLM) else self.llm}, " \
               f"system_message='{self.system_message}', total_messages={len(self)}, messages={excerpt}"
