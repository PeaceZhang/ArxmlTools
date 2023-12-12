from PySide6.QtGui import QAction, QIcon, QFont, Qt
from PySide6.QtWidgets import QWidget, QToolBar, QSizePolicy, QTreeWidget, QVBoxLayout, QTreeWidgetItem, QMenu, QApplication

import autosar
from autosar.workspace import Workspace

from Gui.Dialogs.Dialog_BaseType import BaseTypeDialog

class AutosarView(QWidget):
    def __init__(self):
        super().__init__()

        self.toolbar = QToolBar(self)
        self.toolbar.setFixedHeight(24)
        # self.toolbar.setStyleSheet("background-color: #f0f0f0;")
        # 创建占位符，使工具按钮靠右对齐
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        # 将占位符添加到工具栏
        self.toolbar.addWidget(spacer)

        expand_action = QAction("Expand ALL", self)
        icon = QIcon("../Icon/expand.png")
        expand_action.setIcon(icon)
        expand_action.triggered.connect(self.expand_treeview_allitems)
        self.toolbar.addAction(expand_action)

        collapse_action = QAction("Collapse ALL", self)
        icon = QIcon("../Icon/collapse.png")
        collapse_action.setIcon(icon)
        collapse_action.triggered.connect(self.collapse_treeview_allitems)
        self.toolbar.addAction(collapse_action)

        self.treeview = QTreeWidget(self)
        self.treeview.setSelectionMode(QTreeWidget.ExtendedSelection)
        self.treeview.setFocusPolicy(Qt.NoFocus)
        self.treeview.itemSelectionChanged.connect(self.selected_items_proc)

        layout = QVBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.toolbar)
        layout.addWidget(self.treeview)

        self.treeview.setHeaderLabels(["Ar Model", "Ar path"])
        self.treeview.setColumnWidth(0, 260)
        # 添加根节点
        self.treeview.root_item = QTreeWidgetItem(self.treeview, ["AUTOSAR"])
        # 设置根节点Icon
        icon = QIcon("../Icon/autosar.jpg")
        self.treeview.root_item.setIcon(0, icon)
        # 设置默认展开
        self.treeview.root_item.setExpanded(True)

        # 添加一级子目录
        self.add_datatype_folder()
        self.add_Interfaces_folder()
        self.add_Components_folder()
        self.add_Compositions_folder()
        self.add_Infrastruture_folder()

        self.treeview.setContextMenuPolicy(Qt.CustomContextMenu)
        self.treeview.customContextMenuRequested.connect(self.showContextMenu)

        self.treeview.datatypes_basetypes_folder = None
        self.treeview.datatypes_implementation_folder = None
        self.treeview.Infrastruture_compumethod_folder = None
        self.treeview.Infrastruture_dataconstraint_folder = None
        self.treeview.Infrastruture_Unit_folder = None
        self.treeview.Interfaces_SRIterface_folder = None
        self.treeview.Interfaces_CSIterface_folder = None

    def showContextMenu(self, pos):
        item = self.treeview.itemAt(pos)
        self.current_selected_item = item
        print(item.text(0))

        contextMenu = QMenu(self.treeview)

        if "Base Types" == item.text(0):
            # 添加菜单项
            action1 = QAction("New Base Type...", self.treeview)
            action1.setIcon(QIcon("../Icon/basetype.png"))
            action1.triggered.connect(self.open_newbasetypeview)
            contextMenu.addAction(action1)
        else:
            # 添加菜单项
            action1 = QAction("Action 1", self.treeview)
            # action1.triggered.connect(self.handleAction1)
            contextMenu.addAction(action1)

            action2 = QAction("Action 2", self.treeview)
            # action2.triggered.connect(self.handleAction2)
            contextMenu.addAction(action2)
        # 显示菜单
        if item.childCount():
            action2 = QAction("Select All", self.treeview)
            action2.triggered.connect(self.select_allchild)
            action2.setIcon(QIcon("../Icon/basetype.png"))
            contextMenu.addAction(action2)
        contextMenu.exec(self.treeview.mapToGlobal(pos))

    def selected_items_proc(self):
        selected_items = self.treeview.selectedItems()
        if len(selected_items) > 1:
            for item in selected_items:
                print(item.text(0))
                if item.childCount():
                    item.setSelected(False)

    def open_newbasetypeview(self):
        print("open dialog: new base type view")
        basetype_package = ws.find('/DataTypes/BaseTypes')
        dialog = BaseTypeDialog(isNewBasetype=True, packageofnewbastype=basetype_package)
        dialog.exec()

    def select_allchild(self, pos):
        item = self.current_selected_item
        print(item.childCount())
        for i in range(item.childCount()):
            child_item = item.child(i)
            child_item.setSelected(True)
        item.setSelected(False)

    def expand_treeview_allitems(self):
        self.treeview.expandAll()

    def collapse_treeview_allitems(self):
        self.treeview.collapseAll()

    def add_datatype_folder(self):
        # 添加data type子目录
        self.datatypes_folder = QTreeWidgetItem(self.treeview.root_item, ["Data Types"])
        icon = QIcon("../Icon/DataTypes.png")
        self.datatypes_folder.setIcon(0, icon)

    def add_datatype_basetype_folder(self):
        self.treeview.datatypes_basetypes_folder = QTreeWidgetItem(self.datatypes_folder, ["Base Types"])
        icon = QIcon("../Icon/bastypes.png")
        self.treeview.datatypes_basetypes_folder.setIcon(0, icon)

    def add_basetype_item(self, name):
        if self.treeview.datatypes_basetypes_folder is None:
            self.add_datatype_basetype_folder()
        basetypeitem = QTreeWidgetItem(self.treeview.datatypes_basetypes_folder, name)
        basetypeitem.setFont(0, QFont("Consolas"))
        basetypeitem.setFont(1, QFont("Consolas"))
        basetypeitem.setIcon(0, QIcon("../Icon/basetype.png"))

    def add_datatype_implementation_folder(self):
        self.treeview.datatypes_implementation_folder = QTreeWidgetItem(self.datatypes_folder, ["Implementation Data Types"])
        icon = QIcon("../Icon/bastypes.png")
        self.treeview.datatypes_implementation_folder.setIcon(0, icon)

    def add_impletype_item(self, name):
        if self.treeview.datatypes_implementation_folder is None:
            self.add_datatype_implementation_folder()
        impletype_item = QTreeWidgetItem(self.treeview.datatypes_implementation_folder, name)
        impletype_item.setFont(0, QFont("Consolas"))
        impletype_item.setFont(1, QFont("Consolas"))
        impletype_item.setIcon(0, QIcon("../Icon/basetype.png"))


    def add_Infrastruture_compumethod_folder(self):
        self.treeview.Infrastruture_compumethod_folder = QTreeWidgetItem(self.treeview.Infrastructures_folder, ["Compu Method"])
        icon = QIcon("../Icon/CompuMethod.png")
        self.treeview.Infrastruture_compumethod_folder.setIcon(0, icon)

    def add_compumethod_item(self, name):
        if self.treeview.Infrastruture_compumethod_folder is None:
            self.add_Infrastruture_compumethod_folder()
        compumethod_item = QTreeWidgetItem(self.treeview.Infrastruture_compumethod_folder, name)
        compumethod_item.setFont(0, QFont("Consolas"))
        compumethod_item.setFont(1, QFont("Consolas"))
        compumethod_item.setIcon(0, QIcon("../Icon/CompuMethod.png"))

    def add_Infrastruture_dataconstraint_folder(self):
        self.treeview.Infrastruture_dataconstraint_folder = QTreeWidgetItem(self.treeview.Infrastructures_folder, ["Data Constraint"])
        icon = QIcon("../Icon/dataconstraint.png")
        self.treeview.Infrastruture_dataconstraint_folder.setIcon(0, icon)

    def add_dataconstraint_item(self, name):
        if self.treeview.Infrastruture_dataconstraint_folder is None:
            self.add_Infrastruture_dataconstraint_folder()
        dataconstraint_item = QTreeWidgetItem(self.treeview.Infrastruture_dataconstraint_folder, name)
        dataconstraint_item.setFont(0, QFont("Consolas"))
        dataconstraint_item.setFont(1, QFont("Consolas"))
        dataconstraint_item.setIcon(0, QIcon("../Icon/dataconstraint.png"))

    def add_Infrastruture_Unit_folder(self):
        self.treeview.Infrastruture_Unit_folder = QTreeWidgetItem(self.treeview.Infrastructures_folder, ["Unit"])
        icon = QIcon("../Icon/unit.png")
        self.treeview.Infrastruture_Unit_folder.setIcon(0, icon)

    def add_Unit_item(self, name):
        if self.treeview.Infrastruture_Unit_folder is None:
            self.add_Infrastruture_Unit_folder()
        Unit_item = QTreeWidgetItem(self.treeview.Infrastruture_Unit_folder, name)
        Unit_item.setFont(0, QFont("Consolas"))
        Unit_item.setFont(1, QFont("Consolas"))
        Unit_item.setIcon(0, QIcon("../Icon/unit.png"))

    def add_Interfaces_folder(self):
        self.Interfaces_folder = QTreeWidgetItem(self.treeview.root_item, ["Interfaces"])
        icon = QIcon("../Icon/Interfaces.png")
        self.Interfaces_folder.setIcon(0, icon)

    def add_Interfaces_SRIterface_folder(self):
        self.treeview.Interfaces_SRIterface_folder = QTreeWidgetItem(self.Interfaces_folder, ["SR Interfaces"])
        icon = QIcon("../Icon/srinterface.png")
        self.treeview.Interfaces_SRIterface_folder.setIcon(0, icon)

    def add_SRInterface_item(self, name):
        if self.treeview.Interfaces_SRIterface_folder is None:
            self.add_Interfaces_SRIterface_folder()
        SRInterface_item = QTreeWidgetItem(self.treeview.Interfaces_SRIterface_folder, name)
        SRInterface_item.setFont(0, QFont("Consolas"))
        SRInterface_item.setFont(1, QFont("Consolas"))
        SRInterface_item.setIcon(0, QIcon("../Icon/srinterface.png"))

    def add_Interfaces_CSIterface_folder(self):
        self.treeview.Interfaces_CSIterface_folder = QTreeWidgetItem(self.Interfaces_folder, ["CS Interfaces"])
        icon = QIcon("../Icon/csinterface.png")
        self.treeview.Interfaces_CSIterface_folder.setIcon(0, icon)

    def add_CSInterface_item(self, name):
        if self.treeview.Interfaces_CSIterface_folder is None:
            self.add_Interfaces_CSIterface_folder()
        CSInterface_item = QTreeWidgetItem(self.treeview.Interfaces_CSIterface_folder, name)
        CSInterface_item.setFont(0, QFont("Consolas"))
        CSInterface_item.setFont(1, QFont("Consolas"))
        CSInterface_item.setIcon(0, QIcon("../Icon/csinterface.png"))

    def add_Components_folder(self):
        self.treeview.Components_folder = QTreeWidgetItem(self.treeview.root_item, ["Components"])
        icon = QIcon("../Icon/swc.png")
        self.treeview.Components_folder.setIcon(0, icon)

    def add_swc_item(self, name):
        swc_item = QTreeWidgetItem(self.treeview.Components_folder, name)
        swc_item.setFont(0, QFont("Consolas"))
        swc_item.setFont(1, QFont("Consolas"))
        swc_item.setIcon(0, QIcon("../Icon/swc.png"))

    def add_Compositions_folder(self):
        self.treeview.Compositions_foler = QTreeWidgetItem(self.treeview.root_item, ["Compositions"])
        icon = QIcon("../Icon/composition.png")
        self.treeview.Compositions_foler.setIcon(0, icon)

    def add_composition_item(self, name):
        composition_item = QTreeWidgetItem(self.treeview.Compositions_foler, name)
        composition_item.setFont(0, QFont("Consolas"))
        composition_item.setFont(1, QFont("Consolas"))
        composition_item.setIcon(0, QIcon("../Icon/composition.png"))
        # self.treeview.itemDoubleClicked.connect(ItemsView.show_details)

    def add_Infrastruture_folder(self):
        self.treeview.Infrastructures_folder = QTreeWidgetItem(self.treeview.root_item, ["Infrastructures"])
        icon = QIcon("../Icon/Infrastructures.png")
        self.treeview.Infrastructures_folder.setIcon(0, icon)

