from opaw.model.finetune import FinetuneBot
from opaw import util
from opaw.examples import setup

# api key
setup()

# finetune create
bot = FinetuneBot()
response = bot.create("test_memo for finetune create", task="create", training_file="...")
print("finetune create:", response)

# finetune list
response = bot.create("test_memo for finetune list", task="list")
print("finetune list:", response)

# save history if needed
util.save_history(bot, "history/finetune-hist.json")
