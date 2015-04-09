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

class TestConvertComponentIdToLoincCode(unittest.TestCase):

    def setUp(self):
        redi.configure_logging(DEFAULT_DATA_DIRECTORY)
        
        
    def test_convert_component_id_to_loinc_code(self):
        self.sampleXmlMapData = """<?xml version='1.0' encoding='US-ASCII'?>
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
        self.mapxmlDataTree= etree.ElementTree(etree.fromstring(self.sampleXmlMapData))
        
        self.rawXmlData = """<?xml version="1.0" encoding="utf8"?>
        <study>
            <subject>
                <NAME>test subject 1</NAME>
                <Comp_id>123</Comp_id>
                <RESULT>12.3</RESULT>
                <STUDY_ID>4567</STUDY_ID>
            </subject>
            <subject>
                <NAME>test subject 2</NAME>
                <Comp_id>789</Comp_id>
                <RESULT>12.3</RESULT>
                <STUDY_ID>4537</STUDY_ID>
            </subject>
        </study>"""
        self.rawxmlDataTree= etree.ElementTree(etree.fromstring(self.rawXmlData))
        
        self.result = redi.convert_component_id_to_loinc_code(self.rawxmlDataTree,self.mapxmlDataTree)
        
        self.expect =  etree.tostring(self.result, method='html', pretty_print=True)
        self.output = """<study>
            <subject>
                <NAME>test subject 1</NAME>
                <lcode>456</lcode><RESULT>12.3</RESULT>
                <STUDY_ID>4567</STUDY_ID>
            </subject>
            <subject>
                <NAME>test subject 2</NAME>
                <lcode>456</lcode><RESULT>12.3</RESULT>
                <STUDY_ID>4537</STUDY_ID>
            </subject>
        </study>
"""
        
        self.assertEqual(self.expect, self.output)
    
    def test_convert_component_id_to_loinc_code_with_no_source(self):
        self.sampleXmlMapData = """<?xml version='1.0' encoding='US-ASCII'?>
<clinical_datum>
	<version>0.1.0</version>
	<Description>Test Description</Description>
	<components>
		<component>
			<description>Test Component 1</description>
			<target>
				<name>lcode</name>
				<value>456</value>
			</target>
		</component>

		<component>
			<description>Test Component 2</description>
			<target>
				<name>lcode</name>
				<value>456</value>
			</target>
		</component>
	</components>
</clinical_datum>"""
        self.mapxmlDataTree= etree.ElementTree(etree.fromstring(self.sampleXmlMapData))
    
        self.rawXmlData = """<?xml version="1.0" encoding="utf8"?>
        <study>
            <subject>
                <NAME>test subject 1</NAME>
                <Comp_id>123</Comp_id>
                <RESULT>12.3</RESULT>
                <STUDY_ID>4567</STUDY_ID>
            </subject>
            <subject>
                <NAME>test subject 2</NAME>
                <Comp_id>789</Comp_id>
                <RESULT>12.3</RESULT>
                <STUDY_ID>4537</STUDY_ID>
            </subject>
        </study>"""
        self.rawxmlDataTree= etree.ElementTree(etree.fromstring(self.rawXmlData))
    
        self.assertRaises(Exception,redi.convert_component_id_to_loinc_code,self.rawxmlDataTree, self.mapxmlDataTree)
                
    def tearDown(self):
        return()

if __name__ == '__main__':
    unittest.main()
