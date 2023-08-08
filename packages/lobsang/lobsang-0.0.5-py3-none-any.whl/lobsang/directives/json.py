import ast
import json
import re

import jsonschema
from jsonschema.validators import validator_for, validate

from lobsang.directives.base import Directive


class JSONDirective(Directive):
    """
    A directive that appends instructions to generate a JSON object (with the provided schema) to the message.
    And implements a parse method that tries to parse the response to a JSON object (returned in the info dict as 'json')
    """
    instructions = """\
    {message}
    
    Create a JSON object with the following schema:
    ```json
    {schema}
    ```"""

    def __init__(self, schema: dict, prune=True, instructions: str = None):
        """
        Initializes the JSONDirective with the provided schema.

        **Note:** Replacing the original response helps to keep a clean chat history, hinting that
         i.e. any
        text around the JSON from the original response will be removed.

        :param schema: The schema used to parse the data. It should be a valid JSON schema.
        :param prune: If True, the response will be pruned to the parsed JSON object, i.e. text around the JSON will be
        removed. If False, the response will be returned as-is.
        :param instructions: Instructions to override the default instructions (optional).
        """
        super().__init__(instructions=instructions)

        self.schema = schema
        self.prune = prune
        self.validator = validator_for(schema)

        # Validate schema
        self.validator.check_schema(schema)

    def embed(self, message: str, **kwargs) -> (str, dict):
        """
        Appends instructions to generate a JSON object (with the provided schema) to the message.
        """
        return super().embed(message, schema=self.schema, **kwargs)

    @staticmethod
    def extract(message: str):
        """
        Try to extract content of a JSON block from a message.

        :param message: The message to extract the JSON block from.
        :return: The content of the JSON block or None if no JSON block was found.
        """
        pattern = r'```json\s*(.*?)\s*```'
        match = re.search(pattern=pattern, string=message, flags=re.DOTALL)

        return match.group(1) if match else None

    def parse(self, res: str, **kwargs) -> (str, dict):
        """
        Parses the response to a JSON object (returned in the info dict as 'json').
        If prune is `True` (default) , the response will be pruned to the parsed JSON object, i.e. text around the
        JSON will be removed. If prune is `False`, the response will be returned as-is, i.e, res == parsed_res.

        **Note:** If any error occurs, the response will always be returned as-is (no matter if prune is `True` or
        `False`) and an error message will be returned in the info dict as 'error'.

        :param res: The response to parse.
        :return: The (parsed) response and an info dict with 'json' containing the parsed JSON object or `None` if
        parsing failed and 'error' containing the error message or `None` if no error occurred plus additional
        information.
        """
        info = self._info(res, json=None, error=None, schema=self.schema)

        # Try to extract JSON block
        json_block = self.extract(res)

        # Stop early if no JSON block was found
        if not json_block:
            return res, info | {"error": "No JSON block found.", **kwargs}

        # Try to parse JSON block
        try:
            # We use ast instead of json because ast is less strict (e.g. allows single quotes)
            json_object = json.loads(json_block)
        except json.JSONDecodeError as e:
            return res, info | {"error": f"Not valid JSON. Decode Error: {e}", **kwargs}

        # Validate JSON object
        try:
            validate(json_object, schema=self.schema)
        except jsonschema.exceptions.ValidationError as e:
            return res, info | {"error": f"Does not match schema. Schema Error: {e}", **kwargs}

        # If we get here, the JSON object is valid, so we return it
        info = info | {"json": json_object, **kwargs}
        if self.prune:
            json_str = json.dumps(json_object, indent=4)
            return f"```json\n{json_str}\n```", info
        else:
            return res, info

    @classmethod
    def from_file(cls, path: str, **kwargs):
        """
        Creates a new JSONDirective from a JSON schema file.

        :param path: The path to the JSON schema file.
        :return: A new instance of the JSONDirective.
        :raises: FileNotFoundError if the schema file does not exist.
        :raises: jsonschema.exceptions.SchemaError if the schema is invalid.
        """
        with open(path) as schema_file:
            schema = json.load(schema_file)

        return cls(schema=schema, **kwargs)
