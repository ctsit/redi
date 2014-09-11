#!/usr/bin/env python

"""
TestSendPersonFormDataToRedcap.py:

   Verifies the correct functionality
   of the `_send_person_form_data_to_redcap` function

   Note: This function will be called from inside a loop
        which parses the whole person_form_event (pfe) tree.
"""
import unittest
import logging
import os
import tempfile
from lxml import etree
from mock import patch
import redi
import redi_lib
from redi_lib import FormKey
from utils.redcapClient import redcapClient
import utils.SimpleConfigParser as SimpleConfigParser

class TestSendPersonFormDataToRedcap(unittest.TestCase):
    def setUp(self):
        redi.configure_logging(os.getcwd())

    def dummy_redcapClient_initializer(self, redcap_uri, token, verify_ssl):
        pass

    class DummyClass:
        def_field = 'test'

    def dummy_send_data_to_redcap(self, data, overwrite = False):
        return "Success"

    @patch.multiple(redcapClient, __init__= dummy_redcapClient_initializer,
            project = DummyClass(), send_data_to_redcap = dummy_send_data_to_redcap)
    def test_send_person_form_data_to_redcap(self):
        # 3 Persons
        pfe_xml = """
<person_form_event>
    <person study_id="100">
        <study_id>100</study_id>
        <all_form_events>
            <form form_name="cbc"> <name>cbc</name>
                <event> <name>1_arm_1</name> <field> <name>cbc_lbdtc</name> <value>1905-10-01</value> </field> </event>
            </form>
            <form form_name="inr"> <name>inr</name>
                <event> <name>1_arm_1</name> <field> <name>cbc_lbdtc</name> <value>1905-10-01</value> </field> </event>
            </form>
        </all_form_events>
    </person>
    <person study_id="99">
        <study_id>99</study_id>
        <all_form_events>
            <form form_name="cbc"> <name>cbc</name>
                <event> <name>1_arm_1</name>
                    <field> <name>cbc_lbdtc</name> <value>1905-10-01</value> </field>
                    <field> <name>wbc_lborres</name> <value>3.0</value> </field>
                    <field> <name>wbc_lbstat</name> <value/> </field>
                    <field> <name>neut_lborres</name> <value>500</value> </field>
                    <field> <name>neut_lbstat</name> <value/> </field>
                </event>
            </form>
            <form form_name="inr"> <name>inr</name>
                <event> <name>1_arm_1</name>
                        <field> <name>inr_lbdtc</name> <value>1906-12-01</value> </field>
                        <field> <name>inr_lborres</name> <value/> </field>
                        <field> <name>inr_lbstat</name> <value>NOT_DONE</value> </field>
                </event>
            </form>
        </all_form_events>
    </person>
    <person study_id="98">
        <study_id>98</study_id>
        <all_form_events>
            <form form_name="cbc"> <name>cbc</name>
                <event> <name>1_arm_1</name> <field> <name>cbc_lbdtc</name> <value></value> </field> </event>
                <event> <name>1_arm_2</name> <field> <name>cbc_lbdtc</name> <value></value> </field> </event>
            </form>
        </all_form_events>
    </person>

</person_form_event>
"""
        form_details    = {'Total_cbc_Forms': 3, 'Total_inr_Forms': 2}
        subject_details = {
            '98'  : {'Total_cbc_Forms' : 1 },
            '99'  : {'Total_cbc_Forms' : 1, 'Total_inr_Forms' : 1 },
            '100' : {'Total_cbc_Forms' : 1, 'Total_inr_Forms' : 1 }
        }
        report_data = {
            'total_subjects'        : 3,
            'form_details'          : form_details,
            'subject_details'       : subject_details,
            'errors'                : []
        }

        #redi.logger.info(__name__ + "#test_send_person_form_data_to_redcap() xml: " + pfe_xml)
        email_settings = { }
        redcap_settings = {
            'redcap_uri':'http://localhost:8998/redi/api',
            'token'     : '121212',
            'verify_ssl': False
        }

        class MockDataRepository(object):
            def store(self, data):
                pass

        # Check if REDCap is alive
        client = redi_lib.get_redcap_client(redcap_settings, email_settings)
        pfe_repo = MockDataRepository()
        skip_blanks = False
        summary = redi_lib.init_summary()

        # Loop through the Person_Form_Event tree and generate arrays of dictionaries
        pfe_tree = etree.ElementTree(etree.fromstring(pfe_xml))
        root = pfe_tree.getroot()
        persons = root.xpath('//person')

        for person in persons:
            summary['total_subjects'] += 1
            study_id = person.get('study_id')

            forms = person.xpath('./all_form_events/form')
            for form in forms:
                form_name = form.get('form_name')
                fk = FormKey(study_id, form_name)
                form_summary = redi_lib._send_person_form_data_to_redcap(
                    client, pfe_repo, study_id, form, skip_blanks)
                summary = redi_lib._update_summary(summary, fk, form_summary)

        #print summary
        self.assertEqual(report_data['total_subjects'],     summary['total_subjects'])
        self.assertEqual(report_data['form_details'],       summary['form_details'])
        self.assertEqual(report_data['subject_details'],    summary['subject_details'])
        self.assertEqual(report_data['errors'],             summary['errors'])

    def tearDown(self):
        return()

if __name__ == "__main__":
    unittest.main()

