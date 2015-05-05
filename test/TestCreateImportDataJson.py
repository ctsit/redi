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
TestCreateImportDataJson.py:

   Verifies the correct functionality 
   of the `test_create_import_data_json` function
"""

import unittest
from lxml import etree
import logging
import os
from redi import redi
from redi import upload

DEFAULT_DATA_DIRECTORY = os.getcwd()


class TestCreateImportDataJson(unittest.TestCase):

    def setUp(self):
        redi.configure_logging(DEFAULT_DATA_DIRECTORY)
        self.CONST_STUDY_ID = 73
        return()

    ############################
    # == TEST_1
    def test_empty_event(self):
        redi.configure_logging(DEFAULT_DATA_DIRECTORY)
        logging.info("Running " + __name__ 
            + "#test_empty_event() using study_id: " + `self.CONST_STUDY_ID`)
        # Case 1 input string
        string_1_empty_event = """
<event>
</event>
"""
        out_dict_1 = {'study_id':self.CONST_STUDY_ID}
        etree_1 = etree.ElementTree(etree.fromstring(string_1_empty_event))
        self.assertRaises(Exception, upload.create_import_data_json, out_dict_1, etree_1)
        


    ############################
    # == TEST_2
    def test_empty_event_field_value(self):
        logging.info("Running " + __name__ 
            + "#test_empty_value() for study_id: " + `self.CONST_STUDY_ID`)
        # Case 2 input string
        string_2_empty_values = """
<event>
    <name>1_arm_1</name>
    <field>
        <name>chem_lbdtc</name>
        <value/>
    </field>
    <field>
        <name>chem_complete</name>
        <value/>
    </field>
    <field>
        <name>chem_nximport</name>
        <value/>
    </field>
    <field>
        <name>tbil_lborres</name>
        <value/>
    </field>
    <field>
        <name>tbil_lborresu</name>
        <value/>
    </field>
</event>"""

        string_2_out = """
record,redcap_event_name,field_name,value
73,"1_arm_1",chem_lbdtc,""
73,"1_arm_1",chem_complete,""
73,"1_arm_1",chem_nximport,""
73,"1_arm_1",tbil_lborres,""
73,"1_arm_1",tbil_lborresu,""
"""

        etree_2 = etree.ElementTree(etree.fromstring(string_2_empty_values))
        out_dict_2 = {'study_id':self.CONST_STUDY_ID}
        expected_result_dict_2 = {'contains_data': False, 'json_data': {'chem_complete': '', 'redcap_event_name': '1_arm_1', 'tbil_lborres': '', 'study_id': 73, 'chem_nximport': '', 'tbil_lborresu': '', 'chem_lbdtc': ''}}
        actual_result = upload.create_import_data_json(out_dict_2, etree_2)
        self.assertEqual(expected_result_dict_2,actual_result)


    ############################
    # == Test_3
    def test_mixed_event_field_value(self):
        logging.info("Running " + __name__ 
            + "#test_mixed_event_field_value() for study_id: " + `self.CONST_STUDY_ID`)


        string_3_mixed = """
<event>
    <name>1_arm_1</name>
    <field>
        <name>chem_lbdtc</name>
        <value>1902-12-17</value>
    </field>
    <field>
        <name>chem_complete</name>
        <value>2</value>
    </field>
    <field>
        <name>chem_nximport</name>
        <value>Y</value>
    </field>
    <field>
        <name>tbil_lborres</name>
        <value>1.7</value>
    </field>
    <field>
        <name>tbil_lborresu</name>
        <value/>
    </field>
</event>"""

        string_3_out = """
record,redcap_event_name,field_name,value
73,"1_arm_1",chem_lbdtc,"1902-12-17"
73,"1_arm_1",chem_complete,"2"
73,"1_arm_1",chem_nximport,"Y"
73,"1_arm_1",tbil_lborres,"1.7"
73,"1_arm_1",tbil_lborresu,""
"""
        etree_3 = etree.ElementTree(etree.fromstring(string_3_mixed))
        out_dict_3 = {'study_id':self.CONST_STUDY_ID}
        actual_result = upload.create_import_data_json(out_dict_3, etree_3)
        expected_result = {'contains_data': True, 'json_data': {'chem_complete': '2', 'redcap_event_name': '1_arm_1', 'tbil_lborres': '1.7', 'study_id': 73, 'chem_nximport': 'Y', 'tbil_lborresu': '', 'chem_lbdtc': '1902-12-17'}}
        self.assertEqual(actual_result, expected_result)


    ############################
    # == TEST_4
    def test_empty_event_field_name(self):
        logging.info("Running " + __name__ 
            + "#test_empty_event_field_name() for study_id: " + `self.CONST_STUDY_ID`)

        # Case 4 input string
        string_4_blank_name = """
<event>
    <name>1_arm_1</name>
    <field>
        <name>chem_lbdtc</name>   <!-- valid text -->
        <value>1902-12-17</value>
    </field>
    <field>
        <name></name>             <!-- missing text -->
        <value>2</value>
    </field>
    <field>
        <name>chem_nximport</name>
        <value>Y</value>
    </field>
    <field>
        <name>tbil_lborres</name>
        <value>1.7</value>
    </field>
    <field>
        <name>tbil_lborresu</name>
        <value/>
    </field>
</event> """
        etree_4 = etree.ElementTree(etree.fromstring(string_4_blank_name))
        out_dict_4 = {'study_id':self.CONST_STUDY_ID}
        self.assertRaises(Exception, upload.create_import_data_json, out_dict_4, etree_4)

    # Verify if code checks for blank `event/name`
    def test_empty_event_name(self):
        logging.info("Running " + __name__
            + "#test_empty_event_name() for study_id: " + `self.CONST_STUDY_ID`)

        string_4a_blank_name = """
<event>
    <!-- <name></name> -->
    <name></name>
    <field>
        <name>tbil_lborresu</name>
    </field>
</event> """
        etree_4a = etree.ElementTree(etree.fromstring(string_4a_blank_name))
        self.assertRaises(Exception, upload.create_import_data_json, self.CONST_STUDY_ID, etree_4a)

    ############################
    # == TEST_5
    def test_empty_study_id(self) :
        logging.info("Running " + __name__ 
            + "#test_empty_study_id() for study_id: ''")
        string_1_empty_event = """
<event></event>
"""
        string_5_out = "error_study_id_empty"
        etree_1 = etree.ElementTree(etree.fromstring(string_1_empty_event))
        self.assertRaises(Exception, upload.create_import_data_json,None, etree_1)

    def test_multiple_event(self):
        # motivated by bug 5996
        form = etree.fromstring(
            "<form>"
            "  <event><name>42_arm_42</name>"
            "    <field><name>foo</name><value>bar</value></field>"
            "  </event>"
            "  <event><name>no_arm</name>"
            "    <field><name>foo</name><value>bar</value></field>"
            "  </event>"
            "</form>")

        second_event = form.xpath('//event')[1]
        out_dict_3 = {'study_id':self.CONST_STUDY_ID}

        output = upload.create_import_data_json(out_dict_3, second_event)
        self.assertTrue(output['contains_data'])
        self.assertFalse('42_arm_42' in output['json_data']['redcap_event_name'])
        self.assertTrue('no_arm' in output['json_data']['redcap_event_name'])

    def tearDown(self):
        return()

    
if __name__ == "__main__":
    unittest.main()

