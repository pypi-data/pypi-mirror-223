import pytest
from lobsang.directives import Directive, TextDirective


def test_text_directive():
    """
    Test the TextDirective.
    """
    _input = "Hello, world!"
    text_directive = TextDirective()

    assert isinstance(text_directive, Directive)

    # Test embed method
    message, info = text_directive.embed(_input)
    assert message == _input
    assert info == {}

    # Test parse method
    message, info = text_directive.parse(_input)
    assert message == _input
    assert info == {}
