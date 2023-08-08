import openai
from opaw.model.bot import Bot


class EditBot(Bot):
    """
    Deprecated model

    https://platform.openai.com/docs/api-reference/edits
    """

    def __init__(self, model="text-davinci-edit-001"):
        """
        Deprecated model
        """
        super().__init__(model, "edit")

    def create(self, input, **kargs):
        """
        Deprecated model
        """
        if input is None:
            return None

        request = {
            "model": self.model,
            "input": input,
            **kargs
        }

        self._history_req(request)
        response = openai.Edit.create(**request)
        self._history_res(response)
        return response
