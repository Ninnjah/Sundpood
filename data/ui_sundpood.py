# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'sundpood.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(640, 480)
        MainWindow.setMinimumSize(QtCore.QSize(640, 480))
        MainWindow.setMaximumSize(QtCore.QSize(640, 480))
        MainWindow.setStyleSheet("QWidget{\n"
"    background: rgb(44, 44, 44);    \n"
"    font: 25 14pt \"Calibri Light\";\n"
"}\n"
"\n"
"QLabel{\n"
"    background: none\n"
"}\n"
"\n"
"QPushButton{\n"
"    background: rgb(58, 58, 58);\n"
"    border: none;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"    background: rgb(53, 53, 53);\n"
"}\n"
"\n"
"QListWidget{\n"
"    margin: 4px;\n"
"    border: none;\n"
"}\n"
"QListWidget::item[Custom=\"true\"]{\n"
"    background: rgb(48, 48, 48);\n"
"}\n"
"QListWidget::item:hover{\n"
"    background:  rgb(53, 53, 53);\n"
"}\n"
"QListWidget::item:selected{\n"
"    background: rgb(48, 48, 48);\n"
"    color: black;\n"
"}\n"
"\n"
"QScrollBar:vertical{\n"
"    border: 1px transparent rgb(58, 58, 58);\n"
"    border-radius: 4px;\n"
"    background: rgb(48, 48, 48);\n"
"    width: 16px;\n"
"}\n"
"QScrollBar::handle:vertical{\n"
"    background: rgb(48, 48, 48);\n"
"}\n"
"QScrollBar::sub-page:vertical{\n"
"    background: rgb(58, 58, 58);\n"
"}\n"
"QScrollBar::add-page:vertical{\n"
"    background: rgb(58, 58, 58);\n"
"}\n"
"\n"
"#background{\n"
"    background:rgb(48, 48, 48);\n"
"}\n"
"\n"
"#exit_button{\n"
"    margin-bottom: 1px;\n"
"}\n"
"#exit_button:hover{\n"
"    color: black;\n"
"    background: rgba(254, 119, 122, 128);\n"
"}\n"
"\n"
"#min_button{\n"
"    margin-bottom: 1px;\n"
"}\n"
"#min_button:hover{\n"
"    color: black;\n"
"    background: rgba(194, 213, 254, 128);\n"
"}\n"
"\n"
"#pref_button{\n"
"    margin-bottom: 1px;\n"
"}\n"
"#pref_button:hover{\n"
"    color: black;\n"
"    background: rgba(194, 213, 254, 128);\n"
"}\n"
"\n"
"#hotkeys_button{\n"
"    margin-bottom: 1px;\n"
"}\n"
"#hotkeys_button:hover{\n"
"    color: black;\n"
"    background: rgba(194, 213, 254, 128);\n"
"}\n"
"\n"
"#select_label{\n"
"    background: black;\n"
"    color: white;\n"
"}\n"
"\n"
"#catList::item{\n"
"    padding: 6px;\n"
"}\n"
"\n"
"QSlider::groove:horizontal {\n"
"    border: none;\n"
"    height: 40px;\n"
"    margin: 0px;\n"
"}\n"
"QSlider::handle:horizontal {\n"
"    background-color: rgb(53, 53, 53);\n"
"    border: none;\n"
"    height: 40px;\n"
"    width: 40px;\n"
"     margin: -15px 0px;\n"
"}\n"
"QSlider::sub-page:horizontal {\n"
"    border: none;\n"
"    height: 40px;\n"
"    margin: 1px;\n"
"    background: rgb(63, 63, 63);\n"
"}\n"
"\n"
"#update_button:hover{\n"
"    background:rgba(10, 128, 179, 128);\n"
"}")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.background = QtWidgets.QWidget(self.centralwidget)
        self.background.setGeometry(QtCore.QRect(0, 0, 641, 481))
        self.background.setStyleSheet("")
        self.background.setObjectName("background")
        self.min_button = QtWidgets.QPushButton(self.background)
        self.min_button.setGeometry(QtCore.QRect(560, 0, 41, 31))
        self.min_button.setStyleSheet("")
        self.min_button.setObjectName("min_button")
        self.exit_button = QtWidgets.QPushButton(self.background)
        self.exit_button.setGeometry(QtCore.QRect(600, 0, 41, 31))
        self.exit_button.setStyleSheet("")
        self.exit_button.setObjectName("exit_button")
        self.pref_button = QtWidgets.QPushButton(self.background)
        self.pref_button.setGeometry(QtCore.QRect(0, 0, 111, 31))
        self.pref_button.setObjectName("pref_button")
        self.hotkeys_button = QtWidgets.QPushButton(self.background)
        self.hotkeys_button.setGeometry(QtCore.QRect(110, 0, 111, 31))
        self.hotkeys_button.setObjectName("hotkeys_button")
        self.stop_button = QtWidgets.QPushButton(self.background)
        self.stop_button.setGeometry(QtCore.QRect(0, 120, 171, 41))
        self.stop_button.setObjectName("stop_button")
        self.hkset = QtWidgets.QPushButton(self.background)
        self.hkset.setGeometry(QtCore.QRect(0, 200, 171, 41))
        self.hkset.setObjectName("hkset")
        self.soundList = QtWidgets.QListWidget(self.background)
        self.soundList.setGeometry(QtCore.QRect(170, 60, 471, 421))
        self.soundList.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.soundList.setFrameShadow(QtWidgets.QFrame.Raised)
        self.soundList.setObjectName("soundList")
        self.catList = QtWidgets.QListWidget(self.background)
        self.catList.setGeometry(QtCore.QRect(0, 280, 171, 201))
        self.catList.setStyleSheet("")
        self.catList.setObjectName("catList")
        self.label = QtWidgets.QLabel(self.background)
        self.label.setGeometry(QtCore.QRect(6, 253, 161, 31))
        font = QtGui.QFont()
        font.setFamily("Calibri Light")
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(3)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.volume_slider = QtWidgets.QSlider(self.background)
        self.volume_slider.setGeometry(QtCore.QRect(10, 170, 151, 20))
        self.volume_slider.setMaximum(100)
        self.volume_slider.setProperty("value", 70)
        self.volume_slider.setOrientation(QtCore.Qt.Horizontal)
        self.volume_slider.setObjectName("volume_slider")
        self.play_button = QtWidgets.QPushButton(self.centralwidget)
        self.play_button.setGeometry(QtCore.QRect(0, 70, 171, 41))
        self.play_button.setObjectName("play_button")
        self.select_label = QtWidgets.QLabel(self.centralwidget)
        self.select_label.setGeometry(QtCore.QRect(0, 30, 641, 31))
        self.select_label.setStyleSheet("")
        self.select_label.setText("")
        self.select_label.setAlignment(QtCore.Qt.AlignCenter)
        self.select_label.setObjectName("select_label")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.min_button.setText(_translate("MainWindow", "-"))
        self.exit_button.setText(_translate("MainWindow", "X"))
        self.pref_button.setText(_translate("MainWindow", "Settings"))
        self.hotkeys_button.setText(_translate("MainWindow", "Hotkeys"))
        self.stop_button.setText(_translate("MainWindow", "Stop"))
        self.hkset.setText(_translate("MainWindow", "Set hotkey"))
        self.label.setText(_translate("MainWindow", "Categories"))
        self.play_button.setText(_translate("MainWindow", "Play"))
