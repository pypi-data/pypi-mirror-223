from opaw.model.chat import ChatBot
from opaw import util

# api key
util.setup()

# chat
bot = ChatBot()
bot.add_message("You are a helpful assistant.", role="system")
prompt = "What is openai?"
response = bot.create(prompt)
res_msg = response["choices"][0]["message"]["content"]
print("resopnse:", res_msg)

# save history if needed
util.save_history(bot, "chat-hist.json")
