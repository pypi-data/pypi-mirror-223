from opaw import tool, util
from opaw.model.chat import ChatBot
from opaw.examples import setup

# api key
setup()

# bot
bot = ChatBot("gpt-3.5-turbo-0613")
bot.add_message("You are a helpful assistant that can send function json when need.", role="system")

company = "amazon"
response = bot.create(
    f"What is the {company}'s stock price?",
    functions=tool.info,
    function_call="auto")

if bot.get_fn_call(response):
    fn_result = bot.call_function(response)
    print(f"{company} stock price:", fn_result)
else:
    print("no function call")

# save model history
util.save_history(bot, "history/chat-fn-call-hist.json")