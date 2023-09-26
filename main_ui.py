# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainApp(object):
    def setupUi(self, MainApp):
        MainApp.setObjectName("MainApp")
        MainApp.resize(970, 700)
        MainApp.setMinimumSize(QtCore.QSize(970, 700))
        MainApp.setStyleSheet("QObject {\n"
"border: 0px solid;\n"
"margin: 0px;\n"
"padding: 0px;\n"
"background-color: blue;\n"
"border-color: rgb(0, 0, 255);\n"
"}\n"
"QWidget {\n"
"color: black;\n"
"font: 63 14px \"Noto Sans KR SemiBold\";\n"
"}\n"
"/* scrollbar stylesheet css */\n"
"QScrollBar {\n"
"}\n"
"QScrollBar:vertical {\n"
"border: 0px solid;\n"
"width: 8px;\n"
"margin: 0px;\n"
"}\n"
"QScrollBar::add-page:vertical,\n"
"QScrollBar::sub-page:vertical {\n"
"background: rgba(190, 190, 190, 60);\n"
"border-radius: 4px;\n"
"}\n"
"QScrollBar::handle:vertical {\n"
"background: rgba(190, 190, 190, 200);\n"
"border-radius: 4px;\n"
"}\n"
"QScrollBar::sub-line:vertical {\n"
"height: 0px;\n"
"subcontrol-position: top;\n"
"subcontrol-origin: margin;\n"
"}\n"
"QScrollBar::add-line:vertical {\n"
"height: 0px;\n"
"subcontrol-position: bottom;\n"
"subcontrol-origin: margin;\n"
"}")
        self.mb_1 = QtWidgets.QWidget(MainApp)
        self.mb_1.setObjectName("mb_1")
        self.mb_voca_adj = QtWidgets.QWidget(self.mb_1)
        self.mb_voca_adj.setGeometry(QtCore.QRect(0, 0, 200, 700))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mb_voca_adj.sizePolicy().hasHeightForWidth())
        self.mb_voca_adj.setSizePolicy(sizePolicy)
        self.mb_voca_adj.setMinimumSize(QtCore.QSize(0, 700))
        self.mb_voca_adj.setMaximumSize(QtCore.QSize(200, 16777215))
        self.mb_voca_adj.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.mb_voca_adj.setStyleSheet("#mb_voca_adj {\n"
"background-color: rgb(234, 234, 240);\n"
"}\n"
"QWidget {\n"
"margin: 0px;\n"
"padding: 0px;\n"
"background-color: transparent;\n"
"}\n"
"\n"
"/* Left - Setting --------------------------------- */\n"
"#mb_setting_widget,\n"
"#mb_voca_scroll {\n"
"background-color: white;\n"
"border-radius: 10px;\n"
"margin: 10px;\n"
"}\n"
"\n"
"/* Left - Setting detail name:Auto Scroll */\n"
"#mb_top_bar_auto_scroll {\n"
"margin: 0px 20px 0px 20px;\n"
"}\n"
"#mb_top_bar_auto_scroll_title {\n"
"font: 14px;\n"
"margin: 0px 0px 0px 10px;\n"
"color: black;\n"
"}\n"
"\n"
"/* Left - Title Part:Gray title */\n"
"#mb_setting_title,\n"
"#mb_voca_total_title {\n"
"color: rgb(170, 170, 170);\n"
"font: 13px;\n"
"margin: 20px 20px 0px 20px;\n"
"font-weight: bold;\n"
"text-align: Left;\n"
"}\n"
"#mb_voca_total_title {\n"
"margin: 0px;\n"
"padding: 10px 0px 0px 10px;\n"
"}\n"
"\n"
"/* QScrollWidget PushButton part ------------------ */\n"
"QScrollArea .QLabel {\n"
"padding-left: 10px;\n"
"}\n"
"QScrollArea .QPushButton {\n"
"margin: 5px 10px 5px 10px;\n"
"padding: 0px;\n"
"color: black;\n"
"text-align: left;\n"
"}\n"
"\n"
"/* QListWidget Part ------------------------------ */\n"
"QListView::item {\n"
"border: 0px;\n"
"margin: 5px 0px 5px -4px;\n"
"}\n"
"QListWidget {\n"
"font-weight: light;\n"
"padding-right: 4px;\n"
"}\n"
"QListWidget::item {\n"
"padding: 3px;\n"
"padding-left: 40px;\n"
"color: rgb(180, 180, 180);\n"
"}\n"
"QListWidget::item:hover {\n"
"padding-left: 40px;\n"
"margin: 0px -4px 0px -4px;\n"
"color: black;\n"
"background-color: rgb(204, 227, 249);\n"
"}\n"
"QListWidget::item:selected {\n"
"padding-left: 40px;\n"
"margin: 0px -4px 0px -4px;\n"
"background-color: rgb(232, 232, 237);\n"
"color: black;\n"
"}\n"
"\n"
"/* Add Files Part */\n"
"#mb_voca_open {\n"
"margin: 10px;\n"
"color: white;\n"
"font: 16px;\n"
"font-weight: bold;\n"
"border-radius: 5px;\n"
"background-color: rgb(0, 155, 255);\n"
"}\n"
"#mb_voca_open:hover {\n"
"background-color: rgba(0, 155, 255, 80);\n"
"}")
        self.mb_voca_adj.setObjectName("mb_voca_adj")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.mb_voca_adj)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(1)
        self.verticalLayout.setObjectName("verticalLayout")
        self.mb_top_bar = QtWidgets.QWidget(self.mb_voca_adj)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mb_top_bar.sizePolicy().hasHeightForWidth())
        self.mb_top_bar.setSizePolicy(sizePolicy)
        self.mb_top_bar.setMinimumSize(QtCore.QSize(200, 50))
        self.mb_top_bar.setMaximumSize(QtCore.QSize(200, 50))
        self.mb_top_bar.setObjectName("mb_top_bar")
        self.mb_icon = QtWidgets.QLabel(self.mb_top_bar)
        self.mb_icon.setGeometry(QtCore.QRect(0, 0, 200, 50))
        self.mb_icon.setMinimumSize(QtCore.QSize(0, 50))
        self.mb_icon.setMaximumSize(QtCore.QSize(16777215, 50))
        self.mb_icon.setStyleSheet("")
        self.mb_icon.setLineWidth(0)
        self.mb_icon.setText("")
        self.mb_icon.setIndent(0)
        self.mb_icon.setObjectName("mb_icon")
        self.verticalLayout.addWidget(self.mb_top_bar)
        self.mb_h_line_1 = QtWidgets.QFrame(self.mb_voca_adj)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mb_h_line_1.sizePolicy().hasHeightForWidth())
        self.mb_h_line_1.setSizePolicy(sizePolicy)
        self.mb_h_line_1.setMinimumSize(QtCore.QSize(0, 1))
        self.mb_h_line_1.setMaximumSize(QtCore.QSize(16777215, 1))
        self.mb_h_line_1.setStyleSheet("background-color: rgb(160, 160, 160);\n"
"margin: 0px 10px 0px 10px;")
        self.mb_h_line_1.setLineWidth(1)
        self.mb_h_line_1.setFrameShape(QtWidgets.QFrame.HLine)
        self.mb_h_line_1.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.mb_h_line_1.setObjectName("mb_h_line_1")
        self.verticalLayout.addWidget(self.mb_h_line_1)
        self.mb_setting_widget = QtWidgets.QWidget(self.mb_voca_adj)
        self.mb_setting_widget.setObjectName("mb_setting_widget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.mb_setting_widget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 10)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.mb_setting_title = QtWidgets.QLabel(self.mb_setting_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mb_setting_title.sizePolicy().hasHeightForWidth())
        self.mb_setting_title.setSizePolicy(sizePolicy)
        self.mb_setting_title.setMinimumSize(QtCore.QSize(0, 20))
        self.mb_setting_title.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.mb_setting_title.setStyleSheet("")
        self.mb_setting_title.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.mb_setting_title.setIndent(0)
        self.mb_setting_title.setObjectName("mb_setting_title")
        self.verticalLayout_2.addWidget(self.mb_setting_title)
        self.mb_top_bar_auto_scroll = QtWidgets.QWidget(self.mb_setting_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mb_top_bar_auto_scroll.sizePolicy().hasHeightForWidth())
        self.mb_top_bar_auto_scroll.setSizePolicy(sizePolicy)
        self.mb_top_bar_auto_scroll.setMinimumSize(QtCore.QSize(190, 0))
        self.mb_top_bar_auto_scroll.setMaximumSize(QtCore.QSize(190, 16777215))
        self.mb_top_bar_auto_scroll.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.mb_top_bar_auto_scroll.setObjectName("mb_top_bar_auto_scroll")
        self.mb_top_bar_auto_scroll_verticalLayout = QtWidgets.QHBoxLayout(self.mb_top_bar_auto_scroll)
        self.mb_top_bar_auto_scroll_verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.mb_top_bar_auto_scroll_verticalLayout.setSpacing(5)
        self.mb_top_bar_auto_scroll_verticalLayout.setObjectName("mb_top_bar_auto_scroll_verticalLayout")
        self.mb_top_bar_auto_scroll_title = QtWidgets.QLabel(self.mb_top_bar_auto_scroll)
        self.mb_top_bar_auto_scroll_title.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mb_top_bar_auto_scroll_title.sizePolicy().hasHeightForWidth())
        self.mb_top_bar_auto_scroll_title.setSizePolicy(sizePolicy)
        self.mb_top_bar_auto_scroll_title.setMinimumSize(QtCore.QSize(100, 30))
        self.mb_top_bar_auto_scroll_title.setMaximumSize(QtCore.QSize(100, 16777215))
        self.mb_top_bar_auto_scroll_title.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.mb_top_bar_auto_scroll_title.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.mb_top_bar_auto_scroll_title.setObjectName("mb_top_bar_auto_scroll_title")
        self.mb_top_bar_auto_scroll_verticalLayout.addWidget(self.mb_top_bar_auto_scroll_title)
        spacerItem = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Minimum)
        self.mb_top_bar_auto_scroll_verticalLayout.addItem(spacerItem)
        self.verticalLayout_2.addWidget(self.mb_top_bar_auto_scroll)
        self.verticalLayout.addWidget(self.mb_setting_widget)
        self.mb_voca_scroll = QtWidgets.QScrollArea(self.mb_voca_adj)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mb_voca_scroll.sizePolicy().hasHeightForWidth())
        self.mb_voca_scroll.setSizePolicy(sizePolicy)
        self.mb_voca_scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.mb_voca_scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.mb_voca_scroll.setWidgetResizable(True)
        self.mb_voca_scroll.setObjectName("mb_voca_scroll")
        self.mb_voca_scroll_widget = QtWidgets.QWidget()
        self.mb_voca_scroll_widget.setGeometry(QtCore.QRect(0, 0, 180, 486))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mb_voca_scroll_widget.sizePolicy().hasHeightForWidth())
        self.mb_voca_scroll_widget.setSizePolicy(sizePolicy)
        self.mb_voca_scroll_widget.setObjectName("mb_voca_scroll_widget")
        self.mb_voca_scroll_widget_verticalLayout = QtWidgets.QVBoxLayout(self.mb_voca_scroll_widget)
        self.mb_voca_scroll_widget_verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.mb_voca_scroll_widget_verticalLayout.setSpacing(0)
        self.mb_voca_scroll_widget_verticalLayout.setObjectName("mb_voca_scroll_widget_verticalLayout")
        self.mb_voca_total_title = QtWidgets.QLabel(self.mb_voca_scroll_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mb_voca_total_title.sizePolicy().hasHeightForWidth())
        self.mb_voca_total_title.setSizePolicy(sizePolicy)
        self.mb_voca_total_title.setMinimumSize(QtCore.QSize(0, 31))
        self.mb_voca_total_title.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.mb_voca_total_title.setStyleSheet("")
        self.mb_voca_total_title.setLineWidth(0)
        self.mb_voca_total_title.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.mb_voca_total_title.setIndent(0)
        self.mb_voca_total_title.setObjectName("mb_voca_total_title")
        self.mb_voca_scroll_widget_verticalLayout.addWidget(self.mb_voca_total_title)
        self.mb_voca_widget_0 = QtWidgets.QWidget(self.mb_voca_scroll_widget)
        self.mb_voca_widget_0.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mb_voca_widget_0.sizePolicy().hasHeightForWidth())
        self.mb_voca_widget_0.setSizePolicy(sizePolicy)
        self.mb_voca_widget_0.setObjectName("mb_voca_widget_0")
        self.mb_voca_widget_verticalLayout = QtWidgets.QVBoxLayout(self.mb_voca_widget_0)
        self.mb_voca_widget_verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.mb_voca_widget_verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.mb_voca_widget_verticalLayout.setSpacing(0)
        self.mb_voca_widget_verticalLayout.setObjectName("mb_voca_widget_verticalLayout")
        self.mb_voca_button_adj_0 = QtWidgets.QWidget(self.mb_voca_widget_0)
        self.mb_voca_button_adj_0.setMaximumSize(QtCore.QSize(16777215, 30))
        self.mb_voca_button_adj_0.setStyleSheet("QWidget:hover {\n"
"background-color: rgb(204, 227, 249);\n"
"}")
        self.mb_voca_button_adj_0.setObjectName("mb_voca_button_adj_0")
        self.button_horizontalLayout_0 = QtWidgets.QHBoxLayout(self.mb_voca_button_adj_0)
        self.button_horizontalLayout_0.setContentsMargins(0, 0, 0, 0)
        self.button_horizontalLayout_0.setSpacing(0)
        self.button_horizontalLayout_0.setObjectName("button_horizontalLayout_0")
        self.mb_voca_button_icon_adj_0 = QtWidgets.QLabel(self.mb_voca_button_adj_0)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mb_voca_button_icon_adj_0.sizePolicy().hasHeightForWidth())
        self.mb_voca_button_icon_adj_0.setSizePolicy(sizePolicy)
        self.mb_voca_button_icon_adj_0.setMaximumSize(QtCore.QSize(16777215, 20))
        self.mb_voca_button_icon_adj_0.setStyleSheet("")
        self.mb_voca_button_icon_adj_0.setText("")
        self.mb_voca_button_icon_adj_0.setObjectName("mb_voca_button_icon_adj_0")
        self.button_horizontalLayout_0.addWidget(self.mb_voca_button_icon_adj_0)
        self.mb_voca_button_group_title_adj_0 = QtWidgets.QPushButton(self.mb_voca_button_adj_0)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mb_voca_button_group_title_adj_0.sizePolicy().hasHeightForWidth())
        self.mb_voca_button_group_title_adj_0.setSizePolicy(sizePolicy)
        self.mb_voca_button_group_title_adj_0.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.mb_voca_button_group_title_adj_0.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.mb_voca_button_group_title_adj_0.setCheckable(True)
        self.mb_voca_button_group_title_adj_0.setChecked(False)
        self.mb_voca_button_group_title_adj_0.setObjectName("mb_voca_button_group_title_adj_0")
        self.button_horizontalLayout_0.addWidget(self.mb_voca_button_group_title_adj_0)
        self.mb_voca_widget_verticalLayout.addWidget(self.mb_voca_button_adj_0)
        self.mb_voca_word_adj_0 = QtWidgets.QListWidget(self.mb_voca_widget_0)
        self.mb_voca_word_adj_0.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mb_voca_word_adj_0.sizePolicy().hasHeightForWidth())
        self.mb_voca_word_adj_0.setSizePolicy(sizePolicy)
        self.mb_voca_word_adj_0.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.mb_voca_word_adj_0.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.mb_voca_word_adj_0.setFocusPolicy(QtCore.Qt.NoFocus)
        self.mb_voca_word_adj_0.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.mb_voca_word_adj_0.setStyleSheet("")
        self.mb_voca_word_adj_0.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.mb_voca_word_adj_0.setFrameShadow(QtWidgets.QFrame.Plain)
        self.mb_voca_word_adj_0.setLineWidth(0)
        self.mb_voca_word_adj_0.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.mb_voca_word_adj_0.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.mb_voca_word_adj_0.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.mb_voca_word_adj_0.setAutoScrollMargin(1)
        self.mb_voca_word_adj_0.setProperty("showDropIndicator", True)
        self.mb_voca_word_adj_0.setAlternatingRowColors(False)
        self.mb_voca_word_adj_0.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.mb_voca_word_adj_0.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.mb_voca_word_adj_0.setMovement(QtWidgets.QListView.Free)
        self.mb_voca_word_adj_0.setProperty("isWrapping", False)
        self.mb_voca_word_adj_0.setResizeMode(QtWidgets.QListView.Adjust)
        self.mb_voca_word_adj_0.setLayoutMode(QtWidgets.QListView.SinglePass)
        self.mb_voca_word_adj_0.setViewMode(QtWidgets.QListView.ListMode)
        self.mb_voca_word_adj_0.setWordWrap(False)
        self.mb_voca_word_adj_0.setObjectName("mb_voca_word_adj_0")
        item = QtWidgets.QListWidgetItem()
        self.mb_voca_word_adj_0.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.mb_voca_word_adj_0.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.mb_voca_word_adj_0.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.mb_voca_word_adj_0.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.mb_voca_word_adj_0.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.mb_voca_word_adj_0.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.mb_voca_word_adj_0.addItem(item)
        self.mb_voca_widget_verticalLayout.addWidget(self.mb_voca_word_adj_0)
        self.mb_voca_scroll_widget_verticalLayout.addWidget(self.mb_voca_widget_0)
        self.mb_voca_scroll.setWidget(self.mb_voca_scroll_widget)
        self.verticalLayout.addWidget(self.mb_voca_scroll)
        self.mb_voca_open = QtWidgets.QPushButton(self.mb_voca_adj)
        self.mb_voca_open.setMinimumSize(QtCore.QSize(0, 60))
        self.mb_voca_open.setMaximumSize(QtCore.QSize(16777215, 60))
        self.mb_voca_open.setObjectName("mb_voca_open")
        self.verticalLayout.addWidget(self.mb_voca_open)
        self.mb_show_adj = QtWidgets.QWidget(self.mb_1)
        self.mb_show_adj.setGeometry(QtCore.QRect(200, 0, 771, 700))
        self.mb_show_adj.setStyleSheet("QWidget {\n"
"padding: 0px;\n"
"margin: 0px;\n"
"background-color: white;\n"
"}\n"
"#mb_show_top_bar .QPushButton,\n"
"#mb_show_btns_adj .QPushButton {\n"
"font: 12px;\n"
"padding: 0px;\n"
"background-color: rgb(230, 230, 230);\n"
"border-radius: 13px;\n"
"text-align: center;\n"
"}\n"
"#mb_show_top_bar .QPushButton {\n"
"margin: 0px 5px 0px 0px;\n"
"}\n"
"#mb_show_top_bar .QPushButton:hover,\n"
"#mb_show_btns_adj .QPushButton:hover {\n"
"background-color: rgba(0, 155, 255, 80);\n"
"}\n"
"#mb_show_top_bar .QPushButton:checked {\n"
"background-color: \"#4ed164\";\n"
"}\n"
"#mb_show_eng_adj {\n"
"font: 100px;\n"
"font-weight: bold;\n"
"}\n"
"#mb_show_kor_adj {\n"
"font: 50px;\n"
"font-weight: bold;\n"
"}\n"
"#mb_show_image_adj {\n"
"font: 30px;\n"
"}\n"
"#mb_show_dev {\n"
"background-color: transparent;\n"
"font: 10px;\n"
"}")
        self.mb_show_adj.setObjectName("mb_show_adj")
        self.mb_show_btns_adj = QtWidgets.QWidget(self.mb_show_adj)
        self.mb_show_btns_adj.setGeometry(QtCore.QRect(0, 654, 771, 30))
        self.mb_show_btns_adj.setObjectName("mb_show_btns_adj")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.mb_show_btns_adj)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.mb_show_btn_widget = QtWidgets.QWidget(self.mb_show_btns_adj)
        self.mb_show_btn_widget.setMinimumSize(QtCore.QSize(100, 0))
        self.mb_show_btn_widget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.mb_show_btn_widget.setObjectName("mb_show_btn_widget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.mb_show_btn_widget)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.back = QtWidgets.QPushButton(self.mb_show_btn_widget)
        self.back.setMinimumSize(QtCore.QSize(0, 26))
        self.back.setMaximumSize(QtCore.QSize(26, 26))
        self.back.setObjectName("back")
        self.horizontalLayout_2.addWidget(self.back)
        self.dummy = QtWidgets.QLabel(self.mb_show_btn_widget)
        self.dummy.setMaximumSize(QtCore.QSize(50, 16777215))
        self.dummy.setText("")
        self.dummy.setObjectName("dummy")
        self.horizontalLayout_2.addWidget(self.dummy)
        self.forward = QtWidgets.QPushButton(self.mb_show_btn_widget)
        self.forward.setMinimumSize(QtCore.QSize(0, 26))
        self.forward.setMaximumSize(QtCore.QSize(26, 26))
        self.forward.setObjectName("forward")
        self.horizontalLayout_2.addWidget(self.forward)
        self.horizontalLayout.addWidget(self.mb_show_btn_widget)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.mb_show_eng_adj = QtWidgets.QLabel(self.mb_show_adj)
        self.mb_show_eng_adj.setGeometry(QtCore.QRect(0, 50, 771, 140))
        self.mb_show_eng_adj.setStyleSheet("")
        self.mb_show_eng_adj.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignHCenter)
        self.mb_show_eng_adj.setObjectName("mb_show_eng_adj")
        self.mb_show_image_adj = QtWidgets.QLabel(self.mb_show_adj)
        self.mb_show_image_adj.setGeometry(QtCore.QRect(0, 190, 771, 361))
        self.mb_show_image_adj.setStyleSheet("")
        self.mb_show_image_adj.setAlignment(QtCore.Qt.AlignCenter)
        self.mb_show_image_adj.setObjectName("mb_show_image_adj")
        self.mb_show_kor_adj = QtWidgets.QLabel(self.mb_show_adj)
        self.mb_show_kor_adj.setGeometry(QtCore.QRect(0, 560, 771, 81))
        self.mb_show_kor_adj.setText("")
        self.mb_show_kor_adj.setAlignment(QtCore.Qt.AlignCenter)
        self.mb_show_kor_adj.setObjectName("mb_show_kor_adj")
        self.mb_show_top_bar = QtWidgets.QWidget(self.mb_show_adj)
        self.mb_show_top_bar.setGeometry(QtCore.QRect(0, 0, 771, 50))
        self.mb_show_top_bar.setObjectName("mb_show_top_bar")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.mb_show_top_bar)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.mb_show_top_bar_btns = QtWidgets.QWidget(self.mb_show_top_bar)
        self.mb_show_top_bar_btns.setMinimumSize(QtCore.QSize(100, 0))
        self.mb_show_top_bar_btns.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.mb_show_top_bar_btns.setObjectName("mb_show_top_bar_btns")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.mb_show_top_bar_btns)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem3)
        self.mb_show_top_both = QtWidgets.QPushButton(self.mb_show_top_bar_btns)
        self.mb_show_top_both.setMinimumSize(QtCore.QSize(31, 26))
        self.mb_show_top_both.setMaximumSize(QtCore.QSize(31, 26))
        self.mb_show_top_both.setCheckable(True)
        self.mb_show_top_both.setChecked(True)
        self.mb_show_top_both.setObjectName("mb_show_top_both")
        self.horizontalLayout_4.addWidget(self.mb_show_top_both)
        self.mb_show_top_bar_only_eng = QtWidgets.QPushButton(self.mb_show_top_bar_btns)
        self.mb_show_top_bar_only_eng.setMinimumSize(QtCore.QSize(31, 26))
        self.mb_show_top_bar_only_eng.setMaximumSize(QtCore.QSize(31, 26))
        self.mb_show_top_bar_only_eng.setCheckable(True)
        self.mb_show_top_bar_only_eng.setObjectName("mb_show_top_bar_only_eng")
        self.horizontalLayout_4.addWidget(self.mb_show_top_bar_only_eng)
        self.mb_show_top_bar_only_kor = QtWidgets.QPushButton(self.mb_show_top_bar_btns)
        self.mb_show_top_bar_only_kor.setMinimumSize(QtCore.QSize(31, 26))
        self.mb_show_top_bar_only_kor.setMaximumSize(QtCore.QSize(31, 26))
        self.mb_show_top_bar_only_kor.setCheckable(True)
        self.mb_show_top_bar_only_kor.setObjectName("mb_show_top_bar_only_kor")
        self.horizontalLayout_4.addWidget(self.mb_show_top_bar_only_kor)
        self.horizontalLayout_3.addWidget(self.mb_show_top_bar_btns)
        self.mb_show_dev = QtWidgets.QLabel(self.mb_show_adj)
        self.mb_show_dev.setGeometry(QtCore.QRect(1, 680, 761, 20))
        self.mb_show_dev.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.mb_show_dev.setObjectName("mb_show_dev")
        self.mb_show_eng_adj.raise_()
        self.mb_show_image_adj.raise_()
        self.mb_show_kor_adj.raise_()
        self.mb_show_top_bar.raise_()
        self.mb_show_dev.raise_()
        self.mb_show_btns_adj.raise_()
        self.mb_show_adj.raise_()
        self.mb_voca_adj.raise_()
        MainApp.setCentralWidget(self.mb_1)

        self.retranslateUi(MainApp)
        self.mb_voca_word_adj_0.setCurrentRow(-1)
        QtCore.QMetaObject.connectSlotsByName(MainApp)

    def retranslateUi(self, MainApp):
        _translate = QtCore.QCoreApplication.translate
        MainApp.setWindowTitle(_translate("MainApp", "MainWindow"))
        self.mb_setting_title.setText(_translate("MainApp", "Setting"))
        self.mb_top_bar_auto_scroll_title.setText(_translate("MainApp", "Auto Scroll"))
        self.mb_voca_total_title.setText(_translate("MainApp", "Word List"))
        self.mb_voca_button_group_title_adj_0.setText(_translate("MainApp", "Lesson 1"))
        self.mb_voca_word_adj_0.setSortingEnabled(False)
        __sortingEnabled = self.mb_voca_word_adj_0.isSortingEnabled()
        self.mb_voca_word_adj_0.setSortingEnabled(False)
        item = self.mb_voca_word_adj_0.item(0)
        item.setText(_translate("MainApp", "jump"))
        item = self.mb_voca_word_adj_0.item(1)
        item.setText(_translate("MainApp", "run"))
        item = self.mb_voca_word_adj_0.item(2)
        item.setText(_translate("MainApp", "walk"))
        item = self.mb_voca_word_adj_0.item(3)
        item.setText(_translate("MainApp", "talk"))
        item = self.mb_voca_word_adj_0.item(4)
        item.setText(_translate("MainApp", "calculate"))
        item = self.mb_voca_word_adj_0.item(5)
        item.setText(_translate("MainApp", "see"))
        item = self.mb_voca_word_adj_0.item(6)
        item.setText(_translate("MainApp", "fly"))
        self.mb_voca_word_adj_0.setSortingEnabled(__sortingEnabled)
        self.mb_voca_open.setText(_translate("MainApp", "Edit File"))
        self.back.setText(_translate("MainApp", "◀"))
        self.forward.setText(_translate("MainApp", "▶"))
        self.mb_show_eng_adj.setText(_translate("MainApp", "Visual Voca"))
        self.mb_show_image_adj.setText(_translate("MainApp", "Waiting for Click Event ..."))
        self.mb_show_top_both.setText(_translate("MainApp", "All"))
        self.mb_show_top_bar_only_eng.setText(_translate("MainApp", "En"))
        self.mb_show_top_bar_only_kor.setText(_translate("MainApp", "Ko"))
        self.mb_show_dev.setText(_translate("MainApp", "Developed by Gonyo & AhnJH"))
