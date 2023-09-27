import os
import json


def is_main_app() -> str:
    if os.path.basename(os.path.abspath("./")) != "py":
        base_dir = os.path.abspath(f"./resource/src")
    else:
        base_dir = os.path.abspath(f"../src")

    return base_dir

def load_json_file() -> dict:

    json_data = None
    base_path = is_main_app()
    json_file = f'{base_path}\\config.json'

    with open(json_file, 'r') as f:
        json_data = json.load(f)

    return json_data

def save_json_file(key, value):
    json_data = None
    base_path = is_main_app()
    json_file = f'{base_path}\\config.json'

    with open(json_file, 'r', encoding='utf-8') as f:
        json_data = json.load(f)

    json_data[key] = value

    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent="\t")

    return json_data

