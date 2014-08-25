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
import logging
import os
import tempfile
from lxml import etree
from mock import patch
import redi
import redi_lib
from utils.redcapClient import redcapClient
import utils.SimpleConfigParser as SimpleConfigParser

file_dir = os.path.dirname(os.path.realpath(__file__))
goal_dir = os.path.join(file_dir, "../")
proj_root = os.path.abspath(goal_dir)+'/'

DEFAULT_DATA_DIRECTORY = os.getcwd()

class TestGenerateOutput(unittest.TestCase):
    
    def setUp(self):
        redi.configure_logging(DEFAULT_DATA_DIRECTORY)

    def dummy_redcapClient_initializer(self,redcap_uri,token):
        pass
        
    class dummyClass:
        def_field = 'test'
        

    def dummy_send_data_to_redcap(self, data, overwrite = False):
        dummy_output = """Data sent"""
        return dummy_output
    
    @patch.multiple(redcapClient, __init__= dummy_redcapClient_initializer,
            project = dummyClass(), send_data_to_redcap = dummy_send_data_to_redcap)
    def test_person_form_event(self):
        redi.logger.info("Running " + __name__ 
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
        
        redcap_settings = {
            'rate_limiter_value_in_redcap':500,
            'redcap_uri':'http://fakeURI:fakeport/',
            'token':'faketoken'
        }
        email_settings = {
            'smtp_host_for_outbound_mail': 'smtp.example.com',
            'redcap_support_sender_email': 'please-do-not-reply@example.com',
            'redcap_uri': 'http://localhost:8998/redcap/api/',
            'smtp_port_for_outbound_mail': 25,
            'redcap_support_receiver_email': 'please-do-not-reply@example.com'
        }

        class MockDataRepository(object):
            def store(self, data):
                pass

        etree_1 = etree.ElementTree(etree.fromstring(string_1_xml))
        result = redi_lib.generate_output(etree_1,redcap_settings,email_settings, MockDataRepository())
        self.assertEqual(report_data['total_subjects'], result['total_subjects'])
        self.assertEqual(report_data['form_details'], result['form_details'])
        self.assertEqual(report_data['subject_details'], result['subject_details'])
        self.assertEqual(report_data['errors'], result['errors'])

    def tearDown(self):
        return()

    
if __name__ == "__main__":
    unittest.main()

