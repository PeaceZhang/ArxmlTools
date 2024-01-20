# ArxmlTools
Autosar application arhitecture design toolset
it has CLI mode and GUI mode,

## CLI Mode
### step1: open asw architecture items database, Import/Application.xlsx

### step2: fill in autosar items

![image](https://github.com/PeaceZhang/ArxmlTools/assets/31465472/f5b30e7a-50d6-426f-aa98-12a5b12243a4)

now this database support datatypes, interfaces, components
1. datatypes: basetype, alias type, enumeration, structure
2. portinterfaces: R/S Interfaces, C/S Interfaces
3. components: atomic components, conposition composition, assembly connections, daligation connections

### step3: run scripts
```bash
python ArxmlToolsConvert.py
```
### step4: then you can check the generated arxml files: Export/Application.arxml
![image](https://github.com/PeaceZhang/ArxmlTools/assets/31465472/c2714a35-9271-4303-adf9-dc7d0626737e)



## GUI Mode
not completed yet， bellow is pre view:
![image](https://github.com/PeaceZhang/ArxmlTools/assets/31465472/e9a90a23-8521-4a92-a29c-4139a9ec0a58)
