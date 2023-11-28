from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem
from PySide6.QtGui import QIcon
import autosar
import glob
import os

class ModelExplorer(QTreeWidget):
    def __init__(self, path):
        super().__init__()

        self.setHeaderLabels(["Ar Model", "Ar path"])
        self.setColumnWidth(0, 200)
        # 添加根节点
        self.root_item = QTreeWidgetItem(self, ["AUTOSAR"])
        icon = QIcon("Icon/autosar.jpg")
        self.root_item.setIcon(0, icon)
        AutosarData(path)
        # self.add_datatype_folder()
        # self.add_compumethod_folder()
        # self.add_Interfaces_folder()
        # self.add_Components_folder()
        # self.add_Compositions_folder()
        # self.add_Infrastruture_folder()

    def add_datatype_folder(self):
        # 添加data type子目录
        DataTypes = QTreeWidgetItem(self.root_item, ["Data Types"])
        icon = QIcon("Icon/DataTypes.png")
        DataTypes.setIcon(0, icon)

    def add_compumethod_folder(self):
        CompuMethod = QTreeWidgetItem(self.root_item, ["Compu Method"])
        icon = QIcon("Icon/CompuMethod.png")
        CompuMethod.setIcon(0, icon)

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
        Infrastructures = QTreeWidgetItem(self.root_item, ["Infrastructures"])
        icon = QIcon("Icon/Infrastructures.png")
        Infrastructures.setIcon(0, icon)

        # grandson_item = QTreeWidgetItem(DataTypes, ["grandson1", "grandson1 data"])

    def add_bastype(self):
        pass


class AutosarData:
    def __init__(self, workspace):

        self.arxml_files = []
        self.arxml_files = self.find_files_recursive(workspace, "arxml")
        ws = autosar.workspace()
        for arxml in self.arxml_files:
            ws.loadXML(arxml)
        for pack in ws.listPackages():
            for pack1 in ws.findall(pack):
                self.package_parser(pack1)

    def package_parser(self, package):
        # print("package ref: ", package.ref)
        # print("package name: ", package.name)
        # print("package elements: ", package.elements)
        if package.subPackages:
            for son in package.subPackages:
                self.package_parser(son)
        if package.elements:
            for ele in package.elements:
                if isinstance(ele, autosar.datatype.SwBaseType):
                    print(ele.ref, ele.name, ele.parent, ele.nativeDeclaration, ele.size, ele.typeEncoding, ele.category)

                    pass
                if isinstance(ele, autosar.datatype.ImplementationDataType):
                    # print(ele.ref)
                    pass
                if isinstance(ele, autosar.datatype.CompuMethod):
                    # print(ele.ref)
                    pass
                if isinstance(ele, autosar.datatype.DataConstraint):
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

if __name__ == "__main__":
    AutosarData('D:\AutosarTutorial\ArxmlTools\Export')
