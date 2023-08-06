import json
import os
from os.path import join
from datetime import datetime
import openai

from opaw import util
from opaw.model.chat import ChatBot


def setup():
    openai.api_key = read_api_key()


def read_api_key():
    file = join(project_dir(), "openai-api-key.txt")
    with open(file) as file:
        return file.read()


def models():
    r = openai.Model.list()
    return [model["id"] for model in r["data"]]


def loop_chat(model="gpt-3.5-turbo", system_prompt="You are a helpful assistant."):
    if openai.api_key is None:
        util.setup()

    bot = ChatBot(model)
    bot.add_message(system_prompt, role="system")
    while True:
        user_input = input("User: ")
        if "bye" in user_input:
            print("BYE!")
            break
        response = bot.create(user_input)
        bot_response = response["choices"][0]["message"]["content"]
        print(f"Bot: {bot_response}\n")

    save_history(bot)


def save_history(bot, file=None):
    """
    saves bot's history in "history" directory
    :param file: file name
    """
    if file is None:
        now = datetime.now().strftime("%Y%m%dT%H%M%S")
        file = f"{now}.json"

    file = join(project_dir(), "history", file)
    with open(file, "w") as f:
        json.dump(bot.history, f, indent="\t")


def is_project_dir(path):
    path = path if os.path.isdir(path) else os.path.dirname(path)
    return "requirements.txt" in os.listdir(path)


def project_dir():
    fp = __file__
    while not is_project_dir(fp):
        fp = os.path.dirname(fp)
    return fp

