# pip install pyqt5 pywin32 pillow pyinstaller tinyaes
import os.path
import sys
from glob import glob
import time

from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QWidget
from PyQt5.QtCore import QTimer, pyqtSignal, QRect

from main_ui import Ui_MainApp as mp
from resource.py import get_images

try:
    os.system("pyuic5 main.ui -o main_ui.py")
except:
    print("  Error happend from 'pyuic5' ")


class MainWindow(QMainWindow, mp):
    resized = pyqtSignal()
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.show()
        self.setWindowTitle("  VisualVoca by Gonyo (Released 2022.12.19.)")
        # self.setWindowIcon(QIcon(":/M1/icon.png"))

        self.word = None
        self.calculate_ratio()

        self.resized.connect(self.resize_widget)
        self.mb_voca_word_adj_1.itemClicked.connect(self.change_voca_title)
        self.mb_voca_word_adj_1.itemClicked.connect(self.change_voca_images)

    def calculate_ratio(self):
        init_x, init_y, init_w, init_h = self.geometry().getRect()
        mbs_x, mbs_y, mbs_w, mbs_h = self.mb_show_adj.geometry().getRect()

        # <--- mb_1 영역의 widget 절대값 기록 --->
        self.mb_show_x = self.mb_show_adj.geometry().getRect()[0]
        self.mb_voca_open_y = self.mb_voca_open.geometry().getRect()[1]
        self.mb_voca_open_h = self.mb_voca_open.geometry().getRect()[3]
        self.mb_voca_open_bottom = init_h - (self.mb_voca_open_y + self.mb_voca_open_h)

        # <--- mb_show_adj 영역의 y 비율 계산 --->
        self.mb_show_eng_adj_ratio_y = self.mb_show_eng_adj.geometry().getRect()[1] / mbs_h
        self.mb_show_eng_adj_ratio_h = self.mb_show_eng_adj.geometry().getRect()[3] / mbs_h

        self.mb_show_image_adj_ratio_y = self.mb_show_image_adj.geometry().getRect()[1] / mbs_h
        self.mb_show_image_adj_ratio_h = self.mb_show_image_adj.geometry().getRect()[3] / mbs_h

        self.mb_show_kor_adj_ratio_y = self.mb_show_kor_adj.geometry().getRect()[1] / mbs_h
        self.mb_show_kor_adj_ratio_h = self.mb_show_kor_adj.geometry().getRect()[3] / mbs_h

        self.mb_show_btns_adj_ratio_y = self.mb_show_btns_adj.geometry().getRect()[1] / mbs_h
        self.mb_show_btns_adj_ratio_h = self.mb_show_btns_adj.geometry().getRect()[3] / mbs_h

    def resize_widget(self):
        # Change widget size when window resized event emitted
        x, y, w, h = self.geometry().getRect()

        self.resize_widget_setting(self.mb_1, w=w, h=h)

        self.resize_widget_setting(self.mb_voca_adj, h=h)
        self.resize_widget_setting(self.mb_voca_scroll, h=h)
        # self.resize_widget_setting(self.mb_voca_word_adj_1, h=h)
        self.resize_widget_setting(self.mb_voca_open, h=h)

        self.resize_widget_setting(self.mb_show_adj, w=w, h=h)
        self.resize_widget_setting(self.mb_show_eng_adj, w=w, h=h)
        self.resize_widget_setting(self.mb_show_image_adj, w=w, h=h)
        self.resize_widget_setting(self.mb_show_kor_adj, w=w, h=h)
        self.resize_widget_setting(self.mb_show_btns_adj, w=w, h=h)
        
    def resize_widget_setting(self, obj, w: int = None, h: int = None):
        # get parent geometry
        _x, _y, _w, _h = obj.geometry().getRect()

        if 'mb_voca' in obj.objectName():
            _h = h - _y
            if 'mb_voca_word_adj' in obj.objectName():
                _h = _h - self.mb_voca_open_h - self.mb_voca_open_bottom
            elif 'mb_voca_open' in obj.objectName():
                _y = h - self.mb_voca_open_h - self.mb_voca_open_bottom
                _h = self.mb_voca_open_h

        if 'mb_show' in obj.objectName():
            if w is not None:
                _w = (w - self.mb_show_x)

            if h is not None:
                if 'mb_show_adj' in obj.objectName():
                    _h = h
                elif 'mb_show_eng_adj' in obj.objectName():
                    _y = int(h * self.mb_show_eng_adj_ratio_y)
                    _h = int(h * self.mb_show_eng_adj_ratio_h)
                elif 'mb_show_image_adj' in obj.objectName():
                    _y = int(h * self.mb_show_image_adj_ratio_y)
                    _h = int(h * self.mb_show_image_adj_ratio_h)
                elif 'mb_show_kor_adj' in obj.objectName():
                    _y = int(h * self.mb_show_kor_adj_ratio_y)
                    _h = int(h * self.mb_show_kor_adj_ratio_h)
                elif 'mb_show_btns_adj' in obj.objectName():
                    _y = int(h * self.mb_show_btns_adj_ratio_y)
                    _h = int(h * self.mb_show_btns_adj_ratio_h)

        obj.setGeometry(QRect(_x, _y, _w, _h))

    def change_voca_title(self):
        self.word = self.mb_voca_word.currentItem().text()
        self.mb_show_eng.setText(self.word)

    def change_voca_images(self):
        status = get_images.get_images_from_word(self.word)
        print(status)

        self.pics = [QPixmap(item) for item in glob(f"./resource/img/{self.word}/*.jpg")]

        for pic in self.pics:
            self.mb_show_image.clear()
            self.mb_show_image.setPixmap(pic)
            time.sleep(2)
            self.mb_show_image.repaint()

    def resizeEvent(self, event):
        self.resized.emit()
        return super(MainWindow, self).resizeEvent(event)


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
