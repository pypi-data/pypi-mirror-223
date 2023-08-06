from opaw.model.edit import EditBot
from opaw import util

# api key
util.setup()

# edit
bot = EditBot()
prompt = "Hey, tis was my filst car!!"
instruction = "Fix the spelling mistakes"
response = bot.create(prompt, instruction=instruction)
text = response["choices"][0]["text"]
print("text:", text)

# save history if needed
util.save_history(bot, "edit-hist.json")
