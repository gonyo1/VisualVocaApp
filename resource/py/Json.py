# coding=cp949

import os
import json


def is_main_app() -> str:
    if os.path.basename(os.path.abspath(__file__)) != "py":
        base_dir = os.path.abspath(f"./resource/src")
    else:
        base_dir = os.path.abspath(f"../src")

    return base_dir

def load_json_file() -> dict:

    json_data = None
    base_path = is_main_app()
    json_file = os.path.join(base_path, 'config.json')

    with open(json_file, 'rt', encoding='utf-8') as f:
        json_data = json.load(f)
        f.close()

    return json_data

def save_json_file(key, value):
    json_data = None
    base_path = is_main_app()
    json_file = os.path.join(base_path, 'config.json')

    with open(json_file, 'rt', encoding='utf-8') as f:
        json_data = json.load(f)
        f.close()

    json_data[key] = value

    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)
        f.close()

    return json_data

def generate_init(path):
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
        json.dump(json_data, f, indent="굏")

    return json_data

