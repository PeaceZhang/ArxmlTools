from SystemImport import SystemImport
from PortInterface import PortInterfaces
from DataType import DataTypes
import autosar
import re

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
                    for rswc in ele['receiver swc']:
                        if rswc in self.childcomponent:
                            port = self.childcomponent[rswc].createRequirePort(ele['portname'].replace('P_','R_'), ws.findRolePackage('PortInterface').find(ele['interfaces']).ref)
                            if 'DELEGATION' == swc['componenttype']:
                                self.fathercomposition.createConnector(ele['portname'], port.ref)
                            else:
                                self.fathercomposition.createConnector(swcomponentpackage.ref + '/' + swc['swc name'] + '/' + ele['portname'], port.ref)
                        if rswc in self.childcomposition:
                            port = self.childcomposition[rswc].createRequirePort(ele['portname'].replace('P_','R_') ,ws.findRolePackage('PortInterface').find(ele['interfaces']).ref)
                            if 'DELEGATION' == swc['componenttype']:
                                self.fathercomposition.createConnector(ele['portname'], port.ref)
                            else:
                                self.fathercomposition.createConnector(swcomponentpackage.ref + '/' + swc['swc name'] + '/' + ele['portname'], port.ref)
                        if 'Delegation' == rswc:
                            port = self.fathercomposition.createProvidePort(ele['portname'], ws.findRolePackage('PortInterface').find(ele['interfaces']).ref)
                            self.fathercomposition.createConnector(swcomponentpackage.ref + '/' + swc['swc name'] + '/' + ele['portname'], ele['portname'])

        for swc in syscomponents:
            for ele in swc['elements']:
                if 'Task' == ele['attributes']:
                    if 'INIT' == ele['schedule']:
                        if 'Yes' == ele['defaultportaccess']:
                            pass
                        else:
                            self.childcomponent[swc['swc name']].behavior.createRunnable(swc['swc name'] + '_' + ele['portname'])
                            self.childcomponent[swc['swc name']].behavior.createInitEvent(swc['swc name'] + '_' + ele['portname'])
                    else:
                        if 'Yes' == ele['defaultportaccess']:
                            print(ele['schedule'])
                            print(int(re.findall(r'\d+', ele['schedule'])[0]))
                            self.childcomponent[swc['swc name']].behavior.createRunnable(swc['swc name'] + '_' + ele['portname'])
                            self.childcomponent[swc['swc name']].behavior.createTimerEvent(swc['swc name'] + '_' + ele['portname'], int(re.findall(r'\d+', ele['schedule'])[0]))

        # print(self.fathercomposition.requirePorts[0].name)
        # print(self.fathercomposition.providePorts[0].name)

if __name__ == '__main__':
    System = SystemImport('Application.xlsx')
    ws = autosar.workspace('4.2.2')
    DataTypes(System, ws)
    PortInterfaces(System.interfaceslist, ws)
    Components(System.swcomponentlist, ws)
    ws.saveXML('Validation/Datatypes.arxml')