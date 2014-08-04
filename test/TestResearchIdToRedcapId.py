import unittest
import tempfile
import os
from lxml import etree
from mock import patch
import redi
from utils.redcapClient import redcapClient
import utils.SimpleConfigParser as SimpleConfigParser

file_dir = os.path.dirname(os.path.realpath(__file__))
goal_dir = os.path.join(file_dir, "../")
proj_root = os.path.abspath(goal_dir)+'/'


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
        <STUDY_ID>999-0059</STUDY_ID>
    <timestamp/><redcapFormName>cbc</redcapFormName><eventName/><formDateField>cbc_lbdtc</formDateField><formCompletedFieldName>cbc_complete</formCompletedFieldName><formImportedFieldName>cbc_nximport</formImportedFieldName><redcapFieldNameValue>hemo_lborres</redcapFieldNameValue><redcapFieldNameUnits>hemo_lborresu</redcapFieldNameUnits><redcapFieldNameStatus>hemo_lbstat</redcapFieldNameStatus></subject>
    <subject>
        <NAME>WBC</NAME>
        <loinc_code>999</loinc_code>
        <RESULT>5.4</RESULT>
        <REFERENCE_LOW/>
        <REFERENCE_HIGH/>
        <REFERENCE_UNIT/>
        <DATE_TIME_STAMP/>
        <STUDY_ID>999-0059</STUDY_ID>
    <timestamp/><redcapFormName>cbc</redcapFormName><eventName/><formDateField>cbc_lbdtc</formDateField><formCompletedFieldName>cbc_complete</formCompletedFieldName><formImportedFieldName>cbc_nximport</formImportedFieldName><redcapFieldNameValue>wbc_lborres</redcapFieldNameValue><redcapFieldNameUnits>wbc_lborresu</redcapFieldNameUnits><redcapFieldNameStatus>wbc_lbstat</redcapFieldNameStatus></subject>
    <subject>
        <NAME>PLATELET COUNT</NAME>
        <loinc_code>1009</loinc_code>
        <RESULT>92</RESULT>
        <REFERENCE_LOW/>
        <REFERENCE_HIGH/>
        <REFERENCE_UNIT/>
        <DATE_TIME_STAMP/>
        <STUDY_ID>999-0059</STUDY_ID>
    <timestamp/><redcapFormName>cbc</redcapFormName><eventName/><formDateField>cbc_lbdtc</formDateField><formCompletedFieldName>cbc_complete</formCompletedFieldName><formImportedFieldName>cbc_nximport</formImportedFieldName><redcapFieldNameValue>plat_lborres</redcapFieldNameValue><redcapFieldNameUnits>plat_lborresu</redcapFieldNameUnits><redcapFieldNameStatus>plat_lbstat</redcapFieldNameStatus></subject>
    <subject>
        <NAME>HEMOGLOBIN</NAME>
        <loinc_code>1534435</loinc_code>
        <RESULT>9.5</RESULT>
        <REFERENCE_LOW>12.0</REFERENCE_LOW>
        <REFERENCE_HIGH>16.0</REFERENCE_HIGH>
        <REFERENCE_UNIT>g/dL</REFERENCE_UNIT>
        <DATE_TIME_STAMP/>
        <STUDY_ID>999-0059</STUDY_ID>
    <timestamp/><redcapFormName>cbc</redcapFormName><eventName/><formDateField>cbc_lbdtc</formDateField><formCompletedFieldName>cbc_complete</formCompletedFieldName><formImportedFieldName>cbc_nximport</formImportedFieldName><redcapFieldNameValue>hemo_lborres</redcapFieldNameValue><redcapFieldNameUnits>hemo_lborresu</redcapFieldNameUnits><redcapFieldNameStatus>hemo_lbstat</redcapFieldNameStatus></subject>
    </study>"""

        self.data = etree.ElementTree(etree.fromstring(self.sortedData))
        self.serverResponse = """<records>
    <item><dm_subjid><![CDATA[3]]></dm_subjid><redcap_event_name><![CDATA[1_arm_1]]></redcap_event_name><dm_usubjid><![CDATA[999-0001]]></dm_usubjid></item>
