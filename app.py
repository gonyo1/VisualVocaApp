# pip install pyqt5 pywin32 pillow pyinstaller tinyaes
import os.path
import sys
from glob import glob
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QWidget
from PyQt5.QtCore import QTimer
from main_ui import Ui_MainApp as mp
from resource.py import get_images

try:
    os.system("pyuic5 main.ui -o main_ui.py")
except:
    print("  Error happend from 'pyuic5' ")

class MainWindow(QMainWindow, mp):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.show()
        self.setWindowTitle("  AutoSignature by Gonyo (Released 2022.12.19.)")
        # self.setWindowIcon(QIcon(":/M1/icon.png"))

        self.show_images()
        self.mb_voca_word.itemClicked.connect(self.clicked)

    def clicked(self):
        word = self.mb_voca_word.currentItem().text()
        self.mb_show_eng.setText(word)
        get_images.get_images_from_word(word)
        self.show_images()

    def show_images(self):
        timer = QTimer(self)
        timer.timeout.connect(self.next_image)
        timer.start(3000)
        self.pics = [QPixmap(item) for item in glob(f"./resource/img/jump/*.jpg")]
        self.image_index = 0

    def next_image(self):
        if self.image_index < len(self.pics):
            self.mb_show_image.setPixmap(self.pics[self.image_index])
            self.image_index += 1

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec_())


"""
pyuic5 main.ui -o main_ui.py
pyrcc5 ./AutoSigner/main.qrc -o ./AutoSigner/main_rc.py
pyinstaller -w -F --log-level=WARN --hidden-import AutoSigner/main_ui.py --hidden-import AutoSigner/main_rc.py --icon=./AutoSigner/icon.ico "AutoSig.exe" ./AutoSigner/main.py
pyinstaller -w -F --log-level=WARN --hidden-import ./AutoSigner/main_ui.py --hidden-import ./AutoSigner/main_rc.py --icon=./AutoSigner/icon.ico main.py
pyinstaller -w -F --log-level=WARN --hidden-import AutoSigner/main_ui.py --hidden-import AutoSigner/main_rc.py --icon=./AutoSigner/icon.ico main.py
pyinstaller -w -F --log-level=WARN --hidden-import AutoSigner/main_ui.py --icon=./AutoSigner/icon.ico main.py
pyinstaller -w -F --log-level=WARN --hidden-import ./AutoSigner/main_ui --icon=./AutoSigner/icon.ico main.py
"""
