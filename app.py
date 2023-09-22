# pip install pyqt5 pywin32 pillow pyinstaller tinyaes
import os.path
import sys
from glob import glob
import time

from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QListWidget, QFileDialog, QWidget, QCheckBox
from PyQt5.QtCore import QTimer, pyqtSignal, QRect, QBuffer
from PyQt5 import QtMultimedia

from resource.py import get_images
from resource.py import audio
from resource.py.toggle import Toggle, AnimatedToggle

from main_ui import Ui_MainApp as mp

try:
    os.system("pyuic5 main.ui -o main_ui.py")
    # os.system("pyrcc5 main.qrc -o main_rc.py")
except FileNotFoundError:
    print("  Error happend from 'pyuic or pyrcc' ")


class MainWindow(QMainWindow, mp):
    resized = pyqtSignal()

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.show()
        self.setWindowTitle("  VisualVoca by Gonyo (Released 2023.9.00.)")
        self.setWindowIcon(QIcon("resource/src/app_icon.png"))
        self.mb_icon.setPixmap(QPixmap('resource/src/logo.svg'))

        self.is_variable()
        self.is_signal()
        self.make_gui_widget()

    def is_variable(self):
        self.word = None
        self.pics = None
        self.focused_listwidget = None
        self.auto_slide = True
        self.slideshow_time = 1000
        self.image_idx = 0

        self.timer = QTimer(self)
        self.ani_toggle = QCheckBox(self)
        self.calculate_ratio()

        self.player = QtMultimedia

    def is_signal(self):
        # window resized event
        self.resized.connect(self.resize_widget)

        # voca word clicked event on QListWidget
        self.list_widgets = self.findChildren(QListWidget)
        for widget in self.list_widgets:
            widget.currentRowChanged.connect(lambda: self.change_mb_voca_widget(obj=widget))
            widget.currentRowChanged.connect(lambda: self.get_audio_tts(voca=self.word))
        self.timer.timeout.connect(lambda: self.change_mb_voca_image(idx=self.image_idx))

    def calculate_ratio(self):
        init_x, init_y, init_w, init_h = self.geometry().getRect()
        mbs_x, mbs_y, mbs_w, mbs_h = self.mb_show_adj.geometry().getRect()

        # <--- mb_1 영역의 widget 절대값 기록 --->
        self.mb_show_x = self.mb_show_adj.geometry().getRect()[0]
        self.mb_voca_open_y = self.mb_voca_open.geometry().getRect()[1]
        self.mb_voca_open_h = self.mb_voca_open.geometry().getRect()[3]
        self.mb_show_eng_h = self.mb_show_eng_adj.geometry().getRect()[3]
        self.mb_show_kor_h = self.mb_show_kor_adj.geometry().getRect()[3]
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

    def make_gui_widget(self):
        def make_toggle_button(parent):
            self.ani_toggle = AnimatedToggle(
                checked_color="#4ed164"
            )
            parent.mb_top_bar_onoff_verticalLayout.addWidget(self.ani_toggle)

            self.ani_toggle.setChecked(True)

        make_toggle_button(self)

    # <-- New Voca Clicked Event Handler --------------------------------------------------->
    def change_mb_voca_widget(self, obj):
        # save obj and variables
        self.word = obj.currentItem().text()
        self.focused_listwidget = obj

        # reset index of image
        self.image_idx = 0
        self.timer.stop()
        self.timer.start(0)

        # Start slide show timer
        self.timer.start(self.slideshow_time)


        # Change image
        status = get_images.get_images_from_word(self.word)
        self.pics = [QPixmap(item) for item in glob(f"./resource/voca/img/{self.word}/*.jpg")]

        # Change voca title
        self.mb_show_eng_adj.setText(self.word)



    def change_mb_voca_image(self, idx):
        # Start timer to slide second to end image
        self.timer.stop()
        self.timer.start(1000)
        # add image_idx
        if idx >= len(self.pics):
            self.timer.stop()
            self.move_next_voca()
        else:
            # Get image and change pixmap
            pic = self.pics[idx]

            self.mb_show_image_adj.clear()
            self.mb_show_image_adj.setPixmap(pic)
            self.mb_show_image_adj.repaint()

            self.image_idx += 1

    def move_next_voca(self):
        idx = self.focused_listwidget.currentRow()

        if idx < self.focused_listwidget.count() - 1:
            idx = idx + 1
            self.focused_listwidget.setCurrentRow(idx)
        else:
            print("last word")

    def get_audio_tts(self, voca: str = None, lang: str = None):
        self.audio_path = audio.get_tts(word=voca, lang='en')

        tts = self.player.QSound(self.audio_path)
        print(tts)
        print(self.audio_path)
        tts.play()

    # <-- Resize Event Handler ------------------------------------------------------------->
    def resize_widget(self):
        @staticmethod
        def calculate_font_ratio(obj, origin) -> int:
            font_size = None

            # Calculate resized height ratio
            resized_h = obj.geometry().getRect()[3]
            origin_h = origin

            # Get Original font size
            origin_font_size = origin_h - 31
            resized_font_size = origin_font_size * (resized_h / origin_h)
            font_size = int(resized_font_size)
            font_size = str(font_size) + 'px'

            return font_size

        def resize_widget_setting(parent, obj, w: int = None, h: int = None):
            # get parent geometry
            _x, _y, _w, _h = obj.geometry().getRect()

            if 'mb_voca' in obj.objectName():
                _h = h - _y
                if 'mb_voca_word_adj' in obj.objectName():
                    _h = _h - parent.mb_voca_open_h - parent.mb_voca_open_bottom
                elif 'mb_voca_open' in obj.objectName():
                    _y = h - parent.mb_voca_open_h - parent.mb_voca_open_bottom
                    _h = parent.mb_voca_open_h

            elif 'mb_show' in obj.objectName():
                if w is not None:
                    _w = (w - parent.mb_show_x)

                if h is not None:
                    if 'mb_show_adj' in obj.objectName():
                        _h = h
                    elif 'mb_show_eng_adj' in obj.objectName():
                        _y = int(h * parent.mb_show_eng_adj_ratio_y)
                        _h = int(h * parent.mb_show_eng_adj_ratio_h)
                    elif 'mb_show_image_adj' in obj.objectName():
                        _y = int(h * parent.mb_show_image_adj_ratio_y)
                        _h = int(h * parent.mb_show_image_adj_ratio_h)
                    elif 'mb_show_kor_adj' in obj.objectName():
                        _y = int(h * parent.mb_show_kor_adj_ratio_y)
                        _h = int(h * parent.mb_show_kor_adj_ratio_h)
                    elif 'mb_show_btns_adj' in obj.objectName():
                        _y = int(h * parent.mb_show_btns_adj_ratio_y)
                        _h = int(h * parent.mb_show_btns_adj_ratio_h)

            obj.setGeometry(QRect(_x, _y, _w, _h))

        def change_stylesheet(parent, obj, **kwargs):
            """
            대부분 폰트 사이즈를 윈도우 창 크기에 맞추어 바꾸도록 제작됨
            kwargs는 font=14px 와 같이 stylesheet에 즉시 적용될 수 있을 수준으로 작성 되어야 함
            """

            # Get Object name
            parent_widget = None
            obj_name = obj.objectName()

            if 'mb_show' in obj_name:
                parent_widget = parent.mb_show_adj
            elif 'mb_voca' in obj_name:
                parent_widget = parent.mb_voca_adj

            # Find target selector
            stylesheet = parent_widget.styleSheet()
            start = stylesheet.find("".join(["#", obj_name, " ", "{"]))
            end = start + stylesheet[start:].find("}")

            crop_stylesheet = stylesheet[start:end]

            # Change stylesheet by kwargs
            for key, value in kwargs.items():
                new_start = crop_stylesheet.find(str(key + ":"))
                new_end = crop_stylesheet.find(";")

                new_css = "".join([key, ": ", value, ";\n"])
                stylesheet = "". join([stylesheet[:start],
                                       crop_stylesheet[:new_start],
                                       new_css,
                                       crop_stylesheet[new_end:],
                                       stylesheet[end:]])

            # Set StyleSheet
            parent_widget.setStyleSheet(stylesheet)

        # Change widget size when window resized event emitted
        x, y, w, h = self.geometry().getRect()

        # Window Section
        resize_widget_setting(self, self.mb_1, w=w, h=h)

        # Left - Side Bar Section
        resize_widget_setting(self, self.mb_voca_adj, h=h)
        resize_widget_setting(self, self.mb_voca_scroll, h=h)
        resize_widget_setting(self, self.mb_voca_open, h=h)

        # Right - Main Showing Section
        resize_widget_setting(self, self.mb_show_top_bar, w=w)
        resize_widget_setting(self, self.mb_show_adj, w=w, h=h)
        resize_widget_setting(self, self.mb_show_eng_adj, w=w, h=h)
        resize_widget_setting(self, self.mb_show_image_adj, w=w, h=h)
        resize_widget_setting(self, self.mb_show_kor_adj, w=w, h=h)
        resize_widget_setting(self, self.mb_show_btns_adj, w=w, h=h)

        # Right - Main Font Resize Section
        change_stylesheet(self, self.mb_show_eng_adj, font=calculate_font_ratio(self.mb_show_eng_adj, self.mb_show_eng_h))
        change_stylesheet(self, self.mb_show_kor_adj, font=calculate_font_ratio(self.mb_show_kor_adj, self.mb_show_kor_h))

    def resizeEvent(self, event):
        self.resized.emit()
        return super(MainWindow, self).resizeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec_())


"""
pyinstaller -w -F --log-level=WARN --hidden-import AutoSigner/main_ui.py --hidden-import AutoSigner/main_rc.py --icon=./AutoSigner/icon.ico "AutoSig.exe" ./AutoSigner/main.py
pyinstaller -w -F --log-level=WARN --hidden-import ./AutoSigner/main_ui.py --hidden-import ./AutoSigner/main_rc.py --icon=./AutoSigner/icon.ico main.py
pyinstaller -w -F --log-level=WARN --hidden-import AutoSigner/main_ui.py --hidden-import AutoSigner/main_rc.py --icon=./AutoSigner/icon.ico main.py
pyinstaller -w -F --log-level=WARN --hidden-import AutoSigner/main_ui.py --icon=./AutoSigner/icon.ico main.py
pyinstaller -w -F --log-level=WARN --hidden-import ./AutoSigner/main_ui --icon=./AutoSigner/icon.ico main.py
"""
