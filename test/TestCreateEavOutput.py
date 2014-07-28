#!/usr/bin/env python

"""
TestCreateEavOutput.py:

   Verifies the correct functionality 
   of the `test_create_eav_output` function
"""
__author__      = "Andrei Sura"
__copyright__   = "Copyright 2014, University of Florida"
__license__     = "BSD 2-Clause"
__version__     = "0.1"
__email__       = "asura@ufl.edu"
__status__      = "Development"

import unittest
import sys
import os
file_dir = os.path.dirname(os.path.realpath(__file__))
goal_dir = os.path.join(file_dir, "../")
proj_root = os.path.abspath(goal_dir)+'/'
sys.path.append(proj_root + 'bin/')
from lxml import etree
import logging
import redi
import redi_lib
import os

class TestCreateEavOutput(unittest.TestCase):

    def setUp(self):
        print 'setUp in __function__'
        self.CONST_STUDY_ID = 73
         
        global logger
        logger = logging.getLogger('redi')
        logging.basicConfig(filename=proj_root+'log/redi.log',
                        format='%(asctime)s - %(levelname)s - \
                        %(name)s - %(message)s',
                        datefmt='%m/%d/%Y %H:%M:%S',
                        filemode='w',
                        level=logging.DEBUG)
        return()

    ############################
    # == TEST_1
    def test_empty_event(self):
        redi.configure_logging()
        logger.info("Running " + __name__ 
            + "#test_empty_event() using study_id: " + `self.CONST_STUDY_ID`)
        # Case 1 input string
        string_1_empty_event = """
<event>
</event>
"""
        string_1_out = ""
        etree_1 = etree.ElementTree(etree.fromstring(string_1_empty_event))
        result = redi_lib.create_eav_output(self.CONST_STUDY_ID, etree_1)
        self.assertEqual(string_1_out.strip(), result.strip())


    ############################
    # == TEST_2
    def test_empty_event_field_value(self):
        redi.configure_logging()
        logger.info("Running " + __name__ 
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
        result = redi_lib.create_eav_output(self.CONST_STUDY_ID, etree_2)
        self.assertEqual(string_2_out.strip(), result['csv'].strip())


    ############################
    # == Test_3
    def test_mixed_event_field_value(self):
        redi.configure_logging()
        logger.info("Running " + __name__ 
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
        result = redi_lib.create_eav_output(self.CONST_STUDY_ID, etree_3)
        self.assertEqual(string_3_out.strip(), result['csv'].strip())


    ############################
    # == TEST_4
    def test_empty_event_field_name(self):
        redi.configure_logging()
        logger.info("Running " + __name__ 
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
        self.assertRaises(redi.LogException, redi_lib.create_eav_output, self.CONST_STUDY_ID, etree_4)


    ############################
    # == TEST_5
    def test_empty_study_id(self) :
        redi.configure_logging()
        logger.info("Running " + __name__ 
            + "#test_empty_study_id() for study_id: ''")
        string_1_empty_event = """
<event></event>
"""
        string_5_out = "error_study_id_empty"
        etree_1 = etree.ElementTree(etree.fromstring(string_1_empty_event))
        self.assertRaises(redi.LogException, redi_lib.create_eav_output,None, etree_1)

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

        output = redi_lib.create_eav_output(42, second_event)

        self.assertTrue(output['contains_data'])
        self.assertFalse('42_arm_42' in output['csv'])
        self.assertTrue('no_arm' in output['csv'])

    def tearDown(self):
        return()

    
if __name__ == "__main__":
    unittest.main()

