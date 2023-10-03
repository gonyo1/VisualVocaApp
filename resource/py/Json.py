# coding=utf-8

import os
import json


def is_main_app() -> str:
    path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(path, "src/config.json")
    path = path.replace("\\", "/")

    if os.path.basename(os.path.abspath(__file__)) != "py":
        base_dir = os.path.abspath(f"./resource/src")
    else:
        base_dir = os.path.abspath(f"../src")

    base_dir = base_dir.replace("\\", "/")

    return base_dir

def load_json_file(name:str = 'config.json') -> dict:
    json_data = None
    while True:
        try:
            base_path = is_main_app()
            json_file = os.path.join(base_path, name)
            json_file = json_file.replace("\\", "/")
            print(json_file)

            with open(json_file, 'rt', encoding='utf-8') as f:
                json_data = json.load(f)
                f.close()
                break

        except FileNotFoundError:
            # count += 1
            base_path = is_main_app()

            print(f"  [Info] No Config file Found... {base_path}")
            json_file = os.path.join(base_path, name)
            json_file = json_file.replace("\\", "/")
            generate_init(path=json_file)

    return json_data

def save_json_file(key, value, name:str = 'config.json'):
    json_data = None
    base_path = is_main_app()
    json_file = os.path.join(base_path, name)

    with open(json_file, 'rt', encoding='utf-8') as f:
        json_data = json.load(f)
        f.close()

    json_data[key] = value

    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)
        f.close()

    return json_data

def generate_init(path):
    try:
        json_data = {
            "AppName": "Visual Voca",
            "Version": "1.0",
            "Contributors": [
                "Gonyo",
                "Ahn"
            ],
            "FontFamily": "Noto Sans KR SemiBold",
            "BookmarkIndex": 0,
            "AutoScroll": "True",
            "ImageDownCount": 1,
            "LanguagesShow": {
                "UpperPart": "en",
                "LowerPart": "ko",
                "Reference": "https://learn.microsoft.com/en-us/azure/ai-services/translator/language-support"
            },
            "LanguagesSpeech": {
                "First": "en",
                "Second": "ko",
                "Reference": "https://cloud.google.com/translate/docs/languages?hl=ko"
            },
            "APIKeys": {
                "NaverPapago": "<YOUR_SECRET_API_KEY>",
                "MSAzureTranslator": "d6b7496c3f714146867f5042c0782126"
            },
            "GetImageFromURL": [
                {
                    "URL": "https://www.gettyimagesbank.com/s/?q=",
                    "CSS": ".wrapThumbList > #list700 > #tiles > li > a > img"
                },
                {
                    "URL": "https://tenor.com/ko/search/",
                    "CSS": "div.GifList > div > figure > a > div.Gif > img"
                }
            ]
            }

        with open(path, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=2, ensure_ascii=False)

        return json_data
    except:
        print("  [Error] Directory not found ...")

