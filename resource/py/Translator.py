import requests, uuid, json


def translate(word: str = None, langs: dict = None, key: str = None):
    def set_base_url():
        endpoint = "https://api.cognitive.microsofttranslator.com"
        path = '/translate'
        constructed_url = endpoint + path

        return constructed_url

    def set_headers(key):
        # location, also known as region.
        location = "koreacentral"

        headers = {
            'Ocp-Apim-Subscription-Key': key,
            'Content-type': 'application/json',
            'Ocp-Apim-Subscription-Region': location,
            'X-ClientTraceId': str(uuid.uuid4())
        }
        return headers

    def set_params(*args):
        return {
            'api-version': '3.0',
            'from': args[0][0],
            'to': args[0][1:]
        }

    def get_language_from_dict():
        return list(langs.values())


    """
    Translate를 사용하면 아래와 같은 데이터 타입을 전송 받을 수 있습니다.
    >> type:list
    >> [{'translations': [{'text': '시계', 'to': 'ko'}, {'text': 'часы', 'to': 'ru'}]}]
    
    만약 Error 가 발생한다면 아래와 같은 데이터 타입을 전송 받습니다.
    >> type:dict
    >> {'error': {'code': 401000, 'message': 'The request is not authorized because credentials are missing or invalid.'}}
    """

    lang_list = get_language_from_dict()
    constructed_url = set_base_url()
    headers = set_headers(key)
    params = set_params(lang_list)

    # You can pass more than one object in body.
    body = [{
        'text': word
    }]

    request = requests.post(constructed_url, params=params, headers=headers, json=body)
    response = request.json()

    if


    print("  [Info] MS Azure token subtracted... Please note this info...")
    print(response)
    return response

    # print(json.dumps(response, sort_keys=True, ensure_ascii=False, indent=4, separators=(',', ': ')))

def search_text_by_lang(json, lang) -> str:
    print(json)
    results = json[0]["translations"]
    word = [result["text"] for result in results if lang == result["to"]][0]

    # for result in results:
    #     if lang == result["to"]:
    #         word = result["text"]

    return word