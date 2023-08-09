from opaw.util import log
from opaw.model.image import ImageBot
from opaw import util
from opaw.examples import setup

# api key
setup()

# logger
logger = log.get("image", "logs/image.log")

# image
bot = ImageBot()

# create a image
response = bot.create("A black cat sitting on a frozen lake.", task="create", size="256x256")
logger.info(f"image: {response['data'][0]['url']}")

# save history if needed
bot.save_history("history/image-hist.json")


