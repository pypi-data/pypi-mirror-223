from opaw.model.chat import ChatBot
from opaw import util
from opaw.examples import setup

# api key
setup()

# chat
bot = ChatBot()
bot.add_message("You are a helpful assistant.", role="system")
prompt = "What is openai?"
response = bot.create(prompt)
res_msg = response["choices"][0]["message"]["content"]
print("resopnse:", res_msg)

# save history if needed
util.save_history(bot, "history/chat-hist.json")
