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

import unittest
import tempfile
import os
from lxml import etree
from mock import patch
from redi import redi
from redi.utils import redi_email
from redi.utils.redcapClient import RedcapClient
from redi.utils import SimpleConfigParser
from requests import RequestException

file_dir = os.path.dirname(os.path.realpath(__file__))
goal_dir = os.path.join(file_dir, "../")
proj_root = os.path.abspath(goal_dir)+'/'

DEFAULT_DATA_DIRECTORY = os.getcwd()

class TestResearchIdToRedcapId(unittest.TestCase):

    def setUp(self):
        self.sortedData = """
<study>
    <subject>
        <NAME>HEMOGLOBIN</NAME>
        <loinc_code>1534435</loinc_code>
        <RESULT>10.5</RESULT>
        <REFERENCE_LOW>12.0</REFERENCE_LOW>
        <REFERENCE_HIGH>16.0</REFERENCE_HIGH>
        <REFERENCE_UNIT>g/dL</REFERENCE_UNIT>
        <DATE_TIME_STAMP/>
        <STUDY_ID>999-0001</STUDY_ID>
    <timestamp/><redcapFormName>cbc</redcapFormName><eventName/><formDateField>cbc_lbdtc</formDateField><formCompletedFieldName>cbc_complete</formCompletedFieldName><formImportedFieldName>cbc_nximport</formImportedFieldName><redcapFieldNameValue>hemo_lborres</redcapFieldNameValue><redcapFieldNameUnits>hemo_lborresu</redcapFieldNameUnits><redcapFieldNameStatus>hemo_lbstat</redcapFieldNameStatus>
    </subject>
    <subject>
        <NAME>WBC</NAME>
        <loinc_code>999</loinc_code>
        <RESULT>5.4</RESULT>
        <REFERENCE_LOW/>
        <REFERENCE_HIGH/>
        <REFERENCE_UNIT/>
        <DATE_TIME_STAMP/>
        <STUDY_ID>999-0002</STUDY_ID>
    <timestamp/><redcapFormName>cbc</redcapFormName><eventName/><formDateField>cbc_lbdtc</formDateField><formCompletedFieldName>cbc_complete</formCompletedFieldName><formImportedFieldName>cbc_nximport</formImportedFieldName><redcapFieldNameValue>wbc_lborres</redcapFieldNameValue><redcapFieldNameUnits>wbc_lborresu</redcapFieldNameUnits><redcapFieldNameStatus>wbc_lbstat</redcapFieldNameStatus>
    </subject>
</study>"""

        self.data = etree.ElementTree(etree.fromstring(self.sortedData))
        self.serverResponse = """
<records>
<item><dm_subjid><![CDATA[76]]></dm_subjid><redcap_event_name><![CDATA[1_arm_1]]></redcap_event_name><dm_usubjid><![CDATA[999-0059]]></dm_usubjid></item>
</records>"""

        self.output = """<study>
    <subject lab_id="999-0001">
        <NAME>HEMOGLOBIN</NAME>
        <loinc_code>1534435</loinc_code>
        <RESULT>10.5</RESULT>
        <REFERENCE_LOW>12.0</REFERENCE_LOW>
        <REFERENCE_HIGH>16.0</REFERENCE_HIGH>
        <REFERENCE_UNIT>g/dL</REFERENCE_UNIT>
        <DATE_TIME_STAMP/>
        <STUDY_ID>1</STUDY_ID>
    <timestamp/><redcapFormName>cbc</redcapFormName><eventName/><formDateField>cbc_lbdtc</formDateField><formCompletedFieldName>cbc_complete</formCompletedFieldName><formImportedFieldName>cbc_nximport</formImportedFieldName><redcapFieldNameValue>hemo_lborres</redcapFieldNameValue><redcapFieldNameUnits>hemo_lborresu</redcapFieldNameUnits><redcapFieldNameStatus>hemo_lbstat</redcapFieldNameStatus>
    </subject>
    <subject lab_id="999-0002">
        <NAME>WBC</NAME>
        <loinc_code>999</loinc_code>
        <RESULT>5.4</RESULT>
        <REFERENCE_LOW/>
        <REFERENCE_HIGH/>
        <REFERENCE_UNIT/>
        <DATE_TIME_STAMP/>
        <STUDY_ID>2</STUDY_ID>
    <timestamp/><redcapFormName>cbc</redcapFormName><eventName/><formDateField>cbc_lbdtc</formDateField><formCompletedFieldName>cbc_complete</formCompletedFieldName><formImportedFieldName>cbc_nximport</formImportedFieldName><redcapFieldNameValue>wbc_lborres</redcapFieldNameValue><redcapFieldNameUnits>wbc_lborresu</redcapFieldNameUnits><redcapFieldNameStatus>wbc_lbstat</redcapFieldNameStatus>
    </subject>
</study>"""

        self.expect = etree.tostring(etree.fromstring(self.output))
        self.configuration_directory = tempfile.mkdtemp('/')
        self.research_id_to_redcap_id = "research_id_to_redcap_id_map.xml"
        try:
            f = open(os.path.join(self.configuration_directory, self.research_id_to_redcap_id), "w+")
            f.write("""
<subject_id_field_mapping>
    <redcap_id_field_name>dm_subjid</redcap_id_field_name>
    <research_id_field_name>dm_usubjid</research_id_field_name>
</subject_id_field_mapping>""")
            f.close()
        except:
            print("setUp failed to create file '" + self.research_id_to_redcap_id + "'")

    def dummy_redcapClient_initializer(self, redcap_uri, token, verify_ssl):
        pass
        
    def dummy_get_data_from_redcap(self,records_to_fecth=[],events_to_fetch=[], fields_to_fetch=[], forms_to_fetch=[], return_format='xml'):
        dummy_output = """<?xml version="1.0" encoding="UTF-8" ?>
<records>
    <item>
        <dm_subjid><![CDATA[1]]></dm_subjid>
        <redcap_event_name><![CDATA[1]]></redcap_event_name>
        <dm_usubjid><![CDATA[999-0001]]></dm_usubjid>
    </item>
    <item>
        <dm_subjid><![CDATA[2]]></dm_subjid>
        <redcap_event_name><![CDATA[1]]></redcap_event_name>
        <dm_usubjid><![CDATA[999-0002]]></dm_usubjid>
    </item>
</records>"""
        return dummy_output

    def dummy_redcapClient_initializer_with_exception(self, redcap_uri, token, verify_ssl):
        raise RequestException

    def dummy_send_email_redcap_connection_error(email_settings):
        raise Exception

    def test_research_id_to_redcap_id_converter(self):
        redi.configure_logging(DEFAULT_DATA_DIRECTORY)

        class MockRedcapClient(RedcapClient):
            def __init__(self, context):
                self.__context = context

            def send_data_to_redcap(self, data, overwrite=False):
                raise NotImplementedError()

            def get_data_from_redcap(self, records_to_fetch=None,
                                     events_to_fetch=None, fields_to_fetch=None,
                                     forms_to_fetch=None, return_format='xml'):
                return self.__context.dummy_get_data_from_redcap(
                    records_to_fetch, events_to_fetch, fields_to_fetch,
                    forms_to_fetch, return_format)

        redi.research_id_to_redcap_id_converter(self.data,
                                                MockRedcapClient(self),
                                                self.research_id_to_redcap_id,
                                                self.configuration_directory)
        result = etree.tostring(self.data)
        self.assertEqual(self.expect, result)

    def tearDown(self):
        try:
            os.unlink(os.path.join(self.configuration_directory, self.research_id_to_redcap_id))
        except:
            print("setUp failed to unlink file '" + "research_id_to_redcap_id_map.xml" + "'")
        try:
            os.rmdir(self.configuration_directory)
        except OSError:
            raise LogException("Folder " + self.configuration_directory + "is not empty, hence cannot be deleted.")
        return()

if __name__ == "__main__":
    unittest.main()
