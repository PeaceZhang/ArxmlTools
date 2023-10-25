from SystemImport import SystemImport
from PortInterface import PortInterfaces
from DataType import DataTypes
import autosar

class Components:
    def __init__(self, syscomponents, ws):
        swcomponentpackage = ws.createPackage('ComponentTypes', role='ComponentType')
        self.childcomponent = {}
        self.childcomposition = {}
        self.fathercomposition = None
        for swc in syscomponents:
            # print(swc)
            if 'APP-SWC' == swc['componenttype']:
                swc1 = swcomponentpackage.createApplicationSoftwareComponent(swc['swc name'])
                self.childcomponent[swc['swc name']] = swc1
            if 'APP-COMP' == swc['componenttype']:
                swc1 = swcomponentpackage.createCompositionComponent(swc['swc name'])
                self.childcomposition[swc['swc name']] = swc1
            if 'DELEGATION' == swc['componenttype']:
                swc1 = swcomponentpackage.createCompositionComponent(swc['swc name'])
                self.fathercomposition = swc1
            for ele in swc['elements']:
                if 'Port' == ele['attributes']:
                    if 'Provider' == ele['direction']:
                        swc1.createProvidePort(ele['portname'], ws.findRolePackage('PortInterface').find(ele['interfaces']).ref)
                    if 'Receiver' == ele['direction']:
                        swc1.createRequirePort(ele['portname'], ws.findRolePackage('PortInterface').find(ele['interfaces']).ref)

        for x in self.childcomponent.values():
            self.fathercomposition.createComponentPrototype(x.ref)
        for y in self.childcomposition.values():
            self.fathercomposition.createComponentPrototype(y.ref)

        for swc in syscomponents:
            # print(swc)
            for ele in swc['elements']:
                if None != ele['receiver swc']:
                    for rsl in ele['receiver swc']:
                        if rsl in self.childcomponent:
                            port = self.childcomponent[rsl].createRequirePort(ele['portname'], ws.findRolePackage('PortInterface').find(ele['interfaces']).ref)
                            if 'DELEGATION' == swc['componenttype']:
                                self.fathercomposition.createConnector(ele['portname'], port.ref)
                            else:
                                self.fathercomposition.createConnector(swcomponentpackage.ref + '/' + swc['swc name'] + '/' + ele['portname'], port.ref)
                        if rsl in self.childcomposition:
                            port = self.childcomposition[rsl].createRequirePort(ele['portname'],ws.findRolePackage('PortInterface').find(ele['interfaces']).ref)
                            if 'DELEGATION' == swc['componenttype']:
                                self.fathercomposition.createConnector(ele['portname'], port.ref)
                            else:
                                self.fathercomposition.createConnector(swcomponentpackage.ref + '/' + swc['swc name'] + '/' + ele['portname'], port.ref)
                        if 'Delegation' == rsl:
                            port = self.fathercomposition.createProvidePort(ele['portname'], ws.findRolePackage('PortInterface').find(ele['interfaces']).ref)
                            self.fathercomposition.createConnector(swcomponentpackage.ref + '/' + swc['swc name'] + '/' + ele['portname'], ele['portname'])
        # self.fathercomposition.autoConnect()
        # self.fathercomposition.createConnector("/ComponentTypes/SWC2/P_VehicleConditions", "/ComponentTypes/SWC1/P_VehicleConditions")
        # self.fathercomposition.createConnector("R_VehicleMode",
        #                                        "/ComponentTypes/SWC1/R_VehicleMode")

if __name__ == '__main__':
    System = SystemImport('Application.xlsx')
    ws = autosar.workspace('4.2.2')
    DataTypes(System, ws)
    PortInterfaces(System.interfaceslist, ws)
    Components(System.swcomponentlist, ws)
    ws.saveXML('Validation/Datatypes.arxml')