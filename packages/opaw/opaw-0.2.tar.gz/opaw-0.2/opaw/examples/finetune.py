from opaw.model.finetune import FinetuneBot
from opaw import util

# api key
util.setup()

# finetune create
bot = FinetuneBot()
response = bot.create("test_memo for finetune create", task="create", training_file="...")
print("finetune create:", response)

# finetune list
response = bot.create("test_memo for finetune list", task="list")
print("finetune list:", response)

# save history if needed
util.save_history(bot, "finetune-hist.json")
