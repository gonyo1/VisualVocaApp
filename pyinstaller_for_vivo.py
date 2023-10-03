# coding=utf-8

import os

PyinstallerArgs = " ".join(['--icon=./resource/src/img/Appicon.ico',
                            '--add-data="./resource/py;./resource/py"',
                            '--add-data="./resource/src/font;./resource/src/font"',
                            '--add-data="./resource/src/img;./resource/src/img"',
                            '--add-data="./resource/src/sound;./resource/src/sound"',
                            '--add-data="./resource/src/ui;./resource/src/ui"',
                            '--add-data="./resource/src/img;./resource/src/img"',
                            '--name=VisualVoca',
                            '--log-level=WARN',
                            'launcher.py',
                            '-F'
                            ])
path = os.path.abspath(".").replace("\\", "/")
print(path)

os.system(f"cd {path}")
os.system(f"pyinstaller {PyinstallerArgs}")