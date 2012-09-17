__author__ = 'KV'
def make_schema():
    xml = open("SCL_IED.xsd", "w");
    # описние схемы
    #targetNamespace="http://www.iec.ch/61850/2003/SCL"
    xml.write("""<?xml version="1.0" encoding="UTF-8"?>
    <xs:schema targetNamespace="http://www.iec.ch/61850/2003/SCL"
            xmlns:scl="http://www.iec.ch/61850/2003/SCL"
            xmlns="http://www.iec.ch/61850/2003/SCL"
            xmlns:xs="http://www.w3.org/2001/XMLShema"
            elementFormDefault="qualified" attributeFormDefault="unqualified"
            finalDefault="extension" version="1.0">

            <xs:complexType name="tlED">
	            <xs:complexContent>
		            <xs:extension base="tNaming">
			            <xs:sequence>
				            <xs:element name="Services" type="tServices" minOccurs="0"/>
                            <xs:element name="AccessPoint" type="tAccessPoint" maxOccurs="unbounded">
					            <xs:unique name="uniqueLNlnAccessPoint">
						            <xs:selector xpath=".//scl:LN"/>
                                        <xs:field xpath="@inst"/>
                                        <xs:field xpath="@lnClass"/>
                                        <xs:field xpath="@prefix"/>
					            </xs:unique>
				            </xs:element>
			            </xs:sequence>
                        <xs:attribute name="type" type="xs:normalizedString" use="optional"/>
                        <xs:attribute name="manufacturer" type="xs:normalizedString" use="optional"/>
                        <xs:attribute name="configVersion" type="xs:normalizedString" use="optional"/>
		            </xs:extension>
	            </xs:complexContent>
            </xs:complexType>

            <xs:complexType name="tServices">
                <xs:all>
	                <xs:element name="DynAssociation" type="tServiceYesNo" minOccurs="0"/>
                    <xs:element name="SettingGroups" minOccurs="0">
		                <xs:complexType>
			                <xs:all>
				                <xs:element name="SGEdit" type="tServiceYesNo" minOccurs="0"/>
                                <xs:element name="ConfSG" type="tServiceYesNo" minOccurs="0"/>
			                </xs:all>
		                </xs:complexType>
	                </xs:element>
                    <xs:element name="GetDirectory" type="tServiceYesNo" minOccurs="0"/>
                    <xs:element name="GetDataObjectDefinition" type="tServiceYesNo" minOccurs="0"/>
                    <xs:element name="DataObjectDirectory" type="tServiceYesNo" minOccurs="0"/>
                    <xs:element name="GetDataSetValue" type="tServiceYesNo" minOccurs="0"/>
                    <xs:element name="SetDataSetValue" type="tServiceYesNo" minOccurs="0"/>
                    <xs:element name="DataSetDirectory" type="tServiceYesNo" minOccurs="0"/>
                    <xs:element name="ConfDataSet" type="tServiceWithMaxAndMaxAttributes" minOccurs="0"/>
                    <xs:element name="DynDataSet" type="tServiceWithMaxAndMaxAttributes" minOccurs="0"/>
                    <xs:element name="ReadWrite" type="tServiceYesNo" minOccurs="0"/>
                    <xs:element name="TimerActivatedControl" type="tServiceYesNo" minOccurs="0"/>
                    <xs:element name="ConfReportControl" type="tServiceWithMax" minOccurs="0"/>
                    <xs:element name="GetCBValues" type="tServiceYesNo" minOccurs="0"/>
                    <xs:element name="ConfLogControl" type="tServiceWithMax" minOccurs="0"/>
                    <xs:element name="ReportSettings" type="tReportSettings" minOccurs="0"/>
                    <xs:element name="LogSettings" type="tLogSettings" minOccurs="0"/>
		            <xs:element name="GSESettings" type="tGSESettings" minOccurs="0"/>
	                <xs:element name="SMVSettings" type="tSMVSettings" minOccurs="0"/>
                    <xs:element name="GSEDir" type="tServiceYesNo" minOccurs="0"/>
                    <xs:element name="GOOSE" type="tServiceWithMax" minOccurs="0"/>
                    <xs:element name="GSSE" type="tServiceWithMax" minOccurs="0"/>
                    <xs:element name="FileHandling" type="tServiceYesNo" minOccurs="0"/>
                    <xs:element name="ConfLNs" type="tConfLNs" minOccurs="0"/>
                </xs:all>
            </xs:complexType>


            <xs:complexType name="tAccessPoint">
	            <xs:complexContent>
		            <xs:extension base="tNaming">
			            <xs:choice minOccurs="0">
				            <xs:element name="Server" type="tServer">
					            <xs:unique name="uniqueAssociationlnServer">
						            <xs:selector xpath="./scl:Association"/>
							            <xs:field xpath="@associationlD"/>
					            </xs:unique>
				            </xs:element>
                            <xs:element ref="LN" maxOccurs="unbounded"/>
			            </xs:choice>
                        <xs:attribute name="router" type="xs:boolean" use="optional" default="false">
                        </xs:attribute>
			            <xs:attribute name="clock" type="xs:boolean" use="optional" default="false">
                        </xs:attribute>
		            </xs:extension>
	            </xs:complexContent>
            </xs:complexType>

            <xs:complexType name="tServer">
	            <xs:complexContent>
                    <xs:extension base="tUnNaming">
		                <xs:sequence>
			                    <xs:element name="Authentication">
				                    <xs:complexType>
						                <xs:attributeGroup ref="agAuthentication"/>
					                </xs:complexType>
				                </xs:element>
                                <xs:element name="LDevice" type="tLDevice" maxOccurs="unbounded"/>
                                <xs:element name="Association" type="tAssociation" minOccurs="0" maxOccurs="unbounded"/>
			            </xs:sequence>
                        <xs:attribute name="timeout" type="xs:unsignedlnt" use="optional" default="30"/>
		            </xs:extension>
	            </xs:complexContent>
            </xs:complexType>


            <xs:attributeGroup name="agAuthentication">
	            <xs:attribute name="none" type="xs:boolean" use="optional" default="true"/>
                <xs:attribute name="password" type="xs:boolean" use="optional" default="false"/>
                <xs:attribute name="weak" type="xs:boolean" use="optional" default="false"/>
                <xs:attribute name="strong" type="xs:boolean" use="optional" default="false"/>
                <xs:attribute name="certificate" type="xs:boolean" use="optional" default="false"/>
            </xs:attributeGroup>

            <xs:complexType name="tLDevice">
	            <xs:complexContent>
		            <xs:extension base="tUnNaming">
			            <xs:sequence>
                            <xs:element ref="LN0"/>
                            <xs:element ref="LN" minOccurs="0" maxOccurs="unbounded"/>
                            <xs:element name="AccessControl" type="tAccessControl" minOccurs="0"/>
			            </xs:sequence>
                        <xs:attribute name="inst" type="tName" use="required">
                        </xs:attribute>
		            </xs:extension>
	            </xs:complexContent>
            </xs:complexType>


            <xs:complexType name="tLN0">
	            <xs:complexContent>
		            <xs:extension base="tAnyLN">
			            <xs:sequence>
				            <xs:element name="GSEControl" type="tGSEControl" minOccurs="0" maxOccurs="unbounded"/>
				            <xs:element name="SampledValueControl" type="tSampledValueControl" minOccurs="0" maxOccurs="unbounded"/>
				            <xs:element name="SettingControl" type="tSettingControl" minOccurs="0"/>
                            <xs:element name="SCLControl" type="tSCLControl" minOccurs="0"/>
                            <xs:element name="Log" type="tLog" minOccurs="0"/>
			            </xs:sequence>
                        <xs:attribute name="lnClass" type="tLNCIassEnum" use="required" fixed="LLN0"/>
                        <xs:attribute name="inst" type="xs:normalizedString" use="required" fixed=""/>
		            </xs:extension>
	            </xs:complexContent>
            </xs:complexType>


            <xs:complexType name="tLN">
	            <xs:complexContent>
		            <xs:extension base="tAnyLN">
			            <xs:attribute name="lnClass" type="tLNCIassEnum" use="required"/>
                        <xs:attribute name="inst" type="xs:unsignedlnt" use="required"/>
                        <xs:attribute name="prefix" type="tAnyName" use="optional" default=""/>
		            </xs:extension>
	            </xs:complexContent>
            </xs:complexType>

            <xs:complexType name="tAnyLN" abstract="true">
	            <xs:complexContent>
		            <xs:extension base="tUnNaming">
			            <xs:sequence>
				            <xs:element name="DataSet" type="tDataSet" minOccurs="0" maxOccurs="unbounded"/>
				            <xs:element name="ReportControl" type="tReportControl" minOccurs="0" maxOccurs="unbounded"/>
				            <xs:element name="LogControl" type="tLogControl" minOccurs="0" maxOccurs="unbounded"/>
                            <xs:element name="DOI" type="tDOI" minOccurs="0" maxOccurs="unbounded"/>
				            <xs:element name="lnputs" type="tlnputs" minOccurs="0"/>
			            </xs:sequence>
                        <xs:attribute name="lnType" type="tName" use="required"/>
		            </xs:extension>
	            </xs:complexContent>
            </xs:complexType>


            <xs:complexType name="tDOI">
	            <xs:complexContent>
		            <xs:extension base="tUnNaming">
			            <xs:choice minOccurs="0" maxOccurs="unbounded">
				            <xs:element name="SDI" type=""/>
                            <xs:element name="DAI" type="tDAI"/>
			            </xs:choice>
                        <xs:attribute name="name" type="tRestrName1stU" use="required"/>
                        <xs:attribute name="ix" type="xs:unsignedlnt" use="optional"/>
                        <xs:attribute name="accessControl" type="xs:normalizedString" use="optional"/>
		            </xs:extension>
	            </xs:complexContent>
            </xs:complexType>

            <xs:complexType name="tDAI">
                <xs:complexContent>
	                <xs:extension base="tUnNaming">
		                <xs:sequence>
			                <xs:element name="Val" type="tVal" minOccurs="0" maxOccurs="unbounded"/>
                        </xs:sequence>
                        <xs:attribute name="name" type="tRestrName1stL" use="required"/>
                        <xs:attribute name="sAddr" type="xs:normalizedString" use="optional"/>
                        <xs:attribute name="valKind" type="tValKindEnum" use="optional" default="Set"/>
                        <xs:attribute name="ix" type="xs:unsignedlnt" use="optional"/>
	                </xs:extension>
                </xs:complexContent>
            </xs:complexType>

            <xs:complexType name="tSDI">
	            <xs:complexContent>
		            <xs:extension base="tUnNaming">
			            <xs:choice minOccurs="0" maxOccurs="unbounded">
				            <xs:element name="SDI" type="tSDI"/>
                            <xs:element name="DAI" type="tDAI"/>
			            </xs:choice>
                        <xs:attribute name="name" type="tRestrName1stL" use="required"/>
                        <xs:attribute name="ix" type="xs:unsignedlnt" use="optional"/>
		            </xs:extension>
	            </xs:complexContent>
            </xs:complexType>

            <xs:complexType name="tDataSet">
	            <xs:complexContent>
		            <xs:extension base="tNaming">
			            <xs:sequence>
				        <xs:element name="FCDA" type="tFCDA" maxOccurs="unbounded"/>
			            </xs:sequence>
		            </xs:extension>
	            </xs:complexContent>
            </xs:complexType>

            <xs:complexType name="tFCDA">
	            <xs:attribute name="ldInst" type="tName" use="optional"/>
                <xs:attribute name="prefix" type="tAnyName" use="optional"/>
                <xs:attribute name="lnClass" type="tLNClassEnum" use="optional"/>
                <xs:attribute name="lnInst" type="tName" use="optional"/>
                <xs:attribute name="doName" type="tName" use="optional"/>
                <xs:attribute name="daName" type="tName" use="optional"/>
                <xs:attribute name="fc" type="tFCEnum" use="required"/>
            </xs:complexType>


            <xs:complexType name="tReportControl">
	            <xs:complexContent>
		            <xs:extension base="tControlWithTriggerOpt">
			            <xs:sequence>
				            <xs:element name="OptFields">
					            <xs:complexType>
						            <xs:attributeGroup ref="agOptFields"/>
					            </xs:complexType>
				            </xs:element>
                            <xs:element name="RptEnabled" type="tRptEnabled" minOccurs="0"/>
			            </xs:sequence>
                        <xs:attribute name="rptlD" type="tName" use="required"/>
                        <xs:attribute name="confRev" type="xs:unsignedlnt" use="required"/>
                        <xs:attribute name="buffered" type="xs:boolean" use="optional" default="false"/>
                        <xs:attribute name="bufTime" type="xs:unsignedlnt" use="optional" default="0"/>
		            </xs:extension>
	            </xs:complexContent>
            </xs:complexType>


            <xs:complexType name="tControlWithTriggerOpt" abstract="true">
                 <xs:complexContent>
	                <xs:extension base="tControl">
		                <xs:sequence>
			                <xs:element name="TrgOps" type="tTrgOps" minOccurs="0"/>
		                </xs:sequence>
                        <xs:attribute name="intgPd" type="xs:unsignedlnt" use="optional" default="0"/>
	                </xs:extension>
                </xs:complexContent>
            </xs:complexType>

            <xs:complexType name="tTrgOps">
	            <xs:attribute name="dchg" type="xs:boolean" use="optional" default="false"/>
                <xs:attribute name="qchg" type="xs:boolean" use="optional" default="false"/>
                <xs:attribute name="dupd" type="xs:boolean" use="optional" default="false"/>
                <xs:attribute name="period" type="xs:boolean" use="optional" default="false"/>
            </xs:complexType>

            <xs:element name="OptFields">
	            <xs:complexType>
		            <xs:attributeGroup ref="agOptFields"/>
                </xs:complexType>
            </xs:element>

            <xs:attributeGroup name="agOptFields">
		        <xs:attribute name="seqNum" type="xs:boolean" use="optional" default="false"/>
                <xs:attribute name="timeStamp" type="xs:boolean" use="optional" default="false"/>
                <xs:attribute name="dataSet" type="xs:boolean" use="optional" default="false"/>
                <xs:attribute name="reasonCode" type="xs:boolean" use="optional" default="false"/>
                <xs:attribute name="dataRef" type="xs:boolean" use="optional" default="false"/>
                <xs:attribute name="bufOvfl" type="xs:boolean" use="optional" default="false"/>
                <xs:attribute name="entryID" type="xs:boolean" use="optional" default="false"/>
                <xs:attribute name="configRef" type="xs:boolean" use="optional" default="false"/>
                <xs:attribute name="segmentation" type="xs:boolean" use="optional" default="false"/>
            </xs:attributeGroup>

            <xs:complexType name="tRptEnabled">
	            <xs:complexContent>
		            <xs:extension base="tUnNaming">
			            <xs:sequence>
				            <xs:element name="ClientLN" type="tClientLN" minOccurs="0" maxOccurs="unbounded"/>
			            </xs:sequence>
                        <xs:attribute name="max" type="xs:unsignedlnt" use="optional" default="1"/>
		            </xs:extension>
	            </xs:complexContent>
            </xs:complexType>

            <xs:complexType name="tClientLN">
	            <xs:attributeGroup ref="agLNRef"/>
            </xs:complexType>

            <xs:attributeGroup name="agLNRef">
	            <xs:attributeGroup ref="agLDRef"/>
                <xs:attribute name="prefix" type="xs:normalizedString" use="optional"/>
                <xs:attribute name="lnClass" type="tLNClassEnum" use="required"/>
                <xs:attribute name="lnInst" type="xs:normalizedString" use="required"/>
            </xs:attributeGroup>

            <xs:complexType name="tLogControl">
	            <xs:complexContent>
		            <xs:extension base="tControlWithTriggerOpt">
			            <xs:attribute name="logName" type="tName" use="required"/>
                        <xs:attribute name="logEna" type="xs:boolean" use="optional" default="true"/>
                        <xs:attribute name="reasonCode" type="xs:boolean" use="optional" default="true"/>
		            </xs:extension>
	            </xs:complexContent>
            </xs:complexType>

            <xs:complexType name="tControlWithTriggerOpt" abstract="true">
		            <xs:complexContent>
			            <xs:extension base="tControl">
				            <xs:sequence>
					            <xs:element name="TrgOps" type="tTrgOps" minOccurs="0"/>
				            </xs:sequence>
                            <xs:attribute name="intgPd" type="xs:unsignedlnt" use="optional" default="0"/>
			            </xs:extension>
		            </xs:complexContent>
            </xs:complexType>

            <xs:complexType name="tGSEControl">
	            <xs:complexContent>
		            <xs:extension base="tControlWithlEDName">
			            <xs:attribute name="type" type="tGSEControlTypeEnum" use="optional" default="GOOSE"/>
                        <xs:attribute name="applD" type="xs:normalizedString" use="required"/>
		            </xs:extension>
	            </xs:complexContent>
            </xs:complexType>

            <xs:complexType name="tControlWithlEDName">
	            <xs:complexContent>
		            <xs:extension base="tControl">
			            <xs:sequence>
				            <xs:element name="IEDName" type="tName" minOccurs="0" maxOccurs="unbounded"/>
			            </xs:sequence>
                        <xs:attribute name="confRev" type="xs:unsignedlnt" use="optional"/>
		            </xs:extension>
	            </xs:complexContent>
            </xs:complexType>

            <xs:complexType name="tSampledValueControl">
	            <xs:complexContent>
		            <xs:extension base="tControlWithlEDName">
			            <xs:sequence>
				            <xs:element name="SmvOpts">
					            <xs:complexType>
                                    <xs:attributeGroup ref="agSmvOpts"/>
					            </xs:complexType>
				            </xs:element>
			            </xs:sequence>
                        <xs:attribute name="smvlD" type="xs:normalizedString" use="required"/>
                        <xs:attribute name="multicast" type="xs:boolean" default="true"/>
                        <xs:attribute name="smpRate" type="xs:unsignedlnt" use="required"/>
                        <xs:attribute name="nofASDU" type="xs:unsignedlnt" use="required"/>
		            </xs:extension>
	            </xs:complexContent>
            </xs:complexType>

            <xs:attributeGroup name="agSmvOpts">
	            <xs:attribute name="refreshTime" type="xs:boolean" use="optional" default="false"/>
                <xs:attribute name="sampleSynchronized" type="xs:boolean" use="optional" default="false"/>
                <xs:attribute name="sampleRate" type="xs:boolean" use="optional" default="false"/>
                <xs:attribute name="security" type="xs:boolean" use="optional" default="false"/>
                <xs:attribute name="dataRef" type="xs:boolean" use="optional" default="false"/>
            </xs:attributeGroup>

            <xs:complexType name="tSettingControl">
	            <xs:complexContent>
		            <xs:extension base="tUnNaming">
			            <xs:attribute name="numOfSGs" type="xs:unsignedlnt" use="required"/>
                        <xs:attribute name="actSG" type="xs:unsignedlnt" use="optional" default="1"/>
		            </xs:extension>
                </xs:complexContent>
            </xs:complexType>


            <xs:complexType name="tlnputs">
	            <xs:complexContent>
		            <xs:extension base="tUnNaming">
			            <xs:sequence>
				            <xs:element name="ExtRef" type="tExtRef" maxOccurs="unbounded"/>
			            </xs:sequence>
		            </xs:extension>
	            </xs:complexContent>
            </xs:complexType>


            <xs:complexType name="tExtRef">
	            <xs:attributeGroup ref="agDORef"/>
                <xs:attribute name="daName" type="tName" use="optional"/>
                <xs:attribute name="intAddr" type="xs:normalizedString" use="optional"/>
            </xs:complexType>

            <xs:complexType name="tAccessControl" mixed="true">
	            <xs:complexContent mixed="true">
		            <xs:extension base="tAnyContentFromOtherNamespace"/>
	            </xs:complexContent>
            </xs:complexType>

            <xs:complexType name="tAssociation">
	                <xs:attribute name="kind" type="tAssociationKindEnum" use="required"/>
                    <xs:attribute name="associationID" type="tName" use="optional" />
                    <xs:attributeGroup ref="agLNRef"/>
            </xs:complexType>
    </xs:schema> """);
    xml.close();