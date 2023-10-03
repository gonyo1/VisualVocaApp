import sys
import os.path
import json
import requests
from PyQt5 import QtWidgets, QtCore, QtGui, Qt

from resource.src.ui.updater_ui import Ui_Dialog as LauncherUI

# Import Local Python Files
from resource.py.Application import MainWindow
from resource.py.Json import generate_init, load_json_file
from resource.py.ConvertUI import get_ui_python_file as convert


__author__ = 'https://www.github.com/gonyo1'
__released_date__ = 'October 2023'
update_check = False


class UpdateDownloader(QtCore.QObject):
    signal = QtCore.pyqtSignal()

    def update(self):
        print("  [Info] Updated python file is downloading...")
        url = "https://raw.githubusercontent.com/gonyo1/VisualVocaApp/main/resource/py/Application.py"
        resp = requests.get(url)

        with open(os.path.abspath("resource/py/Application.py"), 'w') as f:
            f.write(resp.text)
        print("  [Info] Updated python file has been finished !")
        self.signal.emit()

    def no_update(self):
        self.signal.emit()


class AppUpdator(QtWidgets.QDialog, LauncherUI):
    """This class automatically updates a PyQt app from a remote
    Gonyo1's VisualVocaApp repository
    # Mercurial repository.
    """
    UPDATECLASS = UpdateDownloader()
    JSON_DATA = load_json_file()

    def __init__(self, parent=None):
        # Overloading MainWindow
        super(AppUpdator, self).__init__(parent)
        self.setupUi(self)
        self.show()

        # Make necessary folder
        self.make_necessary()

        # Function Part
        self.setup_graphic_part()
        self.check_updates()
        self.set_signal()

    @staticmethod
    def make_necessary():
        # Make root directory
        for directory in ["resource", "resource/py",
                          "resource/src", "resource/src/font", "resource/src/img", "resource/src/ui",
                          "resource/voca", "resource/voca/img", "resource/voca/tts"]:
            directory = os.path.abspath(directory).replace("\\", "/")
            if not os.path.isdir(directory):
                os.mkdir(directory)

        # Make json file
        path = os.path.abspath("resource/src/config.json").replace("\\", "/")
        if not os.path.isfile(path):
            generate_init(path)

        # Make CSV file
        path = os.path.abspath("resource/voca/WordList.csv").replace("\\", "/")
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
                     "Transportation,car,자동차\n",
                     ]
                )

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
            url = 'https://raw.githubusercontent.com/gonyo1/VisualVocaApp/main/contributor.json'
            resp = requests.get(url)
            self.github_data = json.loads(resp.text)

            with open(os.path.abspath("./resource/src/github.json"), 'wt') as f:
                f.write(resp.text)

        def check_version():
            if float(self.github_data["Version"]) != float(self.JSON_DATA["Version"]):
                self.UpdaterState.setText("Visual Voca 업데이트가 있습니다")
                update_check = True
            else:
                self.UpdaterState.setText("Visual Voca가 최신 버전입니다")
                self.UpdateSkip.deleteLater()
                self.UpdateDo.setText("Start")
                update_check = False

            return update_check

        get_github_json()
        check_version()

    def set_signal(self):
        def move_next_page():
            if update_check:
                self.UPDATECLASS.update()
            else:
                self.UPDATECLASS.no_update()

        def open_main_app():
            # [방법1] cmd 명령어로 실행: main_app = os.system(f"python {os.path.abspath(f'resource/py/{filename}.py')}")

            # [방법 2] MainWindow 객체를 불러와 실행
            main_app = MainWindow()
            main_app.show()
            self.close()

        self.UpdateDo.clicked.connect(move_next_page)
        self.UPDATECLASS.signal.connect(open_main_app)
        self.UpdateSkip.clicked.connect(open_main_app)

        self.close_.clicked.connect(self.close)
        self.minimize_.clicked.connect(self.showMinimized)



if __name__ == "__main__":

    # Set False when compile to exe file
    convert = convert(dev_mode=True)

    # Run main app
    app = QtWidgets.QApplication(sys.argv)
    main_win = AppUpdator()
    main_win.show()
    sys.exit(app.exec_())