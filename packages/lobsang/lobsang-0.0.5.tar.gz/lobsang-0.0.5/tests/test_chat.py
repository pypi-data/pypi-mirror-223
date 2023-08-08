import pytest

from lobsang import Chat, SystemMessage, UserMessage, AssistantMessage
from lobsang.directives import Directive, TextDirective
from lobsang.llms.fake import FakeLLM


class TestDirective(Directive):
    """
    Dummy directive for testing.
    """
    instructions = "embed {message}"

    def parse(self, response: str, **kwargs) -> (str, dict):
        return f"parse {response}", self._info(response, **kwargs)


class TestLLM(FakeLLM):
    """
    Intercepts messages and stores them in a list.
    """
    messages = None

    def chat(self, messages):
        self.messages = messages
        return super().chat(messages)


@pytest.fixture
def chat():
    return Chat(llm=FakeLLM())


def test_init():
    """
    Test __init__ method.
    """
    # Test default
    chat = Chat()
    assert chat.system_message == SystemMessage("You are a helpful assistant.")
    assert chat.llm is None

    # Test with arguments
    messages = [UserMessage("My name is Bark Twain"), AssistantMessage("Nice to meet you, Bark Twain!")]
    chat = Chat(messages, system_message="This is a test.", llm=FakeLLM())
    assert chat == messages
    assert len(chat) == len(messages)
    assert chat.system_message == SystemMessage("This is a test.")
    assert isinstance(chat.llm, FakeLLM)

    # Test with invalid arguments
    with pytest.raises(AssertionError):
        Chat(1)
    with pytest.raises(AssertionError):
        Chat([1, 2, 3])
    with pytest.raises(AssertionError):
        Chat(system_message=1)
    with pytest.raises(AssertionError):
        Chat(system_message=UserMessage("This should fail."))


def test_call(chat):
    """
    Test __call__ method.

    Only test for __call__ specific behavior. Other tests are covered by test_run.
    """
    res = chat("My name is Bark Twain.")
    assert len(chat) == 2, "Expected 2 messages in total."
    assert isinstance(res, AssistantMessage), "Expected AssistantMessage as return value."

    res = chat(UserMessage("I am a dog."))
    assert len(chat) == 4, "Expected 4 messages in total."
    assert isinstance(res, AssistantMessage), "Expected AssistantMessage as return value."

    # Use with 'append' flag (default is True).
    chat.clear()
    assert len(chat) == 0, "Expected 0 messages in total."
    res = chat("My name is Bark Twain.", append=False)
    assert len(chat) == 0, "Should not have appended anything."
    assert isinstance(res, AssistantMessage), "Expected AssistantMessage as return value."

    # Expect to fail
    with pytest.raises(AssertionError):
        chat(1)
    with pytest.raises(AssertionError):
        chat([1, 2, 3])
    with pytest.raises(AssertionError):
        chat(["My name is Bark Twain."])
    with pytest.raises(AssertionError):
        chat([UserMessage("My name is Bark Twain.")])


