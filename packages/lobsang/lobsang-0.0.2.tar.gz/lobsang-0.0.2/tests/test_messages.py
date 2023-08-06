from lobsang.messages import Message, SystemMessage, UserMessage, AssistantMessage, Role


def test_role_enum():
    """
    Test the Role enum.
    """
    assert issubclass(Role, str), "Role should be a subclass of str."
    assert len(Role) == 3, "There should be exactly three roles: system, user, and assistant."

    # Ensure that the keys are the same as the values
    assert Role.SYSTEM == Role("system") == "system"
    assert Role.USER == Role("user") == "user"
    assert Role.ASSISTANT == Role("assistant") == "assistant"


def test_messages():
    """
    Test the Message class and its subclasses.
    """

    system_message = SystemMessage(text="Hello World")
    user_message = UserMessage(text="Hello World")
    assistant_message = AssistantMessage(text="Hello World")

    # Ensure that the roles are correct
    assert system_message.role == Role.SYSTEM, "SystemMessage should have role Role.SYSTEM."
    assert user_message.role == Role.USER, "UserMessage should have role Role.USER."
    assert assistant_message.role == Role.ASSISTANT, "AssistantMessage should have role Role.ASSISTANT."

    # Ensure inheritance is correct
    assert isinstance(system_message, Message), "SystemMessage should be an instance of Message."
    assert isinstance(user_message, Message), "UserMessage should be an instance of Message."
    assert isinstance(assistant_message, Message), "AssistantMessage should be an instance of Message."