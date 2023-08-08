import textwrap

from lobsang.directives import Directive, TextDirective, JSONDirective


def test_text_directive():
    """
    Test the TextDirective.
    """
    message = "Hello, world!"
    text_directive = TextDirective()

    assert isinstance(text_directive, Directive)

    # Test embed method
    embedded, info = text_directive.embed(message)
    assert embedded == message
    assert info == {'directive': text_directive, 'original': message}

    # Test parse method
    embedded, info = text_directive.parse(message)
    assert embedded == message
    assert info == {'directive': text_directive, 'original': message}


def test_json_directive():
    """
    Test the JSONDirective
    """
    message = "Hello, world"
    schema = {
        'type': 'object',
        'title': 'Test',
        'properties': {
            'test': {
                'type': 'string',
                'description': 'The test string.'
            }
        }
    }
    json_directive = JSONDirective(schema=schema)

    assert isinstance(json_directive, Directive)

    # Test embed method
    embedded, info = json_directive.embed(message)
    formatted = textwrap.dedent(json_directive.instructions.format(message=message, schema=schema))
    assert embedded == formatted
    assert info == {'directive': json_directive, 'original': message, 'schema': schema}

    response = """
    This is some text around the JSON block.
    ```json
    {
        "test": "Hello, world"
    }
    ```
    This is some text after the JSON block.
    """

    # Test parse method
    parsed, info = json_directive.parse(response)
    assert parsed == '```json\n{\n    "test": "Hello, world"\n}\n```'
    assert info == {'directive': json_directive, 'original': response, 'schema': schema,
                    'json': {'test': 'Hello, world'}, 'error': None}

    # Test with prune disabled
    json_directive = JSONDirective(schema=schema, prune=False)
    parsed, info = json_directive.parse(response)
    assert parsed == response
    assert info == {'directive': json_directive, 'original': response, 'schema': schema,
                    'json': {'test': 'Hello, world'}, 'error': None}


def test_json_directive_error():
    """
    Test the JSONDirective with invalid inputs
    """
    schema = {
        'type': 'object',
        'title': 'Test',
        'properties': {
            'test': {
                'type': 'string',
                'description': 'The test string.'
            }
        }
    }
    json_directive = JSONDirective(schema=schema)

    # Test parse method with response w/o JSON block
    response = "This is some text without a JSON block."
    parsed, info = json_directive.parse(response)
    assert parsed == response
    assert info['error'] == 'No JSON block found.'

    # Parse error (here: invalid JSON bc of missing comma)
    response = """
    This is some text around the JSON block.
    ```json
    {
        "test": 123
        'test2': "Hello, world"
    }
    ```
    This is some text after the JSON block.
    """
    parsed, info = json_directive.parse(response)
    assert parsed == response
    assert info['error'] == "Not valid JSON. Decode Error: Expecting ',' delimiter: line 3 column 9 (char 30)"

    # Does not adhere to schema
    response = """
    This is some text around the JSON block.
    ```json
    {
        "test": 123
    }
    ```
    This is some text after the JSON block.
    """
    parsed, info = json_directive.parse(response)
    assert parsed == response
    assert info['error'].startswith("Does not match schema. Schema Error: 123 is not of type 'string'")