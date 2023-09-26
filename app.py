# pip install pyqt5 pywin32 pillow pyinstaller tinyaes
import os.path
import sys
from glob import glob

import PyQt5.QtCore
import pandas
from PyQt5.QtGui import QIcon, QPixmap, QFont, QFontDatabase
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QMainWindow, QApplication, QListWidget, QFileDialog, QWidget, QCheckBox, QLabel, QPushButton, QSizePolicy, QVBoxLayout
from PyQt5.QtCore import QTimer, pyqtSignal, QRect, QBuffer, Qt, QUrl, QSize
from PyQt5.QtMultimedia import QSound, QMediaPlayer, QMediaContent

from resource.py import get_images
from resource.py import get_tts_audio
from resource.py.toggle import Toggle, AnimatedToggle
from resource.py.load_json import load_json_file
from resource.py.load_main_csv import get_main_csv

from main_ui import Ui_MainApp as mp

try:
    os.system("pyuic5 main.ui -o main_ui.py")
    print("  [Info] pyuic5 has done...")
    # os.system("pyrcc5 main.qrc -o main_rc.py")
except FileNotFoundError:
    print("  [Error] Error happened from 'pyuic5 or pyrcc5' ")


class MainWindow(QMainWindow, mp):
    resized = pyqtSignal()
    JSON_DATA = load_json_file()
    CSV_DATA = get_main_csv()

    def __init__(self, parent=None):
        # Overloading MainWindow
        super(MainWindow, self).__init__(parent)

        # Setup GUI Widget
        self.set_font_family()
        self.setupUi(self)
        self.show()

        # Setup Variable
        self.set_variable()

        # Setup Graphic Part
        self.setWindowTitle("  VisualVoca")
        self.setWindowIcon(QIcon("resource/src/img/AppIcon.png"))
        self.mb_icon.setPixmap(QPixmap('resource/src/img/Logo.svg'))
        self.setup_window_graphic()

        # Setup Signal and Slots
        self.set_signal()

    def set_font_family(self):
        def grab_ttf_file() -> list:
            return glob(os.path.abspath("./resource/src/font/*.ttf"))

        def get_font_name(font_path: str = None) -> str:
            from fontTools import ttLib

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
        fontDB = QFontDatabase()

        # Get font name by JSON_DATA
        font_path = None
        font_name = None
        font_file_list = grab_ttf_file()
        user_target_font = self.JSON_DATA['FontFamily']

        try:
            # Check if PC has a font that user want to set as font family
            modified_font_name = del_special_character(user_target_font)
            font_file_name = [del_special_character(os.path.basename(item).replace(".ttf","")) for item in font_file_list]

            # Find User Target Font
            idx = font_file_name.index(modified_font_name)
            font_path = font_file_list[idx]
            font_name = get_font_name(font_path)
            print(f"  [Info] Changed Successfully by User font:{font_name}")

        except Exception as e:
            # Set font as Noto Sans KR Semi Bold if error happened
            font_path = "resource/src/font/NotoSansKR-SemiBold.ttf"
            font_name = "Noto Sans KR SemiBold"
            print(f"  [Error] Changed Failed:{e}")

        fontDB.addApplicationFont(os.path.abspath(font_path))

        # Customize font family
        custom_stylesheet = self.styleSheet()
        custom_stylesheet = custom_stylesheet.replace("Noto Sans KR SemiBold", font_name)
        self.setStyleSheet(custom_stylesheet)

    def set_variable(self):
        # Configuration Variables
        self.auto_scroll_toggle = QCheckBox()
        self.auto_slide = True

        # Voca Variables
        self.word = None
        self.focused_listwidget = None

        # Image Variables
        self.pics = None
        self.is_voca_changed = False
        self.image_idx = 0

        # Audion Variables
        self.player = QMediaPlayer()
        self.lang = ['en', 'ko']
        self.is_playing = False
        self.is_finished = False
        self.tts_idx = 0
        self.tts_repeat = 3

        # ETC
        self.timer = QTimer(self)

    def set_signal(self):
        # window resized event
        self.resized.connect(self.resize_widget)

        # voca word clicked event on QListWidget
        self.list_widgets = self.findChildren(QListWidget)
        print(self.list_widgets)

        self.player.stateChanged.connect(self.play_tts_audio)

        for widget in self.list_widgets:
            widget.itemClicked.connect(lambda: self.change_mb_voca_row(obj=widget))
            widget.currentRowChanged.connect(lambda: self.change_mb_voca_widget(obj=widget))
            widget.currentRowChanged.connect(lambda: self.get_audio_tts(obj=widget))

    def setup_window_graphic(self):
        def make_toggle_button():
            self.auto_scroll_toggle = AnimatedToggle(
                checked_color="#4ed164"
            )
            self.mb_top_bar_auto_scroll_verticalLayout.addWidget(self.auto_scroll_toggle)

            self.auto_scroll_toggle.setStyleSheet("margin: 6px 0px 6px 0px\n")
            self.auto_scroll_toggle.setMaximumHeight(self.mb_top_bar_auto_scroll_title.height())
            self.auto_scroll_toggle.setChecked(True)

        def insert_folder_image():
            # Get Folder Image Path
            base_path = os.path.abspath("./resource/src/img")
            self.folder_icon = QPixmap(os.path.join(base_path, "Folder.svg"))
            self.folder_open_icon = QPixmap(os.path.join(base_path, "FolderOpen.svg"))

            # Find Voca Button Object from parent
            voca_btns = [label for label in self.findChildren(QLabel) if 'mb_voca_button_icon_adj' in label.objectName()]
            push_btns = [push for push in self.findChildren(QPushButton) if 'mb_voca_button_group_title_adj' in push.objectName()]

            # Setup Pixmap
            max_size = int(voca_btns[0].maximumHeight() * 0.8)
            for idx, btn in enumerate(voca_btns):
                self.folder_icon = self.folder_icon.scaledToHeight(max_size)
                self.folder_open_icon = self.folder_open_icon.scaledToHeight(max_size)

                if push_btns[idx].isChecked():
                    btn.setPixmap(self.folder_open_icon)
                else:
                    btn.setPixmap(self.folder_icon)

        def calculate_ratio():
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

        def make_lesson_title():
            def find_mb_voca_widgets():
                voca_widgets = self.findChildren(QWidget)
                voca_widgets = [widget for widget in voca_widgets if "mb_voca_widget" in widget.objectName()]

                return voca_widgets

            def delete_mb_voca_widget():
                widgets = self.findChildren(QWidget)

                for widget in widgets:
                    if widget.objectName() == "mb_voca_widget_1":
                        for i in reversed(range(widget.findChildren(QtCore.QObject))):
                            widget.removeChild(widget.child(i))
                        widget.deleteLater()
                pass

            def mb_voca_widget(groups: list = None):
                def setup_QListWidget(parent=None):
                    obj = QtWidgets.QListWidget(parent)
                    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                                       QtWidgets.QSizePolicy.MinimumExpanding)
                    sizePolicy.setHorizontalStretch(0)
                    sizePolicy.setVerticalStretch(0)
                    sizePolicy.setHeightForWidth(obj.sizePolicy().hasHeightForWidth())
                    obj.setSizePolicy(sizePolicy)
                    obj.setMaximumSize(QtCore.QSize(16777215, 16777215))
                    obj.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                    obj.setFocusPolicy(QtCore.Qt.NoFocus)
                    obj.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
                    obj.setStyleSheet("")
                    obj.setFrameShape(QtWidgets.QFrame.NoFrame)
                    obj.setFrameShadow(QtWidgets.QFrame.Plain)
                    obj.setLineWidth(0)
                    obj.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
                    obj.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
                    obj.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
                    obj.setAutoScrollMargin(1)
                    obj.setProperty("showDropIndicator", True)
                    obj.setAlternatingRowColors(False)
                    obj.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
                    obj.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
                    obj.setMovement(QtWidgets.QListView.Free)
                    obj.setProperty("isWrapping", False)
                    obj.setResizeMode(QtWidgets.QListView.Adjust)
                    obj.setLayoutMode(QtWidgets.QListView.SinglePass)
                    obj.setViewMode(QtWidgets.QListView.ListMode)
                    obj.setWordWrap(False)
                    obj.setObjectName(f"mb_voca_word_adj_{index}")

                    return obj

                def setup_QWidget_wrapper(parent=None):
                    obj = QWidget(parent)
                    sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
                    sizePolicy.setHorizontalStretch(0)
                    sizePolicy.setVerticalStretch(0)
                    sizePolicy.setHeightForWidth(obj.sizePolicy().hasHeightForWidth())
                    obj.setSizePolicy(sizePolicy)
                    obj.setMaximumSize(QSize(16777215, 300))
                    obj.setObjectName(f"mb_voca_widget_{index}")

                    return obj

                def setup_VHox_wrapper(parent=None):
                    obj = QtWidgets.QVBoxLayout(parent)
                    obj.setContentsMargins(0, 0, 0, 0)
                    obj.setSpacing(0)
                    obj.setObjectName(f"mb_voca_widget_verticalLayout_{index}")

                    return obj

                def setup_button_HBOX_wrapper(parent=None):
                    obj_layout = QtWidgets.QHBoxLayout(parent)
                    obj_layout.setContentsMargins(0, 0, 0, 0)
                    obj_layout.setSpacing(0)
                    obj_layout.setObjectName(f"button_horizontalLayout_{index}")

                    return obj_layout

                def setup_button_icon(parent=None):
                    obj = QtWidgets.QLabel(parent)
                    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
                    sizePolicy.setHorizontalStretch(0)
                    sizePolicy.setVerticalStretch(0)
                    sizePolicy.setHeightForWidth(obj.sizePolicy().hasHeightForWidth())

                    obj.setSizePolicy(sizePolicy)
                    obj.setMaximumSize(QSize(16777215, 20))
                    obj.setObjectName(f"mb_voca_button_icon_adj_{index}")

                    return obj

                def setup_voca_title(parent=None):
                    obj = QtWidgets.QPushButton(parent)
                    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
                    sizePolicy.setHorizontalStretch(0)
                    sizePolicy.setVerticalStretch(0)
                    sizePolicy.setHeightForWidth(obj.sizePolicy().hasHeightForWidth())
                    obj.setSizePolicy(sizePolicy)
                    obj.setMaximumSize(QtCore.QSize(16777215, 16777215))
                    obj.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                    obj.setCheckable(True)
                    obj.setChecked(False)
                    obj.setObjectName(f"mb_voca_button_group_title_adj_{index}")

                    return obj

                def make_voca_widget_by_code():
                    # Make QWidget to QScrollWidget -> QWidget:[q_widget_wrapper]
                    NEW_WIDGET_WRAPPER = setup_QWidget_wrapper(parent=self.mb_voca_scroll_widget)
                    self.q_widget_vertical_layout = setup_VHox_wrapper(NEW_WIDGET_WRAPPER)

                    # Make QWidget to "q_widget_wrapper" -> QWidget:[q_widget_button_wrapper]
                    self.q_widget_button_wrapper = QtWidgets.QWidget(NEW_WIDGET_WRAPPER)
                    self.q_widget_button_wrapper_layout = setup_button_HBOX_wrapper(self.q_widget_button_wrapper)

                    # Make QLabel and Add to ["q_widget_button_wrapper"]
                    self.q_label_icon = setup_button_icon(self.q_widget_button_wrapper)
                    self.q_widget_button_wrapper_layout.addWidget(self.q_label_icon)

                    # Make QPushButton and Add to ["q_widget_button_wrapper"]
                    self.q_pushbutton_title = setup_voca_title(self.q_widget_button_wrapper)
                    self.q_widget_button_wrapper_layout.addWidget(self.q_pushbutton_title)

                    # Add to ["q_widget_vertical_layout"]
                    self.q_widget_vertical_layout.addWidget(self.q_widget_button_wrapper)

                    # Make QListWidget and Add to ["q_widget_vertical_layout"]
                    self.q_list_widget = setup_QListWidget(NEW_WIDGET_WRAPPER)
                    self.q_widget_vertical_layout.addWidget(self.q_list_widget)

                    return NEW_WIDGET_WRAPPER

                for index, value in enumerate(groups):
                    index += 1
                    self.q_widget_wrapper = make_voca_widget_by_code()
                    self.mb_voca_widget_verticalLayout.addWidget(self.q_widget_wrapper)

                    self.q_pushbutton_title.setText(value)

                    words_in_group = self.CSV_DATA["dataframe"][self.CSV_DATA["dataframe"]["그룹"] == value]["단어"]
                    words_in_group = words_in_group.to_list()

                    for w_idx, word in enumerate(words_in_group):
                        item = QtWidgets.QListWidgetItem()
                        self.q_list_widget.addItem(item)
                        self.q_list_widget.item(w_idx).setText(word)




                # -------------------------------------------------------

            def make_mb_voca_widget():
                voca_widgets = find_mb_voca_widgets()

                group_name = self.CSV_DATA["unique_name"]
                sub_widget_count = len(group_name) - len(voca_widgets)

                if sub_widget_count != 0:
                    self.add_widget = mb_voca_widget(groups=group_name)
                    voca_widgets = find_mb_voca_widgets()

            # delete_mb_voca_widget()
            make_mb_voca_widget()
            # lessons = list(set(self.CSV_DATA[name]))
            # for lesson in lessons:
                # pass

        make_lesson_title()
        make_toggle_button()
        insert_folder_image()
        calculate_ratio()

    # <-- New Voca Clicked Event Handler --------------------------------------------------->
    @staticmethod
    def change_mb_voca_row(obj):
        idx = obj.currentRow()
        obj.setCurrentRow(idx)

    def change_mb_voca_widget(self, obj):
        # Get currentItem Text
        self.is_voca_changed = True
        print(obj.objectName())

        self.word = obj.currentItem().text()
        self.current_idx = obj.currentRow()
        print(self.current_idx)
        print(type(self.current_idx))

        # save obj and variables
        self.focused_listwidget = obj

        # reset index of image
        self.is_finished = False
        self.tts_idx = 0
        self.image_idx = 0
        self.group_name = obj.parent().findChild(QPushButton).text()
        print(self.group_name)

        # Change image
        status = get_images.get_images_from_word(self.word, self.JSON_DATA["ImageDownCount"])
        self.pics = [QPixmap(item) for item in glob(f"./resource/voca/img/{self.word}/*.jpg")][:self.JSON_DATA["ImageDownCount"]]

        # Change voca title
        self.mb_show_eng_adj.setText(self.word)

        # Change meaning title
        meaning = self.CSV_DATA["dataframe"][self.CSV_DATA["dataframe"]["그룹"] == self.group_name]["뜻"]

        meaning = meaning.iloc[self.current_idx]

        self.mb_show_kor_adj.setText(meaning)

        # Chagne image when voca has been changed
        self.change_mb_voca_image(self.image_idx)

    def change_mb_voca_image(self, idx):
        # Add image_idx
        if idx >= len(self.pics):
            self.move_next_voca()
        else:
            # Get image and change pixmap
            pic = self.pics[idx]

            self.mb_show_image_adj.clear()
            self.mb_show_image_adj.setPixmap(pic)
            self.mb_show_image_adj.repaint()

            self.image_idx += 1

    def move_next_voca(self):
        if self.auto_scroll_toggle.isChecked():
            idx = self.focused_listwidget.currentRow()
            if idx < self.focused_listwidget.count() - 1:
                idx = idx + 1
                self.focused_listwidget.setCurrentRow(idx)
            else:
                self.is_finished = True
                print("  [Info] <-- No more images left to show -->")
        else:
            self.is_playing = False
            self.is_finished = True
            print("  [Info] <-- Auto scroll is not clicked -->")

    # <-- Play audio TTS ------------------------------------------------------------------->
    def play_tts_audio(self):
        if self.player.state() == 0 and not self.is_finished:
            # Todo 마지막에 한번 더 나오는거 어떻게 처리할지 고민해보기

            # Play ALL TTS Audio in language list
            self.tts_idx = self.tts_idx % len(self.lang)

            # If ALL TTS Files played, change images
            if self.tts_idx == 0 and not self.is_voca_changed:
                self.change_mb_voca_image(idx=self.image_idx)

            audio_lang = self.lang[self.tts_idx]

            # 뜻에 맞추어 소리 나도록 설정
            if audio_lang != self.lang[0]:
                if audio_lang == 'ko':
                    self.word = self.mb_show_kor_adj.text()
                    self.word = self.word.replace("~", "무엇 ")
                    self.word = self.word.replace("～", "무엇 ")
                    self.word = self.word.replace("(", " ")
                    self.word = self.word.replace(")", " ")
                    self.word = self.word.replace("=", "같은 표현으로는 ")
                    self.word = self.word.replace("≠", "다른 표현으로는 ")
                    self.word = self.word.replace("(명)", "명사형으로는 ")
                    self.word = self.word.replace("(동)", "동사형으로는 ")
                    self.word = self.word.replace("(형)", "형용사형으로는 ")
                    self.word = self.word.replace("(복수)", "여러 개를 지칭할 땐 ")
                else:
                    self.word = self.mb_show_eng_adj.text()
            else:
                self.word = self.mb_show_eng_adj.text()

            audio_path = get_tts_audio.get_tts(word=self.word, lang=audio_lang)
            url = QUrl.fromLocalFile(audio_path)
            content = QMediaContent(url)

            self.player.setMedia(content)
            self.player.play()

            # Setup [tts_idx, is_voca_changed]
            self.tts_idx += 1
            self.is_voca_changed = False

    def get_audio_tts(self, obj: str = None):
        # Get currentItem Text
        self.word = obj.currentItem().text()

        # Play Audio when is not playing Visual Voca Sliding
        if not self.is_playing:
            self.play_tts_audio()
            self.is_playing = True

    # <-- Resize Event Handler ------------------------------------------------------------->
    def resize_widget(self):
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
            print("  [Info] Resize Event emitted")
            # get parent geometry
            _x, _y, _w, _h = obj.geometry().getRect()

            if 'mb_voca' in obj.objectName():
                _h = h - _y
                if 'mb_voca_scroll' in obj.objectName():
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
                    elif 'mb_show_dev' in obj.objectName():
                        _y = h - _h
                        _w -= 10

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
        resize_widget_setting(self, self.mb_show_dev, w=w, h=h)

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
