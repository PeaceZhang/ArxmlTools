from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem
from PySide6.QtGui import QIcon, QFont
import autosar
import glob
import os

class ModelExplorer:
    def __init__(self, path):
        super().__init__()
        self.view = AutosarView()

        # 解析arxml数据
        AutosarData(path, self.view)

class AutosarView(QTreeWidget):
    def __init__(self):
        super().__init__()

        self.setHeaderLabels(["Ar Model", "Ar path"])
        self.setColumnWidth(0, 200)
        # 添加根节点
        self.root_item = QTreeWidgetItem(self, ["AUTOSAR"])
        # 设置根节点Icon
        icon = QIcon("Icon/autosar.jpg")
        self.root_item.setIcon(0, icon)
        # 设置默认展开
        self.root_item.setExpanded(True)

        # 添加一级子目录
        self.add_datatype_folder()
        self.add_Interfaces_folder()
        self.add_Components_folder()
        self.add_Compositions_folder()
        self.add_Infrastruture_folder()

        self.datatypes_basetypes_folder = None
        self.datatypes_implementation_folder = None
        self.Infrastruture_compumethod_folder = None
        self.Infrastruture_dataconstraint_folder = None

    def add_datatype_folder(self):
        # 添加data type子目录
        self.datatypes_folder = QTreeWidgetItem(self.root_item, ["Data Types"])
        icon = QIcon("Icon/DataTypes.png")
        self.datatypes_folder.setIcon(0, icon)

    def add_datatype_basetype_folder(self):
        self.datatypes_basetypes_folder = QTreeWidgetItem(self.datatypes_folder, ["Base Types"])
        icon = QIcon("Icon/bastypes.png")
        self.datatypes_basetypes_folder.setIcon(0, icon)

    def add_basetype_item(self, name):
        if self.datatypes_basetypes_folder is None:
            self.add_datatype_basetype_folder()
        basetypeitem = QTreeWidgetItem(self.datatypes_basetypes_folder, name)
        basetypeitem.setFont(0, QFont("Consolas"))
        basetypeitem.setFont(1, QFont("Consolas"))
        basetypeitem.setIcon(0, QIcon("Icon/basetype.png"))

    def add_datatype_implementation_folder(self):
        self.datatypes_implementation_folder = QTreeWidgetItem(self.datatypes_folder, ["Implementation Data Types"])
        icon = QIcon("Icon/bastypes.png")
        self.datatypes_implementation_folder.setIcon(0, icon)

    def add_impletype_item(self, name):
        if self.datatypes_implementation_folder is None:
            self.add_datatype_implementation_folder()
        impletype_item = QTreeWidgetItem(self.datatypes_implementation_folder, name)
        impletype_item.setFont(0, QFont("Consolas"))
        impletype_item.setFont(1, QFont("Consolas"))
        impletype_item.setIcon(0, QIcon("Icon/basetype.png"))


    def add_Infrastruture_compumethod_folder(self):
        self.Infrastruture_compumethod_folder = QTreeWidgetItem(self.Infrastructures_folder, ["Compu Method"])
        icon = QIcon("Icon/CompuMethod.png")
        self.Infrastruture_compumethod_folder.setIcon(0, icon)

    def add_compumethod_item(self, name):
        if self.Infrastruture_compumethod_folder is None:
            self.add_Infrastruture_compumethod_folder()
        compumethod_item = QTreeWidgetItem(self.Infrastruture_compumethod_folder, name)
        compumethod_item.setFont(0, QFont("Consolas"))
        compumethod_item.setFont(1, QFont("Consolas"))
        compumethod_item.setIcon(0, QIcon("Icon/CompuMethod.png"))

    def add_Infrastruture_dataconstraint_folder(self):
        self.Infrastruture_dataconstraint_folder = QTreeWidgetItem(self.Infrastructures_folder, ["Data Constraint"])
        icon = QIcon("Icon/dataconstraint.png")
        self.Infrastruture_dataconstraint_folder.setIcon(0, icon)

    def add_dataconstraint_item(self, name):
        if self.Infrastruture_dataconstraint_folder is None:
            self.add_Infrastruture_dataconstraint_folder()
        dataconstraint_item = QTreeWidgetItem(self.Infrastruture_dataconstraint_folder, name)
        dataconstraint_item.setFont(0, QFont("Consolas"))
        dataconstraint_item.setFont(1, QFont("Consolas"))
        dataconstraint_item.setIcon(0, QIcon("Icon/dataconstraint.png"))

    def add_Interfaces_folder(self):
        Interfaces = QTreeWidgetItem(self.root_item, ["Interfaces"])
        icon = QIcon("Icon/Interfaces.png")
        Interfaces.setIcon(0, icon)

    def add_Components_folder(self):
        Components = QTreeWidgetItem(self.root_item, ["Components"])
        icon = QIcon("Icon/swc.png")
        Components.setIcon(0, icon)

    def add_Compositions_folder(self):
        Compositions = QTreeWidgetItem(self.root_item, ["Compositions"])
        icon = QIcon("Icon/composition.png")
        Compositions.setIcon(0, icon)

    def add_Infrastruture_folder(self):
        self.Infrastructures_folder = QTreeWidgetItem(self.root_item, ["Infrastructures"])
        icon = QIcon("Icon/Infrastructures.png")
        self.Infrastructures_folder.setIcon(0, icon)

class AutosarData:
    def __init__(self, workspace, view):

        self.arxml_files = []
        self.arxml_files = self.find_files_recursive(workspace, "arxml")
        ws = autosar.workspace()
        for arxml in self.arxml_files:
            ws.loadXML(arxml)
        for pack in ws.listPackages():
            for pack1 in ws.findall(pack):
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
                    print(ele.ref, ele.name, ele.parent, ele.category, ele.arraySize, ele.compuMethodRef, ele.baseTypeRef, ele.implementationTypeRef)
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
                    # print(ele.ref)
                    pass
                if isinstance(ele, autosar.portinterface.SenderReceiverInterface):
                    # print(ele.ref)
                    pass
                if isinstance(ele, autosar.portinterface.ClientServerInterface):
                    # print(ele.ref)
                    pass
                if isinstance(ele, autosar.component.ApplicationSoftwareComponent):
                    # print(ele.ref)
                    pass
                if isinstance(ele, autosar.component.CompositionComponent):
                    # print(ele.ref)
                    pass

    def find_files_recursive(self, folder_path, file_extension):
        pattern = os.path.join(folder_path, f"**/*.{file_extension}")
        file_list = glob.glob(pattern, recursive=True)
        return file_list


