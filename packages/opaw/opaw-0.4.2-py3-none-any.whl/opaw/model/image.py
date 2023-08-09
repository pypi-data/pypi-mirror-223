import openai
from opaw.model.bot import Bot
from opaw import util


class ImageBot(Bot):
    """
    https://platform.openai.com/docs/api-reference/images
    """

    def __init__(self, model=util.default_models["image"]):
        super().__init__(model, "image")

    def create(self, prompt, **kargs):
        """
        :kargs: select task "create" or "edit" or "variation"
        """
        if prompt is None or not kargs.get("task"):
            return None

        model = openai.Image
        methods = {
            "create": model.create,
            "edit": model.create_edit,
            "variation": model.create_variation
        }

        task = kargs.pop('task')
        if task not in methods:
            return None

        request = {
            "prompt": prompt,
            **kargs
        }

        if task == "variation":  # remove prompt when variation
            request.pop("prompt")

        self._history_req(request)

        response = methods[task](**request)
        self._history_res(response)
        return response

    def img_format(self, img):
        """
        img could be url or data scheme encoded in base64
        """
        return "url" if img.startswith("http") else "data"
