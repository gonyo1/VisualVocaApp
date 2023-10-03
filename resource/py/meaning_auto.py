# coding=cp949
# <-- dev ahn part -->
import pandas as pd
import re
import requests
import json

CLIENT_ID, CLIENT_SECRET = "21scjke3n3ZaiiPZ8c5S", "rzH1SmWvOy"

def translate(text, source="en", target="ko"):

    # 1. API Ȱ�� ���� ���
    url = "https://openapi.naver.com/v1/papago/n2mt"
    headers = {
     "Content-Type": "application/json",
     "X-Naver-Client-Id": CLIENT_ID,
     "X-Naver-Client-Secret": CLIENT_SECRET
    }
    params = {"source": source, "target": target, "text": text}

    # 2. ��û
    response = requests.post(url, json.dumps(params), headers=headers)

    # 3. json ���·� ��� �ޱ�
    return response.json()["message"]["result"]["translatedText"]
#
# text = "jump"
# test = translate(text)
# print(test)

