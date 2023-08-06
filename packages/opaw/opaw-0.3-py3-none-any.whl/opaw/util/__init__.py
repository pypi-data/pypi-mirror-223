import json
import os
from os.path import join
from datetime import datetime
import openai


def setup(api_key_f="openai-api-key.txt"):
    openai.api_key = read_api_key(api_key_f)


def read_api_key(file):
    with open(file) as file:
        return file.read()


def models():
    r = openai.Model.list()
    return [model["id"] for model in r["data"]]


def save_history(bot, file):
    """
    saves bot's history in "history" directory
    :param file: the history file name (parent dirs will be created automatically)
    """

    # save with date format if dir is given
    if os.path.isdir(file):
        now = datetime.now().strftime("%Y%m%dT%H%M%S")
        file = join(file, f"{now}.json")

    # make all parent dirs
    mkdirs(file)
    with open(file, "w") as f:
        json.dump(bot.history, f, indent="\t")


def mkdirs(file):
    parent_dir = os.path.dirname(file)
    os.makedirs(parent_dir, exist_ok=True)
