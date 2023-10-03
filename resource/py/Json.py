# coding=utf-8

import os
import json
from resource.py.Path import get_root_directory

def get_directory():
    __dir__ = get_root_directory()
    return __dir__


def load_json_file(name:str = 'config.json') -> dict:
    base_path = get_directory()
    path = os.path.join(base_path, "src").replace("\\", "/")

    json_file = os.path.join(path, name)
    json_file = json_file.replace("\\", "/")
    print(json_file)

    if not os.path.isfile(json_file):
        generate_init()

    with open(json_file, 'rt', encoding='utf-8') as f:
        json_data = json.load(f)
        f.close()

    return json_data

def save_json_file(key, value, name:str = 'config.json'):
    base_path = get_directory()
    json_file = os.path.join(base_path, f"src/{name}").replace("\\", "/")

    with open(json_file, 'rt', encoding='utf-8') as f:
        json_data = json.load(f)
        f.close()

    json_data[key] = value

    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)
        f.close()

    return json_data

def generate_init():
    base_path = get_directory()

    if not os.path.isdir(base_path):
        os.mkdir(base_path)

    path = os.path.join(base_path, "src").replace("\\", "/")
    if not os.path.isdir(path):
        os.mkdir(path)

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

        path = os.path.join(base_path, "src/config.json").replace("\\", "/")

        with open(path, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=2, ensure_ascii=False)

        return json_data
    except:
        print("  [Error] Directory not found ...")

