# -*- coding: utf-8 -*-
__author__ = 'KV'
from schema import  *
def open_file(File_Name):
    file= open(File_Name,"r");
    Config_Dict={};
    #считываем общюю кофигурацию устройства
    Config_Dict['name']=file.readline().replace("\n","").strip();
    Config_Dict['desc']=file.readline().replace("\n","").strip();
    Config_Dict['type']=file.readline().replace("\n","").strip();
    Config_Dict['manufacturer']=file.readline().replace("\n","").strip();
    Config_Dict['config_version']=file.readline().replace("\n","").strip();
    #считываем сервисы, должны быть из списка:
    # DynAssociation; SettingGroups: SGEdit,ConfSG; GetDirectory; GetDataObjectDefinition;
    #DataObjectDirectory; GetDataSetValue; SetDataSetValue; DataSetDirectory; ConfDataSet;
    #DynDataSet; ReadWrite; TimerActivatedControl; ConfReportControl; GetCBValues;ConfLogControl
    #ReportSettings; LogSettings; GSESettings; SMVSettings; ConfLNs; GSEDir; GOOSE; GSSE; FileHandling
    tmp = [];
    check_list=['DynAssociation', 'SGEdit' ,'ConfSG', 'GetDirectory', 'GetDataObjectDefinition',
                'DataObjectDirectory', 'GetDataSetValue', 'SetDataSetValue', 'DataSetDirectory', 'ConfDataSet',
                'DynDataSet', 'ReadWrite', 'TimerActivatedControl', 'ConfReportControl', 'GetCBValues', 'ConfLogControl',
                'ReportSettings', 'LogSettings', 'GSESettings', 'SMVSettings', 'ConfLNs', 'GSEDir', 'GOOSE', 'GSSE', 'FileHandling' ];

    tmp = file.readline().replace("\n","").strip().split(" ");
    for i in tmp:
        if (i in check_list)==False:
                print("Wrong service name");
                exit(-1);
    Config_Dict['services']=tmp;
    tmp=file.readline().replace("\n","").strip().split(" ");
    Config_Dict['AccessPoint']=tmp;
    tmp = file.readline().replace("\n","").strip().split(" ");
    Config_Dict['AccessPoint_deck']=tmp;
    tmp = file.readline().replace("\n","").strip().split(" ");
    Config_Dict['router']=tmp;
    tmp = file.readline().replace("\n","").strip().split(" ");
    Config_Dict['clock']=tmp;


    return  Config_Dict;

def print_closed(Attr,Value):
    return("<"+Attr+">"+Value+"</"+Attr+">"+"\n");

def make_xml(Dict):
    xml= open("Conf.xml","w");
    xml.write("""<?xml version="1.0" encoding="UTF-8"?>
    <SCL xmlns="http://www.iec.ch/61850/2003/SCL"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="SCL_IED.xsd">""");
    xml.write("""<Header id="ICD File" version="0" revision="1" toolID="1" nameStructure="IEDName" />""")
    xml.write("<lED>\n");
    xml.write(print_closed("name",Dict['name']));
    xml.write(print_closed("desk",Dict['desc']));
    for i in Dict['services']:
        xml.write(print_closed("Service",i));
    #обработка точек доступа
    for i in range(0, len(Dict['AccessPoint'])):
        xml.write("<AccessPoint>");
        xml.write(print_closed("name",Dict['AccessPoint'][i]));
        xml.write(print_closed("deck",Dict['AccessPoint_deck'][i]));
        xml.write(print_closed("router",Dict['router'][i]));
        xml.write((print_closed("clock",Dict['clock'][i])))
        
        xml.write("</AccessPoint>");
    xml.write(print_closed("type",Dict['type']));
    xml.write(print_closed("manufacturer",Dict['manufacturer']));
    xml.write(print_closed("configversion",Dict['config_version']));
    xml.write("</lED>\n");
    xml.write("""</SCL>""");
    xml.close();

if __name__ == "__main__":
    print("Starting Config");
    Dict = open_file("anna.conf");
    make_schema();
    make_xml(Dict);
    print("Config Finished");

