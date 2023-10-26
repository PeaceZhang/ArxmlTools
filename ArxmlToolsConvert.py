from SRC/SystemImport import SystemImport
from PortInterface import PortInterfaces
from DataType import DataTypes
from Component import Components
import autosar

if __name__ == '__main__':
    System = SystemImport('Application.xlsx')
    ws = autosar.workspace('4.2.2')
    DataTypes(System, ws)
    PortInterfaces(System.interfaceslist, ws)
    Components(System.swcomponentlist, ws)
    ws.saveXML('Validation/Datatypes.arxml')