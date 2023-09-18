import os
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# <--- Import or Install Packages --->
try:
    import lxml.html
except ModuleNotFoundError:
    os.popen("pip install lxml")
    import lxml.html


# <--- Get Main Image src url from "GettyImage Web Site" --->

def get_images_from_word(word: str = None) -> str:
    def is_directory(path: str = None):
        if not os.path.isdir(path):
            os.mkdir(path)

    def is_image_downloaded(path: str = None, word: str = None):
        base_path = None
        if os.path.basename(os.path.abspath("./")) != "py":
            base_path = os.path.abspath(f"./resource/img/{word}")
        else:
            base_path = os.path.abspath(f"../img/{word}")
        is_directory(base_path)
        os.path.isfile()

    def download_image_from_url(url: str = None, index: int = None, word: str = None):
        idx = str(index + 1)
        print(f"curl {url} > {word}({idx}).jpg")
        os.system(f"curl -k {url} > {base_path}\\{word}({idx}).jpg")

    url = str()
    keyword = word
    base_url = f"https://www.gettyimagesbank.com/s/?q={keyword}"

    res = requests.get(base_url, verify=False)

    if res.status_code == 200:
        print("  Starting web site crawling...")
        html = res.text
        tree = lxml.html.fromstring(html)
        selectors = tree.cssselect('#tiles > li > a > img')
        src = [img.get("src") for img in selectors]
        for idx, url in enumerate(src[:3]):
            download_image_from_url(url, idx, word)

    return url