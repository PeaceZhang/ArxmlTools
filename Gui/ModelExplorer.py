from PySide6.QtWidgets import (QWidget, QTreeWidget, QTreeWidgetItem, QToolBar, QVBoxLayout, QSizePolicy, QMenu, QDialog, \
                               QLabel, QDialogButtonBox, QFrame, QGroupBox)
from PySide6.QtGui import QIcon, QFont, QAction
from PySide6.QtCore import Qt, QPoint
from ItemsView import ItemsView
import autosar
import glob
import os

class ModelExplorer:
    def __init__(self, path):
        super().__init__()
        self.view = AutosarView()

        # 解析arxml数据
        self.ardata = AutosarData(path, self.view)

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
        icon = QIcon("Icon/expand.png")
        expand_action.setIcon(icon)
        expand_action.triggered.connect(self.expand_treeview_allitems)
        self.toolbar.addAction(expand_action)

        collapse_action = QAction("Collapse ALL", self)
        icon = QIcon("Icon/collapse.png")
        collapse_action.setIcon(icon)
        collapse_action.triggered.connect(self.collapse_treeview_allitems)
        self.toolbar.addAction(collapse_action)

        self.treeview = QTreeWidget(self)

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
        icon = QIcon("Icon/autosar.jpg")
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
        print(item.text(0))

        contextMenu = QMenu(self.treeview)

        if "Base Types" == item.text(0):
            # 添加菜单项
            action1 = QAction("New Base Type...", self.treeview)
            action1.setIcon(QIcon("Icon/basetype.png"))
            action1.triggered.connect(self.openPopup)
            contextMenu.addAction(action1)

            action2 = QAction("Select All", self.treeview)
            # action2.triggered.connect(self.handleAction2)
            action2.setIcon(QIcon("Icon/basetype.png"))
            contextMenu.addAction(action2)
        else:
            # 添加菜单项
            action1 = QAction("Action 1", self.treeview)
            # action1.triggered.connect(self.handleAction1)
            contextMenu.addAction(action1)

            action2 = QAction("Action 2", self.treeview)
            # action2.triggered.connect(self.handleAction2)
            contextMenu.addAction(action2)
        # 显示菜单
        contextMenu.exec(self.treeview.mapToGlobal(pos))
    def openPopup(self, itemName):
        # 创建弹出窗口
        popup = QDialog(self)
        popup.setWindowTitle(f"Popup for {itemName}")
        popup.resize(200,200)
        # 在弹出窗口中添加一些内容
        layout = QVBoxLayout(popup)

        # 创建灰色线框
        # 创建灰色矩形框
        GroupBox = QGroupBox(popup)
        GroupBox.setTitle("ars")
        GroupBox.resize(100, 50)
        print(GroupBox.size())

        layout.addWidget(GroupBox)

        # 创建按钮框
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel | QDialogButtonBox.Apply)
        buttons.accepted.connect(popup.accept)
        buttons.rejected.connect(popup.reject)
        buttons.clicked.connect(lambda button: self.handleButtonClick(button, itemName))

        # 将按钮框添加到布局中
        layout.addWidget(buttons)

        # 显示弹出窗口
        result = popup.exec_()
        if result == QDialog.Accepted:
            print(f"OK button clicked for {itemName}")
        elif result == QDialog.Rejected:
            print(f"Cancel button clicked for {itemName}")

    def handleButtonClick(self, button, itemName):
        if button.text() == "Apply":
            print(f"Apply button clicked for {itemName}")

    def expand_treeview_allitems(self):
        self.treeview.expandAll()

    def collapse_treeview_allitems(self):
        self.treeview.collapseAll()

    def add_datatype_folder(self):
        # 添加data type子目录
        self.datatypes_folder = QTreeWidgetItem(self.treeview.root_item, ["Data Types"])
        icon = QIcon("Icon/DataTypes.png")
        self.datatypes_folder.setIcon(0, icon)

    def add_datatype_basetype_folder(self):
        self.treeview.datatypes_basetypes_folder = QTreeWidgetItem(self.datatypes_folder, ["Base Types"])
        icon = QIcon("Icon/bastypes.png")
        self.treeview.datatypes_basetypes_folder.setIcon(0, icon)

    def add_basetype_item(self, name):
        if self.treeview.datatypes_basetypes_folder is None:
            self.add_datatype_basetype_folder()
        basetypeitem = QTreeWidgetItem(self.treeview.datatypes_basetypes_folder, name)
        basetypeitem.setFont(0, QFont("Consolas"))
        basetypeitem.setFont(1, QFont("Consolas"))
        basetypeitem.setIcon(0, QIcon("Icon/basetype.png"))

    def add_datatype_implementation_folder(self):
        self.treeview.datatypes_implementation_folder = QTreeWidgetItem(self.datatypes_folder, ["Implementation Data Types"])
        icon = QIcon("Icon/bastypes.png")
        self.treeview.datatypes_implementation_folder.setIcon(0, icon)

    def add_impletype_item(self, name):
        if self.treeview.datatypes_implementation_folder is None:
            self.add_datatype_implementation_folder()
        impletype_item = QTreeWidgetItem(self.treeview.datatypes_implementation_folder, name)
        impletype_item.setFont(0, QFont("Consolas"))
        impletype_item.setFont(1, QFont("Consolas"))
        impletype_item.setIcon(0, QIcon("Icon/basetype.png"))


    def add_Infrastruture_compumethod_folder(self):
        self.treeview.Infrastruture_compumethod_folder = QTreeWidgetItem(self.treeview.Infrastructures_folder, ["Compu Method"])
        icon = QIcon("Icon/CompuMethod.png")
        self.treeview.Infrastruture_compumethod_folder.setIcon(0, icon)

    def add_compumethod_item(self, name):
        if self.treeview.Infrastruture_compumethod_folder is None:
            self.add_Infrastruture_compumethod_folder()
        compumethod_item = QTreeWidgetItem(self.treeview.Infrastruture_compumethod_folder, name)
        compumethod_item.setFont(0, QFont("Consolas"))
        compumethod_item.setFont(1, QFont("Consolas"))
        compumethod_item.setIcon(0, QIcon("Icon/CompuMethod.png"))

    def add_Infrastruture_dataconstraint_folder(self):
        self.treeview.Infrastruture_dataconstraint_folder = QTreeWidgetItem(self.treeview.Infrastructures_folder, ["Data Constraint"])
        icon = QIcon("Icon/dataconstraint.png")
        self.treeview.Infrastruture_dataconstraint_folder.setIcon(0, icon)

    def add_dataconstraint_item(self, name):
        if self.treeview.Infrastruture_dataconstraint_folder is None:
            self.add_Infrastruture_dataconstraint_folder()
        dataconstraint_item = QTreeWidgetItem(self.treeview.Infrastruture_dataconstraint_folder, name)
        dataconstraint_item.setFont(0, QFont("Consolas"))
        dataconstraint_item.setFont(1, QFont("Consolas"))
        dataconstraint_item.setIcon(0, QIcon("Icon/dataconstraint.png"))

    def add_Infrastruture_Unit_folder(self):
        self.treeview.Infrastruture_Unit_folder = QTreeWidgetItem(self.treeview.Infrastructures_folder, ["Unit"])
        icon = QIcon("Icon/unit.png")
        self.treeview.Infrastruture_Unit_folder.setIcon(0, icon)

    def add_Unit_item(self, name):
        if self.treeview.Infrastruture_Unit_folder is None:
            self.add_Infrastruture_Unit_folder()
        Unit_item = QTreeWidgetItem(self.treeview.Infrastruture_Unit_folder, name)
        Unit_item.setFont(0, QFont("Consolas"))
        Unit_item.setFont(1, QFont("Consolas"))
        Unit_item.setIcon(0, QIcon("Icon/unit.png"))

    def add_Interfaces_folder(self):
        self.Interfaces_folder = QTreeWidgetItem(self.treeview.root_item, ["Interfaces"])
        icon = QIcon("Icon/Interfaces.png")
        self.Interfaces_folder.setIcon(0, icon)

    def add_Interfaces_SRIterface_folder(self):
        self.treeview.Interfaces_SRIterface_folder = QTreeWidgetItem(self.Interfaces_folder, ["SR Interfaces"])
        icon = QIcon("Icon/srinterface.png")
        self.treeview.Interfaces_SRIterface_folder.setIcon(0, icon)

    def add_SRInterface_item(self, name):
        if self.treeview.Interfaces_SRIterface_folder is None:
            self.add_Interfaces_SRIterface_folder()
        SRInterface_item = QTreeWidgetItem(self.treeview.Interfaces_SRIterface_folder, name)
        SRInterface_item.setFont(0, QFont("Consolas"))
        SRInterface_item.setFont(1, QFont("Consolas"))
        SRInterface_item.setIcon(0, QIcon("Icon/srinterface.png"))

    def add_Interfaces_CSIterface_folder(self):
        self.treeview.Interfaces_CSIterface_folder = QTreeWidgetItem(self.Interfaces_folder, ["CS Interfaces"])
        icon = QIcon("Icon/csinterface.png")
        self.treeview.Interfaces_CSIterface_folder.setIcon(0, icon)

    def add_CSInterface_item(self, name):
        if self.treeview.Interfaces_CSIterface_folder is None:
            self.add_Interfaces_CSIterface_folder()
        CSInterface_item = QTreeWidgetItem(self.treeview.Interfaces_CSIterface_folder, name)
        CSInterface_item.setFont(0, QFont("Consolas"))
        CSInterface_item.setFont(1, QFont("Consolas"))
        CSInterface_item.setIcon(0, QIcon("Icon/csinterface.png"))

    def add_Components_folder(self):
        self.treeview.Components_folder = QTreeWidgetItem(self.treeview.root_item, ["Components"])
        icon = QIcon("Icon/swc.png")
        self.treeview.Components_folder.setIcon(0, icon)

    def add_swc_item(self, name):
        swc_item = QTreeWidgetItem(self.treeview.Components_folder, name)
        swc_item.setFont(0, QFont("Consolas"))
        swc_item.setFont(1, QFont("Consolas"))
        swc_item.setIcon(0, QIcon("Icon/swc.png"))

    def add_Compositions_folder(self):
        self.treeview.Compositions_foler = QTreeWidgetItem(self.treeview.root_item, ["Compositions"])
        icon = QIcon("Icon/composition.png")
        self.treeview.Compositions_foler.setIcon(0, icon)

    def add_composition_item(self, name):
        composition_item = QTreeWidgetItem(self.treeview.Compositions_foler, name)
        composition_item.setFont(0, QFont("Consolas"))
        composition_item.setFont(1, QFont("Consolas"))
        composition_item.setIcon(0, QIcon("Icon/composition.png"))
        # self.treeview.itemDoubleClicked.connect(ItemsView.show_details)

    def add_Infrastruture_folder(self):
        self.treeview.Infrastructures_folder = QTreeWidgetItem(self.treeview.root_item, ["Infrastructures"])
        icon = QIcon("Icon/Infrastructures.png")
        self.treeview.Infrastructures_folder.setIcon(0, icon)

