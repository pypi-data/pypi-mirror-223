from opaw.model.embedding import EmbeddingBot
from opaw import util

# api key
util.setup()

# embedding
bot = EmbeddingBot()
prompt = "Cheese is melting on my laptop"
response = bot.create(prompt)
embeddings = response["data"][0]["embedding"]
print("embeddings:", embeddings)

# save history if needed
util.save_history(bot, "embedding-hist.json")


