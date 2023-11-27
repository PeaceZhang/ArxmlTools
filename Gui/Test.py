from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PySide6.QtGui import QAction, QIcon
import sys

class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 创建一个版本信息动作
        action_version = QAction("Version", self)
        action_version.triggered.connect(self.show_version_dialog)

        # 创建菜单栏
        menu_bar = self.menuBar()

        # 创建 "About" 菜单
        about_menu = menu_bar.addMenu("About")

        # 在 "About" 菜单下添加版本信息动作
        about_menu.addAction(action_version)

    def show_version_dialog(self):
        # 显示版本信息对话框
        version_text = "ArxmlTools V0010"
        QMessageBox.information(self, "Version", version_text)

def main():
    app = QApplication(sys.argv)

    # 创建主窗口对象
    main_window = MyMainWindow()

    # 设置主窗口属性
    main_window.setWindowTitle("ArxmlTools")
    main_window.resize(800, 600)
    ArxmlToolsIcon = QIcon("Icon/arxmltoolsicon.png")
    main_window.setWindowIcon(ArxmlToolsIcon)

    # 显示主窗口
    main_window.show()

    # 运行应用程序
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
