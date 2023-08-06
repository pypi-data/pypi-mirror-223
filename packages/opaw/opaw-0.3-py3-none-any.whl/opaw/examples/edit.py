from opaw.model.edit import EditBot
from opaw import util
from opaw.examples import setup

# api key
setup()

# edit
bot = EditBot()
prompt = "Hey, tis was my filst car!!"
instruction = "Fix the spelling mistakes"
response = bot.create(prompt, instruction=instruction)
text = response["choices"][0]["text"]
print("text:", text)

# save history if needed
util.save_history(bot, "history/edit-hist.json")
