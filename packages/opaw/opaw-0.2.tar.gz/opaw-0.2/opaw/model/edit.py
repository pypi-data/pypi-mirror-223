import openai
from opaw.model.bot import Bot


class EditBot(Bot):
    """
    https://platform.openai.com/docs/api-reference/edits
    """

    def __init__(self, model="text-davinci-edit-001"):
        super().__init__(model, "edit")

    def create(self, prompt, **kargs):
        input = prompt
        if input is None:
            return None

        request = {
            "model": self.model,
            "input": input,
            **kargs
        }

        self._history_req(input, kargs)
        response = openai.Edit.create(**request)
        self._history_res(response)
        return response
