from opaw.model.completion import CompletionBot
from opaw import util

# api key
util.setup()

# completion
bot = CompletionBot()
prompt = "Tell some lies"
response = bot.create(prompt)
res_msg = response["choices"][0]["text"]
print(res_msg)

# save history if needed
util.save_history(bot, "completion-hist.json")


