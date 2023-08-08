"""
This package contains the directives used to instruct the LLM.

A directive's scope is one user message, and it's corresponding response from the LLM.
The directive embeds a user message with instructions for the LLM to follow.
Once the LLM generated a response, the directive will parse the response according to the directive's context.

For example, a JSONDirective will embed specific instructions for the LLM to follow and to return a JSON response.
Since, the LLM only returns text, the JSONDirective will try to parse the response as JSON and return the result.
"""

from lobsang.directives.base import Directive
from lobsang.directives.text import TextDirective
from lobsang.directives.json import JSONDirective
