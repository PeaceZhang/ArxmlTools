import copy

from openpyxl import load_workbook

class SystemImport:
    def __init__(self, excelFiles):
        wb = load_workbook(excelFiles, read_only=True, data_only=True)
        print(wb.sheetnames)
        datatypes_sheet = wb['DataTypes']
        self.basetypelist = []
        self.enumtypelist = []
        self.structtypelist = []
        basetype = {}
        enumtype = {}
        structtype = {}
        for row in datatypes_sheet:
            if "Base Types" == row[2].value:
                basetype['name'] = row[1].value
                basetype['native declaration'] = row[3].value
                self.basetypelist.append(basetype)
                basetype = {}
            if "Enum" == row[2].value:
                enumtype = \
                    {
                        'name':  row[1].value,
                        'value table': [],
                        'value': []
                    }
                # self.enumtypelist.append(enumtype)
            if {} != enumtype:
                if row[3].value is not None:
                    enumtype['value table'].append(row[3].value)
                    enumtype['value'].append(row[4].value)
                else:
                    self.enumtypelist.append(enumtype)
                    enumtype = {}
            if "Struct" == row[2].value:
                structtype = \
                    {
                        'name': row[1].value,
                        'elements': [],
                        'element type': []
                    }
            if {} != structtype:
                if row[3].value is not None:
                    structtype['elements'].append(row[3].value)
                    structtype['element type'].append(row[4].value)
                else:
                    self.structtypelist.append(structtype)
                    structtype = {}

        print(self.basetypelist)
        print(self.enumtypelist)
        print(self.structtypelist)

if __name__ == '__main__':
    SystemImport('Application.xlsx')
