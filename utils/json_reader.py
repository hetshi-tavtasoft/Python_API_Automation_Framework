import json

def read_json(filepath):
    with open(filepath) as file:
        return json.load(file)
