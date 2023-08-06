import time
import copy
import math


class Bot:
    """
    https://platform.openai.com/docs/api-reference/introduction
    """

    def __init__(self, model, type="bot"):
        self.model = model
        # chat, completion, image, audio, embedding, file, finetune, moderation, edit
        self.type = type
        self.history = []

    def create(self, prompt, **kargs):
        """
        Send prompt to the bot and gets a result
        :param prompt: the prompt to send
        :param kargs: other args
        :return: response from the bot
        """
        pass

    def _history_req(self, prompt="", kargs=None):
        """
        history user's request
        """
        history = {"model": self.model,
               "type": self.type,
               "prompt": copy.deepcopy(prompt),
               "created": math.floor(time.time()),
               "from": "user"
               }

        if kargs:
            history.update(copy.deepcopy(kargs))  # kargs

        self.history.append(history)

    def _history_res(self, response):
        """
        history response of the bot
        """
        copied_res = copy.deepcopy(response)
        copied_res.update({
            "from": "bot"
        })

        self.history.append(copied_res)
