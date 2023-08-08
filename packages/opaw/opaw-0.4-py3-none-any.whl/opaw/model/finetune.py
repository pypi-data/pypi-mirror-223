import openai
from opaw.model.bot import Bot


class FinetuneBot(Bot):
    """
    https://platform.openai.com/docs/api-reference/fine-tunes
    """

    def __init__(self, model="curie"):
        super().__init__(model, "finetune")

    def create(self, _=None, **kargs):
        """
        :param _: is not used (use kargs instead)
        """
        if not kargs.get("task"):
            return None

        model = openai.FineTune
        methods = {
            "create": model.create,
            "list": model.list,
            "retrieve": model.retrieve,
            "cancel": model.cancel,
            "delete": model.delete,
        }

        task = kargs.pop('task')
        if task not in methods:
            return None

        request = {
            "model": self.model,
            **kargs
        }
        self._history_req(request)

        response = methods[task](**request)
        self._history_res(response)
        return response
