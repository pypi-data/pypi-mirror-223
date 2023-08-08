import time
import copy
import json
import os
from os.path import join
from datetime import datetime
import openai
import traceback


def setup(api_key_file="openai-api-key.txt"):
    key = None
    try:
        with open(api_key_file) as file:
            key = file.read()
    except FileNotFoundError:
        print(f"No file: {api_key_file} for openai api key.")
        print("Searching environment variable: \"OPENAI_API_KEY\"...")

        # env var
        key = os.environ.get("OPENAI_API_KEY")
        if key is None:
            print("There's no environment variable: \"OPENAI_API_KEY\".")
    finally:
        if key is None:
            print("Failed to find openai api key.")
            print(f"Create a \"{api_key_file}\" file or set environment variable: \"OPENAI_API_KEY\".")
        else:
            try:
                openai.api_key = key
                print("OpenAI API key is setup!")
                openai.Model.list()  # test for the api_key is valid or not
            except Exception as e:
                traceback.print_exc()
                time.sleep(0.1)
                print("Your API key has a problem. Check here: "
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


