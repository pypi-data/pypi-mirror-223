import openai
from opaw.model.bot import Bot


class FinetuneBot(Bot):
    """
    https://platform.openai.com/docs/api-reference/fine-tunes
    """

    def __init__(self, model="curie"):
        super().__init__(model, "finetune")

    def create(self, prompt, **kargs):
        """
        :param prompt: is not used for model. just for memo in history
        """
        if prompt is None or not kargs.get("task"):
            return None
        memo = prompt

        request = {
            "model": self.model,
            **kargs
        }
        self._history_req(memo, kargs)

        model = openai.FineTune
        methods = {
            "create": model.create,
            "list": model.list,
            "retrieve": model.retrieve,
            "cancel": model.cancel,
            "delete": model.delete,
        }

        # remove task from request
        task = request.pop('task')
        if task not in methods:
            return None

        response = methods[task](**request)
        self._history_res(response)
        return response