class AutosarData:
    def __init__(self, workspace, view):

        self.arxml_files = []
        self.arxml_files = self.find_files_recursive(workspace, "arxml")
        self.ws = autosar.workspace()
        for arxml in self.arxml_files:
            self.ws.loadXML(arxml)
        for pack in self.ws.listPackages():
            for pack1 in self.ws.findall(pack):
                self.package_parser(pack1, view)

    def package_parser(self, package, view):
        if package.subPackages:
            for son in package.subPackages:
                self.package_parser(son, view)
        if package.elements:
            for ele in package.elements:
                if isinstance(ele, autosar.datatype.SwBaseType):
                    # print(ele.ref, ele.name, ele.parent, ele.nativeDeclaration, ele.size, ele.typeEncoding, ele.category)
                    view.add_basetype_item([ele.name, ele.ref])
                    pass
                if isinstance(ele, autosar.datatype.ImplementationDataType):
                    # print(ele.ref, ele.name, ele.parent, ele.category, ele.arraySize, ele.compuMethodRef, ele.baseTypeRef, ele.implementationTypeRef)
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

    def find_files_recursive(self, folder_path, file_extension):
        pattern = os.path.join(folder_path, f"**/*.{file_extension}")
        file_list = glob.glob(pattern, recursive=True)
        return file_list


