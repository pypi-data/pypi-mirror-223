import openai
from opaw.model.bot import Bot


class AudioBot(Bot):
    """
    https://platform.openai.com/docs/api-reference/audio
    """

    def __init__(self, model="whisper-1"):
        super().__init__(model, "audio")

    def create(self, prompt, **kargs):
        """
        :kargs: select task "stt(transcript)" or "mt(translation)"

        language (stt): https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes
        """
        if prompt is None or not kargs.get("task"):
            return None
        file = prompt

        request = {
            "model": self.model,
            "file": open(file, "rb"),
            **kargs
        }
        self._history_req(file, kargs)


        model = openai.Audio
        methods = {
            "transcript": model.transcribe,
            "stt": model.transcribe,
            "translation": model.translate,
            "mt": model.translate,
        }

        # remove task from request
        task = request.pop('task')
        if task not in methods:
            return None


        response = methods[task](**request)
        self._history_res(response)
        return response

