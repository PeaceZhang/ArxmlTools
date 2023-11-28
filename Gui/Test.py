from PySide6.QtWidgets import QApplication, QMainWindow, QTreeWidget, QTreeWidgetItem
import sys


class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 创建 QTreeWidget
        tree_widget = QTreeWidget(self)

        # 创建树形控件的列
        tree_widget.setColumnCount(2)
        tree_widget.setHeaderLabels(["Item", "Value"])

        # 添加根节点
        root_item = QTreeWidgetItem(tree_widget)
        root_item.setText(0, "Root")
        root_item.setText(1, "Root Value")

        # 添加子节点
        for i in range(3):
            child_item = QTreeWidgetItem(root_item)
            child_item.setText(0, f"Child {i}")
            child_item.setText(1, f"Child Value {i}")

        # 设置主窗口的中央部件为 QTreeWidget
        self.setCentralWidget(tree_widget)

        # 获取根节点下的所有子节点
        child_items = self.get_child_items(root_item)
        print("Child items of root:")
        for item in child_items:
            print(item.text(0))

    def get_child_items(self, parent_item):
        child_items = []
        for i in range(parent_item.childCount()):
            child_items.append(parent_item.child(i))
        return child_items


def main():
    app = QApplication(sys.argv)

    # 创建主窗口对象
    main_window = MyMainWindow()

    # 显示主窗口
    main_window.show()

    # 运行应用程序
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
