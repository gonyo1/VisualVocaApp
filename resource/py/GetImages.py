import os
import requests
import json
import cssselect

import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# <--- Import or Install Packages --->
try:
    import lxml.html
except ModuleNotFoundError:
    os.system("pip install lxml")
    import lxml.html


# <--- Get Main Image src url from "GettyImage Web Site" --->

def get_images_from_word(word: str = None, count: int = 4, *args) -> str:
    # args는 파일타입(이미지 파일 타입)
    def is_main_app(word: str = None) -> str:
        base_dir = str()
        base_dir = os.path.abspath(".")
        print(os.path.abspath("./"),' dddddddddddddddd')

        if os.path.basename(os.path.abspath("./")) != "py":
            base_dir = os.path.abspath(f"./resource/voca/img/{word}")
        else:
            base_dir = os.path.abspath(f"../voca/img/{word}")

        return base_dir

    def is_directory(path: str = None):
        if not os.path.isdir(path):
            os.mkdir(path)

    def download_image_from_url(word: str = None):
        # [repair] GettyImage 사이트에서 이미지 검색하는 URL로 사이트 업데이트에 대한 대응 필요한 부분
        site_idx = 0
        src = list()

        try:
            while True:
                # Setup URL
                base_url = args[0]["GetImageFromURL"][site_idx]["URL"]
                base_url = f"{base_url}{word}"
                print(base_url)

                res = requests.get(base_url, verify=False, timeout=10)

                if res.status_code == 200:

                    print("  [Web] Starting website crawling...")
                    html = res.text
                    tree = lxml.html.fromstring(html)

                    selector_tag = args[0]["GetImageFromURL"][site_idx]["CSS"]
                    selectors = tree.cssselect(selector_tag)

                    src.extend([img.get("src") for img in selectors])
                    if len(src) >= count:
                        break
                    else:
                        site_idx += 1

            for idx, url in enumerate(src[:count]):
                idx = str(idx + 1)
                extension = url[url.rfind("."):]

                path = os.path.join(base_dir, f"{word}({idx}){extension}")
                if not os.path.isfile(path):
                    img_data = requests.get(url).content
                    with open(path, 'wb') as img_file:
                        img_file.write(img_data)
                    # os.system(f"curl -k {url} > {path}")
        except Exception as e:
            print(e)
            print("  [WebError] Please Check Internet Network ...")

    def is_image_downloaded(path: str = None, word: str = None) -> str:
        status = "waiting"

        filetypes = tuple(os.path.join(path, f"{word}({str(count)}){extension[1:]}") for extension in args[1])

        for filetype in filetypes:
            if os.path.isfile(os.path.abspath(filetype)):
                status = "saved"
                break

        if status == "waiting":
            is_directory(path)
            download_image_from_url(word)
            status = "downloaded"
        return status

    base_dir = is_main_app(word=word)
    status = is_image_downloaded(path=base_dir, word=word)

    return status
