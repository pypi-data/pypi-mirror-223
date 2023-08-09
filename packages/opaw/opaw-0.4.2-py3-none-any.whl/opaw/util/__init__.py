import logging
from opaw.util import log
import time
import copy
import json
import os
from os.path import join
from datetime import datetime
import openai
import traceback

default_models = {
    "chat": "gpt-3.5-turbo",
    "completion": "text-davinci-003",
    "image": "DALL-E",
    "audio": "whisper-1",
    "embedding": "text-embedding-ada-002",
    "file": "",
    "finetune": "curie",
    "moderation": "text-moderation-latest",
    "edit": "text-davinci-edit-001"
}


def setup(api_key_file="openai-api-key.txt"):
    logger = log.get("opaw")
    # remove logger file handler
    logger.handlers = [h for h in logger.handlers if not isinstance(h, logging.FileHandler)]

    key = None
    try:
        with open(api_key_file) as file:
            key = file.read()
    except FileNotFoundError:
        logger.warning(f"No file: {api_key_file} for openai api key.")
        logger.warning("Searching environment variable: \"OPENAI_API_KEY\"...")

        # env var
        key = os.environ.get("OPENAI_API_KEY")
        if key is None:
            logger.warning("There's no environment variable: \"OPENAI_API_KEY\".")
    finally:
        if key is None:
            logger.warning("Failed to find openai api key.")
            logger.warning(f"Create a \"{api_key_file}\" file or set environment variable: \"OPENAI_API_KEY\".")
        else:
            try:
                openai.api_key = key
                logger.info("OpenAI API key is setup!")
                openai.Model.list()  # test for the api_key is valid or not
            except Exception as e:
                traceback.print_exc()
                time.sleep(0.1)
                logger.warning("Your API key has a problem. Check here: "
                               "https://platform.openai.com/docs/guides/error-codes/api-errors")


def models():
    r = openai.Model.list()
    return [model["id"] for model in r["data"]]


def mkdirs(file):
    parent_dir = os.path.dirname(file)
    os.makedirs(parent_dir, exist_ok=True)


def filter_args(data):
    """
    remove special arguments
    :param data: history or messages (format: [{}, {}, {}...])
    """
    common_args = ["type", "created", "from"]
    etc_args = ["task", "memo"]
    remove_args = common_args + etc_args

    data = copy.deepcopy(data)
    return [{k: v for k, v in e.items() if k not in remove_args} for e in data]


def pprint(d):
    """
    Pretty print
    """
    print(pprints(d))


def pprints(d):
    """
    Pretty print string
    """
    return json.dumps(d, indent="\t")
