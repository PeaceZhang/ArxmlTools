from PySide6.QtWidgets import QApplication, QMainWindow, QTreeWidget, QTreeWidgetItem
import sys

class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 设置主窗口的默认大小
        self.setGeometry(100, 100, 400, 300)

        # 使用 QTreeWidget 显示树形数据
        tree_widget = QTreeWidget(self)
        tree_widget.setHeaderLabels(["Column 1", "Column 2"])

        # 添加根节点
        root_item = QTreeWidgetItem(tree_widget, ["Root", "Root Data"])

        # 添加子节点
        child_item = QTreeWidgetItem(root_item, ["Child", "Child Data"])

        # 设置主窗口的中央部件为 QTreeWidget
        self.setCentralWidget(tree_widget)

        # 设置主窗口属性
        self.setWindowTitle("QTreeWidget Example")

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
