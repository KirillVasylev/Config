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
        if i not in check_list:
                print("Wrong service name");
                exit(-1);
    Config_Dict['services']=tmp;
    Config_Dict['AccessPoint']=file.readline().replace("\n","").strip().split(" ");
    Config_Dict['AccessPoint_deck']=file.readline().replace("\n","").strip().split(" ");
    Config_Dict['router']=file.readline().replace("\n","").strip().split(" ");
    Config_Dict['clock']=file.readline().replace("\n","").strip().split(" ");
    #считываем настройки сервера по одному для каждой точки доступа.
    Config_Dict['timeout']=file.readline().replace("\n","").strip().split(" ");
    Config_Dict['authentication_none']=file.readline().replace("\n","").strip().split(" ");
    Config_Dict['password']=file.readline().replace("\n","").strip().split(" ");
    Config_Dict['authentication_weak']=file.readline().replace("\n","").strip().split(" ");
    Config_Dict['authentication_strong']=file.readline().replace("\n","").strip().split(" ");
    Config_Dict['certificate']=file.readline().replace("\n","").strip().split(" ");
    if len(Config_Dict['AccessPoint']) != len(Config_Dict['timeout']):
        print("Wrong server config, wrong timeout count");
    if len(Config_Dict['AccessPoint']) != len(Config_Dict['authentication_none']):
        print("Wrong server config, wrong authentication_none count");
    if len(Config_Dict['AccessPoint']) != len(Config_Dict['password']):
        print("Wrong server config, wrong password count");
    if len(Config_Dict['AccessPoint']) != len(Config_Dict['authentication_strong']):
        print("Wrong server config, wring Authentication_strong count");
    if len(Config_Dict['AccessPoint']) != len(Config_Dict['authentication_weak']):
        print("Wrong server config, wrong Authentication_weak count");
    if len(Config_Dict['AccessPoint']) != len(Config_Dict['certificate']):
        print("Wrong server config, wrong certificate count")

     # считываем конфигурацию логических устройскв
    Config_Dict['LDevice']=file.readline().replace("\n","").strip().split(" ");
    Config_Dict['Ldevice_desc']=file.readline().replace("\n","").strip().split(" ");
    return  Config_Dict;

def print_closed(Attr,Value):
    return("<"+Attr+">"+Value+"</"+Attr+">");
def print_attrib(Attr,Value):
    return (Attr+"=\""+ Value+ "\" ");

