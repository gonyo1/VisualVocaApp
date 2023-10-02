import os


def get_ui_python_file(dev_mode:bool = False):
    if dev_mode is True:
        try:
            os.system("pyuic5 ./resource/src/ui/main.ui -o ./resource/src/ui/main_ui2.py")
            os.system("pyuic5 ./resource/src/ui/updater.ui -o ./resource/src/ui/updater_ui.py")

            print("  [Info] pyuic5 has done...")
            # os.system("pyrcc5 main.qrc -o main_rc.py")
        except FileNotFoundError:
            print("  [Error] Error happened from 'pyuic5 or pyrcc5' ")
    return dev_mode