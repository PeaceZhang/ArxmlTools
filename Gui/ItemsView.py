from PySide6.QtWidgets import QWidget, QTreeWidget, QTreeWidgetItem, QVBoxLayout
class ItemsView(QWidget):
    def __init__(self):
        super().__init__()

        # 创建垂直布局
        layout = QVBoxLayout(self)

        self.tree_view = QTreeWidget(self)

        layout.addWidget(self.tree_view)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        # 设置主窗口的布局
        self.setLayout(layout)

        self.tree_view.setHeaderLabels(["Item", "Properties"])

    def show_details(self, item, sss):
        print(item)
        print(sss)
        # if 0 == item.childCount():
        #     composition_item = QTreeWidgetItem(self.root_item, [item.text(0)])
        # else:
        #     self.root_item.addChild(item)
        #     self.tree_view.addTopLevelItem(self.root_item)
        self.tree_view.clear()
        QTreeWidgetItem(self.tree_view, [item.text(0), item.text(1)])
