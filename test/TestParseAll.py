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

"""
TestParseAll.py:

   Verifies the correct functionality 
   of all functions with prefix `parse_`
"""

import unittest
from lxml import etree
import logging
import os
from redi import redi

DEFAULT_DATA_DIRECTORY = os.getcwd()

class TestParseAll(unittest.TestCase):

    def setUp(self):
        redi.configure_logging(DEFAULT_DATA_DIRECTORY)

    ############################
    # == TEST_1 - config/formEvents.xml
    def test_parse_form_events(self):
        string_1_xml = """<?xml version="1.0" encoding="UTF-8"?>
<redcapProject>
	<name>Project</name>
	<form>
		<name>cbc</name>
		<formDateField>cbc_lbdtc</formDateField>
		<formCompletedFieldName>cbc_complete</formCompletedFieldName>
        <formCompletedFieldValue>2</formCompletedFieldValue>
		<formImportedFieldName>cbc_nximport</formImportedFieldName>
        <formImportedFieldValue>Y</formImportedFieldValue>
		<event>
    		<name>1_arm_1</name>
		</event>
		<event>
		    <name>2_arm_1</name>
		</event>
		<event>
		    <name>3_arm_1</name>
		</event>
	</form>
	<form>
		<name>chemistry</name>
		<formDateField>chem_lbdtc</formDateField>
		<formCompletedFieldName>chemistry_complete</formCompletedFieldName>
        <formCompletedFieldValue>2</formCompletedFieldValue>
		<formImportedFieldName>chem_nximport</formImportedFieldName>
        <formImportedFieldValue>Y</formImportedFieldValue>
		<event>
		    <name>1_arm_1</name>
		</event>
		<event>
		    <name>2_arm_1</name>
		</event>
    </form>
</redcapProject>
"""
        temp_file = 'tmp.xml'
        fh = open(temp_file, 'w')
        fh.write(string_1_xml)
        fh.close()

        etree_1 = etree.ElementTree(etree.fromstring(string_1_xml))
        result_tree = redi.parse_form_events(temp_file)
        result_xml  = etree.tostring(result_tree) 

        par = etree.XMLParser(remove_blank_text = True)
        clean_tree   = etree.XML(string_1_xml, parser = par)
        clean_result = etree.XML(result_xml, parser = par)

        self.assertEqual(etree.tostring(clean_tree), etree.tostring(clean_result))
        os.remove(temp_file)

    def tearDown(self):
        return()

    
if __name__ == "__main__":
    unittest.main()