def test_run(chat):
    """
    Test run method.
    """
    # Expect AssertionError if chat has no valid llm.
    llm = chat.llm
    chat.llm = None
    with pytest.raises(AssertionError):
        chat.run(["My name is Bark Twain."])
    chat.llm = "This is not a valid llm."
    with pytest.raises(AssertionError):
        chat.run(["My name is Bark Twain."])
    chat.llm = llm

    # Expect AssertionError if input is not a 'Sequence[str | Message | Directive]' or empty.
    with pytest.raises(AssertionError):
        chat.run(1)
    with pytest.raises(AssertionError):
        chat.run([1, 2, 3])
    with pytest.raises(AssertionError):
        chat.run(["My name is Bark Twain.", 1])
    with pytest.raises(AssertionError):
        chat.run([])

    # Expect AssertionError if system_message is not a str or SystemMessage.
    with pytest.raises(AssertionError):
        chat.run(["My name is Bark Twain."], system_message=1)
    with pytest.raises(AssertionError):
        chat.run(["My name is Bark Twain."], system_message=UserMessage("This should fail."))
    with pytest.raises(AssertionError):
        chat.run(["My name is Bark Twain."], system_message=AssistantMessage("This should fail."))

    # Test if 'append' flag works and if system message is passed down to llm.
    llm = chat.llm
    chat.llm = TestLLM()
    chat.run(["My name is Bark Twain."], append=False)
    assert chat.llm.messages[0] == SystemMessage("You are a helpful assistant."), \
        "Expected default system message to be passed down to llm as first message."
    chat.run(["My name is Bark Twain."], append=False, system_message="This is a test.")
    assert chat.llm.messages[0] == SystemMessage("This is a test."), \
        "Expected custom system message to be passed down to llm as first message."
    assert len(chat) == 0, "Should not have appended anything."
    chat.llm = llm
    assert isinstance(chat.llm, FakeLLM)

    # Test if messages are appended to chat (default behavior).
    chat.clear()
    assert len(chat) == 0, "Expected 0 messages in total."
    chat.run(["My name is Bark Twain.", "I am a dog."])
    assert len(chat) == 4, "Expected 4 messages in total."
    assert chat[0].text == 'My name is Bark Twain.', "Expected user message to be unchanged."

    # Test return value.
    chat.clear()
    res = chat.run(["My name is Bark Twain.", "I am a dog."])
    assert len(chat) == 4, "Expected 4 messages in total."
    assert all(isinstance(m, UserMessage) for i, m in enumerate(res) if i % 2 == 0), \
        "Expected UserMessage at even indices, e.g. first message should be a user message."
    assert all(isinstance(m, AssistantMessage) for i, m in enumerate(res) if i % 2 == 1), \
        "Expected AssistantMessage at odd indices, i.e. as responses to user messages (even indices)."

    # Test return value with already resolved messages as input.
    chat.clear()
    messages = [UserMessage("My name is Bark Twain."), AssistantMessage("Nice to meet you, Bark Twain!")] * 2
    res = chat.run(messages)
    assert len(chat) == 4, "Expected 2 messages in total."
    assert res == messages, "Expected return value to be the same as input."

    # Test chat with directive.
    chat.clear()
    res = chat.run(["My name is Rex", TextDirective(), UserMessage("I am a dog."), TextDirective()])
    assert len(res) == 4, "Expected 4 messages in total."
    assert res[0].text == "My name is Rex", "Expected user message to be unchanged."
    assert isinstance(res[1], AssistantMessage), "Expected AssistantMessage as return value."
    assert res[2].text == "I am a dog.", "Expected user message to be unchanged."
    assert isinstance(res[3], AssistantMessage), "Expected AssistantMessage as return value."


def test_interpolate(chat):
    """
    Test _interpolate method.
    """
    # Test if interpolation works.
    sequence = [
        UserMessage("My name is Bark Twain."),
        AssistantMessage("Nice to meet you, Bark Twain!"),
        UserMessage("I am a dog."),
        TestDirective(),
        UserMessage("I am a dog."),
        UserMessage("I am a dog.")
    ]
    res = chat._interpolate(sequence, default_directive=TestDirective())
    assert res[:5] == sequence[:5], "Expected first 5 messages to be unchanged."
    assert len(res) == 8, "Expected 8 messages in total."
    assert isinstance(res[5], TestDirective), "Expected Directive at index 5."
    assert isinstance(res[7], TestDirective), "Expected Directive at index 7."

    # Test if interpolation works with other default directive.
    chat._interpolate(sequence, default_directive=TextDirective())
    assert isinstance(res[5], TestDirective), "Expected Directive at index 5."
    assert isinstance(res[7], TestDirective), "Expected Directive at index 7."

    # Expect fail
    with pytest.raises(AssertionError):
        chat._interpolate(1)
    with pytest.raises(AssertionError):
        chat._interpolate([1, 2, 3])
    with pytest.raises(AssertionError):
        chat._interpolate(["My name is Bark Twain.", 1])
    with pytest.raises(AssertionError):
        chat._interpolate([])


def test_invoke_with_directive(chat):
    """
    Test _invoke_with_directive method.
    """
    # Use TestLLM to test if messages are passed down correctly.
    chat.llm = TestLLM()

    # Add messages to chat (the context for the test)
    chat.append(UserMessage("My name is Bark Twain."))

    # Create a message, embed it, and parse it with the test directive.
    res = chat._invoke_with_directive(TextDirective(), context=chat)
    assert isinstance(res, AssistantMessage), "Expected AssistantMessage as return value."
    assert isinstance(res.info["directive"], TextDirective), "Expected TextDirective to added to info."
    assert chat.llm.messages[0] == SystemMessage("You are a helpful assistant."), \
        "Expected default system message to be passed down to llm as first message."

    # Test if directive is applied correctly
    chat[0] = UserMessage("My name is Rex.")
    res = chat._invoke_with_directive(TestDirective(), context=chat)
    assert chat[0].text == "embed My name is Rex.", "Expected message to be embedded."
    assert chat[0].info["original"] == "My name is Rex.", "Expected original message to be passed down to info."
    assert res.text == "parse DUMMY RESPONSE for 'embed My name is Rex.'", "Expected message to be unchanged."
    assert res.info["original"] == "DUMMY RESPONSE for 'embed My name is Rex.'", \
        "Expected original message to be passed down to info."
    assert isinstance(res.info["directive"], TestDirective), "Expected TestDirective to added to info."

    # Test if system message is passed down correctly.
    chat._invoke_with_directive(TextDirective(), context=chat, system_message="This should be passed down.")
    assert chat.llm.messages[0] == SystemMessage("This should be passed down."), \
        "Expected custom system message to be passed down to llm as first message."


