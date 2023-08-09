import openai
from opaw.model.bot import Bot
from opaw import util

class AudioBot(Bot):
    """
    https://platform.openai.com/docs/api-reference/audio
    """

    def __init__(self, model=util.default_models["audio"]):
        super().__init__(model, "audio")

    def create(self, file, **kargs):
        """
        :kargs: select task "stt(transcript)" or "mt(translation)"

        language (stt): https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes
        """
        if file is None or not kargs.get("task"):
            return None

        model = openai.Audio
        methods = {
            "transcript": model.transcribe,
            "stt": model.transcribe,
            "translation": model.translate,
            "mt": model.translate,
        }

        # remove task from request
        task = kargs.pop('task')
        if task not in methods:
            return None

        request = {
            "model": self.model,
            "file": file,
            **kargs
        }
        self._history_req(request)

        request["file"] = open(file, "rb")
        response = methods[task](**request)
        self._history_res(response)
        return response
