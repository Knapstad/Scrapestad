import json
import os
from pathlib import Path


file_prefix = Path(os.path.dirname(__file__))

with open(file_prefix/"config.json") as file:
    config = json.load(file)


def set_config(key, value):
    config[key] = value
    with open(file_prefix/"config.json", "w") as file:
        json.dump(config, file)

def clear_config():
    config = {}
    with open(file_prefix/"config.json", "w") as file:
        json.dump(config, file)