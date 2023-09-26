import os
import requests
import pprint

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# <--- Import or Install Packages --->
try:
    import lxml.html
except ModuleNotFoundError:
    os.system("pip install lxml")
    import lxml.html


# <--- Get Main Image src url from "GettyImage Web Site" --->

def get_images_from_word(word: str = None, count: int = 4) -> str:
    def is_main_app(word: str = None) -> str:
        base_dir = str()

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
        base_url = f"https://www.gettyimagesbank.com/s/?q={word}"
        try:
            res = requests.get(base_url, verify=False, timeout=5)

            if res.status_code == 200:
                print("  [Web] Starting website crawling...")
                html = res.text
                tree = lxml.html.fromstring(html)
                selectors = tree.cssselect('.wrapThumbList > #list700 > #tiles > li > a > img')
                src = [img.get("src") for img in selectors]
                for idx, url in enumerate(src[:count]):
                    idx = str(idx + 1)

                    if not os.path.isfile(f"{base_dir}\\{word}({idx}).jpg"):
                        os.system(f"curl -k {url} > {base_dir}\\{word}({idx}).jpg")
        except Exception as e:
            print("  [WebError] Please Check Internet Network ...")

    def is_image_downloaded(path: str = None, word: str = None) -> str:
        status = "waiting"

        if os.path.isfile(os.path.abspath(f"{path}\\{word}({str(count)}).jpg")):
            status = "saved"
        else:
            is_directory(path)
            download_image_from_url(word)
            status = "downloaded"
        return status

    base_dir = is_main_app(word=word)
    status = is_image_downloaded(path=base_dir, word=word)

    return status
