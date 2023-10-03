# coding=cp949
# <-- dev ahn part -->
import pandas as pd
import re
import requests
import json

CLIENT_ID, CLIENT_SECRET = "21scjke3n3ZaiiPZ8c5S", "rzH1SmWvOy"

def translate(text, source="en", target="ko"):

    # 1. API 활용 접근 방식
    url = "https://openapi.naver.com/v1/papago/n2mt"
    headers = {
     "Content-Type": "application/json",
     "X-Naver-Client-Id": CLIENT_ID,
     "X-Naver-Client-Secret": CLIENT_SECRET
    }
    params = {"source": source, "target": target, "text": text}

    # 2. 요청
    response = requests.post(url, json.dumps(params), headers=headers)

    # 3. json 형태로 결과 받기
    return response.json()["message"]["result"]["translatedText"]
#
# text = "jump"
# test = translate(text)
# print(test)

