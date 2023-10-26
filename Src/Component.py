from Src.SystemImport import SystemImport
from Src.PortInterface import PortInterfaces
from Src.DataType import DataTypes
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
            portinterfaces = ws.findRolePackage('PortInterface')
            for ele in swc['elements']:
                if 'Task' == ele['attributes']:
                    if 'INIT' == ele['schedule']:
                        if 'Yes' == ele['defaultportaccess']:
                            portAccessList = self.findportaccesstable(swc['swc name'], portinterfaces)
                            self.childcomponent[swc['swc name']].behavior.createRunnable(swc['swc name'] + '_' + ele['portname'], portAccess=portAccessList)
                            self.childcomponent[swc['swc name']].behavior.createInitEvent(swc['swc name'] + '_' + ele['portname'])
                        else:
                            self.childcomponent[swc['swc name']].behavior.createRunnable(swc['swc name'] + '_' + ele['portname'])
                            self.childcomponent[swc['swc name']].behavior.createInitEvent(swc['swc name'] + '_' + ele['portname'])
                    else:
                        if 'Yes' == ele['defaultportaccess']:
                            portAccessList = self.findportaccesstable(swc['swc name'], portinterfaces)
                            self.childcomponent[swc['swc name']].behavior.createRunnable(swc['swc name'] + '_' + ele['portname'], portAccess=portAccessList)
                            self.childcomponent[swc['swc name']].behavior.createTimerEvent(swc['swc name'] + '_' + ele['portname'], int(re.findall(r'\d+', ele['schedule'])[0]))
                        else:
                            self.childcomponent[swc['swc name']].behavior.createRunnable(swc['swc name'] + '_' + ele['portname'])
                            self.childcomponent[swc['swc name']].behavior.createTimerEvent(swc['swc name'] + '_' + ele['portname'], int(re.findall(r'\d+', ele['schedule'])[0]))
    def findportaccesstable(self, swcname, pipackage):
        portAccessList = []
        swcports = self.childcomponent[swcname].requirePorts + self.childcomponent[swcname].providePorts
        for port in swcports:
            portelements = [x.name for x in pipackage.find(port.portInterfaceRef).dataElements]
            for ele in portelements:
                portAccessList.append(port.name + "/" + ele)
        return portAccessList

if __name__ == '__main__':
    System = SystemImport('../Import/Application.xlsx')
    ws = autosar.workspace('4.2.2')
    DataTypes(System, ws)
    PortInterfaces(System.interfaceslist, ws)
    Components(System.swcomponentlist, ws)
    ws.saveXML('../Export/Application.arxml')