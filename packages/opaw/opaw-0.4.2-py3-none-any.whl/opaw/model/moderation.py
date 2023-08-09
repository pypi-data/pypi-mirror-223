import openai
from opaw.model.bot import Bot
from opaw import util


class ModerationBot(Bot):
    """
    https://platform.openai.com/docs/api-reference/moderations
    """

    def __init__(self, model=util.default_models["moderation"]):
        super().__init__(model, "moderation")

    def create(self, input, **kargs):
        if input is None:
            return None

        request = {
            "model": self.model,
            "input": input,
            **kargs
        }

        self._history_req(request)
        response = openai.Moderation.create(**request)
        self._history_res(response)
        return response
