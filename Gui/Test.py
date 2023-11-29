from PySide6.QtWidgets import QApplication, QMainWindow, QTreeWidget, QTreeWidgetItem
import sys
from ModelExplorer import ModelExplorer

class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        ME = ModelExplorer('D:\AutosarTutorial\ArxmlTools\Export')
        # 设置主窗口的中央部件为 QTreeWidget
        self.setCentralWidget(ME.view)


def main():
    app = QApplication(sys.argv)

    # 创建主窗口对象
    main_window = MyMainWindow()

    # 显示主窗口
    main_window.show()

    # 运行应用程序
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
