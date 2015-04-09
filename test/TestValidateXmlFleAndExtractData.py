#!/usr/bin/env python

# Contributors:
# Christopher P. Barnes <senrabc@gmail.com>
# Andrei Sura: github.com/indera
# Mohan Das Katragadda <mohan.das142@gmail.com>
# Philip Chase <philipbchase@gmail.com>
# Ruchi Vivek Desai <ruchivdesai@gmail.com>
# Taeber Rapczak <taeber@ufl.edu>
# Nicholas Rejack <nrejack@ufl.edu>
# Josh Hanna <josh@hanna.io>
# Copyright (c) 2014-2015, University of Florida
# All rights reserved.
#
# Distributed under the BSD 3-Clause License
# For full text of the BSD 3-Clause License see http://opensource.org/licenses/BSD-3-Clause

'''
@author : Mohan
email : mohan88@ufl.edu

This file tests for the function parse_raw_xml

'''
import unittest
import os
from lxml import etree
from redi import redi

file_dir = os.path.dirname(os.path.realpath(__file__))
goal_dir = os.path.join(file_dir, "../")
proj_root = os.path.abspath(goal_dir)+'/'

DEFAULT_DATA_DIRECTORY = os.getcwd()

class TestValidateXmlFleAndExtractData(unittest.TestCase):

    def setUp(self):
        redi.configure_logging(DEFAULT_DATA_DIRECTORY)
        
        
    def test_validate_xml_file_and_extract_data_valid_xml(self):
        xml_file_name = "tempxmlFile.xml"
        temp_xml = open(xml_file_name, "wb")
        self.sampleXmlData = """<?xml version='1.0' encoding='US-ASCII'?>
<clinical_datum>
	<version>0.1.0</version>
	<Description>Test Description</Description>
	<components>
		<component>
			<description>Test Component 1</description>
			<source>
				<name>Comp_id</name>
				<value>123</value>
			</source>
			<target>
				<name>lcode</name>
				<value>456</value>
			</target>
		</component>

		<component>
			<description>Test Component 2</description>
			<source>
				<name>Comp_id</name>
				<value>789</value>
			</source>
			<target>
				<name>lcode</name>
				<value>456</value>
			</target>
		</component>
	</components>
</clinical_datum>"""
        temp_xml.write(self.sampleXmlData)
        temp_xml.close()
        
        xsd_file_name = "tempxsdFile.xsd"
        temp_xsd = open(xsd_file_name, "wb")
        self.sampleXsdData = """<xs:schema attributeFormDefault="unqualified" elementFormDefault="qualified" xmlns:xs="http://www.w3.org/2001/XMLSchema">
          <xs:element name="clinical_datum">
            <xs:complexType>
              <xs:sequence>
                <xs:element type="xs:string" name="version"/>
                <xs:element type="xs:string" name="Description"/>
                <xs:element name="components">
                  <xs:complexType>
                    <xs:sequence>
                      <xs:element name="component" maxOccurs="unbounded" minOccurs="0">
                        <xs:complexType>
                          <xs:sequence>
                            <xs:element type="xs:string" name="description"/>
                            <xs:element name="source">
                              <xs:complexType>
                                <xs:sequence>
                                  <xs:element type="xs:string" name="name"/>
                                  <xs:element type="xs:string" name="value"/>
                                </xs:sequence>
                              </xs:complexType>
                            </xs:element>
                            <xs:element name="target">
                              <xs:complexType>
                                <xs:sequence>
                                  <xs:element type="xs:string" name="name"/>
                                  <xs:element type="xs:string" name="value"/>
                                </xs:sequence>
                              </xs:complexType>
                            </xs:element>
                          </xs:sequence>
                        </xs:complexType>
                      </xs:element>
                    </xs:sequence>
                  </xs:complexType>
                </xs:element>
              </xs:sequence>
            </xs:complexType>
          </xs:element>
        </xs:schema>
        """
        temp_xsd.write(self.sampleXsdData)
        temp_xsd.close()
        self.result = redi.validate_xml_file_and_extract_data(xml_file_name, xsd_file_name)
        self.expect =  etree.tostring(self.result, method='html', pretty_print=True)
        self.output = """<clinical_datum>
	<version>0.1.0</version>
	<Description>Test Description</Description>
	<components>
		<component>
			<description>Test Component 1</description>
			<source>
				<name>Comp_id</name>
				<value>123</value>
			</source>
			<target>
				<name>lcode</name>
				<value>456</value>
			</target>
		</component>

		<component>
			<description>Test Component 2</description>
			<source>
				<name>Comp_id</name>
				<value>789</value>
			</source>
			<target>
				<name>lcode</name>
				<value>456</value>
			</target>
		</component>
	</components>
</clinical_datum>
"""
        self.assertEqual(self.expect, self.output)
        
        os.remove(xml_file_name)
        os.remove(xsd_file_name)
    
    def test_validate_xml_file_and_extract_data_invalid_xml(self):
        xml_file_name = "tempxmlFile.xml"
        temp_xml = open(xml_file_name, "wb")
        self.sampleXmlData = """<?xml version='1.0' encoding='US-ASCII'?>
<clinical_datum>
	<version>0.1.0</version>
	<Description>Test Description</Description>
	<components>
		<component>
			<description>Test Component 1</description>
			<source>
				<name>Comp_id</name>
				<value>123</value>
			</source>
			<target>
				<name>lcode</name>
				<value>456</value>
			</target>
		</component>

		<component>
			<description>Test Component 2</description>
			<source>
				<name>Comp_id</name>
				<value>789</value>
			</source>
			<target>
				<name>lcode</name>
				<value>456</value>
			</target>
		</component>
	</components>
</clinical_datum>"""
        temp_xml.write(self.sampleXmlData)
        temp_xml.close()
    
        xsd_file_name = "tempxsdFile.xsd"
        temp_xsd = open(xsd_file_name, "wb")
        self.sampleXsdData = """<xs:schema attributeFormDefault="unqualified" elementFormDefault="qualified" xmlns:xs="http://www.w3.org/2001/XMLSchema">
          <xs:element name="clinical_datum">
            <xs:complexType>
              <xs:sequence>
                <xs:element type="xs:string" name="version"/>
                <xs:element type="xs:string" name="Description"/>
                <xs:element name="components">
                  <xs:complexType>
                    <xs:sequence>
                      <xs:element name="component" maxOccurs="unbounded" minOccurs="0">
                        <xs:complexType>
                          <xs:sequence>
                            <xs:element type="xs:integer" name="description"/>
                            <xs:element name="source">
                              <xs:complexType>
                                <xs:sequence>
                                  <xs:element type="xs:string" name="name"/>
                                  <xs:element type="xs:string" name="value"/>
                                </xs:sequence>
                              </xs:complexType>
                            </xs:element>
                            <xs:element name="target">
                              <xs:complexType>
                                <xs:sequence>
                                  <xs:element type="xs:string" name="name"/>
                                  <xs:element type="xs:string" name="value"/>
                                </xs:sequence>
                              </xs:complexType>
                            </xs:element>
                          </xs:sequence>
                        </xs:complexType>
                      </xs:element>
                    </xs:sequence>
                  </xs:complexType>
                </xs:element>
              </xs:sequence>
            </xs:complexType>
          </xs:element>
        </xs:schema>
        """
        temp_xsd.write(self.sampleXsdData)
        temp_xsd.close()
        self.assertRaises(Exception,redi.validate_xml_file_and_extract_data,xml_file_name, xsd_file_name)
        os.remove(xml_file_name)
        os.remove(xsd_file_name)
        
    def tearDown(self):
        return()

if __name__ == '__main__':
    unittest.main()
