from lobsang.directives.base import Directive


class TextDirective(Directive):
    """
    The text directive. Neither changes the message nor the response but is required to comply with the directive
    interface of lobsang.

    This is the default directive in lobsang. Use it if you want a plain text response from the LLM.
    It does not change the corresponding user message (i.e. the message just before the directive in the chat).
    """
    instructions = "{message}"

    def parse(self, response: str, **kwargs) -> (str, dict):
        """
        No parsing is required for the text directive.

        :param response: The response from the LLM. Will not be changed by the text directive.
        :return: Tuple (str, dict). The response as-is and dict with additional info.
        """
        return response, self._info(response, **kwargs)
