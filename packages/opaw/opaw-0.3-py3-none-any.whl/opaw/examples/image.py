from opaw.model.image import ImageBot
from opaw import util
from opaw.examples import setup

# api key
setup()

# image
bot = ImageBot()

# create a image
response = bot.create("A black cat sitting on a frozen lake.", task="create", size="256x256")
print("image:", response["data"][0]["url"])

# save history if needed
util.save_history(bot, "history/image-hist.json")


