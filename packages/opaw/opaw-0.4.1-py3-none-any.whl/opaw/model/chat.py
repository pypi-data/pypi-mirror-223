import json
import openai
from opaw.model import bot


class ChatBot(bot.Bot):
    """
    https://platform.openai.com/docs/api-reference/chat
    """

    def __init__(self, model="gpt-3.5-turbo", messages=None):
        super().__init__(model, "chat")
        # conversation history
        self.messages = [] if messages is None else messages

    def create(self, prompt=None, **kargs):
        """
        Gets a response from bot
        :param prompt: get a response with messages (content)
        :param kargs: other args
        :return:
        """
        # default
        role = kargs["role"] if kargs.get("role") else "user"

        if prompt is not None:
            prompt = prompt if isinstance(prompt, str) else str(prompt)
            self.messages.append({"role": role, "content": prompt})

        request = {
            "model": self.model,
            "messages": self.messages,
            **kargs
        }

        self._history_req(self.messages[-1], kargs)
        response = openai.ChatCompletion.create(**request)

        # insert response message to the messages
        res_msg = self._get_res_msg(response)
        self.messages.append(res_msg)
        self._history_res(response)

        return response

    def add_message(self, content, role="user"):
        self.messages.append({"role": role, "content": content})
        self._history_req(self.messages[-1])

    def call_function(self, response):
        fn_call = self.get_fn_call(response)

        # if function_call exist
        if fn_call:
            function_name = fn_call["name"]
            function = tool.funcs[function_name]

            fn_args = json.loads(fn_call["arguments"])
            return function(**fn_args)

    def get_fn_call(self, response):
        return self._get_res_msg(response).get("function_call")

    def _get_res_msg(self, response):
        return response["choices"][0]["message"]

    def total_tokens(self, messages):
        """
        returns number of used all tokens
        """
        return sum([int(msg["usage"]["total_tokens"]) for msg in messages])



# fn_call_msg = {
#     "role": "function",
#     "name": function_name,
#     "content": fn_result,
# }
