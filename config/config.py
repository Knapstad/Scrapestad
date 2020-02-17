import json

with open("config/config.json") as file:
    config = json.load(file)


def set_config(key, value):
    config[key] = value
    with open("config/config.json", "w") as file:
        json.dump(config, file)

def clear_config():
    config = {}
    with open("config/config.json", "w") as file:
        json.dump(config, file)