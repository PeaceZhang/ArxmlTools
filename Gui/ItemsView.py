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

    def show_details(self, item):
        self.tree_view.clear()
        self.tree_view.addTopLevelItem(item.clone())

