from opaw.model.embedding import EmbeddingBot
from opaw import util
from opaw.examples import setup

# api key
setup()

# embedding
bot = EmbeddingBot()
prompt = "Cheese is melting on my laptop"
response = bot.create(prompt)
embeddings = response["data"][0]["embedding"]
print("embeddings:", embeddings)

# save history if needed
util.save_history(bot, "history/embedding-hist.json")


