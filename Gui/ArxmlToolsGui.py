from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox, QTextEdit, QSplitter, QTabWidget, QFileDialog
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QAction, QIcon
from FileExplorer import FileExplorer
from ModelExplorer import ModelExplorer
import sys


class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setGeometry(100, 100, 800, 600)

        # 设置主窗口属性
        self.setWindowTitle("ArxmlTools")
        ArxmlToolsIcon = QIcon("Icon/arxmltoolsicon.png")
        self.setWindowIcon(ArxmlToolsIcon)

        # 创建一个版本信息动作
        action_version = QAction("Version", self)
        action_version.triggered.connect(self.show_version_dialog)

        # 创建一个问价夹打开动作
        action_openfolder = QAction("Open Folder", self)
        action_openfolder.triggered.connect(self.open_folder)

        # 创建菜单栏
        menu_bar = self.menuBar()

        # 创建 "File" 菜单
        file_menu = menu_bar.addMenu("File")

        # 创建 "About" 菜单
        about_menu = menu_bar.addMenu("About")

        # 在 "File" 菜单下添加打开文件夹操作
        file_menu.addAction(action_openfolder)

        # 在 "About" 菜单下添加版本信息动作
        about_menu.addAction(action_version)

        self.project_view = QTabWidget()
        # 创建右侧 Splitter
        content_view = QSplitter(Qt.Vertical)
        content_view.addWidget(QTextEdit())
        content_view.addWidget(QTextEdit())
        content_view.setSizes([100, 100])

        # 创建左侧 Splitter
        explorer_view = QSplitter(Qt.Vertical)
        explorer_view.addWidget(self.project_view)
        explorer_view.addWidget(QTextEdit())
        explorer_view.setSizes([100, 100])

        # 创建一个 QSplitter
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(explorer_view)
        splitter.addWidget(content_view)
        splitter.setSizes([230, 570])

        # 设置主窗口的中央部件为 QSplitter
        self.setCentralWidget(splitter)

    def show_version_dialog(self):
        # 显示版本信息对话框
        version_text = "ArxmlTools V0010"
        QMessageBox.information(self, "Version", version_text)

    def open_folder(self):
        # 打开文件夹
        folder_path = QFileDialog.getExistingDirectory(self, "Open Folder", "D:\AutosarTutorial\ArxmlTools\Export")
        print(folder_path)
        self.draw_model_explorer(folder_path)
        self.draw_file_explorer(folder_path)

    def draw_model_explorer(self, path):
        project_view_model_explorer = ModelExplorer(path)
        self.project_view.addTab(project_view_model_explorer.view, "Model Explorer")
        pass

    def draw_file_explorer(self, path):
        project_view_file_explorer = FileExplorer(path)
        self.project_view.addTab(project_view_file_explorer, "File Explorer")
        pass

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
