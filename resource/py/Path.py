import os
import sys
def get_paths():
    if getattr(sys, 'frozen', False):
        APPLICATION_EXE_DIR = os.path.dirname(sys.executable)
        APPLICATION_DATA_DIR = sys._MEIPASS
    else:
        APPLICATION_EXE_DIR = os.path.dirname(os.path.abspath(__file__))
        APPLICATION_DATA_DIR = APPLICATION_EXE_DIR

    APPLICATION_EXE_DIR = os.path.abspath(APPLICATION_EXE_DIR)
    APPLICATION_DATA_DIR = os.path.abspath(APPLICATION_DATA_DIR)

    # Python Executed from IDEs (ex: pycharm)
    if os.path.basename(APPLICATION_EXE_DIR) == "py":
        APPLICATION_EXE_DIR = os.path.abspath("./")
        APPLICATION_DATA_DIR = os.path.abspath("./")


    print(f"  [Info] APPLICATION_EXE_DIR: {APPLICATION_EXE_DIR}\n"
          f"         APPLICATION_DATA_DIR: {APPLICATION_DATA_DIR}")

    return APPLICATION_EXE_DIR, APPLICATION_DATA_DIR


def get_root_directory():
    EXEPATH, INTERNALDATAPATH = get_paths()
    root_directory = os.path.basename(os.path.abspath("./"))

    if root_directory != "resource":
        # if Application.py called from Launcher.py
        path = os.path.abspath(os.path.join(EXEPATH, "resource"))
        path = path.replace("\\", "/")
        return path

    elif root_directory == "resource":
        # if Application.py called from itself
        path = os.path.join(root_directory, "resource")
        path = path.replace("\\", "/")
        return path
