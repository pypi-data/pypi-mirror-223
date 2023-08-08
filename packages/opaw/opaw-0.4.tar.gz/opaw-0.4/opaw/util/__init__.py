import copy
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


