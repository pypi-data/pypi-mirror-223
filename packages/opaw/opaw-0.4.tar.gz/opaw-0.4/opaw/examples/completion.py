from opaw.util import log
from opaw.model.completion import CompletionBot
from opaw import util
from opaw.examples import setup

# api key
setup()

# logger
logger = log.get("completion", "logs/completion.log")

# completion
bot = CompletionBot()
prompt = "Tell some lies"
response = bot.create(prompt, max_tokens=50)
res_msg = response["choices"][0]["text"]
logger.info(res_msg)

# save history if needed
bot.save_history("history/completion-hist.json")


