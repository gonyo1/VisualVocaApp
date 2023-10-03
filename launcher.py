# coding=utf-8

import sys
import os.path
import json
import requests
import zipfile
from PyQt5 import QtWidgets, QtCore, QtGui, Qt

# Import Local Python Files
from resource.src.ui.updater_ui import Ui_Dialog as LauncherUI
from resource.py.Json import load_json_file
from resource.py.Path import get_root_directory, get_paths
from resource.py.ConvertUI import get_ui_python_file as convert


__dir__ = get_root_directory()
__exepath__, __internalpath__ = get_paths()
__author__ = 'https://www.github.com/gonyo1'
__released_date__ = 'October 2023'


# Make necessary folder
def make_necessary():
    # Make root directory
    for directory in [".", "./py",
                      "./src", "./src/font", "./src/img", "./src/ui",
                      "./voca", "./voca/img", "./voca/tts"]:
        exe_base_directory = os.path.abspath(os.path.join(__dir__, directory)).replace("\\", "/")

        if not os.path.isdir(exe_base_directory):
            resource_base_directory = "/".join([__internalpath__, directory.replace(".", "resource")])

            if os.path.isdir(resource_base_directory):
                print(f"  >> move {resource_base_directory} {exe_base_directory}")
                os.system(f"move {resource_base_directory} {exe_base_directory}")
            else:
                print(f"  >> mkdir {exe_base_directory}")
                os.mkdir(exe_base_directory)

    # Make json file
    path = os.path.abspath(os.path.join(__dir__, "src/config.json")).replace("\\", "/")
    if not os.path.isfile(path):
        load_json_file(path)

    # Make CSV file
    path = os.path.abspath(os.path.join(__dir__, "voca/WordList.csv")).replace("\\", "/")
    if not os.path.isfile(path):
        with open(path, 'w') as f:
            f.writelines(
                ["GroupName,en,ko\n",
                 "Fruit,apple,사과\n",
                 "Fruit,avocado,아보카도\n",
                 "Fruit,banana,바나나\n",
                 "Fruit,blackberry,블랙베리\n",
                 "Animals,Polar bear,북극곰\n",
                 "Animals,dog,개\n",
                 "Animals,Turtle,거북이\n",
                 "Transportation,bicycle,자전거\n",
                 "Transportation,bus,버스\n",
                 "Transportation,car,자동차"
                 ]
            )
make_necessary()

class UpdateDownloader(QtCore.QObject):
    signal = QtCore.pyqtSignal()
    __update_check__ = False

    def update(self):
        print("  [Info] Updated python file is downloading...")
        output_path = os.path.abspath(__dir__)
        url = "https://raw.githubusercontent.com/gonyo1/VisualVocaApp/main/update/resource.zip"
        req = requests.get(url)

        # Split URL to get the file name
        filename = os.path.join(output_path, url.split('/')[-1])

        # Writing the file to the local file system
        with open(filename, 'wb') as file:
            file.write(req.content)
        print('  [Info] Downloading Completed')

        zipfile.ZipFile(filename).extractall(output_path)

        print("  [Info] Updated python file has been finished !")
        self.signal.emit()

    def no_update(self):
        self.signal.emit()


class Launcher(QtWidgets.QDialog, LauncherUI):
    """This class automatically updates a PyQt app from a remote
    Gonyo1's VisualVocaApp repository
    # Mercurial repository.
    """
    UPDATECLASS = UpdateDownloader()
    JSON_DATA = load_json_file()

    def __init__(self, parent=None):
        # Overloading MainWindow
        super(Launcher, self).__init__(parent)
        self.setupUi(self)
        self.show()

        # Function Part
        self.setup_graphic_part()
        self.check_updates()
        self.set_signal()

    def setup_graphic_part(self):

        def round_corners():
            radius = 9.0
            path = QtGui.QPainterPath()
            path.addRoundedRect(QtCore.QRectF(self.rect()), radius, radius)
            mask = QtGui.QRegion(path.toFillPolygon().toPolygon())
            self.setMask(mask)

        # Setup Graphic Part
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setWindowIcon(Qt.QIcon("resource/src/img/AppIcon.ico"))

        # Window shape setting
        round_corners()

    def check_updates(self):
        def get_github_json():
            # Github의 Contributor.json 파일을 다운로드하여 github.json에 저장
            url = 'https://raw.githubusercontent.com/gonyo1/VisualVocaApp/main/update/contributor.json'
            resp = requests.get(url)
            self.github_data = json.loads(resp.text)

            with open(os.path.abspath("./resource/src/github.json"), 'wt') as f:
                f.write(resp.text)

        def check_version():
            if float(self.github_data["Version"]) != float(self.JSON_DATA["Version"]):
                self.UpdaterState.setText("Visual Voca 업데이트가 있습니다")
                self.UpdaterState.setStyleSheet("color: tomato;\nfont: 14px;")
                self.__update_check__ = True
            else:
                self.UpdaterState.setText("Visual Voca가 최신 버전입니다")
                self.UpdateSkip.deleteLater()
                self.UpdateDo.setText("Start")
                self.__update_check__ = False

            return self.__update_check__

        def is_force_stop():
            if self.github_data["ForceStop"] == "True":
                self.UpdaterState.setText("Visual Voca 서비스가 중단되었습니다.")
                self.UpdaterState.setStyleSheet("color: tomato;\nfont: 14px;")
                self.UpdateSkip.deleteLater()
                self.UpdateDo.setText("Exit")

        get_github_json()
        check_version()
        is_force_stop()

    def set_signal(self):
        def move_next_page():
            if self.__update_check__:
                self.UPDATECLASS.update()
            else:
                self.UPDATECLASS.no_update()

        def open_main_app():
            from resource.py.Application import MainWindow
            # [방법1] cmd 명령어로 실행: main_app = os.system(f"python {os.path.abspath(f'resource/py/{filename}.py')}")

            # [방법 2] MainWindow 객체를 불러와 실행
            main_app = MainWindow()
            main_app.show()
            self.close()

        if self.github_data["ForceStop"] == "True":
            self.UpdateDo.clicked.connect(self.close)
        else:
            self.UpdateDo.clicked.connect(move_next_page)

        self.UPDATECLASS.signal.connect(open_main_app)
        self.UpdateSkip.clicked.connect(open_main_app)

        self.close_.clicked.connect(self.close)
        self.minimize_.clicked.connect(self.showMinimized)



if __name__ == "__main__":
    # Set False when compile to exe file
    convert = convert(dev_mode=True, path=__dir__)

    # Run main app
    app = QtWidgets.QApplication(sys.argv)
    main_win = Launcher()
    main_win.show()
    sys.exit(app.exec_())
