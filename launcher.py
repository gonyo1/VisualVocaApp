import sys
import os.path
import json
import requests
from glob import glob
from fontTools import ttLib
from PyQt5 import QtWidgets, QtCore, QtGui, Qt, QtMultimedia

from resource.src.ui.updater_ui import Ui_Dialog as subp

# Import Local Python Files
from resource.py import GetImages
from resource.py import GetAudio
from resource.py.Translator import translate, search_text_by_lang
from resource.py.ToggleButton import AnimatedToggle
from resource.py.Json import load_json_file, save_json_file, generate_init
from resource.py.CSVData import get_main_csv
from resource.py.ConvertUI import get_ui_python_file as convert


__author__ = 'https://www.github.com/gonyo1'
__released_date__ = 'October 2023'
__credits__ = ['Gonyo', 'AhnJH']
__version__ = '1.0'

class AppUpdator(QtWidgets.QDialog, subp):
    """This class automatically updates a PyQt app from a remote
    Gonyo1's VisualVocaApp repository
    # Mercurial repository.
    """
    def __init__(self, parent=None):
        # Overloading MainWindow
        super(AppUpdator, self).__init__(parent)
        self.setupUi(self)
        self.show()
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)

        # Setup Graphic Part
        self.setWindowTitle(f"  VisualVoca Launcher (Ver.{__version__})")
        self.setWindowIcon(Qt.QIcon("resource/src/img/AppIcon.ico"))

        # Function Part
        self.get_github_json()
        self.check_version()
        self.round_corners()
        self.set_signal()

    def round_corners(self):
        radius = 9.0
        path = QtGui.QPainterPath()
        path.addRoundedRect(QtCore.QRectF(self.rect()), radius, radius)
        mask = QtGui.QRegion(path.toFillPolygon().toPolygon())
        self.setMask(mask)

    def set_signal(self):
        self.UpdateDo.clicked.connect(self.open_main_app)
        self.UpdateSkip.clicked.connect(self.open_main_app)
        self.close_.clicked.connect(self.close)
        self.minimize_.clicked.connect(self.showMinimized)

    def check_version(self):
        if float(github_data["Version"]) != float(__version__):
            self.UpdaterState.setText("Visual Voca 업데이트가 있습니다")
        else:
            self.UpdaterState.setText("Visual Voca가 최신 버전입니다")
            self.UpdateSkip.deleteLater()
            self.UpdateDo.setText("Start")

    def update(self):
        url = "pass"

    def open_main_app(self):
        self.close()
        main_app = os.system(f"python {os.path.abspath('resource/py/app.py')}")

    def get_github_json(self):
        global github_data

        url = 'https://raw.githubusercontent.com/gonyo1/VisualVocaApp/main/contributor.json'
        resp = requests.get(url)
        github_data = json.loads(resp.text)

        with open(os.path.abspath("./resource/src/github.txt"), 'w') as f:
            f.write(resp.text)


if __name__ == "__main__":

    def make_dir():
        # Make root directory
        for dir in ["resource", "resource/py",
                    "resource/src", "resource/src/font", "resource/src/img", "resource/src/ui",
                    "resource/voca", "resource/voca/img", "resource/voca/tts"]:
            _dir = os.path.abspath(dir)
            if not os.path.isdir(_dir):
                os.mkdir(_dir)

        # Make json file
        path = os.path.abspath("resource/src/config.json")
        if not os.path.isfile(path):
            generate_init(path)

        # Make CSV file
        path = os.path.abspath("resource/voca/WordList.csv")
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


    # Convert .ui to .py
    make_dir()

    # Run main app
    app = QtWidgets.QApplication(sys.argv)
    main_win = AppUpdator()
    main_win.show()
    sys.exit(app.exec_())
