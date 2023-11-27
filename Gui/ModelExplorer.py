from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem


class ModelExplorer(QTreeWidget):
    def __init__(self):
        super().__init__()

        self.setHeaderLabels(["Ar Model", "Ar path"])
        # 添加根节点
        root_item = QTreeWidgetItem(self, ["Root", "Root Data"])

        # 添加子节点
        child_item = QTreeWidgetItem(root_item, ["Child", "Child Data"])
        child1_item = QTreeWidgetItem(root_item, ["Child1", "Child Data1"])

        grandson_item = QTreeWidgetItem(child_item, ["grandson1", "grandson1 data"])