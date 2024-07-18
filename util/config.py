import json
import os


def config(nome):
    return json.load(open(os.path.join(os.path.dirname(os.pardir), "config.json")))[nome]
