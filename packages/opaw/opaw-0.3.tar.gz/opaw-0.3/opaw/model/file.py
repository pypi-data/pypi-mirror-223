import openai
from opaw.model.bot import Bot


class FileBot(Bot):
    """
    https://platform.openai.com/docs/api-reference/files
    """

    def __init__(self):
        super().__init__("bot", "file")

    def create(self, prompt=None, **kargs):
        """
        :param prompt: is not used for model, just memo in history (use kargs)
        """
        if not kargs.get("task"):
            return None
        memo = prompt

        request = {
            **kargs
        }
        self._history_req(memo, kargs)

        model = openai.File
        methods = {
            "list": model.list,
            "upload": model.create,
            "delete": model.delete,
            "retrieve": model.retrieve,
            "download": model.download,
        }

        # remove task from request
        task = request.pop('task')
        if task not in methods:
            return None

        response = methods[task](**request)
        self._history_res(response)
        return response