<item><dm_subjid><![CDATA[76]]></dm_subjid><redcap_event_name><![CDATA[1_arm_1]]></redcap_event_name><dm_usubjid><![CDATA[999-0059]]></dm_usubjid></item>
<item><dm_subjid><![CDATA[5]]></dm_subjid><redcap_event_name><![CDATA[1_arm_1]]></redcap_event_name><dm_usubjid><![CDATA[001-0005]]></dm_usubjid></item></records>"""


        self.output = """<study>
    <subject>
        <NAME>HEMOGLOBIN</NAME>
        <loinc_code>1534435</loinc_code>
        <RESULT>10.5</RESULT>
        <REFERENCE_LOW>12.0</REFERENCE_LOW>
        <REFERENCE_HIGH>16.0</REFERENCE_HIGH>
        <REFERENCE_UNIT>g/dL</REFERENCE_UNIT>
        <DATE_TIME_STAMP/>
        <STUDY_ID>1</STUDY_ID>
    <timestamp/><redcapFormName>cbc</redcapFormName><eventName/><formDateField>cbc_lbdtc</formDateField><formCompletedFieldName>cbc_complete</formCompletedFieldName><formImportedFieldName>cbc_nximport</formImportedFieldName><redcapFieldNameValue>hemo_lborres</redcapFieldNameValue><redcapFieldNameUnits>hemo_lborresu</redcapFieldNameUnits><redcapFieldNameStatus>hemo_lbstat</redcapFieldNameStatus></subject>
    <subject>
        <NAME>WBC</NAME>
        <loinc_code>999</loinc_code>
        <RESULT>5.4</RESULT>
        <REFERENCE_LOW/>
        <REFERENCE_HIGH/>
        <REFERENCE_UNIT/>
        <DATE_TIME_STAMP/>
        <STUDY_ID>1</STUDY_ID>
    <timestamp/><redcapFormName>cbc</redcapFormName><eventName/><formDateField>cbc_lbdtc</formDateField><formCompletedFieldName>cbc_complete</formCompletedFieldName><formImportedFieldName>cbc_nximport</formImportedFieldName><redcapFieldNameValue>wbc_lborres</redcapFieldNameValue><redcapFieldNameUnits>wbc_lborresu</redcapFieldNameUnits><redcapFieldNameStatus>wbc_lbstat</redcapFieldNameStatus></subject>
    <subject>
        <NAME>PLATELET COUNT</NAME>
        <loinc_code>1009</loinc_code>
        <RESULT>92</RESULT>
        <REFERENCE_LOW/>
        <REFERENCE_HIGH/>
        <REFERENCE_UNIT/>
        <DATE_TIME_STAMP/>
        <STUDY_ID>1</STUDY_ID>
    <timestamp/><redcapFormName>cbc</redcapFormName><eventName/><formDateField>cbc_lbdtc</formDateField><formCompletedFieldName>cbc_complete</formCompletedFieldName><formImportedFieldName>cbc_nximport</formImportedFieldName><redcapFieldNameValue>plat_lborres</redcapFieldNameValue><redcapFieldNameUnits>plat_lborresu</redcapFieldNameUnits><redcapFieldNameStatus>plat_lbstat</redcapFieldNameStatus></subject>
    <subject>
        <NAME>HEMOGLOBIN</NAME>
        <loinc_code>1534435</loinc_code>
        <RESULT>9.5</RESULT>
        <REFERENCE_LOW>12.0</REFERENCE_LOW>
        <REFERENCE_HIGH>16.0</REFERENCE_HIGH>
        <REFERENCE_UNIT>g/dL</REFERENCE_UNIT>
        <DATE_TIME_STAMP/>
        <STUDY_ID>1</STUDY_ID>
    <timestamp/><redcapFormName>cbc</redcapFormName><eventName/><formDateField>cbc_lbdtc</formDateField><formCompletedFieldName>cbc_complete</formCompletedFieldName><formImportedFieldName>cbc_nximport</formImportedFieldName><redcapFieldNameValue>hemo_lborres</redcapFieldNameValue><redcapFieldNameUnits>hemo_lborresu</redcapFieldNameUnits><redcapFieldNameStatus>hemo_lbstat</redcapFieldNameStatus></subject>
    </study>"""

        self.expect = etree.tostring(etree.fromstring(self.output))
        # setup_json = proj_root+'config/setup.json'
        # creating dummy settings.ini file
        self.setupFile = tempfile.mkstemp()
        self.input = """{ job_owner_name = John Doe\njob_email = johndoe@example.org\ndata_provider_name = Jane Doe\ndata_provider_email = janedoe@example.org\nsmtp_host_for_outbound_mail = smtp.example.org\nsystem_log_file = log/redi\ntranslation_table_file = TestTranslationTable.xml\nform_events_file = TestFormEvents.xml\nraw_xml_file = TestRaw.xml\nresearch_id_to_redcap_id = research_id_to_redcap_id_map.xml\nsubject_map_header = studyID, mrn, facilityCode, startDate, endDate\\n\nredcap_uri = https://example.org/redcap/api/\ntoken = ABCDEF878D219CFA5D3ADF7F9AB12345"""
        f = open(self.setupFile[1], 'r+')
        f.write(self.input)
        f.close()
        self.settings = SimpleConfigParser.SimpleConfigParser()
        # extracting path of temporary directory in which dummy settings.ini file is located
        last_slash = self.setupFile[1].rfind("/")
        self.configuration_directory = self.setupFile[1][:last_slash]+"/"
        #creating temporary files which read_config and research_id_to_redcap_id_converter functions need
        try:
            f = open(self.configuration_directory+"research_id_to_redcap_id_map.xml", "w+")
            f.write("""<subject_id_field_mapping>
  <redcap_id_field_name>dm_subjid</redcap_id_field_name>
  <research_id_field_name>dm_usubjid</research_id_field_name>
</subject_id_field_mapping>""")
            f.close()
        except:
            print("setUp failed to create file '" + "research_id_to_redcap_id_map.xml" + "'")
        try:
            f = open(self.configuration_directory+"TestTranslationTable.xml", "w+")
        except:
            print("setUp failed to create file '" + "TestTranslationTable.xml" + "'")
        try:
            f = open(self.configuration_directory+"TestFormEvents.xml", "w+")
        except:
            print("setUp failed to create file '" + "TestFormEvents.xml" + "'")
        try:
            f = open(self.configuration_directory+"TestRaw.xml", "w+")
        except:
            print("setUp failed to create file '" + "TestRaw.xml" + "'")
        # parse the settings.ini file
        self.settings.read(self.setupFile[1])
        self.settings.set_attributes()
        redi.read_config(self.setupFile[1],self.configuration_directory, self.settings)

    def dummy_redcapClient_initializer(self,settings):
        pass
        
    def dummy_get_data_from_redcap(self,records_to_fecth=[],events_to_fetch=[], fields_to_fetch=[], forms_to_fetch=[], return_format='xml'):
        dummy_output = """<?xml version="1.0" encoding="UTF-8" ?>
<records>
<item><dm_subjid><![CDATA[1]]></dm_subjid><redcap_event_name><![CDATA[1]]></redcap_event_name><dm_usubjid><![CDATA[999-0059]]></dm_usubjid></item>
</records>"""
        return dummy_output

    @patch.multiple(redcapClient, __init__ = dummy_redcapClient_initializer, get_data_from_redcap = dummy_get_data_from_redcap)
    def test_research_id_to_redcap_id_converter(self):
        self.settings.set_attributes()
        redi.configure_logging(proj_root+'log/redi.log')
        redi.research_id_to_redcap_id_converter(self.data, self.settings,self.configuration_directory)
        result = etree.tostring(self.data)
        self.assertEqual(self.expect, result)

    
    def tearDown(self):
        try:
            os.unlink(self.configuration_directory+"research_id_to_redcap_id_map.xml")
        except:
            print("setUp failed to unlink file '" + "research_id_to_redcap_id_map.xml" + "'")
        try:
            os.unlink(self.configuration_directory+"TestTranslationTable.xml")
        except:
            print("setUp failed to unlink file '" + "TestTranslationTable.xml" + "'")
        try:
            os.unlink(self.configuration_directory+"TestFormEvents.xml")
        except:
            print("setUp failed to unlink file '" + "TestFormEvents.xml" + "'")
        try:
            os.unlink(self.configuration_directory+"TestRaw.xml")
        except:
            print("setUp failed to unlink file '" + "TestRaw.xml" + "'")
        try:
            os.unlink(self.setupFile[1])
        except:
            print("setUp failed to unlink file '" + self.setupFile[1] + "'")
        return()

if __name__ == "__main__":
    unittest.main()
