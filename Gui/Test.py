# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_test.ui'
##
## Created by: Qt User Interface Compiler version 6.6.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QMainWindow, QMenu, QMenuBar,
    QSizePolicy, QStatusBar, QWidget, QMessageBox)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        # set mian window's object name/default size/Icon
        MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        ArxmlTooolsIcon = QIcon("Icon/arxmltoolsicon.png")
        MainWindow.setWindowIcon(ArxmlTooolsIcon)

        # set action for menu bar terminal items
        self.actionMenubar_About_Version = QAction(MainWindow)
        self.actionMenubar_About_Version.setObjectName(u"actionMenubar_About_Version")
        # self.actionMenubar_About_Version.triggered.connect(self.show_version_diaglog)

        self.actionMenubar_File_New_file = QAction(MainWindow)
        self.actionMenubar_File_New_file.setObjectName(u"actionMenubar_File_New_file")

        self.actionMenubar_File_Open = QAction(MainWindow)
        self.actionMenubar_File_Open.setObjectName(u"actionMenubar_File_Open")

        # set centralwidget for main window
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)

        # new and setup menu bar
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 21))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuAbout = QMenu(self.menubar)
        self.menuAbout.setObjectName(u"menuAbout")
        MainWindow.setMenuBar(self.menubar)

        # new and setup status bar
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        # assign action to menu bar items
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())
        self.menuFile.addAction(self.actionMenubar_File_Open)
        self.menuFile.addAction(self.actionMenubar_File_New_file)
        self.menuAbout.addAction(self.actionMenubar_About_Version)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi
    # def show_version_diaglog(self, MainWindow):
    #     version_text = "My Application Version 1.0"
    #     QMessageBox.aboutQt(MainWindow, "Version")

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"ArxmlTools", None))
        self.actionMenubar_About_Version.setText(QCoreApplication.translate("MainWindow", u"Version", None))
        self.actionMenubar_File_New_file.setText(QCoreApplication.translate("MainWindow", u"New file...", None))
        self.actionMenubar_File_Open.setText(QCoreApplication.translate("MainWindow", u"Open...", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuAbout.setTitle(QCoreApplication.translate("MainWindow", u"About", None))
    # retranslateUi


class MyWindow(QMainWindow):  # 这里的继承的父类一定要注意使用你定义UI窗体类型
    def __init__(self):
        super().__init__()
        # 使用ui文件，导入定义的界面类
        self.ui = Ui_MainWindow()
        # 初始化界面
        self.ui.setupUi(self)
        self.ui.actionMenubar_About_Version.triggered.connect(self.show_version_diaglog)
    def show_version_diaglog(self):
        version_text = "My Application Version 1.0"
        QMessageBox.information(self.ui, "Version", version_text)

# 启动窗口
app = QApplication([])
mywin = MyWindow()
mywin.show()
app.exec()