from opaw.util import log
import json
from opaw.model.chat import ChatBot
from opaw.examples import setup
from opaw import util

# api key
setup()

# logger
logger = log.get("load-chat", "logs/load-chat.log")

# chat
bot = ChatBot()
bot.load_msgs("history/chat-hist.json")  # load history

response = bot.create("Then, what products are made in there?")
res_msg = response["choices"][0]["message"]["content"]
logger.info(f"response: {res_msg}")

bot.save_history("history/load-chat-hist.json")  # save history
