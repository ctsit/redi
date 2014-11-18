#!/usr/bin/env python

"""
TestParseAll.py:

   Verifies the correct functionality 
   of all functions with prefix `parse_`
"""
__author__      = "Andrei Sura"
__copyright__   = "Copyright 2014, University of Florida"
__license__     = "BSD 2-Clause"
__version__     = "0.1"
__email__       = "asura@ufl.edu"
__status__      = "Development"

import unittest
from lxml import etree
import logging
import os
from redi import redi

file_dir = os.path.dirname(os.path.realpath(__file__))
goal_dir = os.path.join(file_dir, "../")
proj_root = os.path.abspath(goal_dir)+'/'

DEFAULT_DATA_DIRECTORY = os.getcwd()

class TestParseAll(unittest.TestCase):

    def setUp(self):
        global logger
        logger = logging.getLogger('redi')
        logging.basicConfig(filename=DEFAULT_DATA_DIRECTORY,
                        format='%(asctime)s - %(levelname)s - \
                        %(name)s - %(message)s',
                        datefmt='%m/%d/%Y %H:%M:%S',
                        filemode='w',
                        level=logging.DEBUG)
        return()

    ############################
    # == TEST_1 - config/formEvents.xml
    def test_parse_form_events(self):
        redi.configure_logging(DEFAULT_DATA_DIRECTORY)
        logger.info("Running " + __name__ 
            + "#test_person_form_event() using xml: " )
        string_1_xml = """<?xml version="1.0" encoding="UTF-8"?>
<redcapProject>
	<name>Project</name>
	<form>
		<name>cbc</name>
		<formDateField>cbc_lbdtc</formDateField>
		<formCompletedFieldName>cbc_complete</formCompletedFieldName>
		<formImportedFieldName>cbc_nximport</formImportedFieldName>
        <formCompletedFieldValue>2</formCompletedFieldValue>
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
		<formImportedFieldName>chem_nximport</formImportedFieldName>
        <formCompletedFieldValue>2</formCompletedFieldValue>
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

