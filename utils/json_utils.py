import json


def read_json(filepath):
    with open(filepath, encoding="utf-8") as f:
        return json.load(f)


def write_json(filepath, data, indent=2):
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=indent)
