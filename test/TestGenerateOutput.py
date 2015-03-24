#!/usr/bin/env python
#
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
TestGenerateOutput.py:

   Verifies the correct functionality 
   of the `generate_output` function
"""

import unittest
import os
from lxml import etree
from redi import redi
from redi import upload
from redi.utils.redcapClient import RedcapClient


DEFAULT_DATA_DIRECTORY = os.getcwd()


class TestGenerateOutput(unittest.TestCase):

    def setUp(self):
        redi.configure_logging(DEFAULT_DATA_DIRECTORY)

    class dummyClass:
        def_field = 'test'

    def test_person_form_event(self):
        string_1_xml = """
<person_form_event>
    <person lab_id="999-0100">
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
    <person lab_id="999-0099">
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
    <person lab_id="999-0098">
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

        form_details    = {'Total_cbc_Forms': 2, 'Total_inr_Forms': 3}
        subject_details = {
                '98'  : {'Total_cbc_Forms' : 0, 'Total_inr_Forms' : 1, 'lab_id': "999-0098" },
                '99'  : {'Total_cbc_Forms' : 1, 'Total_inr_Forms' : 1, "lab_id": "999-0099" },
                '100' : {'Total_cbc_Forms' : 1, 'Total_inr_Forms' : 1, "lab_id": "999-0100" }
        } 
 
        report_data = {
            'total_subjects'        : 3,
            'form_details'          : form_details,
            'subject_details'       : subject_details,
            'errors'                : []
        }

        class MockSentEventIndex(object):
            def __init__(self):
                self.sent_events = []

            def __len__(self):
                return len(self.sent_events)

            def mark_sent(self, study_id_key, form_name, event_name):
                form_event_key = study_id_key, form_name, event_name
                self.sent_events.append(form_event_key)

            def was_sent(self, study_id_key, form_name, event_name):
                form_event_key = study_id_key, form_name, event_name
                return form_event_key in self.sent_events

        class MockRedcapClient(RedcapClient):
            def __init__(self):
                self.project = TestGenerateOutput.dummyClass()

            def get_data_from_redcap(self, records_to_fetch=None,
                                     events_to_fetch=None,
                                     fields_to_fetch=None,
                                     forms_to_fetch=None,
                                     return_format='xml'):
                raise NotImplementedError()

            def send_data_to_redcap(self, data, max_retry_count,
                overwrite=False):
                return """Data sent"""

        etree_1 = etree.ElementTree(etree.fromstring(string_1_xml))
        result = upload.generate_output(etree_1, MockRedcapClient(), 500,
                                        MockSentEventIndex(), 10)
        self.assertEqual(report_data['total_subjects'], result['total_subjects'])
        self.assertEqual(report_data['form_details'], result['form_details'])
        self.assertEqual(report_data['subject_details'], result['subject_details'])
        self.assertEqual(report_data['errors'], result['errors'])


if __name__ == "__main__":
    unittest.main()

