# <-- Import main pyqt app modules ----------------------------------------------------------->
import sys
import os.path
import json
import requests
from glob import glob
from fontTools import ttLib
from PyQt5 import QtWidgets, QtCore, QtGui, Qt, QtMultimedia

# Import Local Python Files
import GetImages
import GetAudio

from Translator import translate, search_text_by_lang
from ToggleButton import AnimatedToggle
from Json import load_json_file, save_json_file, generate_init
from CSVData import get_main_csv
from ConvertUI import get_ui_python_file as convert


# Set False when compile to exe file
convert = convert(True)

__author__ = 'https://www.github.com/gonyo1'
__released_date__ = 'October 2023'
__credits__ = ['Gonyo', 'AhnJH']
__version__ = None

root_path = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
print(root_path)
sys.path.append(root_path)

from src.ui.main_ui import Ui_MainApp as mp

class MainWindow(QtWidgets.QMainWindow, mp):
    resized = QtCore.pyqtSignal()
    JSON_DATA = load_json_file()
    CSV_DATA = get_main_csv()

    def __init__(self, parent=None, geometry=None):
        # Overloading MainWindow
        super(MainWindow, self).__init__(parent)

        # Setup GUI Widget
        self.set_font_family()
        self.setupUi(self)
        self.show()

        # Setup Variable
        self.set_variable()

        # Setup Graphic Part
        self.setWindowTitle(f"  VisualVoca (Ver.{__version__})")
        self.setWindowIcon(Qt.QIcon("./resource/src/img/AppIcon.ico"))
        self.mb_icon.setPixmap(Qt.QPixmap('./resource/src/img/logo.svg'))
        self.get_github_json()
        self.setup_window_graphic()

        # Setup Signal and Slots
        self.set_signal()

        # Re-position MainWidget
        if geometry != None:
            self.setGeometry(geometry)

        # Broadcast FIRSTRUN Finished
        self.init_show_option.click()
        self.FIRSTRUN = False

        # For updating software
        # self.thread = AppUpdator()
        return

    def set_font_family(self):
        def grab_ttf_file() -> list:
            return glob(os.path.abspath("./resource/src/font/*.ttf"))

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
            base_name = "./resource/src/font/NotoSansKR-SemiBold"
            font_path = ".".join([base_name, "ttf"])
            font_name = "Noto Sans KR SemiBold"
            print(f"  [Error] Error happened while getting font name: {e}")

        fontDB.addApplicationFont(os.path.abspath(font_path))

        # Customize font family
        self.setFont(QtGui.QFont(font_name))
        custom_stylesheet = self.styleSheet()
        custom_stylesheet = custom_stylesheet.replace("Noto Sans KR SemiBold", font_name)
        self.setStyleSheet(custom_stylesheet)

    def set_variable(self):
        # Github variables
        self.github_data = None

        # Configuration Variables
        self.PLATFORM = sys.platform
        self.init_show_option = None
        self.FIRSTRUN = True
        self.FIRSTCHANGE = False
        self.auto_scroll_toggle = QtWidgets.QCheckBox()
        self.auto_slide = True
        self.show_langs = list(self.JSON_DATA["LanguagesShow"].values())
        self.option_btns = [self.mb_top_bar_all, self.mb_top_bar_only_eng, self.mb_top_bar_only_kor, self.mb_top_bar_only_img]
        self.show_labels = [self.mb_show_eng_adj, self.mb_show_image_adj, self.mb_show_kor_adj, self.mb_show_special_case_adj, self.mb_show_btns_adj]

        del self.JSON_DATA["LanguagesSpeech"]["Reference"]
        self.speech_langs = list(self.JSON_DATA["LanguagesSpeech"].values())

        # Voca Variables
        self.word = None
        self.spacer = None
        self.sending_from_widget = None
        self.focused_listwidget = None

        # Image Variables
        self.is_pause_clicked = False
        self.file_type = ('*.jpg', '*.gif', '*.jpeg', '*.bmp')
        self.pics = None
        self.is_voca_changed = False
        self.image_idx = 0

        # Audio Variables
        self.player = QtMultimedia.QMediaPlayer()
        self.lang = list(self.JSON_DATA["LanguagesSpeech"].values())
        self.is_playing = False
        self.is_playing_alarm = False
        self.is_finished = False
        self.tts_idx = 0
        self.tts_repeat = 3

        # ETC
        self.timer = QtCore.QTimer(self)
        
    def setup_window_graphic(self):
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

            self.mb_show_special_case_adj_ratio_y = self.mb_show_special_case_adj.geometry().getRect()[1] / mbs_h
            self.mb_show_special_case_adj_ratio_h = self.mb_show_special_case_adj.geometry().getRect()[3] / mbs_h

            self.mb_show_btns_adj_ratio_y = self.mb_show_btns_adj.geometry().getRect()[1] / mbs_h
            self.mb_show_btns_adj_ratio_h = self.mb_show_btns_adj.geometry().getRect()[3] / mbs_h

        def make_voca_groups():
            def find_mb_voca_widgets():
                voca_widgets = self.findChildren(QtWidgets.QWidget)
                voca_widgets = [widget for widget in voca_widgets if "mb_voca_widget" in widget.objectName()]

                return voca_widgets

            def make_mb_voca_widget():
                group_name = self.CSV_DATA["unique_name"]
                subtract_widget_count = len(group_name) - len(voca_widgets)

                if subtract_widget_count != 0:
                    self.add_widget = mb_voca_widget(groups=group_name)

            def mb_voca_widget(groups: list = None):
                def make_voca_widget_by_code():
                    # Make QWidget to QScrollWidget -> QWidget:[q_widget_wrapper]
                    NEW_WIDGET_WRAPPER = setup_QWidget_wrapper(parent=self.mb_voca_scroll_widget)
                    self.q_widget_vertical_layout = setup_VHox_wrapper(NEW_WIDGET_WRAPPER)

                    # Make QWidget to "q_widget_wrapper" -> QWidget:[q_widget_button_wrapper]
                    self.q_widget_button_wrapper = setup_button_main_widget(NEW_WIDGET_WRAPPER)
                    self.q_widget_button_wrapper_layout = setup_button_HBOX_wrapper(self.q_widget_button_wrapper)

                    # Make QLabel and Add to ["q_widget_button_wrapper"]
                    self.q_label_icon = setup_button_icon(self.q_widget_button_wrapper)
                    self.q_widget_button_wrapper_layout.addWidget(self.q_label_icon)

                    # Make QPushButton and Add to ["q_widget_button_wrapper"]
                    self.q_pushbutton_title = setup_pushbutton_voca_title(self.q_widget_button_wrapper)
                    self.q_widget_button_wrapper_layout.addWidget(self.q_pushbutton_title)

                    # Add to ["q_widget_vertical_layout"]
                    self.q_widget_vertical_layout.addWidget(self.q_widget_button_wrapper)

                    # Make QListWidget and Add to ["q_widget_vertical_layout"]
                    self.q_list_widget = setup_QListWidget(NEW_WIDGET_WRAPPER)
                    self.q_widget_vertical_layout.addWidget(self.q_list_widget)

                    return NEW_WIDGET_WRAPPER

                def setup_QWidget_wrapper(parent=None):
                    obj = QtWidgets.QWidget(parent)
                    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
                    sizePolicy.setHorizontalStretch(0)
                    sizePolicy.setVerticalStretch(0)
                    sizePolicy.setHeightForWidth(obj.sizePolicy().hasHeightForWidth())
                    obj.setSizePolicy(sizePolicy)
                    # setMinimumSize 설정하면 고정 되어버림
                    # obj.setMinimumSize(QtCore.QSize(180, 35))
                    obj.setMaximumSize(QtCore.QSize(16777215, 16777215))
                    obj.setObjectName(f"mb_voca_widget_{index}")

                    return obj

                def setup_VHox_wrapper(parent=None):
                    obj = QtWidgets.QVBoxLayout(parent)
                    obj.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
                    obj.setContentsMargins(0, 0, 0, 0)
                    obj.setSpacing(0)
                    obj.setObjectName(f"mb_voca_widget_verticalLayout_{index}")

                    return obj

                def setup_button_main_widget(parent=None):
                    obj = QtWidgets.QWidget(parent)
                    obj.setMinimumSize(QtCore.QSize(180, 35))
                    obj.setMaximumSize(QtCore.QSize(180, 35))
                    obj.setObjectName(f"mb_voca_button_adj_{index}")
                    obj.setStyleSheet("QWidget:hover {background-color: rgb(242, 214, 130)}")

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
                    obj.setStyleSheet("padding-left: 5px;\n"
                                      "background-repeat: none;\n"
                                      "background-position: right;")
                    obj.setSizePolicy(sizePolicy)
                    obj.setMaximumSize(QtCore.QSize(16777215, 25))
                    obj.setObjectName(f"mb_voca_button_icon_adj_{index}")

                    return obj

                def setup_pushbutton_voca_title(parent=None):
                    obj = QtWidgets.QPushButton(parent)
                    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
                    sizePolicy.setHorizontalStretch(0)
                    sizePolicy.setVerticalStretch(0)
                    sizePolicy.setHeightForWidth(obj.sizePolicy().hasHeightForWidth())
                    obj.setFocusPolicy(QtCore.Qt.NoFocus)
                    obj.setSizePolicy(sizePolicy)
                    obj.setMinimumSize(QtCore.QSize(0, 35))
                    obj.setMaximumSize(QtCore.QSize(16777215, 16777215))
                    obj.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                    obj.setFocusPolicy(QtCore.Qt.NoFocus)
                    obj.setCheckable(True)
                    obj.setChecked(False)
                    obj.setObjectName(f"mb_voca_button_group_title_adj_{index}")

                    return obj

                def setup_QListWidget(parent=None):
                    obj = QtWidgets.QListWidget(parent)
                    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                                       QtWidgets.QSizePolicy.Preferred)
                    sizePolicy.setHorizontalStretch(0)
                    sizePolicy.setVerticalStretch(0)
                    sizePolicy.setHeightForWidth(obj.sizePolicy().hasHeightForWidth())
                    obj.setSizePolicy(sizePolicy)
                    obj.setMinimumSize(QtCore.QSize(184, 0))
                    obj.setMaximumSize(QtCore.QSize(184, 16777215))
                    obj.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                    obj.setFocusPolicy(QtCore.Qt.NoFocus)
                    obj.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
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

                for index, value in enumerate(reversed(groups)):
                    index += 1

                    # Make QWidget for wrapping
                    self.q_widget_wrapper = make_voca_widget_by_code()
                    self.mb_voca_scroll_widget_verticalLayout.insertWidget(1, self.q_widget_wrapper)

                    # Set Group name to QPushButton Title
                    self.q_pushbutton_title.setText(value)

                    # Get Voca from Selected Group
                    upper_text_language = self.JSON_DATA["LanguagesShow"]["UpperPart"]
                    words_in_group = self.CSV_DATA["dataframe"][self.CSV_DATA["dataframe"]["GroupName"] == value][
                        upper_text_language]
                    words_in_group = words_in_group.to_list()

                    # Set QListWidgetItem text as voca
                    for w_idx, word in enumerate(words_in_group):
                        item = QtWidgets.QListWidgetItem()

                        # 빈칸이면 빈 셀로 변환하기
                        item.setCheckState(QtCore.Qt.Unchecked)
                        self.q_list_widget.addItem(item)
                        self.q_list_widget.item(w_idx).setText(str(word))

            voca_widgets = find_mb_voca_widgets()
            make_mb_voca_widget()

            # find PushButton
            self.voca_widget_button = [btn for btn in self.findChildren(QtWidgets.QPushButton) if
                                       'mb_voca_button_group_title_adj' in btn.objectName()]
            self.voca_widget_button = [btn for btn in self.voca_widget_button if not btn.isVisible()]

        def make_toggle_button():
            if self.FIRSTRUN:
                self.auto_scroll_toggle = AnimatedToggle(checked_color="#fabc01")
                self.mb_top_bar_auto_scroll_verticalLayout.addWidget(self.auto_scroll_toggle)

                self.auto_scroll_toggle.setStyleSheet("margin: 6px 0px 6px 0px\n")
                self.auto_scroll_toggle.setMaximumHeight(self.mb_top_bar_auto_scroll_title.height())
                self.auto_scroll_toggle.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

                _bool = True if self.JSON_DATA["AutoScroll"] == 'True' else False
                self.auto_scroll_toggle.setChecked(_bool)

        def make_black_vail():
            self.BLACK = QtWidgets.QLabel(self.mb_show_adj)
            self.BLACK.setObjectName("BLACK")
            self.BLACK.setStyleSheet("background-color: black;\n")
            self.BLACK.setGeometry(-1, -1, 772, 702)
            self.BLACK.hide()

        def insert_folder_image():
            # Get Folder Image Path
            base_path = os.path.abspath("./resource/src/img")
            self.folder_icon = Qt.QPixmap(os.path.join(base_path, "Folder.svg"))
            self.folder_open_icon = Qt.QPixmap(os.path.join(base_path, "FolderOpen.svg"))

            # Find Voca Button Object from parent
            voca_btns = [label for label in self.findChildren(QtWidgets.QLabel) if
                         'mb_voca_button_icon_adj' in label.objectName()]
            push_btns = [push for push in self.findChildren(QtWidgets.QPushButton) if
                         'mb_voca_button_group_title_adj' in push.objectName()]

            # Setup Pixmap
            max_size = int(voca_btns[0].maximumHeight() * 0.8)
            for idx, btn in enumerate(voca_btns):
                self.folder_icon = self.folder_icon.scaledToHeight(max_size)
                self.folder_open_icon = self.folder_open_icon.scaledToHeight(max_size)

                if push_btns[idx].isChecked():
                    btn.setPixmap(self.folder_open_icon)
                else:
                    btn.setPixmap(self.folder_icon)

        def insert_refresh_icon():
            # Get Folder Image Path
            base_path = os.path.abspath("./resource/src/img")

            refresh = os.path.join(base_path, "Refresh.svg")
            refresh = refresh.replace("\\", "/")

            refresh_hover = os.path.join(base_path, "RefreshHover.svg")
            refresh_hover = refresh_hover.replace("\\", "/")

            self.mb_voca_refresh.setStyleSheet("QPushButton {margin: 5px;\n"
                                               "padding: 0px;\n"
                                               "border: 0px solid;\n"
                                               f"background-image: url({refresh});\n"
                                               "background-repeat: none;\n"
                                               "background-position: center;\n"
                                               "}\n"
                                               "QPushButton:hover {\n"
                                               f"background-image: url({refresh_hover});\n"
                                               "}\n"
                                               )

        def insert_bookmark_icon():
            # Get Folder Image Path
            self.mb_voca_bookmark.setEnabled(True)
            base_path = os.path.abspath("./resource/src/img")

            bookmark = os.path.join(base_path, "Bookmark.svg")
            bookmark = bookmark.replace("\\", "/")

            bookmark_hover = os.path.join(base_path, "BookmarkHover.svg")
            bookmark_hover = bookmark_hover.replace("\\", "/")

            bookmark_checked = os.path.join(base_path, "BookmarkChecked.svg")
            bookmark_checked = bookmark_checked.replace("\\", "/")

            self.mb_voca_bookmark.setStyleSheet("QPushButton {\n"
                                                "margin: 5px;\n"
                                                "padding: 0px;\n"
                                                "border: 0px solid;\n"
                                                f"background-image: url({bookmark});\n"
                                                "background-repeat: none;\n"
                                                "background-position: center;\n"
                                                "}\n"
                                                
                                                "QPushButton:hover {\n"
                                                f"background-image: url({bookmark_hover});\n"
                                                "}\n"
                                                
                                                "QPushButton:checked {\n"
                                                f"background-image: url({bookmark_checked});\n"
                                                "}\n"
                                                )

        def insert_FrontImage():
            self.VIVOCLEAR = os.path.abspath("./resource/src/img/Indicator.svg")
            self.VIVOIMAGE = os.path.abspath("./resource/src/img/FrontImage.svg")
            self.VIVOIMAGE = self.VIVOIMAGE.replace("\\", "/")

            self.change_stylesheet(self.mb_show_special_case_adj, background_image=f"url({self.VIVOIMAGE})")

            self.mb_show_image_adj.setText("")
            self.change_stylesheet(self.mb_show_eng_adj, color="white")

        def insert_player_button_image():
            for button in [self.back, self.forward, self.pause]:
                button_name = button.objectName().capitalize()
                button.setText("")
                button.setStyleSheet("QPushButton {\n"
                                     f"background-image: url({self.pyqt_image_url(f'{button_name}.svg')});\n"
                                     "}\n"
                                     "QPushButton:hover {\n"
                                     f"background-image: url({self.pyqt_image_url(f'{button_name}Hover.svg')});"
                                     "}")

        def which_option_clicked():
            idx = self.JSON_DATA["BookmarkIndex"]

            for btn in self.option_btns:
                btn.setChecked(False)

            self.init_show_option = self.option_btns[idx]

        def update_contact():
            dev_text = str()

            self.mb_show_dev_contact.setText("Contact" + "\n" * len(self.github_data["Contact"]) + "Contributor")
            for data in self.github_data:
                if data == "Contact":
                    for line in self.github_data[data]:
                        dev_text += "".join([line, "\n"])
                elif data == "Contributor":
                    dev_text += ", ".join(self.github_data[data])

            self.mb_show_dev_detail.setText(dev_text)

        self.setGeometry(self.geometry().x(), self.geometry().y(), 970, 700)

        # UI 에서 샘플로 만들었던 위젯 지우기
        self.mb_voca_widget_0.hide()
        self.mb_show_btns_adj.hide()

        # SpinBox Value 설정하기
        self.mb_top_bar_repeat_spinbox.setValue(int(self.JSON_DATA["ImageDownCount"]))

        # Do Something...
        make_voca_groups()
        make_toggle_button()
        make_black_vail()

        insert_folder_image()
        insert_refresh_icon()
        insert_bookmark_icon()
        insert_FrontImage()
        insert_player_button_image()
        which_option_clicked()

        self.voca_widget_button_event()

        calculate_ratio()
        update_contact()
        self.mb_voca_refresh.setEnabled(True)

    def set_signal(self, *args):
        def insert_total_signal():
            # Mainwindow buttons
            self.mb_voca_open.clicked.connect(is_open_folder_clicked)
            self.mb_top_bar_all.clicked.connect(is_option_button_clicked)
            self.mb_top_bar_only_eng.clicked.connect(is_option_button_clicked)
            self.mb_top_bar_only_kor.clicked.connect(is_option_button_clicked)
            self.mb_top_bar_only_img.clicked.connect(is_option_button_clicked)
            self.mb_voca_bookmark.clicked.connect(is_bookmark_button_clicked)
            self.mb_voca_refresh.clicked.connect(is_refresh_clicked)
            self.auto_scroll_toggle.stateChanged.connect(lambda state, key="AutoScroll": self.change_json_file(key=key))

            # mb_show part
            self.pause.clicked.connect(is_pause_button_clicked)
            self.back.clicked.connect(is_direction_button_clicked)
            self.forward.clicked.connect(is_direction_button_clicked)
            self.mb_top_bar_repeat_spinbox.valueChanged.connect(lambda: self.change_json_file(key="ImageDownCount"))
            self.player.stateChanged.connect(self.start_player)

            # window resized event
            self.resized.connect(self.resize_widget)

            # pushbutton clicked event on QListWidget
            insert_pushbutton_signal()

            # voca word clicked event on QListWidget
            insert_QListWidget_item_signal()

        def insert_pushbutton_signal():
            for btn in self.voca_widget_button:
                btn.clicked.connect(self.voca_widget_button_event)

        def is_bookmark_button_clicked():
            listwidgets = self.findChildren(QtWidgets.QListWidget)
            word_bookmark = list()
            for listwidget in listwidgets:
                count = listwidget.count()
                for row in range(count):
                    item_obj = listwidget.item(row)
                    if item_obj.checkState() == 2:
                        word_bookmark.append(item_obj)
                        # word_bookmark_ad

        def insert_QListWidget_item_signal():
            self.list_widgets = self.findChildren(QtWidgets.QListWidget)

            self.list_widgets = [wdg for wdg in self.list_widgets if not wdg.isVisible()]

            for idx, widget in enumerate(self.list_widgets):
                if widget.objectName() != "mb_voca_word_adj_0":
                    widget.itemClicked.connect(is_voca_button_clicked)
                    widget.currentRowChanged.connect(lambda: self.change_mb_voca_widget(obj=self.sending_from_widget))
                    widget.currentRowChanged.connect(lambda: self.get_tts_audio(obj=self.sending_from_widget))

        # Event Slots ------------------------------------
        def is_voca_button_clicked():
            self.player.stop()
            self.sending_from_widget = self.sender()

            if (self.sending_from_widget != None):
                idx = self.sending_from_widget.currentRow()

                # 첫번째는 어쩔 수 없이 직접 실행해야하나 봄...
                self.sending_from_widget.setCurrentRow(idx)
                self.change_mb_voca_widget(obj=self.sending_from_widget)
                self.get_tts_audio(obj=self.sending_from_widget)

        def is_pause_button_clicked():
            if not self.is_pause_clicked:
                # stop player
                self.stop_player()

                # change setting
                self.is_finished = True
                self.is_playing = False
                self.is_pause_clicked = True

                # show black
                self.BLACK.show()
                for item in self.show_labels:
                    if item.isVisible():
                        item.raise_()
                        item.show()
                        item.setStyleSheet("color: white;\n")

                self.mb_show_btns_adj.setStyleSheet("color: black;\n")
            else:
                # play player
                self.change_mb_voca_widget(obj=self.sending_from_widget)
                self.get_tts_audio(obj=self.sending_from_widget)

                # change setting
                self.is_pause_clicked = False

                # hide black
                self.BLACK.hide()

                for item in self.show_labels:
                    if item.isVisible():
                        item.raise_()
                        item.show()
                        item.setStyleSheet("color: black;\n")

                self.pause.setStyleSheet("QPushButton {\n"
                                         f"background-image: url({self.pyqt_image_url(f'Pause.svg')});\n"
                                         "}\n"
                                         "QPushButton:hover {\n"
                                         f"background-image: url({self.pyqt_image_url(f'PauseHover.svg')});"
                                         "}"
                                         )

        def is_direction_button_clicked():
            # Stop Player and reset setting
            self.stop_player()

            # Get obj from sender
            obj = self.sender()
            name = obj.objectName()

            # Change current index
            if name == "back":
                idx = self.sending_from_widget.currentRow()
                self.sending_from_widget.setCurrentRow(idx - 1)
            elif name == "forward":
                idx = self.sending_from_widget.currentRow()
                self.sending_from_widget.setCurrentRow(idx + 1)

            self.is_pause_clicked = False

            for item in self.show_labels:
                item.raise_()
                item.show()
                item.setStyleSheet("color: black")
                if item.objectName() == "mb_show_special_case_adj":
                    self.change_stylesheet(item, background_image=f"url({self.VIVOCLEAR})")

            self.pause.setStyleSheet("QPushButton {\n"
                                     f"background-image: url({self.pyqt_image_url(f'Pause.svg')});\n"
                                     "}\n"
                                     "QPushButton:hover {\n"
                                     f"background-image: url({self.pyqt_image_url(f'PauseHover.svg')});"
                                     "}"
                                     )

        def is_refresh_clicked():

            # Setup GUI Widget
            # self.set_font_family()
            self.JSON_DATA = load_json_file()
            self.CSV_DATA = get_main_csv()

            self.close()

            geometry = self.geometry()
            self.__init__(geometry=geometry)
            self.mb_show_image_adj.setStyleSheet(f"background-image: url({self.VIVOCLEAR})")
            # self.mb_show_special_case_adj.setStyleSheet(f"background-image: url({self.VIVOIMAGE})")

        def is_open_folder_clicked():
            base_path = os.path.abspath("WordList.csv")

            if self.PLATFORM == "win32":
                os.startfile(base_path)
            elif self.PLATFORM == 'drawin':
                os.system(f"open {base_path}")

        def is_option_button_clicked():
            def clean_show_adj_btns():
                for item in self.show_labels[:-1]:
                    item.clear()

            def raise_labels():
                self.mb_show_special_case_adj.show()
                self.mb_show_special_case_adj.raise_()
                self.mb_show_btns_adj.hide()
                self.mb_show_dev.show()
                self.mb_show_dev.raise_()

            # ALL, KOR, ENG, etc.. 클릭되면 무엇이 나오게 할지
            btn = self.sender()

            # 본인을 제외한 다른 옵션 버튼을 unchecked 로 변경하기
            for item in self.option_btns:
                item.setChecked(False)
            btn.setChecked(True)

            # <-- Dev. AhnJH part 간소화
            self.mb_show_kor_adj.hide()
            self.mb_show_eng_adj.hide()
            self.mb_show_image_adj.hide()
            self.mb_show_special_case_adj.hide()
            self.mb_show_special_case_adj.clear()

            if btn == self.mb_top_bar_all:
                self.mb_show_kor_adj.show()
                self.mb_show_eng_adj.show()
                self.mb_show_image_adj.show()
                self.change_stylesheet(self.mb_show_special_case_adj, background_image=f"url({self.VIVOCLEAR})")
                if self.FIRSTCHANGE == False:
                    clean_show_adj_btns()
                    raise_labels()
                    self.change_stylesheet(self.mb_show_special_case_adj, background_image=f"url({self.VIVOIMAGE})")

            elif btn == self.mb_top_bar_only_eng:
                self.change_stylesheet(self.mb_show_special_case_adj, color="black")
                self.change_stylesheet(self.mb_show_special_case_adj, background_image=f"url({self.VIVOCLEAR})")
                self.mb_show_special_case_adj.setText(self.mb_show_eng_adj.text())
                self.mb_show_special_case_adj.show()
                if self.FIRSTCHANGE == False:
                    clean_show_adj_btns()
                    raise_labels()
                    self.mb_show_special_case_adj.setText("Visual Voca")
            elif btn == self.mb_top_bar_only_kor:
                self.change_stylesheet(self.mb_show_special_case_adj, color="black")
                self.change_stylesheet(self.mb_show_special_case_adj, background_image=f"url({self.VIVOCLEAR})")
                self.mb_show_special_case_adj.setText(self.mb_show_kor_adj.text())
                self.mb_show_special_case_adj.show()
                if self.FIRSTCHANGE == False:
                    clean_show_adj_btns()
                    raise_labels()
                    self.mb_show_special_case_adj.setText("비쥬얼 보카")
            elif btn == self.mb_top_bar_only_img:
                self.mb_show_special_case_adj.setText("")
                self.mb_show_image_adj.show()
                if self.FIRSTCHANGE == False:
                    clean_show_adj_btns()
                    raise_labels()
                    self.change_stylesheet(self.mb_show_special_case_adj, background_image=f"url({self.VIVOIMAGE})")

            idx = self.option_btns.index(btn)
            self.change_json_file(key="BookmarkIndex", value=idx)

        # Insert Signal to main window
        if self.FIRSTRUN:
            insert_total_signal()
        if len(args) > 0:
            if args[0] == 'pushbutton':
                insert_pushbutton_signal()
            elif args[0] == 'qlistwidget':
                insert_QListWidget_item_signal()

    def get_github_json(self):
        file = open(os.path.abspath("./resource/src/github.txt"))
        data = file.read()
        self.github_data = json.loads(data)


    # <-- Main Window Section -------------------------------------------------------------->
    def change_json_file(self, key=None, value=None):
        if key == "AutoScroll":
            value = str(self.auto_scroll_toggle.isChecked())
            save_json_file(key, value)

        elif key == "ImageDownCount":
            value = self.mb_top_bar_repeat_spinbox.value()
            self.JSON_DATA["ImageDownCount"] = value
            save_json_file(key, value)

        else:
            self.JSON_DATA[key] = value
            save_json_file(key, value)

    @staticmethod
    def pyqt_image_url(filename):
        base_path = os.path.abspath("./resource/src/img")
        return os.path.join(base_path, filename).replace("\\", "/")



    # <-- New Voca Clicked Event Handler --------------------------------------------------->
    def change_mb_voca_widget(self, obj):
        self.change_stylesheet(self.mb_show_eng_adj, color="black")
        self.change_stylesheet(self.mb_show_kor_adj, color="black")
        self.change_stylesheet(self.mb_show_special_case_adj, color="black")
        self.mb_show_dev.hide()
        self.mb_show_btns_adj.show()
        self.mb_show_special_case_adj.hide()
        self.mb_show_special_case_adj.clear()
        self.player.stop()
        self.BLACK.hide()

        # Get currentItem Text
        if (self.sending_from_widget != None):
            self.is_voca_changed = True
            self.FIRSTCHANGE = True

            # 처음 실행 때 즐겨찾기만 할 경우 대비한 코드
            if obj.currentRow() != -1:

                self.word = obj.currentItem().text()  # Upper text 가 될 부분 (나중에 Ko -> ru(러시아어)로 변경가능)
                self.current_idx = obj.currentRow()

                # reset index of image
                self.is_finished = False
                self.tts_idx = 0
                self.image_idx = 0
                self.group_name = obj.parent().findChild(QtWidgets.QPushButton).text()

                # Change image
                self.pics = list()
                status = GetImages.get_images_from_word(self.word, self.JSON_DATA["ImageDownCount"], self.JSON_DATA,
                                                        self.file_type)
                file_types = tuple(f"./resource/voca/img/{self.word}/{extention}" for extention in self.file_type)
                for file_type in file_types:
                    self.pics.extend([Qt.QPixmap(item) for item in glob(file_type)])

                # When Image Files are not downloaded enough
                if len(self.pics) < self.JSON_DATA["ImageDownCount"]:
                    no_image = Qt.QPixmap(os.path.abspath("./resource/src/img/NoImage.svg"))
                    count = self.JSON_DATA["ImageDownCount"] - len(self.pics)
                    for time in range(count):
                        self.pics.append(no_image)

                # Slice pictures by "ImageDownCount"
                self.pics = self.pics[:self.JSON_DATA["ImageDownCount"]]

                # Change voca title
                self.mb_show_eng_adj.setText(self.word)

                # Todo:finish // FOR TEST MS AZURE TRANSLATOR
                pass

                # Change meaning(under_text) title
                lower_text_language = self.JSON_DATA["LanguagesShow"]["LowerPart"]
                try:
                    lower_text = self.CSV_DATA["dataframe"][self.CSV_DATA["dataframe"]["GroupName"] == self.group_name][
                        lower_text_language]
                    lower_text = lower_text.iloc[self.current_idx]

                    # iloc 에 해당하는 값이 None (비어있음)이면 자동번역기 실행
                    if type(lower_text) is float:
                        self.translated_result = translate(word=self.word,
                                                           langs=self.JSON_DATA["LanguagesSpeech"],
                                                           key=self.JSON_DATA["APIKeys"]["MSAzureTranslator"])
                        lower_text = search_text_by_lang(self.translated_result, lower_text_language)

                # CSV 파일에 LanguageShow 언어가 없다면 자동번역기 실행하기
                except KeyError:
                    print("  [Info] No Column found in CSV file. Do Auto Translate... ")
                    self.translated_result = translate(word=self.word,
                                                       langs=self.JSON_DATA["LanguagesSpeech"],
                                                       key=self.JSON_DATA["APIKeys"]["MSAzureTranslator"])
                    lower_text = search_text_by_lang(self.translated_result, lower_text_language)

                self.mb_show_kor_adj.setText(lower_text)

                # Change image when voca has been changed
                self.change_mb_voca_image(self.image_idx)


                # Check if special case clicked
                if self.mb_top_bar_only_eng.isChecked():
                    self.mb_show_special_case_adj.setText(self.word)
                    self.mb_show_special_case_adj.show()
                elif self.mb_top_bar_only_kor.isChecked():
                    self.mb_show_special_case_adj.setText(lower_text)
                    self.mb_show_special_case_adj.show()

    def change_mb_voca_image(self, idx):
        def move_to_next_voca_image():
            if self.auto_scroll_toggle.isChecked():
                idx = self.sending_from_widget.currentRow()

                if idx < self.sending_from_widget.count() - 1:
                    idx = idx + 1
                    self.sending_from_widget.setCurrentRow(idx)
                else:
                    self.stop_player()
                    print("  [Info] <-- No more images left to show -->")
            else:
                self.stop_player()
                self.BLACK.hide()
                self.FIRSTCHANGE = False
                [item.click() for item in self.option_btns if item.isChecked()]
                print("  [Info] <-- Auto scroll is not clicked -->")

        def move_to_next_image():
            pic = self.pics[idx]
            self.mb_show_image_adj.clear()
            self.mb_show_image_adj.setPixmap(
                pic.scaled(
                    QtCore.QSize(self.mb_show_image_adj.width(),
                                 self.mb_show_image_adj.height()),
                    aspectRatioMode=QtCore.Qt.KeepAspectRatio,
                    transformMode=QtCore.Qt.SmoothTransformation
                )
            )
            self.mb_show_image_adj.repaint()
            self.image_idx += 1

        # Add image_idx
        if idx >= len(self.pics):
            # Get image and change pixmap in NEXT WORD
            move_to_next_voca_image()
        else:
            # Get image and change pixmap in ONE WORD
            move_to_next_image()

    def voca_widget_button_event(self):
        self.stop_player()
        self.BLACK.hide()
        self.pause.setStyleSheet("QPushButton {\n"
                                 f"background-image: url({self.pyqt_image_url(f'Pause.svg')});\n"
                                 "}\n"
                                 "QPushButton:hover {\n"
                                 f"background-image: url({self.pyqt_image_url(f'PauseHover.svg')});"
                                 "}"
                                 )

        clicked_btn = self.sender()

        for btn in self.voca_widget_button:
            append_list_widget = btn.parent().parent().findChild(QtWidgets.QListWidget)
            append_label = btn.parent().findChild(QtWidgets.QLabel)
            if btn == clicked_btn:
                if btn.isChecked():
                    btn.setChecked(True)
                    append_label.setPixmap(self.folder_open_icon)
                    append_list_widget.setHidden(False)

                    w = append_list_widget.width()
                    # w를 아이템 크기에 맞출 때 사용할 수 있음
                    # w = append_list_widget.sizeHintForColumn(0) + append_list_widget.frameWidth() * 2
                    h = append_list_widget.sizeHintForRow(0) * append_list_widget.count() + 2 * append_list_widget.frameWidth()
                    append_list_widget.setFixedSize(w, h)

                else:
                    btn.setChecked(False)
                    append_label.setPixmap(self.folder_icon)
                    append_list_widget.setHidden(True)

            else:
                btn.setChecked(False)
                append_label.setPixmap(self.folder_icon)
                append_list_widget.setHidden(True)

        # insert SpacerItem
        if self.FIRSTRUN:
            self.spacer = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
            self.mb_voca_scroll_widget_verticalLayout.addItem(self.spacer)



    # <-- Play audio TTS ------------------------------------------------------------------->
    def start_player(self):
        def replace_korean(word):
            word = word.replace("~", "무엇 ")
            word = word.replace("～", "무엇 ")
            word = word.replace("-", "무엇 ")
            word = word.replace("(", " ")
            word = word.replace(")", " ")
            word = word.replace("=", "같은 표현으로는 ")
            word = word.replace("≠", "다른 표현으로는 ")
            word = word.replace("(명)", "명사형으로는 ")
            word = word.replace("(동)", "동사형으로는 ")
            word = word.replace("(형)", "형용사형으로는 ")
            word = word.replace("(복수)", "여러 개를 지칭할 땐 ")

            return word

        def play_alarm_sound():
            audio_path = os.path.abspath("./resource/src/sound/chime.wav")
            url = QtCore.QUrl.fromLocalFile(audio_path)
            content = QtMultimedia.QMediaContent(url)
            self.player.setMedia(content)
            self.player.play()
            self.is_playing_alarm = True
            print("  [Info] Played Practice Alarm sound... (done)")

        def play_tts_audio_file():
            # content 가져오기
            content = get_downloaded_tts_audio_file()
            self.player.setMedia(content)
            self.player.play()

            # Setup [tts_idx, is_voca_changed]
            self.tts_idx += 1
            self.is_voca_changed = False
            self.is_playing_alarm = False
            print("  [Info] Played TTS sound... (done)")

        def get_detected_word(lang: str = None) -> str:
            if lang == self.JSON_DATA["LanguagesShow"]["UpperPart"]:
                word = self.mb_show_eng_adj.text()
            elif lang == self.JSON_DATA["LanguagesShow"]["LowerPart"]:
                word = self.mb_show_kor_adj.text()
            else:
                # 위 아래에 제시되는 언어가 아닐경우 (예: ru : 러시아어)
                try:
                    csv_word = self.CSV_DATA["dataframe"][self.CSV_DATA["dataframe"]["GroupName"] == self.group_name][lang]
                    word = csv_word.iloc[self.current_idx]

                    # iloc 에 해당하는 값이 None (비어있음)이면 자동번역기 실행
                    if type(word) is float:
                        print(f"  [Info] There is no word in CSV file. from:"
                              f"{self.JSON_DATA['LanguagesShow']['UpperPart']}-{self.mb_show_eng_adj.text()} -> "
                              f"to:{lang}-???")
                        word = search_text_by_lang(self.translated_result, lang)

                except KeyError:
                    # CSV 파일에 열이 생성되지도 않았을 때
                    print(f"  [info] Doesn't have Column:{lang}")
                    try:
                        # Check lang in show_lang // 혹시나 중국어와 같이 zh-Han / zh-CN 처럼 뒤 코드가 다를 경우 대비
                        if not lang in self.show_langs:
                            short_langs = [lang[0:2] for lang in self.show_langs]
                            # print(short_langs)
                            if lang[0:2] in short_langs:
                                # find lang index in short lang index
                                idx = short_langs.index(lang[0:2])
                                modified_lang = self.show_langs[idx]
                            else:
                                modified_lang = lang
                        word = search_text_by_lang(self.translated_result, modified_lang)
                    except KeyError:
                        word = ""
            return word
        
        def get_downloaded_tts_audio_file():
            audio_path = GetAudio.get_tts(word=self.word, lang=audio_lang,
                                          main_word=self.mb_show_eng_adj.text(),
                                          main_lang=self.JSON_DATA["LanguagesSpeech"]["First"])

            url = QtCore.QUrl.fromLocalFile(audio_path)
            content = QtMultimedia.QMediaContent(url)

            return content


        if self.player.state() == 0 and not self.is_finished and not self.is_playing_alarm:

            # 소리 내야 하는 언어 개수(self.lang)가 몇번 반복 됐는지 확인
            self.tts_idx = self.tts_idx % len(self.lang)

            # 소리 내야 하는 언어를 모두 재생 했지만, 단어 반복 횟수(예: 2번)가 다 돌지 않았다면 사진 바꾸기
            if self.tts_idx == 0:
                if not self.mb_top_bar_all.isChecked():
                    # Set practice time
                    practice_time = 500
                    self.timer.singleShot(practice_time, play_alarm_sound)
                if not self.is_voca_changed:
                    self.change_mb_voca_image(idx=self.image_idx)


            # 언어에 해당하는 단어가 소리 나도록 설정
            audio_lang = self.lang[self.tts_idx]
            self.word = get_detected_word(audio_lang)            

            # Korean이면 특수문자 제거하기
            self.word = replace_korean(self.word) if audio_lang == 'ko' else self.word

            # 아이들이 영어 따라 말할 수 있는 시간 주기
            if not self.mb_top_bar_all.isChecked():
                practice_time = 1500 if self.tts_idx == 0 else 0
                self.timer.singleShot(practice_time, play_tts_audio_file)
            else:
                play_tts_audio_file()

    def stop_player(self):
        self.is_finished = True
        self.is_playing = False

        self.BLACK.show()
        self.player.stop()

        self.pause.setStyleSheet("QPushButton {\n"
                                 f"background-image: url({self.pyqt_image_url(f'Play.svg')});\n"
                                 "}\n"
                                 "QPushButton:hover {\n"
                                 f"background-image: url({self.pyqt_image_url(f'PlayHover.svg')});"
                                 "}"
                                 )
        self.mb_show_btns_adj.raise_()

    def get_tts_audio(self, obj: str = None):
        # Get currentItem Text
        if (self.sending_from_widget != None and obj.currentRow() != -1):
            self.word = obj.currentItem().text()

            # Play Audio when is not playing Visual Voca Sliding
            if not self.is_playing:
                self.start_player()
                self.is_playing = True



    # <-- Resize Event Handler ------------------------------------------------------------->
    def change_stylesheet(self, obj, **kwargs):
        """
        대부분 폰트 사이즈를 윈도우 창 크기에 맞추어 바꾸도록 제작됨
        kwargs는 font=14px 와 같이 stylesheet에 즉시 적용될 수 있을 수준으로 작성 되어야 함
        """

        # Get Object name
        parent_widget = None
        obj_name = obj.objectName()

        if 'mb_show' in obj_name:
            parent_widget = self.mb_show_adj
        elif 'mb_voca' in obj_name:
            parent_widget = self.mb_voca_adj
        elif 'MainAPP' in obj_name:
            parent_widget = self

        # Find target selector and Crop Stylesheet
        stylesheet = parent_widget.styleSheet()
        start = stylesheet.find("".join(["#", obj_name, " ", "{"]))
        end = start + stylesheet[start:].find("}")
        crop_stylesheet = stylesheet[start:end]

        # Change stylesheet by kwargs
        for key, value in kwargs.items():
            key = key.replace("_", "-")
            new_start = crop_stylesheet.find("\n" + str(key) + ":") + 1
            new_end = new_start + crop_stylesheet[new_start:].find(";") + 1

            new_css = "".join([key, ": ", value, ";"])

            if new_start != 0:
                # print(f"  [Info] {obj_name}'s css has changed from:{crop_stylesheet[new_start:new_end]} -> to:{new_css})")
                if value != "del":
                    stylesheet = "".join([stylesheet[:start],
                                          crop_stylesheet[:new_start],
                                          new_css,
                                          crop_stylesheet[new_end:],
                                          stylesheet[end:]])
                elif value == "del":
                    stylesheet = "".join([stylesheet[:start],
                                          crop_stylesheet[:new_start],
                                          crop_stylesheet[new_end:],
                                          stylesheet[end:]])

            else:
                stylesheet = "".join([stylesheet[:start],
                                      crop_stylesheet,
                                      new_css,
                                      crop_stylesheet[new_end:],
                                      stylesheet[end:]])

            stylesheet = stylesheet.replace("\n\n", "\n")
        # Set StyleSheet
        parent_widget.setStyleSheet(stylesheet)

    def resize_widget(self):
        def calculate_font_ratio(obj, origin) -> int:
            font_size = None

            # Calculate resized height ratio
            resized_h = obj.geometry().getRect()[3]
            origin_h = origin

            # Get Original font size
            origin_font_size = origin_h - 40
            resized_font_size = origin_font_size * (resized_h / origin_h)
            font_size = int(resized_font_size)
            font_size = str(font_size) + 'px'

            return font_size

        def resize_widget_setting(obj, w: int = None, h: int = None):
            # get parent geometry
            obj_name = obj.objectName()
            _x, _y, _w, _h = obj.geometry().getRect()

            if 'mb_voca' in obj_name:
                _h = h - _y
                if 'mb_voca_scroll' in obj_name:
                    _h = _h - self.mb_voca_open_h - self.mb_voca_open_bottom
                elif 'mb_voca_open' in obj_name:
                    _y = h - self.mb_voca_open_h - self.mb_voca_open_bottom
                    _h = self.mb_voca_open_h

            elif 'mb_show' in obj_name:
                if w is not None:
                    _w = (w - self.mb_show_x)

                if h is not None:
                    if 'mb_show_adj' in obj_name:
                        _h = h
                    elif 'mb_show_eng_adj' in obj_name:
                        _y = int(h * self.mb_show_eng_adj_ratio_y)
                        _h = int(h * self.mb_show_eng_adj_ratio_h)
                    elif 'mb_show_image_adj' in obj_name:
                        _y = int(h * self.mb_show_image_adj_ratio_y)
                        _h = int(h * self.mb_show_image_adj_ratio_h)
                    elif 'mb_show_kor_adj' in obj_name:
                        _y = int(h * self.mb_show_kor_adj_ratio_y)
                        _h = int(h * self.mb_show_kor_adj_ratio_h)
                    elif 'mb_show_special_case_adj' in obj_name:
                        _y = int(h * self.mb_show_special_case_adj_ratio_y)
                        _h = int(h * self.mb_show_special_case_adj_ratio_h)
                    elif 'mb_show_btns_adj' in obj_name:
                        _y = int(h * self.mb_show_btns_adj_ratio_y)
                        _h = int(h * self.mb_show_btns_adj_ratio_h)
                    elif 'mb_show_dev' in obj_name:
                        _y = h - _h
                        _w -= 10

            elif 'BLACK' in obj_name:
                _w = w + 2
                _h = h + 2

            elif 'movie' in obj_name:
                _h = h + 10

            obj.setGeometry(QtCore.QRect(_x, _y, _w, _h))

        # Change widget size when window resized event emitted
        x, y, w, h = self.geometry().getRect()

        # Window Section
        resize_widget_setting(self.mb_1, w=w, h=h)

        # Left - Side Bar Section
        resize_widget_setting(self.mb_voca_adj, h=h)
        resize_widget_setting(self.mb_voca_scroll, h=h)
        resize_widget_setting(self.mb_voca_open, h=h)

        # Right - Main Showing Section
        resize_widget_setting(self.mb_show_adj, w=w, h=h)
        resize_widget_setting(self.mb_show_eng_adj, w=w, h=h)
        resize_widget_setting(self.mb_show_image_adj, w=w, h=h)
        resize_widget_setting(self.mb_show_kor_adj, w=w, h=h)
        resize_widget_setting(self.mb_show_special_case_adj, w=w, h=h)
        resize_widget_setting(self.mb_show_btns_adj, w=w, h=h)
        resize_widget_setting(self.mb_show_dev, w=w, h=h)
        resize_widget_setting(self.BLACK, w=w, h=h)

        # Right - Main Font Resize Section
        self.change_stylesheet(self.mb_show_eng_adj, font=calculate_font_ratio(self.mb_show_eng_adj, self.mb_show_eng_h))
        self.change_stylesheet(self.mb_show_kor_adj, font=calculate_font_ratio(self.mb_show_kor_adj, self.mb_show_kor_h))
        self.change_stylesheet(self.mb_show_special_case_adj, font=calculate_font_ratio(self.mb_show_eng_adj, self.mb_show_eng_h))

    def resizeEvent(self, event):
        self.resized.emit()
        return super(MainWindow, self).resizeEvent(event)


if __name__ == "__main__":
    # Run main app
    app = QtWidgets.QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec_())

"""
pyinstaller -w -F --log-level=WARN --hidden-import AutoSigner/main_ui.py --hidden-import AutoSigner/main_rc.py --icon=./AutoSigner/icon.ico "AutoSig.exe" ./AutoSigner/main.py
pyinstaller -w -F --log-level=WARN --hidden-import ./AutoSigner/main_ui.py --hidden-import ./AutoSigner/main_rc.py --icon=./AutoSigner/icon.ico main.py
pyinstaller -w -F --log-level=WARN --hidden-import AutoSigner/main_ui.py --hidden-import AutoSigner/main_rc.py --icon=./AutoSigner/icon.ico main.py
pyinstaller -w -F --log-level=WARN --hidden-import AutoSigner/main_ui.py --icon=./AutoSigner/icon.ico main.py
pyinstaller -w -F --log-level=WARN --hidden-import ./AutoSigner/main_ui --icon=./AutoSigner/icon.ico main.py

pyinstaller -w -F --log-level=WARN --icon=./resource/src/img/Appicon.ico app.py
pyinstaller -F --log-level=WARN --icon=./resource/src/img/Appicon.ico app.py
"""