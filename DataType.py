from SystemImport import SystemImport
import autosar

class DataTypes:
    def __init__(self, systemimport, ws):
        # ws = autosar.workspace('4.2.2')
        datatypes_package = ws.createPackage('DataTypes', role='DataType')
        datatypes_package.createSubPackage('BaseTypes')
        datatypes_package.createSubPackage('ImplementationTypes')
        datatypes_package.createSubPackage('CompuMethods', role='CompuMethod')
        datatypes_package.createSubPackage('DataConstrs', role='DataConstraint')

        self.definebasetype(systemimport, datatypes_package)
        self.defineenumtype(systemimport, datatypes_package)
        self.definestructtype(systemimport, datatypes_package)
        # ws.saveXML('Validation/Datatypes.arxml')

    def definebasetype(self, systemimport, package):
        basetypes = package.find('BaseTypes')
        implementationtypes = package.find('ImplementationTypes')
        for bt in systemimport.basetypelist:
            definedbasetypes = basetypes.createSwBaseType(bt['name'], size=bt['bit size'], nativeDeclaration=bt['native declaration'])
            implementationtypes.createImplementationDataType(bt['name'], definedbasetypes.ref)

    def defineenumtype(self, systemimport, package):
        for et in systemimport.enumtypelist:
            vt = list(map(lambda x, y: (x, y), et['value'], et['value table']))
            implementationtypes = package.find('ImplementationTypes')
            implementationtypes.createImplementationDataTypeRef(
                et['name'],
                implementationtypes.find('Uint8').ref,
                valueTable=vt
            )

    def definestructtype(self, systemimport, package):
        #print(systemimport.structtypelist)
        implementationtypes = package.find('ImplementationTypes')
        for st in systemimport.structtypelist:
            eletyperef = [implementationtypes.find(x).ref for x in st['element type']]
            elements = list(map(lambda x, y: (x, y), st['elements'], eletyperef))
            implementationtypes.createImplementationRecordDataType(st['name'], elements)

if __name__ == '__main__':
    System = SystemImport('Application.xlsx')
    ws = autosar.workspace('4.2.2')
    DataTypes(System, ws)