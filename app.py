# <-- Import main pyqt app modules ----------------------------------------------------------->
import sys
import os.path
from glob import glob
from fontTools import ttLib
from PyQt5 import QtWidgets, QtCore, QtGui, Qt, QtMultimedia

# Import Local Python Files
from resource.py import GetImages
from resource.py import GetAudio
from resource.py.Translator import translate, search_text_by_lang
from resource.py.ToggleButton import AnimatedToggle
from resource.py.Json import load_json_file, save_json_file, generate_init
from resource.py.CSVData import get_main_csv
from resource.src.ui.main_ui import Ui_MainApp as mp

# <-- Import App Update modules --------------------------------------------------------------->
import logging
import shutil
import stat
import tempfile
import traceback

REPO_DIR = os.path.expanduser('~' + os.sep + '.myrepo')
URL = 'https://MYPROJECT.googlecode.com/hg/'
MYAPPLOGGER = 'WHATEVER'

__author__ = 'https://www.github.com/gonyo1'
__date__ = 'October 2023'
__credits__ = ['Gonyo', 'AhnJH']


class AppUpdator(QtCore.QThread):
    """This class automatically updates a PyQt app from a remote
    Gonyo1's VisualVocaApp repository
    # Mercurial repository.
    """

    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)
        # self.ui = ui.ui()
        self.logger = logging.getLogger(MYAPPLOGGER)
        self.info = lambda msg: self.logger.info(msg)
        self.debug = lambda msg: self.logger.debug(msg)
        self.ui = ui.ui()
        self.url = 'https://open-ihm.googlecode.com/hg/'
        try:
            self.repo = hg.repository(self.ui, REPO_DIR)
        except Exception:
            self.repo = hg.repository(self.ui, REPO_DIR, create=True)
        return

    def run(self):
        # Redirect stdin and stdout to tempfiles.
        # This fixes a Windows bug which causes a Bad File Descriptor error.
        sys.stdout = tempfile.TemporaryFile()
        sys.stderr = tempfile.TemporaryFile()
        try:
            self.pullAndMerge()
        except Exception:
            self.fail()
            return
        try:
            self.install()
        except Exception:
            self.fail()
            return
        self.emit(QtCore.SIGNAL("updateSuccess()"))
        return

    def chmod(self):
        """Fix a Windows bug which marks files / folders in REPO_DIR read-only.
        """
        if not (sys.platform == 'win32' or sys.platform == 'cygwin'):
            return
        for root, dirs, files in os.walk(REPO_DIR):
            for name in files:
                os.chmod(os.path.join(root, name), stat.S_IWRITE)
            for name in dirs:
                os.chmod(os.path.join(root, name), stat.S_IWRITE)
        return

    def fail(self):
        """Called if an error occurs.
        Take the traceback, log it and notify the MainWindow.
        """
        ty, value, tback = sys.exc_info()
        msg = ''.join(traceback.format_exception(ty, value, tback))
        self.debug(msg)
        self.updateFail(msg)
        return

    def clone(self):
        """If we don't have a copy of the open-ihm repository on disk
        clone one now.
        """
        try:
            self.chmod()
            commands.clone(self.ui, self.url, dest=REPO_DIR, insecure=True)
        except Exception:
            self.fail()
        return

    def pullAndMerge(self):
        """Run an hg pull and update.
        Overwrite all local changes by default.
        If anything goes wrong with the pull or update, clone instead.
        """
        try:
            self.chmod()
            commands.pull(self.ui, self.repo, source=self.url)
            self.chmod()
            commands.update(self.ui, self.repo, clean=True)
        except error.RepoError:
            if os.path.exists(REPO_DIR):
                shutil.rmtree(REPO_DIR)
                self.clone()
        return

    def install(self):
        # Use distutils or whatever to install app.
        return

    def updateFail(self, message):
        """If checking for updates times out (for example, if there
        is no current network connection) then fail silently.
        """
        self.emit(QtCore.SIGNAL("updateFailure(QString)"), QtCore.QString(message))
        return


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
        self.setWindowTitle("  VisualVoca")
        self.setWindowIcon(Qt.QIcon("resource/src/img/AppIcon.ico"))
        self.mb_icon.setPixmap(Qt.QPixmap('resource/src/img/Logo.svg'))
        self.setup_window_graphic()

        # Setup Signal and Slots
        self.set_signal()

        # Repostion of mainwidget
        if geometry != None:
            self.setGeometry(geometry)

        # Broadcast FIRSTRUN Finished
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
            base_name = "resource/src/font/NotoSansKR-SemiBold"
            font_path = ".".join(base_name, "ttf")
            font_name = "Noto Sans KR SemiBold"
            print(f"  [Error] Error happened while getting font name: {e}")

        fontDB.addApplicationFont(os.path.abspath(font_path))

        # Customize font family
        self.setFont(QtGui.QFont(font_name))
        custom_stylesheet = self.styleSheet()
        custom_stylesheet = custom_stylesheet.replace("Noto Sans KR SemiBold", font_name)
        self.setStyleSheet(custom_stylesheet)

    def set_variable(self):
        # Configuration Variables
        self.PLATFORM = sys.platform
        self.FIRSTRUN = True
        self.auto_scroll_toggle = QtWidgets.QCheckBox()
        self.auto_slide = True

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

        # Audion Variables
        self.player = QtMultimedia.QMediaPlayer()
        self.lang = list(self.JSON_DATA["LanguagesSpeech"].values())
        self.is_playing = False
        self.is_finished = False
        self.tts_idx = 0
        self.tts_repeat = 3

        # ETC
        self.timer = QtCore.QTimer(self)

    def set_signal(self, *args):
        def insert_total_signal():
            # Mainwindow buttons
            self.mb_voca_open.clicked.connect(self.open_folder)
            self.mb_voca_refresh.clicked.connect(self.refresh_all_component)
            self.auto_scroll_toggle.stateChanged.connect(lambda state, key="AutoScroll": self.change_json_file(key=key))

            # mb_show part
            self.pause.clicked.connect(self.is_clicked_pause)
            for btn in [self.forward, self.back]:
                btn.clicked.connect(self.player.stop)
                btn.clicked.connect(self.is_clicked_back_forward)
            self.mb_show_top_bar_repeat_TextEdit.textEdited.connect(lambda: self.change_json_file(key="ImageDownCount"))

            # window resized event
            self.resized.connect(self.resize_widget)

            # pushbutton clicked event on QListWidget
            insert_pushbutton_signal()

            # voca word clicked event on QListWidget
            insert_QListWidget_item_signal()

        def insert_pushbutton_signal():
            for btn in self.voca_widget_button:
                btn.clicked.connect(self.voca_widget_button_event)

        def insert_QListWidget_item_signal():
            self.list_widgets = self.findChildren(QtWidgets.QListWidget)

            self.list_widgets = [wdg for wdg in self.list_widgets if not wdg.isVisible()]

            for idx, widget in enumerate(self.list_widgets):
                if widget.objectName() != "mb_voca_word_adj_0":
                    widget.itemClicked.connect(self.change_current_widget)
                    widget.currentRowChanged.connect(lambda: self.change_mb_voca_widget(obj=self.sending_from_widget))
                    widget.currentRowChanged.connect(lambda: self.get_audio_tts(obj=self.sending_from_widget))

        self.player.stateChanged.connect(self.play_tts_audio)

        if self.FIRSTRUN:
            insert_total_signal()
        if len(args) > 0:
            if args[0] == 'pushbutton':
                insert_pushbutton_signal()
            elif args[0] == 'qlistwidget':
                insert_QListWidget_item_signal()

    # <-- Main Window Section -------------------------------------------------------------->
    def setup_window_graphic(self):
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
                    obj.setObjectName(f"mb_voca_widget_{index}")

                    return obj

                def setup_VHox_wrapper(parent=None):
                    obj = QtWidgets.QVBoxLayout(parent)
                    obj.setContentsMargins(0, 0, 0, 0)
                    obj.setSpacing(0)
                    obj.setObjectName(f"mb_voca_widget_verticalLayout_{index}")

                    return obj

                def setup_button_main_widget(parent=None):
                    obj = QtWidgets.QWidget(parent)
                    obj.setMaximumSize(QtCore.QSize(16777215, 30))
                    obj.setObjectName(f"mb_voca_button_adj_{index}")
                    obj.setStyleSheet("QWidget:hover {background-color: rgb(204, 227, 249);}")

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
                    obj.setMaximumSize(QtCore.QSize(16777215, 20))
                    obj.setStyleSheet("")
                    obj.setText("")
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
                    obj.setMaximumSize(QtCore.QSize(16777215, 16777215))
                    obj.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
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
                        self.q_list_widget.addItem(item)
                        self.q_list_widget.item(w_idx).setText(word)

            voca_widgets = find_mb_voca_widgets()
            make_mb_voca_widget()

            # find PushButton
            self.voca_widget_button = [btn for btn in self.findChildren(QtWidgets.QPushButton) if
                                       'mb_voca_button_group_title_adj' in btn.objectName()]
            self.voca_widget_button = [btn for btn in self.voca_widget_button if not btn.isVisible()]

        def make_toggle_button():
            if self.FIRSTRUN:
                self.auto_scroll_toggle = AnimatedToggle(
                    checked_color="#4ed164"
                )
                self.mb_top_bar_auto_scroll_verticalLayout.addWidget(self.auto_scroll_toggle)

                self.auto_scroll_toggle.setStyleSheet("margin: 6px 0px 6px 0px\n")
                self.auto_scroll_toggle.setMaximumHeight(self.mb_top_bar_auto_scroll_title.height())
                self.auto_scroll_toggle.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

                _bool = True if self.JSON_DATA["AutoScroll"] == 'True' else False
                self.auto_scroll_toggle.setChecked(_bool)

        def make_black_vail():
            self.BLACK = QtWidgets.QLabel(self.mb_show_adj)
            self.BLACK.setObjectName("BLACK")
            self.BLACK.setStyleSheet("background-color: rgba(0, 0, 0, 200);\n")
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

        def insert_refresh_icon():
            # Get Folder Image Path
            base_path = os.path.abspath("./resource/src/img")

            refresh = os.path.join(base_path, "Refresh.svg")
            refresh = refresh.replace("\\", "/")

            refresh_hover = os.path.join(base_path, "RefreshHover.svg")
            refresh_hover = refresh_hover.replace("\\", "/")

            self.mb_voca_refresh.setStyleSheet("QPushButton {margin: 5px;\n"
                                               "padding: 0px;\n"
                                               f"background-image: url({refresh});\n"
                                               "background-repeat: none;\n"
                                               "background-position: center;\n"
                                               "}\n"
                                               "QPushButton:hover {\n"
                                               f"background-image: url({refresh_hover});\n"
                                               "}\n"
                                               )

        def insert_FrontImage():
            self.movie = QtGui.QMovie(os.path.abspath("./resource/src/img/FrontAnimation.gif"), QtCore.QByteArray(),
                                      self)
            self.movie.setCacheMode(QtGui.QMovie.CacheAll)

            self.mb_show_image_adj.setMovie(self.movie)
            self.movie.start()

        # UI 에서 샘플로 만들었던 위젯 지우기
        self.mb_voca_widget_0.hide()
        self.mb_voca_refresh.setEnabled(True)
        self.mb_show_btns_adj.hide()
        self.mb_show_top_bar_repeat_TextEdit.setText(str(self.JSON_DATA["ImageDownCount"]))

        # Do Something...
        make_voca_groups()
        make_toggle_button()
        make_black_vail()

        insert_folder_image()
        insert_refresh_icon()
        insert_FrontImage()

        self.voca_widget_button_event()

        calculate_ratio()

    def refresh_all_component(self):

        # Setup GUI Widget
        # self.set_font_family()
        self.JSON_DATA = load_json_file()
        self.CSV_DATA = get_main_csv()

        self.close()

        geometry = self.geometry()
        self.__init__(geometry=geometry)
        self.mb_show_image_adj.setMovie(self.movie)

    def open_folder(self):
        base_path = os.path.abspath("./resource/voca/WordList.csv")

        if self.PLATFORM == "win32":
            os.startfile(base_path)
        elif self.PLATFORM == 'drawin':
            os.system(f"open {base_path}")

    def remove_item_from_VBox(self, parent, obj):
        _type = str(type(parent))
        if _type in ("PyQt5.QtWidgets.QVBoxLayout"):
            idx = parent.indexOf(obj)
            item = parent.itemAt(idx)
            parent.removeItem(item)
        elif _type == ("<class 'PyQt5.QtWidgets.QWidget'>",
                       "<class 'PyQt5.QtWidgets.QListWidget'>"):
            obj.deleteLater()

    def change_json_file(self, key=None, value=None):
        if key == "AutoScroll":
            value = str(self.auto_scroll_toggle.isChecked())
            save_json_file(key, value)

        elif key == "ImageDownCount":
            value = self.mb_show_top_bar_repeat_TextEdit.text()
            value = int(value) if value.isdigit() else 3
            value = 10 if (value > 10) else value
            self.mb_show_top_bar_repeat_TextEdit.setText(str(value))
            self.JSON_DATA["ImageDownCount"] = value
            save_json_file(key, value)

    # <-- New Voca Clicked Event Handler --------------------------------------------------->
    def change_current_widget(self):
        self.player.stop()

        self.sending_from_widget = self.sender()

        if (self.sending_from_widget != None):
            idx = self.sending_from_widget.currentRow()

            # 첫번째는 어쩔 수 없이 직접 실행해야하나 봄...
            self.sending_from_widget.setCurrentRow(idx)
            self.change_mb_voca_widget(obj=self.sending_from_widget)
            self.get_audio_tts(obj=self.sending_from_widget)

    def change_mb_voca_widget(self, obj):
        self.mb_show_eng_adj.setStyleSheet("color: black;\n")
        self.mb_show_kor_adj.setStyleSheet("color: black;\n")
        self.mb_show_btns_adj.show()
        self.BLACK.hide()
        self.player.stop()

        # Get currentItem Text
        if (self.sending_from_widget != None):
            self.is_voca_changed = True
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
                self.translated_result = translate(word=self.word,
                                                   langs=self.JSON_DATA["LanguagesSpeech"],
                                                   key=self.JSON_DATA["APIKeys"]["MSAzureTranslator"])
                lower_text = search_text_by_lang(self.translated_result, lower_text_language)

            self.mb_show_kor_adj.setText(lower_text)

            # Change image when voca has been changed
            self.change_mb_voca_image(self.image_idx)

    def change_mb_voca_image(self, idx):
        # Add image_idx
        if idx >= len(self.pics):
            self.move_next_voca()
        else:
            # Get image and change pixmap
            pic = self.pics[idx]

            self.mb_show_image_adj.clear()
            # self.mb_show_image_adj.setPixmap(pic)
            self.mb_show_image_adj.setPixmap(
                pic.scaled(QtCore.QSize(self.mb_show_image_adj.width(), self.mb_show_image_adj.height()),
                           aspectRatioMode=QtCore.Qt.KeepAspectRatio,
                           transformMode=QtCore.Qt.SmoothTransformation
                           )
                )
            self.mb_show_image_adj.repaint()

            self.image_idx += 1

    def move_next_voca(self):
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
            print("  [Info] <-- Auto scroll is not clicked -->")

    def stop_player(self):
        self.is_finished = True
        self.is_playing = False

        self.BLACK.show()
        self.player.stop()

        self.mb_show_btns_adj.raise_()
        self.pause.setText("▶")
        # self.mb_show_btns_adj.hide()

    def voca_widget_button_event(self):
        self.stop_player()
        self.BLACK.hide()
        self.pause.setText("■")

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
                    h = append_list_widget.sizeHintForRow(
                        0) * append_list_widget.count() + 2 * append_list_widget.frameWidth()
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

    # <-- Top/Bottom Bar Button Event ------------------------------------------------------>
    def is_clicked_pause(self):
        if not self.is_pause_clicked:
            # stop player
            self.stop_player()

            # change setting
            self.is_finished = True
            self.is_playing = False
            self.is_pause_clicked = True

            # show black
            self.BLACK.show()

            for item in [self.mb_show_eng_adj, self.mb_show_image_adj, self.mb_show_kor_adj, self.mb_show_btns_adj]:
                item.raise_()
                item.show()
                item.setStyleSheet("color: white;\n")

            self.mb_show_btns_adj.setStyleSheet("color: black;\n")
            self.pause.setText("▶")
        else:
            # play player
            self.change_mb_voca_widget(obj=self.sending_from_widget)
            self.get_audio_tts(obj=self.sending_from_widget)

            # change setting
            self.is_pause_clicked = False

            # hide black
            self.BLACK.hide()

            for item in [self.mb_show_eng_adj, self.mb_show_image_adj, self.mb_show_kor_adj, self.mb_show_btns_adj]:
                item.raise_()
                item.show()
                item.setStyleSheet("color: black;\n")

            self.pause.setText("■")

    def is_clicked_back_forward(self):
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

        for item in [self.mb_show_eng_adj, self.mb_show_image_adj, self.mb_show_kor_adj, self.mb_show_btns_adj]:
            item.raise_()
            item.show()
            item.setStyleSheet("color: black")

        self.pause.setText("■")

    # <-- Play audio TTS ------------------------------------------------------------------->
    def play_tts_audio(self):
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

        if self.player.state() == 0 and \
                not self.is_finished:
            # Todo 마지막에 한번 더 나오는거 어떻게 처리할지 고민해보기

            # Play ALL TTS Audio in language list
            self.tts_idx = self.tts_idx % len(self.lang)

            # If ALL TTS Files played, change images
            if self.tts_idx == 0 and not self.is_voca_changed:
                self.change_mb_voca_image(idx=self.image_idx)

            audio_lang = self.lang[self.tts_idx]

            # 뜻에 맞추어 소리 나도록 설정
            if audio_lang == self.JSON_DATA["LanguagesShow"]["UpperPart"]:
                self.word = self.mb_show_eng_adj.text()
            elif audio_lang == self.JSON_DATA["LanguagesShow"]["LowerPart"]:
                self.word = self.mb_show_kor_adj.text()
            else:
                try:
                    csv_word = self.CSV_DATA["dataframe"][self.CSV_DATA["dataframe"]["GroupName"] == self.group_name][
                        audio_lang]
                    self.word = csv_word.iloc[self.current_idx]

                    print(self.word)
                    # iloc 에 해당하는 값이 None (비어있음)이면 자동번역기 실행
                    if type(self.word) is float:
                        print(f"  [Info] There is no word in CSV file. from:"
                              f"{self.JSON_DATA['LanguagesShow']['UpperPart']}-{self.mb_show_eng_adj.text()} -> "
                              f"to:{audio_lang}-???")
                        self.word = search_text_by_lang(self.translated_result, audio_lang)
                except KeyError:
                    print(f"  [info] Doesn't have Column:{audio_lang}")
                    # CSV 파일에 audio_lang 언어가 없다면 자동번역기 실행하기
                    self.word = search_text_by_lang(self.translated_result, audio_lang)

            # Korean이면 특수문자 제거하기
            if audio_lang == 'ko':
                self.word = replace_korean(self.word)

            audio_path = GetAudio.get_tts(word=self.word, lang=audio_lang)

            url = QtCore.QUrl.fromLocalFile(audio_path)
            content = QtMultimedia.QMediaContent(url)
            # content = QtMultimedia.QMediaContent()

            self.player.setMedia(content)
            self.player.play()

            # Setup [tts_idx, is_voca_changed]
            self.tts_idx += 1
            self.is_voca_changed = False

    def get_audio_tts(self, obj: str = None):
        # Get currentItem Text
        if (self.sending_from_widget != None):
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
            origin_font_size = origin_h - 40
            resized_font_size = origin_font_size * (resized_h / origin_h)
            font_size = int(resized_font_size)
            font_size = str(font_size) + 'px'

            return font_size

        def resize_widget_setting(parent, obj, w: int = None, h: int = None):
            # print("  [Info] Resize Event emitted")
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

            elif 'BLACK' in obj.objectName():
                _w = w + 2
                _h = h + 2

            obj.setGeometry(QtCore.QRect(_x, _y, _w, _h))

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
                stylesheet = "".join([stylesheet[:start],
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
        resize_widget_setting(self, self.BLACK, w=w, h=h)

        # Right - Main Font Resize Section
        change_stylesheet(self, self.mb_show_eng_adj,
                          font=calculate_font_ratio(self.mb_show_eng_adj, self.mb_show_eng_h))
        change_stylesheet(self, self.mb_show_kor_adj,
                          font=calculate_font_ratio(self.mb_show_kor_adj, self.mb_show_kor_h))

    def resizeEvent(self, event):
        self.resized.emit()
        return super(MainWindow, self).resizeEvent(event)


if __name__ == "__main__":
    def get_ui_python_file():
        try:
            os.system("pyuic5 resource/src/ui/main.ui -o resource/src/ui/main_ui.py")
            print("  [Info] pyuic5 has done...")
            # os.system("pyrcc5 main.qrc -o main_rc.py")
        except FileNotFoundError:
            print("  [Error] Error happened from 'pyuic5 or pyrcc5' ")


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
    get_ui_python_file()

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

__author__ = 'https://www.github.com/gonyo1'
__date__ = 'October 2023'
__credits__ = ['Gonyo', 'AhnJH']


class AppUpdator(QtCore.QThread):
    """This class automatically updates a PyQt app from a remote
    Gonyo1's VisualVocaApp repository
    # Mercurial repository.
    """
    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)
        # self.ui = ui.ui()
        self.logger = logging.getLogger(MYAPPLOGGER)
        self.info = lambda msg: self.logger.info(msg)
        self.debug = lambda msg: self.logger.debug(msg)
        self.ui = ui.ui()
        self.url = 'https://open-ihm.googlecode.com/hg/'
        try:
            self.repo = hg.repository(self.ui, REPO_DIR)
        except Exception:
            self.repo = hg.repository(self.ui, REPO_DIR, create=True)
        return

    def run(self):
        # Redirect stdin and stdout to tempfiles.
        # This fixes a Windows bug which causes a Bad File Descriptor error.
        sys.stdout = tempfile.TemporaryFile()
        sys.stderr = tempfile.TemporaryFile()
        try:
            self.pullAndMerge()
        except Exception:
            self.fail()
            return
        try:
            self.install()
        except Exception:
            self.fail()
            return
        self.emit(QtCore.SIGNAL("updateSuccess()"))
        return

    def chmod(self):
        """Fix a Windows bug which marks files / folders in REPO_DIR read-only.
        """
        if not (sys.platform == 'win32' or sys.platform == 'cygwin'):
            return
        for root, dirs, files in os.walk(REPO_DIR):
            for name in files:
                os.chmod(os.path.join(root, name), stat.S_IWRITE)
            for name in dirs:
                os.chmod(os.path.join(root, name), stat.S_IWRITE)
        return

    def fail(self):
        """Called if an error occurs.
        Take the traceback, log it and notify the MainWindow.
        """
        ty, value, tback = sys.exc_info()
        msg = ''.join(traceback.format_exception(ty, value, tback))
        self.debug(msg)
        self.updateFail(msg)
        return

    def clone(self):
        """If we don't have a copy of the open-ihm repository on disk
        clone one now.
        """
        try:
            self.chmod()
            commands.clone(self.ui, self.url, dest=REPO_DIR, insecure=True)
        except Exception:
            self.fail()
        return

    def pullAndMerge(self):
        """Run an hg pull and update.
        Overwrite all local changes by default.
        If anything goes wrong with the pull or update, clone instead.
        """
        try:
            self.chmod()
            commands.pull(self.ui, self.repo, source=self.url)
            self.chmod()
            commands.update(self.ui, self.repo, clean=True)
        except error.RepoError:
            if os.path.exists(REPO_DIR):
                shutil.rmtree(REPO_DIR)
                self.clone()
        return

    def install(self):
        # Use distutils or whatever to install app.
        return

    def updateFail(self, message):
        """If checking for updates times out (for example, if there
        is no current network connection) then fail silently.
        """
        self.emit(QtCore.SIGNAL("updateFailure(QString)"), QtCore.QString(message))
        return


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
        self.setWindowTitle("  VisualVoca")
        self.setWindowIcon(Qt.QIcon("resource/src/img/AppIcon.ico"))
        self.mb_icon.setPixmap(Qt.QPixmap('resource/src/img/Logo.svg'))
        self.setup_window_graphic()

        # Setup Signal and Slots
        self.set_signal()

        # Repostion of mainwidget
        if geometry != None:
            self.setGeometry(geometry)

        # Broadcast FIRSTRUN Finished
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
            font_file_name = [del_special_character(os.path.basename(item).replace(".ttf","")) for item in font_file_list]

            # Find User Target Font
            idx = font_file_name.index(modified_font_name)
            font_path = font_file_list[idx]
            font_name = get_font_name(font_path)
            print(f"  [Info] Font changed Successfully to User font:{font_name}")

        except Exception as e:
            # Set font as Noto Sans KR Semi Bold if error happened
            base_name = "resource/src/font/NotoSansKR-SemiBold"
            font_path = ".".join(base_name, "ttf")
            font_name = "Noto Sans KR SemiBold"
            print(f"  [Error] Error happened while getting font name: {e}")

        fontDB.addApplicationFont(os.path.abspath(font_path))

        # Customize font family
        self.setFont(QtGui.QFont(font_name))
        custom_stylesheet = self.styleSheet()
        custom_stylesheet = custom_stylesheet.replace("Noto Sans KR SemiBold", font_name)
        self.setStyleSheet(custom_stylesheet)

    def set_variable(self):
        # Configuration Variables
        self.PLATFORM = sys.platform
        self.FIRSTRUN = True
        self.auto_scroll_toggle = QtWidgets.QCheckBox()
        self.auto_slide = True

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

        # Audion Variables
        self.player = QtMultimedia.QMediaPlayer()
        self.lang = ['en', 'ko']
        self.is_playing = False
        self.is_finished = False
        self.tts_idx = 0
        self.tts_repeat = 3

        # ETC
        self.timer = QtCore.QTimer(self)

    def set_signal(self, *args):
        def insert_total_signal():
            # Mainwindow buttons
            self.mb_voca_open.clicked.connect(self.open_folder)
            self.mb_voca_refresh.clicked.connect(self.refresh_all_component)
            self.auto_scroll_toggle.stateChanged.connect(lambda state, key="AutoScroll": self.change_json_file(key=key))

            # mb_show part
            self.pause.clicked.connect(self.is_clicked_pause)
            for btn in [self.forward, self.back]:
                btn.clicked.connect(self.player.stop)
                btn.clicked.connect(self.is_clicked_back_forward)
            self.mb_show_top_bar_repeat_TextEdit.textEdited.connect(lambda: self.change_json_file(key="ImageDownCount"))

            # window resized event
            self.resized.connect(self.resize_widget)

            # pushbutton clicked event on QListWidget
            insert_pushbutton_signal()

            # voca word clicked event on QListWidget
            insert_QListWidget_item_signal()

        def insert_pushbutton_signal():
            for btn in self.voca_widget_button:
                btn.clicked.connect(self.voca_widget_button_event)

        def insert_QListWidget_item_signal():
            self.list_widgets = self.findChildren(QtWidgets.QListWidget)

            self.list_widgets = [wdg for wdg in self.list_widgets if not wdg.isVisible()]

            for idx, widget in enumerate(self.list_widgets):
                if widget.objectName() != "mb_voca_word_adj_0":
                    widget.itemClicked.connect(self.change_current_widget)
                    widget.currentRowChanged.connect(lambda: self.change_mb_voca_widget(obj=self.sending_from_widget))
                    widget.currentRowChanged.connect(lambda: self.get_audio_tts(obj=self.sending_from_widget))

        self.player.stateChanged.connect(self.play_tts_audio)

        if self.FIRSTRUN:
            insert_total_signal()
        if len(args) > 0:
            if args[0] == 'pushbutton':
                insert_pushbutton_signal()
            elif args[0] == 'qlistwidget':
                insert_QListWidget_item_signal()

    # <-- Main Window Section -------------------------------------------------------------->
    def setup_window_graphic(self):
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
                    obj.setObjectName(f"mb_voca_widget_{index}")

                    return obj

                def setup_VHox_wrapper(parent=None):
                    obj = QtWidgets.QVBoxLayout(parent)
                    obj.setContentsMargins(0, 0, 0, 0)
                    obj.setSpacing(0)
                    obj.setObjectName(f"mb_voca_widget_verticalLayout_{index}")

                    return obj

                def setup_button_main_widget(parent=None):
                    obj = QtWidgets.QWidget(parent)
                    obj.setMaximumSize(QtCore.QSize(16777215, 30))
                    obj.setObjectName(f"mb_voca_button_adj_{index}")
                    obj.setStyleSheet("QWidget:hover {background-color: rgb(204, 227, 249);}")

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
                    obj.setMaximumSize(QtCore.QSize(16777215, 20))
                    obj.setStyleSheet("")
                    obj.setText("")
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
                    obj.setMaximumSize(QtCore.QSize(16777215, 16777215))
                    obj.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
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


                for index, value in enumerate(reversed(groups)):
                    index += 1

                    # Make QWidget for wrapping
                    self.q_widget_wrapper = make_voca_widget_by_code()
                    self.mb_voca_scroll_widget_verticalLayout.insertWidget(1, self.q_widget_wrapper)

                    # Set Group name to QPushButton Title
                    self.q_pushbutton_title.setText(value)

                    # Get Voca from Selected Group
                    words_in_group = self.CSV_DATA["dataframe"][self.CSV_DATA["dataframe"]["그룹"] == value]["단어"]
                    words_in_group = words_in_group.to_list()

                    # Set QListWidgetItem text as voca
                    for w_idx, word in enumerate(words_in_group):
                        item = QtWidgets.QListWidgetItem()
                        self.q_list_widget.addItem(item)
                        self.q_list_widget.item(w_idx).setText(word)

            voca_widgets = find_mb_voca_widgets()
            make_mb_voca_widget()

            # find PushButton
            self.voca_widget_button = [btn for btn in self.findChildren(QtWidgets.QPushButton) if
                                       'mb_voca_button_group_title_adj' in btn.objectName()]
            self.voca_widget_button = [btn for btn in self.voca_widget_button if not btn.isVisible()]

        def make_toggle_button():
            if self.FIRSTRUN:
                self.auto_scroll_toggle = AnimatedToggle(
                    checked_color="#4ed164"
                )
                self.mb_top_bar_auto_scroll_verticalLayout.addWidget(self.auto_scroll_toggle)

                self.auto_scroll_toggle.setStyleSheet("margin: 6px 0px 6px 0px\n")
                self.auto_scroll_toggle.setMaximumHeight(self.mb_top_bar_auto_scroll_title.height())
                self.auto_scroll_toggle.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))


                _bool = True if self.JSON_DATA["AutoScroll"] == 'True' else False
                self.auto_scroll_toggle.setChecked(_bool)

        def make_black_vail():
            self.BLACK = QtWidgets.QLabel(self.mb_show_adj)
            self.BLACK.setObjectName("BLACK")
            self.BLACK.setStyleSheet("background-color: rgba(0, 0, 0, 200);\n")
            self.BLACK.setGeometry(-1, -1, 772, 702)
            self.BLACK.hide()

        def insert_folder_image():
            # Get Folder Image Path
            base_path = os.path.abspath("./resource/src/img")
            self.folder_icon = Qt.QPixmap(os.path.join(base_path, "Folder.svg"))
            self.folder_open_icon = Qt.QPixmap(os.path.join(base_path, "FolderOpen.svg"))

            # Find Voca Button Object from parent
            voca_btns = [label for label in self.findChildren(QtWidgets.QLabel) if 'mb_voca_button_icon_adj' in label.objectName()]
            push_btns = [push for push in self.findChildren(QtWidgets.QPushButton) if 'mb_voca_button_group_title_adj' in push.objectName()]

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

        def insert_refresh_icon():
            # Get Folder Image Path
            base_path = os.path.abspath("./resource/src/img")

            refresh = os.path.join(base_path, "Refresh.svg")
            refresh = refresh.replace("\\", "/")

            refresh_hover = os.path.join(base_path, "RefreshHover.svg")
            refresh_hover = refresh_hover.replace("\\", "/")

            self.mb_voca_refresh.setStyleSheet("QPushButton {margin: 5px;\n"
                                               "padding: 0px;\n"
                                               f"background-image: url({refresh});\n"
                                               "background-repeat: none;\n"
                                               "background-position: center;\n"
                                               "}\n"
                                               "QPushButton:hover {\n"
                                               f"background-image: url({refresh_hover});\n"
                                               "}\n"
                                               )

        def insert_FrontImage():
            self.movie = QtGui.QMovie(os.path.abspath("./resource/src/img/FrontAnimation.gif"), QtCore.QByteArray(), self)
            self.movie.setCacheMode(QtGui.QMovie.CacheAll)

            self.mb_show_image_adj.setMovie(self.movie)
            self.movie.start()

        # UI 에서 샘플로 만들었던 위젯 지우기
        self.mb_voca_widget_0.hide()
        self.mb_voca_refresh.setEnabled(True)
        self.mb_show_btns_adj.hide()
        self.mb_show_top_bar_repeat_TextEdit.setText(str(self.JSON_DATA["ImageDownCount"]))

        # Do Something...
        make_voca_groups()
        make_toggle_button()
        make_black_vail()
        
        insert_folder_image()
        insert_refresh_icon()
        insert_FrontImage()
        
        self.voca_widget_button_event()
        
        calculate_ratio()

    def refresh_all_component(self):

        # Setup GUI Widget
        # self.set_font_family()
        self.JSON_DATA = load_json_file()
        self.CSV_DATA = get_main_csv()

        self.close()

        geometry = self.geometry()
        self.__init__(geometry=geometry)
        self.mb_show_image_adj.setMovie(self.movie)

    def open_folder(self):
        base_path = os.path.abspath("./resource/voca/WordList.csv")

        if self.PLATFORM == "win32":
            os.startfile(base_path)
        elif self.PLATFORM == 'drawin':
            os.system(f"open {base_path}")

    def remove_item_from_VBox(self, parent, obj):
        _type = str(type(parent))
        if _type in ("PyQt5.QtWidgets.QVBoxLayout"):
            idx = parent.indexOf(obj)
            item = parent.itemAt(idx)
            parent.removeItem(item)
        elif _type == ("<class 'PyQt5.QtWidgets.QWidget'>",
                       "<class 'PyQt5.QtWidgets.QListWidget'>"):
            obj.deleteLater()

    def change_json_file(self, key=None, value=None):
        if key == "AutoScroll":
            value = str(self.auto_scroll_toggle.isChecked())
            save_json_file(key, value)

        elif key == "ImageDownCount":
            value = self.mb_show_top_bar_repeat_TextEdit.text()
            value = int(value) if value.isdigit() else 3
            value = 10 if (value > 10) else value
            self.mb_show_top_bar_repeat_TextEdit.setText(str(value))
            self.JSON_DATA["ImageDownCount"] = value
            save_json_file(key, value)


    # <-- New Voca Clicked Event Handler --------------------------------------------------->
    def change_current_widget(self):
        self.player.stop()

        self.sending_from_widget = self.sender()

        if (self.sending_from_widget != None):
            idx = self.sending_from_widget.currentRow()

            # 첫번째는 어쩔 수 없이 직접 실행해야하나 봄...
            self.sending_from_widget.setCurrentRow(idx)
            self.change_mb_voca_widget(obj=self.sending_from_widget)
            self.get_audio_tts(obj=self.sending_from_widget)

    def change_mb_voca_widget(self, obj):
        self.mb_show_eng_adj.setStyleSheet("color: black;\n")
        self.mb_show_kor_adj.setStyleSheet("color: black;\n")
        self.mb_show_btns_adj.show()
        self.BLACK.hide()
        self.player.stop()

        # Get currentItem Text
        if (self.sending_from_widget != None):
            self.is_voca_changed = True
            self.word = obj.currentItem().text()
            self.current_idx = obj.currentRow()

            # reset index of image
            self.is_finished = False
            self.tts_idx = 0
            self.image_idx = 0
            self.group_name = obj.parent().findChild(QtWidgets.QPushButton).text()

            # Change image
            self.pics = list()
            status = get_images.get_images_from_word(self.word, self.JSON_DATA["ImageDownCount"], self.JSON_DATA, self.file_type)
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

            # Change meaning title
            meaning = self.CSV_DATA["dataframe"][self.CSV_DATA["dataframe"]["그룹"] == self.group_name]["뜻"]

            meaning = meaning.iloc[self.current_idx]

            self.mb_show_kor_adj.setText(meaning)

            # Change image when voca has been changed
            self.change_mb_voca_image(self.image_idx)

    def change_mb_voca_image(self, idx):
        # Add image_idx
        if idx >= len(self.pics):
            self.move_next_voca()
        else:
            # Get image and change pixmap
            pic = self.pics[idx]

            self.mb_show_image_adj.clear()
            # self.mb_show_image_adj.setPixmap(pic)
            self.mb_show_image_adj.setPixmap(pic.scaled(QtCore.QSize(self.mb_show_image_adj.width(),self.mb_show_image_adj.height()),
                                                        aspectRatioMode=QtCore.Qt.KeepAspectRatio,
                                                        transformMode =QtCore.Qt.SmoothTransformation
                                                        )
                                             )
            self.mb_show_image_adj.repaint()

            self.image_idx += 1

    def move_next_voca(self):
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
            print("  [Info] <-- Auto scroll is not clicked -->")

    def stop_player(self):
        self.is_finished = True
        self.is_playing = False

        self.BLACK.show()
        self.player.stop()

        self.mb_show_btns_adj.raise_()
        self.pause.setText("▶")
        # self.mb_show_btns_adj.hide()

    def voca_widget_button_event(self):
        self.stop_player()
        self.BLACK.hide()

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

    # <-- Top/Bottom Bar Button Event ------------------------------------------------------>
    def is_clicked_pause(self):
        if not self.is_pause_clicked:
            # stop player
            self.stop_player()

            # change setting
            self.is_finished = True
            self.is_playing = False
            self.is_pause_clicked = True

            # show black
            self.BLACK.show()

            for item in [self.mb_show_eng_adj, self.mb_show_image_adj, self.mb_show_kor_adj, self.mb_show_btns_adj]:
                item.raise_()
                item.show()
                item.setStyleSheet("color: white;\n")

            self.mb_show_btns_adj.setStyleSheet("color: black;\n")
            self.pause.setText("▶")
        else:
            # play player
            self.change_mb_voca_widget(obj=self.sending_from_widget)
            self.get_audio_tts(obj=self.sending_from_widget)

            # change setting
            self.is_pause_clicked = False

            # hide black
            self.BLACK.hide()

            for item in [self.mb_show_eng_adj, self.mb_show_image_adj, self.mb_show_kor_adj, self.mb_show_btns_adj]:
                item.raise_()
                item.show()
                item.setStyleSheet("color: black;\n")

            self.pause.setText("■")

    def is_clicked_back_forward(self):
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

        for item in [self.mb_show_eng_adj, self.mb_show_image_adj, self.mb_show_kor_adj, self.mb_show_btns_adj]:
            item.raise_()
            item.show()
            item.setStyleSheet("color: black")

        self.pause.setText("■")



    # <-- Play audio TTS ------------------------------------------------------------------->
    def play_tts_audio(self):
        if self.player.state() == 0 and \
                not self.is_finished:
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
                    self.word = self.word.replace("-", "무엇 ")
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

            buf = QtCore.QBuffer()
            buf.open(QtCore.QBuffer.ReadWrite)
            audio_path.write_to_fp(buf)
            buf.open(QtCore.QIODevice.ReadOnly)


            # url = QtCore.QUrl.fromLocalFile(audio_path)
            # content = QtMultimedia.QMediaContent(url)
            content = QtMultimedia.QMediaContent()

            self.player.setMedia(content, buf)
            self.player.play()

            # Setup [tts_idx, is_voca_changed]
            self.tts_idx += 1
            self.is_voca_changed = False

    def get_audio_tts(self, obj: str = None):
        # Get currentItem Text
        if (self.sending_from_widget != None):
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
            origin_font_size = origin_h - 40
            resized_font_size = origin_font_size * (resized_h / origin_h)
            font_size = int(resized_font_size)
            font_size = str(font_size) + 'px'

            return font_size

        def resize_widget_setting(parent, obj, w: int = None, h: int = None):
            # print("  [Info] Resize Event emitted")
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

            elif 'BLACK' in obj.objectName():
                _w = w + 2
                _h = h + 2

            obj.setGeometry(QtCore.QRect(_x, _y, _w, _h))

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
        resize_widget_setting(self, self.BLACK, w=w, h=h)

        # Right - Main Font Resize Section
        change_stylesheet(self, self.mb_show_eng_adj, font=calculate_font_ratio(self.mb_show_eng_adj, self.mb_show_eng_h))
        change_stylesheet(self, self.mb_show_kor_adj, font=calculate_font_ratio(self.mb_show_kor_adj, self.mb_show_kor_h))

    def resizeEvent(self, event):
        self.resized.emit()
        return super(MainWindow, self).resizeEvent(event)



if __name__ == "__main__":
    def get_ui_python_file():
        try:
            os.system("pyuic5 resource/src/ui/main.ui -o resource/src/ui/main_ui.py")
            print("  [Info] pyuic5 has done...")
            # os.system("pyrcc5 main.qrc -o main_rc.py")
        except FileNotFoundError:
            print("  [Error] Error happened from 'pyuic5 or pyrcc5' ")

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
                    ["그룹,단어,뜻\n",
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
    get_ui_python_file()

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
