import json

def load_keys():
    with open('app/main/resources/key.json', 'r') as f:
        keys = json.load(f)
    return keys