class AutosarViewDraw:
    def __init__(self, ws, arview):
        if isinstance(ws, Workspace):
            for pack in ws.listPackages():
                for pack1 in ws.findall(pack):
                    self.package_parser(pack1, arview)

    def package_parser(self, package, view):
        if package.subPackages:
            for son in package.subPackages:
                self.package_parser(son, view)
        if package.elements:
            for ele in package.elements:
                if isinstance(ele, autosar.datatype.SwBaseType):
                    view.add_basetype_item([ele.name, ele.ref])
                    pass
                if isinstance(ele, autosar.datatype.ImplementationDataType):
                    # print(ele.ref)
                    view.add_impletype_item([ele.name, ele.ref])
                    pass
                if isinstance(ele, autosar.datatype.CompuMethod):
                    # print(ele.ref)
                    view.add_compumethod_item([ele.name, ele.ref])
                    pass
                if isinstance(ele, autosar.datatype.DataConstraint):
                    view.add_dataconstraint_item([ele.name, ele.ref])
                    # print(ele.ref)
                    pass
                if isinstance(ele, autosar.datatype.Unit):
                    view.add_Unit_item([ele.name, ele.ref])
                    # print(ele.ref)
                    pass
                if isinstance(ele, autosar.portinterface.SenderReceiverInterface):
                    view.add_SRInterface_item([ele.name, ele.ref])
                    # print(ele.ref)
                    pass
                if isinstance(ele, autosar.portinterface.ClientServerInterface):
                    # print(ele.ref)
                    view.add_CSInterface_item([ele.name, ele.ref])
                    pass
                if isinstance(ele, autosar.component.ApplicationSoftwareComponent):
                    view.add_swc_item([ele.name, ele.ref])
                    # print(ele.ref)
                    pass
                if isinstance(ele, autosar.component.CompositionComponent):
                    view.add_composition_item([ele.name, ele.ref])
                    # print(ele.ref)
                    pass

if __name__ == '__main__':
    from PySide6.QtWidgets import QApplication
    import sys
    app = QApplication([])

    ws = autosar.workspace()
    ws.loadXML("../../Export/Application.arxml")

    widget = AutosarView()
    AutosarViewDraw(ws, widget)
    widget.show()

    app.exec()

    # sys.exit(app.exec())

    ws.saveXML("../../Export/ars.arxml")
    print("______________________________________________")