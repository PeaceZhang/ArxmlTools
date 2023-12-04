from PySide6.QtWidgets import QApplication, QTreeWidget, QTreeWidgetItem, QMenu, QDialog, QVBoxLayout, QLabel
from PySide6.QtGui import QAction
class CustomTreeWidget(QTreeWidget):
    def __init__(self):
        super().__init__()

        # 初始化UI
        self.initUI()

    def initUI(self):
        # 填充QTreeWidget的数据
        self.populateTree()

        # 连接customContextMenuRequested信号到槽函数
        self.customContextMenuRequested.connect(self.showContextMenu)

    def populateTree(self):
        # 这里添加QTreeWidget的数据
        # 示例数据
        parent = QTreeWidgetItem(self)
        parent.setText(0, "Parent Item")

        child1 = QTreeWidgetItem(parent)
        child1.setText(0, "Child 1")

        child2 = QTreeWidgetItem(parent)
        child2.setText(0, "Child 2")

    def showContextMenu(self, pos):
        # 获取当前点击的项目
        item = self.itemAt(pos)

        # 创建右键菜单
        contextMenu = QMenu(self)

        # 添加菜单项
        if item is not None:
            action1 = QAction(f"Open Popup for {item.text(0)}", self)
            action1.triggered.connect(lambda: self.openPopup(item.text(0)))
            contextMenu.addAction(action1)

        # 显示菜单
        contextMenu.exec_(self.mapToGlobal(pos))

    def openPopup(self, itemName):
        # 创建弹出窗口
        popup = QDialog(self)
        popup.setWindowTitle(f"Popup for {itemName}")

        # 在弹出窗口中添加一些内容
        layout = QVBoxLayout(popup)
        label = QLabel(f"This is a popup for {itemName}")
        layout.addWidget(label)

        # 显示弹出窗口
        popup.exec_()

if __name__ == '__main__':
    app = QApplication([])
    window = CustomTreeWidget()
    window.show()
    app.exec_()
