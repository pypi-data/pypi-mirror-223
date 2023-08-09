from opaw.util import log
from opaw.model.audio import AudioBot
from opaw import util
from opaw.examples import setup

# api key
setup()

# logger
logger = log.get("audio", "logs/audio.log")

# audio
bot = AudioBot()

# transcript (language: https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes)
response = bot.create("audio1.mp3", task="stt", language="en")
logger.info(f"stt: {response['text']}")

# translation
response = bot.create("audio1.mp3", task="mt", language="en")
logger.info(f"mt: {response['text']}")

# save history if needed
bot.save_history("history/audio-hist.json")