def test_setitem(chat):
    """
    Test modified __setitem__ method.
    """
    # Add some messages to the chat
    chat.run(["My name is Bark Twain.", "I am a dog.", "What is your name?", "How old are you?"])

    # Test index
    message = UserMessage("This should work.")
    chat[0] = message
    assert chat[0] is message, "UserMessage not set correctly."

    # Works but not encouraged, validate would fail here bc we only want UserMessages and AssistantMessages in the chat
    message = SystemMessage("This should also work.")
    chat[-1] = message
    assert chat[-1] is message, "Message not set correctly."

    # Test slice
    messages = [UserMessage("Message 1 in slice"), UserMessage("Message 2 in slice")]
    chat[1:3] = messages
    assert chat[1:3] == messages, "Messages not set correctly."

    # Expected to fail
    with pytest.raises(AssertionError):
        chat[0] = "This should fail."
    with pytest.raises(IndexError):
        chat[100] = UserMessage("This should fail.")
    with pytest.raises(IndexError):
        chat[-100] = UserMessage("This should also fail.")
    with pytest.raises(AssertionError):
        chat[0] = [UserMessage("This should fail too.")]


def test_getitem(chat):
    """
    Test modified __getitem__ method.
    """
    # Add some messages to the chat
    messages = [
        UserMessage("My name is Bark Twain."),
        AssistantMessage("Nice to meet you, Bark Twain!"),
        UserMessage("I am a dog."),
        AssistantMessage("I am a virtual assistant."),
        UserMessage("What is your name?"),
        AssistantMessage("I don't have a name."),
    ]
    chat.extend(messages)

    # Test index
    for i, message in enumerate(chat):
        assert chat[i] is message, "Message not retrieved correctly."

    # Test slice
    sliced_chat = chat[:3]
    assert sliced_chat == messages[:3], "Messages not retrieved correctly."
    assert isinstance(sliced_chat, Chat), "Expected sliced chat to be a Chat object."
    assert len(sliced_chat) == 3, "Expected 3 messages in sliced chat."

    sliced_chat2 = chat[1:3:2]
    assert sliced_chat2 == messages[1:3:2], "Messages not retrieved correctly."
    assert isinstance(sliced_chat2, Chat), "Expected sliced chat to be a Chat object."
    assert len(sliced_chat2) == 1, "Expected 1 message in sliced chat."

    sliced_chat3 = chat[1:-2]
    assert sliced_chat3 == messages[1:-2], "Messages not retrieved correctly."
    assert isinstance(sliced_chat3, Chat), "Expected sliced chat to be a Chat object."
    assert len(sliced_chat3) == 3, "Expected 3 messages in sliced chat."


def test_not_implemented(chat):
    """
    Ensures that all methods that are explicitly not implemented raise a NotImplementedError.
    """
    with pytest.raises(NotImplementedError):
        chat.sort()
    with pytest.raises(NotImplementedError):
        chat.__add__([])
    with pytest.raises(NotImplementedError):
        chat.__radd__([])


def test_append(chat):
    """
    Test modified append method.
    """
    message = UserMessage("This should work.")
    chat.append(message)
    assert chat[0] is message, "Message not appended correctly."

    with pytest.raises(AssertionError):
        chat.append("This should fail.")


def test_extend(chat):
    """
    Test modified extend method.
    """
    messages = [UserMessage("My name is Bark Twain."), AssistantMessage("Hello, Bark Twain.")]
    chat.extend(messages)
    assert len(chat) == 2, "Messages not extended correctly."
    assert chat == messages, "Messages not extended correctly."

    with pytest.raises(AssertionError):
        chat.extend("This should fail.")

    with pytest.raises(AssertionError):
        chat.extend(["This should also fail."])


