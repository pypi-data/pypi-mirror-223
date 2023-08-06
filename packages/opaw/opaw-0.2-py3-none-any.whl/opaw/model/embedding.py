import openai
from opaw.model.bot import Bot

class EmbeddingBot(Bot):
    """
    https://platform.openai.com/docs/api-reference/embeddings
    """
    def __init__(self, model="text-embedding-ada-002"):
        super().__init__(model, "embedding")

    def create(self, prompt, **kargs):
        if prompt is None:
            return None

        request = {
            "model": self.model,
            "input": prompt,
            **kargs
        }

        self._history_req(prompt, kargs)
        response = openai.Embedding.create(**request)
        self._history_res(response)
        return response
