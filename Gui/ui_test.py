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
    QSizePolicy, QStatusBar, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.actionVersion = QAction(MainWindow)
        self.actionVersion.setObjectName(u"actionVersion")
        self.actionRecent_project = QAction(MainWindow)
        self.actionRecent_project.setObjectName(u"actionRecent_project")
        self.actionNew = QAction(MainWindow)
        self.actionNew.setObjectName(u"actionNew")
        self.actionNew_file = QAction(MainWindow)
        self.actionNew_file.setObjectName(u"actionNew_file")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 21))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuOpen_Project = QMenu(self.menuFile)
        self.menuOpen_Project.setObjectName(u"menuOpen_Project")
        self.menuAbout = QMenu(self.menubar)
        self.menuAbout.setObjectName(u"menuAbout")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())
        self.menuFile.addAction(self.menuOpen_Project.menuAction())
        self.menuFile.addAction(self.actionNew_file)
        self.menuOpen_Project.addAction(self.actionRecent_project)
        self.menuOpen_Project.addAction(self.actionNew)
        self.menuAbout.addAction(self.actionVersion)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionVersion.setText(QCoreApplication.translate("MainWindow", u"Version", None))
        self.actionRecent_project.setText(QCoreApplication.translate("MainWindow", u"Recent project", None))
        self.actionNew.setText(QCoreApplication.translate("MainWindow", u"New project", None))
        self.actionNew_file.setText(QCoreApplication.translate("MainWindow", u"New file", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuOpen_Project.setTitle(QCoreApplication.translate("MainWindow", u"Open Project", None))
        self.menuAbout.setTitle(QCoreApplication.translate("MainWindow", u"About", None))
    # retranslateUi

class MyWindow(QMainWindow):  # 这里的继承的父类一定要注意使用你定义UI窗体类型
    def __init__(self):
        super().__init__()
        # 使用ui文件，导入定义的界面类
        self.ui = Ui_MainWindow()
        # 初始化界面
        self.ui.setupUi(self)


# 启动窗口
app = QApplication([])
mywin = MyWindow()
mywin.show()
app.exec()