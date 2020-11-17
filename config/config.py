import json
import os


file_prefix = os.path.dirname(__file__)

with open(f"{file_prefix}\config.json") as file:
    config = json.load(file)


def set_config(key, value):
    config[key] = value
    with open("config/config.json", "w") as file:
        json.dump(config, file)

def clear_config():
    config = {}
    with open("config/config.json", "w") as file:
        json.dump(config, file)