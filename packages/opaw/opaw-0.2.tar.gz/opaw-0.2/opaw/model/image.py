import openai
from opaw.model.bot import Bot


class ImageBot(Bot):
    """
    https://platform.openai.com/docs/api-reference/images
    """

    def __init__(self, model="DALL-E"):
        super().__init__(model, "image")

    def create(self, prompt, **kargs):
        """
        :kargs: select task "create" or "edit" or "variation"
        """
        if prompt is None or not kargs.get("task"):
            return None

        request = {
            "model": self.model,
            "prompt": prompt,
            **kargs
        }

        self._history_req(prompt, kargs)

        model = openai.Image
        methods = {
            "create": model.create,
            "edit": model.create_edit,
            "variation": model.create_variation
        }

        # remove task from request
        task = request.pop('task')
        if task not in methods:
            return None

        # remove model key from request
        request.pop("model")
        response = methods[task](**request)
        self._history_res(response)
        return response

    def img_format(self, img):
        """
        img could be url or data scheme encoded in base64
        """
        return "url" if img.startswith("http") else "data"