from PySide6.QtWidgets import QWidget, QTreeWidget, QTreeWidgetItem, QVBoxLayout
from PySide6.QtGui import QIcon, QFont
import autosar

class ItemsView(QWidget):
    def __init__(self):
        super().__init__()

        self.armodel = None

        # 创建垂直布局
        layout = QVBoxLayout(self)

        self.tree_view = QTreeWidget(self)

        layout.addWidget(self.tree_view)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        # 设置主窗口的布局
        self.setLayout(layout)

        self.tree_view.setHeaderLabels(["Item", "Properties"])

    def get_armodel(self, armodel):
        self.armodel = armodel

    def show_details(self, item):
        self.tree_view.clear()
        self.tree_view.addTopLevelItem(item.clone())
        if 0 == item.childCount():
            obj = self.armodel.find(item.text(1))
            if isinstance(obj, autosar.component.CompositionComponent):
                if 0 != len(obj.requirePorts):
                    r_port_folder = QTreeWidgetItem(self.tree_view.topLevelItem(0), ['R Ports'])
                    r_port_folder.setIcon(0, QIcon("Icon/rport.png"))
                if 0 != len(obj.providePorts):
                    p_port_folder = QTreeWidgetItem(self.tree_view.topLevelItem(0), ['P Ports'])
                    p_port_folder.setIcon(0, QIcon("Icon/pport.png"))
                if 0 != len(obj.components):
                    component_folder = QTreeWidgetItem(self.tree_view.topLevelItem(0), ['Components'])
                    component_folder.setIcon(0, QIcon("Icon/component.png"))
                for rp in obj.requirePorts:
                    rp_item = QTreeWidgetItem(r_port_folder, [rp.name, rp.ref])
                    rp_item.setIcon(0, QIcon("Icon/rport.png"))
                    rp_item.setFont(0, QFont("Consolas"))
                    rp_item.setFont(1, QFont("Consolas"))
                for pp in obj.providePorts:
                    pp_item = QTreeWidgetItem(p_port_folder, [pp.name, pp.ref])
                    pp_item.setIcon(0, QIcon("Icon/pport.png"))
                    pp_item.setFont(0, QFont("Consolas"))
                    pp_item.setFont(1, QFont("Consolas"))
                for component in obj.components:
                    component_item = QTreeWidgetItem(component_folder, [component.name, component.ref])
                    component_item.setIcon(0, QIcon("Icon/swc.png"))
                    component_item.setFont(0, QFont("Consolas"))
                    component_item.setFont(1, QFont("Consolas"))
                    component_item_typeref = QTreeWidgetItem(component_item, ['TypeRef', self.armodel.find(component.ref).typeRef])
                    component_item_typeref.setFont(0, QFont("Consolas"))
                    component_item_typeref.setFont(1, QFont("Consolas"))
                    component_item_typeref.setIcon(0, QIcon("Icon/reference.png"))

        self.tree_view.expandAll()






