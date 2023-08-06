from opaw.model.file import FileBot
from opaw import util
from opaw.examples import setup

# api key
setup()

bot = FileBot()

# file upload

file = open("file-upload.jsonl", "rb")
response = bot.create(task="upload", file=file, purpose="fine-tune")
print("file-upload response:", response)
id = response["id"]

# retrieve a file
response = bot.create(task="retrieve", file_id=id)
print("list response:", response)

# download file
response = bot.create(task="download", file_id=id)
print("download response:", response)

# save history if needed
util.save_history(bot, "history/file-hist.json")

