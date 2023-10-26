from Src.SystemImport import SystemImport
from Src.DataType import DataTypes
from Src.PortInterface import PortInterfaces
from Src.Component import Components
import autosar

if __name__ == '__main__':
    System = SystemImport('Import/Application.xlsx')
    ws = autosar.workspace('4.2.2')
    DataTypes(System, ws)
    PortInterfaces(System.interfaceslist, ws)
    Components(System.swcomponentlist, ws)
    ws.saveXML('Export/Application.arxml')