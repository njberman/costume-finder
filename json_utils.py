from paths import JSON_PATH
import json

def read_json():
  with open(JSON_PATH, 'r') as f:
    return json.load(f)

def write_json(new_json):
  with open(JSON_PATH, 'w') as f:
    json.dump(new_json, f, indent=2)

  return read_json()