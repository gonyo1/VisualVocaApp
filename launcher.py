# coding=utf-8

import sys
import os.path
import json
import requests
import zipfile
from glob import glob
from fontTools import ttLib
from PyQt5 import QtWidgets, QtCore, QtGui, Qt


# Import Local Python Files
from resource.py.Path import get_root_directory, get_paths
from resource.py.ConvertUI import get_ui_python_file as convert
from resource.src.ui.updater_ui import Ui_Dialog as LauncherUI
from resource.py.ChangeStylesheet import change_stylesheet
from resource.py.Json import load_json_file, save_json_file

__dir__ = get_root_directory()
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
            resource_base_directory = os.path.join(get_paths()[1], "resource").replace("\\", "/")

            if os.path.isdir(resource_base_directory):
                print(f"  >> move {resource_base_directory} {exe_base_directory}")
                os.system(f"move {resource_base_directory} {exe_base_directory}")
            else:
                print(f"  >> mkdir {exe_base_directory}")
                os.mkdir(exe_base_directory)

    # Make CSV file
    path = os.path.abspath(os.path.join(__dir__, "voca/WordList.csv")).replace("\\", "/")
    if not os.path.isfile(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)

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
        # Get github raw zip file
        output_path = os.path.dirname(os.path.abspath(__dir__))
        url = "https://raw.githubusercontent.com/gonyo1/VisualVocaApp/main/update/resource.zip"
        req = requests.get(url)

        # Save zip to local
        filename = os.path.join(output_path, url.split('/')[-1])
        with open(filename, 'wb') as file:
            file.write(req.content)
        print('  [Info] Downloading Completed')

        # Backup User Json file
        origin_name = os.path.join(output_path, "resource/src/config.json")
        modified_name = os.path.join(output_path, "resource/src/config_user.json")
        os.rename(origin_name, modified_name)

        # Extract and Erase files
        zipfile.ZipFile(filename).extractall(output_path)
        os.remove(filename)

        # Change downloaded json to user json except version
        version = github_data["Version"]

        # Just in case if developer missed version data..
        save_json_file(key="Version", value=version, name="config.json")

        user_json = load_json_file("config_user.json")
        for key in ["FontFamily",
                    "BookmarkIndex",
                    "AutoScroll",
                    "ImageDownCount",
                    "LanguagesShow",
                    "LanguagesSpeech",
                    "APIKeys",
                    "GetImageFromURL"]:
            value = user_json[key]
            save_json_file(key=key, value=value, name="config.json")

        os.remove(modified_name)
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
        self.set_font_family()
        self.setup_graphic_part()
        self.check_updates()
        self.set_signal()

    def set_font_family(self):
        def grab_ttf_file() -> list:
            return glob(os.path.abspath(f"{__dir__}/src/font/*.ttf"))

        def get_font_name(font_path: str = None) -> str:
            font = ttLib.TTFont(font_path)
            font_family_name = font['name'].getDebugName(1)
            # fullName = font['name'].getDebugName(4)

            return font_family_name

        def del_special_character(font: str = None) -> str:
            font = font.replace("-", "")
            font = font.replace("_", "")
            font = font.replace(" ", "")
            font = font.lower()

            return font

        # Make Font Database
        fontDB = Qt.QFontDatabase()

        # Get font name by JSON_DATA
        font_path = None
        font_name = None
        font_file_list = grab_ttf_file()
        user_target_font = self.JSON_DATA['FontFamily']

        try:
            # Check if PC has a font that user want to set as font family
            modified_font_name = del_special_character(user_target_font)
            font_file_name = [del_special_character(os.path.basename(item).replace(".ttf", "")) for item in
                              font_file_list]

            # Find User Target Font
            idx = font_file_name.index(modified_font_name)
            font_path = font_file_list[idx]
            font_name = get_font_name(font_path)
            print(f"  [Info] Font changed Successfully to User font:{font_name}")

        except Exception as e:
            # Set font as Noto Sans KR Semi Bold if error happened
            base_name = f"{__dir__}/src/font/NotoSansKR-SemiBold"
            font_path = ".".join([base_name, "ttf"])
            font_name = "Noto Sans KR SemiBold"
            print(f"  [Error] Error happened while getting font name: {e}")

        fontDB.addApplicationFont(os.path.abspath(font_path))

        # Customize font family
        self.setFont(QtGui.QFont(font_name))
        custom_stylesheet = self.styleSheet()
        custom_stylesheet = custom_stylesheet.replace("Noto Sans KR SemiBold", font_name)
        self.setStyleSheet(custom_stylesheet)

    def setup_graphic_part(self):

        def round_corners():
            radius = 9.0
            path = QtGui.QPainterPath()
            path.addRoundedRect(QtCore.QRectF(self.rect()), radius, radius)
            mask = QtGui.QRegion(path.toFillPolygon().toPolygon())
            self.setMask(mask)

        def set_updator_image():
            background_image = f"url('{os.path.join(__dir__, 'src/img/UpdateImage.svg')}')".replace("\\", "/")
            stylesheet = change_stylesheet(parent_widget=self,
                                           obj_name="UpdaterBackground",
                                           background_image=background_image)

            # Set StyleSheet
            self.setStyleSheet(stylesheet)

        # Setup Graphic Part
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setWindowIcon(Qt.QIcon("resource/src/img/AppIcon.ico"))

        # Window shape setting
        set_updator_image()
        round_corners()

    def check_updates(self):
        def get_github_json():
            global github_data
            # Github의 Contributor.json 파일을 다운로드하여 github.json에 저장
            url = 'https://raw.githubusercontent.com/gonyo1/VisualVocaApp/main/update/contributor.json'
            resp = requests.get(url)
            github_data = json.loads(resp.text)

            with open(os.path.abspath("./resource/src/github.json"), 'wt') as f:
                f.write(resp.text)

        def check_version():
            if float(github_data["Version"]) != float(self.JSON_DATA["Version"]):
                self.UpdaterState.setText("Visual Voca 업데이트가 있습니다")
                self.UpdaterState.setStyleSheet("color: tomato;\nfont: 14px;")
                self.__update_check__ = True
            else:
                self.UpdaterState.setText("Visual Voca가 최신 버전입니다")
                self.UpdateSkip.deleteLater()
                self.UpdateDo.setText("Start")
                # self.timer.singleShot(500, lambda txt="Main APP이 실행됩니다...": self.UpdaterState.setText(txt))
                # self.timer.singleShot(2000, self.UpdateDo.click)
                self.__update_check__ = False

            return self.__update_check__

        def is_force_stop():
            if github_data["ForceStop"] == "True":
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

        if github_data["ForceStop"] == "True":
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
