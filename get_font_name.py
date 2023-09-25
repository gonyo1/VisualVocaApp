import os
from fontTools import ttLib

file = os.path.abspath("./resource/src/font/NotoSansKR-SemiBold.ttf")
with open(file, 'r') as f:
    print(f.readlines(encodings='cp949'))