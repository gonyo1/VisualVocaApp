import os
import json


def load_json_file() -> dict:
    def is_main_app() -> str:
        if os.path.basename(os.path.abspath("./")) != "py":
            base_dir = os.path.abspath(f"./resource/src")
        else:
            base_dir = os.path.abspath(f"../src")

        return base_dir

    json_data = None
    base_path = is_main_app()
    json_file = f'{base_path}\\config.json'

    with open(json_file, 'r') as f:
        json_data = json.load(f)

    return json_data