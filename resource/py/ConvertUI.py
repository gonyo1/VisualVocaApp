# coding=utf-8

import os


def get_ui_python_file(dev_mode:bool = False, path: str = None):
    if dev_mode is True:
        try:
            os.system(f"pyuic5 {path}/src/ui/main.ui -o {path}/src/ui/main_ui2.py")
            os.system(f"pyuic5 {path}/src/ui/updater.ui -o {path}/src/ui/updater_ui.py")

            print("  [Info] pyuic5 has done...")
            # os.system("pyrcc5 main.qrc -o main_rc.py")
        except FileNotFoundError:
            print("  [Error] Error happened from 'pyuic5 or pyrcc5' ")
    return dev_mode