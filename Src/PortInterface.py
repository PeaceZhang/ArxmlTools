from Src.SystemImport import SystemImport
from Src.DataType import DataTypes
import autosar

class PortInterfaces:
    def __init__(self, System, ws):
        portinterfacepackage = ws.createPackage('PortInterfaces', role='PortInterface')
        for sif in System.interfaceslist:
            implementationtypes = ws.findRolePackage('DataType').find('ImplementationTypes')
            portinterfacepackage.createSenderReceiverInterface(
            sif['name'],
                [autosar.element.DataElement(sif['elements'][x], implementationtypes.find(sif['element type'][x]).ref) for x in range(0, len(sif['elements']))]
            )

        for csif in System.csinterfaceslist:
            applicationerrtup = self.calapplicationerror(System.enumaetypelist, csif['application error'])
            csportinterface = portinterfacepackage.createClientServerInterface(csif['name'],
                                                                               [x['operation name'] for x in csif['operations']],
                                                                               errors=applicationerrtup[0],
                                                                               isService=False
                                                                               )
            for op in csif['operations']:
                csportinterface[op['operation name']].possibleErrors = applicationerrtup[1]
                if [] != op['arguments']:
                    for arg in op['arguments']:
                        if 'IN' == arg['direction']:
                            csportinterface[op['operation name']].createInArgument(arg['argument name'], implementationtypes.find(arg['argstype']).ref, "NOT-ACCESSIBLE", "USE-ARGUMENT-TYPE")
                        if 'OUT' == arg['direction']:
                            csportinterface[op['operation name']].createOutArgument(arg['argument name'], implementationtypes.find(arg['argstype']).ref, "NOT-ACCESSIBLE", "USE-ARGUMENT-TYPE")
                        if 'INOUT' == arg['direction']:
                            csportinterface[op['operation name']].createInOutArgument(arg['argument name'], implementationtypes.find(arg['argstype']).ref, "NOT-ACCESSIBLE", "USE-ARGUMENT-TYPE")
    def calapplicationerror(self, aelist, apperror):
        for ae in aelist:
            if apperror == ae['name']:
                return ([autosar.ApplicationError(ae['value table'][x], ae['value'][x]) for x in range(0, len(ae['value table']))], ae['value table'])

if __name__ == '__main__':
    System = SystemImport('../Import/Application.xlsx')
    ws = autosar.workspace('4.2.2')
    DataTypes(System, ws)
    PortInterfaces(System, ws)
    ws.saveXML('../Export/Application.arxml')