from SystemImport import SystemImport
from DataType import DataTypes
import autosar

class PortInterfaces:
    def __init__(self, sysportinterfaces, ws):
        portinterfacepackage = ws.createPackage('PortInterfaces', role='PortInterface')
        for sif in sysportinterfaces:
            implementationtypes = ws.findRolePackage('DataType').find('ImplementationTypes')
            portinterfacepackage.createSenderReceiverInterface(
            sif['name'],
                [autosar.element.DataElement(sif['elements'][x], implementationtypes.find(sif['element type'][x]).ref) for x in range(0, len(sif['elements']))]
            )

if __name__ == '__main__':
    System = SystemImport('Application.xlsx')
    ws = autosar.workspace('4.2.2')
    DataTypes(System, ws)
    PortInterfaces(System.interfaceslist, ws)
    ws.saveXML('Validation/Datatypes.arxml')