def make_xml(Dict):
    xml= open("Conf.xml","w");
    xml.write("""<?xml version="1.0" encoding="UTF-8"?><SCL xmlns="http://www.iec.ch/61850/2003/SCL" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="SCL_IED.xsd">""");
    #xml.write("""<Header id="ICD File" version="0" revision="1" toolID="1" nameStructure="IEDName" />""") непонятно зачем надо
    xml.write("""<IED """);
    xml.write(print_attrib("name",Dict['name']));
    xml.write(print_attrib("desc",Dict['desc']));
    xml.write(print_attrib("type",Dict['type']));
    xml.write(print_attrib("manufacturer",Dict['manufacturer']));
    xml.write(print_attrib("configversion",Dict['config_version']));
    xml.write(">")

    for i in Dict['services']:
        xml.write(print_closed("Service",i));
    #обработка точек доступа
    for i in range(0, len(Dict['AccessPoint'])):
        xml.write("<AccessPoint ");
        xml.write(print_attrib("name",Dict['AccessPoint'][i]));
        xml.write(print_attrib("deck",Dict['AccessPoint_deck'][i]));
        xml.write(print_attrib("router",Dict['router'][i]));
        xml.write((print_attrib("clock",Dict['clock'][i])));
        xml.write(">");
        #добавляем к точке доступа сервер, по одному на точку доступа
        xml.write("<Server ");
        xml.write(print_attrib("timeout", Dict['timeout'][i]));
        xml.write(">");
        #теперь добавляем аутентификацию <Authentication none="true" password="false" weak="false" strong="false" certificate="false" />
        xml.write("<Authentication ");
        xml.write(print_attrib("none", Dict['authentication_none'][i]));
        xml.write(print_attrib("password", Dict['password'][i]));
        xml.write(print_attrib("weak", Dict['authentication_weak'][i]));
        xml.write(print_attrib("strong", Dict['authentication_strong'][i]));
        xml.write(print_attrib("certificate", Dict['certificate'][i]));
        xml.write("/>")
        #добавляем логические устройства
        for j in range(0, len(Dict['LDevice'])):
            xml.write("<LDevice ");
            xml.write(print_attrib("inst",Dict['LDevice'][j]));
            xml.write(print_attrib("desc",Dict['Ldevice_desc'][j]));
            xml.write(">")
            #каждый логический узел содержит 2 класса
            #LN0 - жестко заданный не конфигурируемый
            xml.write("""<LN0 lnType="LLN01" lnClass="LLN0" inst="">""")
            xml.write("""<DOI name="Status">""");
            xml.write("""<DAI name="q" valKind="Spec"/>""");
            xml.write("""<DAI name="stVal" valKind="Spec">""");
            xml.write("""</DAI>""")
            xml.write("""<DAI name="t" valKind="Spec"/>""");
            xml.write("""</DOI>""");
            xml.write("</LN0>");
            #и  узел Ln,  тоже конфигурировать особо нечего кроме базового класса, описанного в data_node
            xml.write("""<LN lnType="LPHD1" lnClass="LPHD" inst="1" prefix="">""")
            #определяем состояние, q -реальное значение(см 7-2),stVal-номинальное значение, t - timestamp
            xml.write("""<DOI name="Status">""");
            xml.write("""<DAI name="q" valKind="Spec" />""");
            xml.write("""<DAI name="stVal" valKind="Spec">""");
            xml.write("""</DAI>""")
            xml.write("""<DAI name="t" valKind="Spec" />""");
            xml.write("""</DOI>""");

            #управление: stVal- значение, t- timetamp
            xml.write("""<DOI name="Control">""");
            xml.write("""<DAI name="stVal" valKind="Spec">""");
            xml.write("""</DAI>""")
            xml.write("""<DAI name="t" valKind="Spec" />""");
            xml.write("""</DOI>""");

            #режим работы
            xml.write("""<DOI name="Work_Mode">""");
            xml.write("""<DAI name="stVal" valKind="Spec">""");
            xml.write("""</DAI>""")
            xml.write("""<DAI name="t" valKind="Spec" />""");
            xml.write("""</DOI>""");

            xml.write("</LN>")
            xml.write("</LDevice>");
        xml.write("</Server>")
        xml.write("</AccessPoint>");

    xml.write("</IED>");
    #определяем шаблон используемых данных в узлах
    xml.write("<DataTypeTemplates>");
    #шаблон конфигурации LN0
    xml.write("""<LNodeType id="LLN01" lnClass="LLN0">""");
    xml.write("""<DO name="Status" type="StatusType" transient="false" />""");
    xml.write("</LNodeType>")
    #шаблон конфигурации LN
    xml.write("""<LNodeType id="LPHD1" lnClass="LPHD">""");
    xml.write("""<DO name="Setpoint_Voltage" type="Setpoint_VoltageType" transient="false" />""");
    xml.write("""<DO name="Setpoint_Amperage" type="Setpoint_AmperageType" transient="false" />""");
    xml.write("""<DO name="Work_Mode" type="Work_ModeType" transient="false" />""");
    xml.write("""<DO name="Control" type="ControlType" transient="false" />""");
    xml.write("""<DO name="Status" type="StatusType" transient="false" />""");
    xml.write("</LNodeType>");

    #Определяем типы
    #режим
    xml.write("""<DOType id="StatusType" iedType="" cdc="INS">""");
    xml.write("""<DA name="q" bType="Quality" valKind="Spec" count="0" dchg="false" qchg="false" dupd="false" fc="ST" />""");
    xml.write("""<DA name="stVal" bType="Enum" valKind="Spec" type="StatusEnum" count="0" dchg="false" qchg="false" dupd="false" fc="ST">""");
    xml.write("""<Val>off</Val>""");
    xml.write("""</DA>""");
    xml.write("""<DA name="t" bType="Timestamp" valKind="Spec" count="0" dchg="false" qchg="false" dupd="false" fc="ST" />""");
    xml.write("""</DOType>""");

    #управление
    xml.write("""<DOType id="ControlType" iedType="" cdc="INS">""");
    xml.write("""<DA name="stVal" bType="Enum" valKind="Spec" type="ControlEnum" count="0" dchg="false" qchg="false" dupd="false" fc="ST">""");
    xml.write("""</DA>""");
    xml.write("""<DA name="t" bType="Timestamp" valKind="Spec" count="0" dchg="false" qchg="false" dupd="false" fc="ST" />""");
    xml.write("""</DOType>""");

    #режим работы
    xml.write("""<DOType id="Work_ModeType" iedType="" cdc="INC">""");
    xml.write("""<DA name="stVal" bType="Enum" valKind="Spec" type="WorkEnum" count="0" dchg="false" qchg="false" dupd="false" fc="ST">""");
    xml.write("""</DA>""");
    xml.write("""<DA name="t" bType="Timestamp" valKind="Spec" count="0" dchg="false" qchg="false" dupd="false" fc="ST" />""");
    xml.write("""</DOType>""");
    #определяем перечисления
    #параметры работы: готов, неисправность, пререгрев, пререгрука
    xml.write("""<EnumType id="StatusEnum">""")
    xml.write("""<EnumVal ord="0">ready</EnumVal>""");
    xml.write("""<EnumVal ord="1">malfunction</EnumVal>""");
    xml.write("""<EnumVal ord="2">overheat</EnumVal>""");
    xml.write("""<EnumVal ord="3">overload</EnumVal>""");
    xml.write("""<EnumVal ord="4">off</EnumVal>""");
    xml.write("""</EnumType>""");

    #управление: местное, удаленное
    xml.write("""<EnumType id="ControlEnum">""");
    xml.write("""<EnumVal ord="0">local</EnumVal>""");
    xml.write("""<EnumVal ord="1">remoute</EnumVal>""");
    xml.write("""</EnumType>""");

    #режим работы
    xml.write("""<EnumType id="WorkEnum">""");
    xml.write("""<EnumVal ord="0">voltage_regulation</EnumVal>""");
    xml.write("""<EnumVal ord="1">amperage_regulation</EnumVal>""");
    xml.write("""</EnumType>""");

    xml.write("</DataTypeTemplates>");
    xml.write("""</SCL>""");
    xml.close();

if __name__ == "__main__":
    print("Starting Config");
    Dict = open_file("anna.conf");
    #make_schema();
    make_xml(Dict);
    print("Config Finished");

