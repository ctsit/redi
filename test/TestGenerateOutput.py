#!/usr/bin/env python

"""
TestGenerateOutput.py:

   Verifies the correct functionality 
   of the `generate_output` function
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
import datetime
import pprint
import redi
import redi_lib
import os

class TestGenerateOutput(unittest.TestCase):

    def setUp(self):
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
    def test_person_form_event(self):
        redi.configure_logging()
        logger.info("Running " + __name__ 
            + "#test_person_form_event() using xml: " )
        string_1_xml = """
<person_form_event>
    <person>
        <study_id>100</study_id>
        <all_form_events>
            <form>
                <name>cbc</name>
                <event>
                    <name>1_arm_1</name>
                    <field>
                        <name>cbc_lbdtc</name>
                        <value>1905-10-01</value>
                    </field>
                </event>
            </form>
            <form>
                <name>inr</name>
                <event>
                    <name>1_arm_1</name>
                    <field>
                        <name>cbc_lbdtc</name>
                        <value>1905-10-01</value>
                    </field>
                </event>
            </form>
 
        </all_form_events>
    </person>
    <person>
        <study_id>99</study_id>
        <all_form_events>
            <form>
                <name>cbc</name>
                <event>
                    <name>1_arm_1</name>
                    <field>
                        <name>cbc_lbdtc</name>
                        <value>1905-10-01</value>
                    </field>
                    <field>
                        <name>wbc_lborres</name>
                        <value>3.0</value>
                    </field>
                    <field>
                        <name>wbc_lbstat</name>
                        <value/>
                    </field>
                    <field>
                        <name>neut_lborres</name>
                        <value>500</value>
                    </field>
                    <field>
                        <name>neut_lbstat</name>
                        <value/>
                    </field>
                </event>
            </form>
            <form>
                <name>inr</name>
                <event>
                    <name>1_arm_1</name>
                    <field>
                        <name>inr_lbdtc</name>
                        <value>1906-12-01</value>
                    </field>
                    <field>
                        <name>inr_lborres</name>
                        <value/>
                    </field>
                    <field>
                        <name>inr_lbstat</name>
                        <value>NOT_DONE</value>
                    </field>
                </event>
            </form>
        </all_form_events>
    </person>
    <person>
        <study_id>98</study_id>
        <all_form_events>
            <form>
                <name>cbc</name>
                <event>
                    <name>1_arm_1</name>
                    <field>
                        <name>cbc_lbdtc</name>
                        <value></value>
                    </field>
                </event>
            </form>
            <form>
                <name>inr</name>
                <event>
                    <name>1_arm_1</name>
                    <field>
                        <name>cbc_lbdtc</name>
                        <value>1905-10-01</value>
                    </field>
                </event>
            </form>
        </all_form_events>
    </person>

</person_form_event>

"""
        #date_format = "%Y-%m-%d"
        #earliest_date   = datetime.datetime.strptime('1905-10-01', date_format).date()
        #latest_date     = datetime.datetime.strptime('1906-10-01', date_format).date()

        form_details    = {'Total_cbc_Forms': 2, 'Total_inr_Forms': 3}
        subject_details = {
            '98'  : {'Total_cbc_Forms' : 0, 'Total_inr_Forms' : 1 },
            '99'  : {'Total_cbc_Forms' : 1, 'Total_inr_Forms' : 1 },
            '100' : {'Total_cbc_Forms' : 1, 'Total_inr_Forms' : 1 }
        } 
 
        report_data = {
            'total_subjects'        : 3,
            'form_details'          : form_details,
            'subject_details'       : subject_details,
            'errors'                : []
        }

        etree_1 = etree.ElementTree(etree.fromstring(string_1_xml))
        result = redi_lib.generate_output(etree_1)
        self.assertEqual(report_data['total_subjects'], result['total_subjects'])
        self.assertEqual(report_data['form_details'], result['form_details'])
        self.assertEqual(report_data['subject_details'], result['subject_details'])
        self.assertEqual(report_data['errors'], result['errors'])
        #self.assertEqual(report_data, result)

    def tearDown(self):
        return()

    
if __name__ == "__main__":
    unittest.main()