def test_insert(chat):
    """
    Test modified insert method.
    """
    test_message = UserMessage("This should work.")

    # Add some messages to the chat
    chat.run(["My name is Bark Twain.", "I am a dog.", "What is your name?", "How old are you?"])

    # Insert a message at the beginning of the cha
    chat.insert(0, test_message)
    assert chat[0].text == test_message.text, "Message not inserted correctly."

    # Insert a message in the middle of the chat
    chat.insert(4, test_message)
    assert chat[4].text == test_message.text, "Message not inserted correctly."

    # Insert a message at the end of the chat
    chat.insert(len(chat), test_message)
    assert chat[-1].text == test_message.text, "Message not inserted correctly."

    # Expected to fail
    with pytest.raises(AssertionError):
        chat.insert(0, "This should fail.")


def test_len(chat):
    """
    Test __len__ method.
    """
    assert len(chat) == 0, "Chat length not calculated correctly."

    # Add some messages to the chat
    chat.run(["My name is Bark Twain.", "I am a dog.", "What is your name?", "How old are you?"])
    assert len(chat) == 8, "Chat length not calculated correctly."

    chat.clear()
    chat.extend([UserMessage("My name is Bark Twain."), AssistantMessage("Hello, Bark Twain.")])
    assert len(chat) == 2, "Chat length not calculated correctly."


def test_iter(chat):
    """
    Test __iter__ method.
    """
    # Add some messages to the chat
    chat.run(["My name is Bark Twain.", "I am a dog.", "What is your name?", "How old are you?"])

    for idx, message in enumerate(chat):
        assert message is chat[idx], "Message not iterated correctly."


def test_copy(chat):
    """
    Test copy method.
    """
    # Add some messages to the chat
    chat.run(["My name is Bark Twain.", "I am a dog.", "What is your name?", "How old are you?"])

    chat_copy = chat.copy()
    assert chat == chat_copy, "Chat not copied correctly."

    # Test that chat_copy is not a deepcopy of chat
    chat_copy[0].text = "This should change."
    assert chat[0].text == chat_copy[0].text, "Chat not copied correctly."


def test_validate(chat):
    """
    Test validate method.

    **Note:** It is not possible to test the validate method for all possible invalid cases. However, this test
    covers a broad range of cases and should be sufficient. Famous last words...
    """
    assert chat.validate(), "Chat not validated correctly."

    # Add some messages to the chat
    chat.run(["My name is Bark Twain.", "I am a dog.", "What is your name?", "How old are you?"])

    # Should still be valid
    assert chat.validate(), "Chat not validated correctly."

    # Replace a user message or assistant message with a system message is invalid
    chat[0] = SystemMessage("This should fail.")  # 👈 Replacing a user message with a system message is invalid
    chat[1] = SystemMessage("This should fail.")  # 👈 Replacing an assistant message with a system message is invalid
    with pytest.raises(ValueError):
        chat.validate()
    chat.pop(0)
    with pytest.raises(ValueError):
        chat.validate()
    chat.pop(0)
    assert chat.validate(), "Chat not validated correctly."

    # Replace a user message with assistant message and vice versa is invalid
    chat[0] = AssistantMessage("This should fail.")  # 👈 Replacing a user message with an assistant message is invalid
    chat[1] = UserMessage("This should fail.")  # 👈 Replacing an assistant message with a user message is invalid
    with pytest.raises(ValueError):
        chat.validate()
    chat.pop(0)
    with pytest.raises(ValueError):
        chat.validate()
    chat.pop(0)
    assert chat.validate(), "Chat not validated correctly."

    # Test inserting messages corrupting the alternating user/assistant pattern of chat
    # 1. Add an assistant message at the beginning of the chat (any message type but UserMessage is invalid)
    chat.insert(0, AssistantMessage("This should fail."))  # 👈 Anything but a user message at the beginning is invalid
    with pytest.raises(ValueError):
        chat.validate()
    chat.pop(0)
    assert chat.validate(), "Chat not validated correctly."

    # 2. Add an assistant message to the middle of the chat
    chat.insert(2, AssistantMessage("This should fail."))  # 👈 Corrupts pattern
    with pytest.raises(ValueError):
        chat.validate()
    chat.pop(2)
    assert chat.validate(), "Chat not validated correctly."

    # 3. Add a user message to the end of the chat
    chat.append(UserMessage("This should fail."))  # 👈 A trailing user message w/o a response is invalid
    with pytest.raises(ValueError):
        chat.validate()
    chat.pop()
    assert chat.validate(), "Chat not validated correctly."
