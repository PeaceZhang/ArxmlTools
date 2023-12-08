from PySide6.QtWidgets import QApplication, QWidget, QDialog, QVBoxLayout, QLineEdit, QComboBox, QFormLayout, QLabel, \
    QFrame, QGroupBox, QHBoxLayout, QDialogButtonBox, QMessageBox
import autosar, re


class BaseTypeWidget(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        self.baseTypeEnCoding_dict = {
            "1C": "1C: One's Complement",
            "2C": "2C: Two's Complement",
            "BCD-P": "BCD-P: Packed Binary Coded Decimals",
            "BCD-UP": "BCD-UP: Unpacked Binary Coded Decimal",
            "DSP-FRACTIONAL": "DSP-FRACTIONAL: Digtal Signal Process",
            "SM": "SM: Sign Magnitude",
            "IEEE754": "IEEE754: Floating Point",
            "ISO-8859-1": "ISO-8859-1: ASCII-Strings",
            "ISO-8859-2": "ISO-8859-2: ASCII-Strings",
            "WINDOWS-1252": "Windows-1252: ASCII Strings",
            "UTF-8": "UTF-8: UCS Transformation Format8",
            "UCS-2": "UCS-2: Universal Character Set 2",
            "NONE": "NONE: Unsigned Integer",
            "VOID": "VOID: C Language",
            "BOOLEAN": "BOOLEAN: Logical Type",
            "UTF-16": "UTF-16: Character encoding for Unicode code points"
        }
        self.baseTypeEnCoding_bdDict = {v: k for k, v in self.baseTypeEnCoding_dict.items()}

        self.BaseTypeEncoding_LineEdit = QComboBox()
        for key in self.baseTypeEnCoding_bdDict:
            self.BaseTypeEncoding_LineEdit.addItem(key)

        default_text = "NONE: Unsigned Integer"
        self.BaseTypeEncoding_LineEdit.setCurrentText(default_text)

        self.BaseTypeSize_LineEdit = QLineEdit()
        self.BaseTypeNativeDeclaration_LineEdit = QLineEdit()

        layout_base_type_definition = QFormLayout()
        layout_base_type_definition.addRow(QLabel("BaseTypeSize"), self.BaseTypeSize_LineEdit)
        layout_base_type_definition.addRow(QLabel("BaseTypeEncoding"), self.BaseTypeEncoding_LineEdit)
        layout_base_type_definition.addRow(QLabel("NativeDeclaration"), self.BaseTypeNativeDeclaration_LineEdit)

        line = QFrame(self)
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setFixedHeight(30)

        group_box = QGroupBox(self)
        group_box.setTitle("BaseTypeDefinition")
        group_box.resize(100, 50)
        group_box.setLayout(layout_base_type_definition)

        name_layout = QHBoxLayout(self)
        name_header = QLabel("Name:")
        self.name_LineEdit = QLineEdit(self)
        name_layout.addWidget(name_header)
        name_layout.addWidget(self.name_LineEdit)

        layout.addLayout(name_layout)
        layout.addWidget(line)
        layout.addWidget(group_box)

class BaseTypeModel(BaseTypeWidget):
    def __init__(self):
        super().__init__()
        self.editbasetypemodel: autosar.datatype.SwBaseType
    def read_base_type_view(self, basetypemodel):
        if isinstance(basetypemodel, autosar.datatype.SwBaseType):
            self.editbasetypemodel = basetypemodel
            self.name_LineEdit.setText(basetypemodel.name)
            self.BaseTypeSize_LineEdit.setText(str(basetypemodel.size))
            self.BaseTypeNativeDeclaration_LineEdit.setText(basetypemodel.nativeDeclaration)
            self.BaseTypeEncoding_LineEdit.setCurrentText(self.baseTypeEnCoding_dict.get(basetypemodel.typeEncoding))
        else:
            pass

    def set_base_type_model(self):
        if isinstance(self.editbasetypemodel, autosar.datatype.SwBaseType):
            self.editbasetypemodel.name = self.name_LineEdit.text()
            self.editbasetypemodel.size = int(self.BaseTypeSize_LineEdit.text())
            self.editbasetypemodel.typeEncoding = self.baseTypeEnCoding_bdDict.get(self.BaseTypeEncoding_LineEdit.currentText())
            self.editbasetypemodel.nativeDeclaration = self.BaseTypeNativeDeclaration_LineEdit.text()
        else:
            pass

    def save_new_base_type(self, package):
        if isinstance(package, autosar.package.Package):
            name = self.name_LineEdit.text()
            size = self.BaseTypeSize_LineEdit.text()
            typeEncoding = self.baseTypeEnCoding_bdDict.get(self.BaseTypeEncoding_LineEdit.currentText())
            nativeDeclaration = self.BaseTypeNativeDeclaration_LineEdit.text()
            self.newbasetypeitem = package.createSwBaseType(name, size=size, nativeDeclaration=nativeDeclaration, encoding=typeEncoding)
        pass

class BaseTypeDialog(QDialog):
    def __init__(self, isNewBasetype=False, packageofnewbastype=None, existitem=None):
        super().__init__()

        self.isCurrentNew = isNewBasetype

        if isNewBasetype is True:
            self.setWindowTitle("New Base Type")
            if isinstance(packageofnewbastype, autosar.package.Package):
                self.newbasetypepackage = packageofnewbastype
        else:
            if isinstance(existitem, autosar.datatype.SwBaseType):
                self.setWindowTitle(f"Base Type: '{ existitem.name }'")
                self.exitem = existitem

        self.BaseType = BaseTypeModel()

        layout = QVBoxLayout(self)
        layout.addWidget(self.BaseType)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel | QDialogButtonBox.Apply)
        buttons.accepted.connect(self.usraccept)
        buttons.rejected.connect(self.reject)
        buttons.button(QDialogButtonBox.Apply).clicked.connect(self.applyChanges)
        layout.addWidget(buttons)

    def usraccept(self):
        result = self.checkparameters()
        if "OK" == result:
            # self.BaseType.set_base_type_model()
            if self.isCurrentNew is True:
                self.BaseType.save_new_base_type(self.newbasetypepackage)
                self.isCurrentNew = False
            else:
                self.BaseType.set_base_type_model()
            self.accept()
        else:
            QMessageBox.information(self, result[0], result[1])

    def applyChanges(self):
        result = self.checkparameters()
        if "OK" == result:
            # self.BaseType.set_base_type_model()
            if self.isCurrentNew is True:
                self.BaseType.save_new_base_type(self.newbasetypepackage)
                self.isCurrentNew = False
                self.BaseType.editbasetypemodel = self.BaseType.newbasetypeitem
                self.setWindowTitle(f"Base Type: '{self.BaseType.newbasetypeitem.name}'")
            else:
                self.BaseType.set_base_type_model()
        else:
            QMessageBox.information(self, result[0], result[1])

    def checkparameters(self):
        isNameValid = self.checkname(self.BaseType.name_LineEdit.text())
        isSizeValid = self.checksize(self.BaseType.BaseTypeSize_LineEdit.text())
        isNativeDecValid = self.checknativedeclaration(self.BaseType.BaseTypeNativeDeclaration_LineEdit.text())
        if isNameValid is False:
            return ["Error Name", f"User input '{self.BaseType.name_LineEdit.text()}' is invalid"]
        elif isSizeValid is False:
            return ["Error Size", f"User input '{self.BaseType.BaseTypeSize_LineEdit.text()}' is invalid"]
        elif isNativeDecValid is False:
            return ["Error NativeDeclaration", f"User input '{self.BaseType.BaseTypeNativeDeclaration_LineEdit.text()}' is invalid"]
        else:
            return "OK"

    def checkname(self, text):
        pattern = r'^[a-zA-Z_][a-zA-Z0-9_]*$'
        return re.match(pattern, text) is not None

    def checksize(self, text):
        pattern = r'^[1-9]\d*$'
        return re.match(pattern, text) is not None

    def checknativedeclaration(self, text):
        pattern = r'^[a-zA-Z_][a-zA-Z0-9_ ]*$'
        return re.match(pattern, text) is not None


def modify():
    ws = autosar.workspace()
    ws.loadXML("../../Export/Application.arxml")

    basetype_uint8 = ws.find('/DataTypes/BaseTypes/Uint8')

    test_app = QApplication([])
    widget = BaseTypeDialog(existitem=basetype_uint8)
    widget.setGeometry(200, 200, 400, 500)
    widget.BaseType.read_base_type_view(basetype_uint8)
    widget.exec()
    ws.saveXML("../../Export/ars.arxml")

def New():
    ws = autosar.workspace()
    ws.loadXML("../../Export/Application.arxml")

    basetype_package = ws.find('/DataTypes/BaseTypes')
    print(basetype_package)

    test_app = QApplication([])
    widget = BaseTypeDialog(isNewBasetype=True, packageofnewbastype=basetype_package)
    widget.setGeometry(200, 200, 400, 500)
    # widget.BaseType.save_new_base_type_(basetype_package)
    widget.exec()
    ws.saveXML("../../Export/ars.arxml")

if __name__ == '__main__':
    New()

