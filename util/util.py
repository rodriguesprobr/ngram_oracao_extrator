import json
import os
from datetime import datetime


def log(mensagem):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {mensagem}")


def get_config(nome):
    return json.load(open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "config.json")))[nome]
