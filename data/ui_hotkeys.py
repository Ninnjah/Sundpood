# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'hotkeys.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(420, 468)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(420, 468))
        MainWindow.setMaximumSize(QtCore.QSize(420, 468))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
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
        self.exit_button = QtWidgets.QPushButton(self.centralwidget)
        self.exit_button.setGeometry(QtCore.QRect(380, 0, 41, 31))
        self.exit_button.setStyleSheet("")
        self.exit_button.setObjectName("exit_button")
        self.min_button = QtWidgets.QPushButton(self.centralwidget)
        self.min_button.setGeometry(QtCore.QRect(340, 0, 41, 31))
        self.min_button.setStyleSheet("")
        self.min_button.setObjectName("min_button")
        self.Hotkeys = QtWidgets.QLabel(self.centralwidget)
        self.Hotkeys.setGeometry(QtCore.QRect(20, 40, 291, 20))
        self.Hotkeys.setStyleSheet("background: none;\n"
"")
        self.Hotkeys.setObjectName("Hotkeys")
        self.background = QtWidgets.QWidget(self.centralwidget)
        self.background.setGeometry(QtCore.QRect(0, 0, 421, 71))
        self.background.setStyleSheet("")
        self.background.setObjectName("background")
        self.hotkeyList = QtWidgets.QListWidget(self.centralwidget)
        self.hotkeyList.setGeometry(QtCore.QRect(0, 70, 421, 351))
        self.hotkeyList.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.hotkeyList.setObjectName("hotkeyList")
        self.delete_button = QtWidgets.QPushButton(self.centralwidget)
        self.delete_button.setGeometry(QtCore.QRect(0, 420, 101, 51))
        self.delete_button.setStyleSheet("")
        self.delete_button.setObjectName("delete_button")
        self.background.raise_()
        self.exit_button.raise_()
        self.min_button.raise_()
        self.Hotkeys.raise_()
        self.hotkeyList.raise_()
        self.delete_button.raise_()
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Hotkeys"))
        self.exit_button.setText(_translate("MainWindow", "X"))
        self.min_button.setText(_translate("MainWindow", "-"))
        self.Hotkeys.setText(_translate("MainWindow", "Hotkeys"))
        self.delete_button.setText(_translate("MainWindow", "Delete"))
