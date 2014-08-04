import unittest
import sys
import os
file_dir = os.path.dirname(os.path.realpath(__file__))
goal_dir = os.path.join(file_dir, "../")
proj_root = os.path.abspath(goal_dir)+'/'
sys.path.append(proj_root + 'bin/')
from lxml import etree
import redi
import thread
import requests
from wsgiref.simple_server import make_server
import os

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
        <STUDY_ID>76</STUDY_ID>
    <timestamp/><redcapFormName>cbc</redcapFormName><eventName/><formDateField>cbc_lbdtc</formDateField><formCompletedFieldName>cbc_complete</formCompletedFieldName><formImportedFieldName>cbc_nximport</formImportedFieldName><redcapFieldNameValue>hemo_lborres</redcapFieldNameValue><redcapFieldNameUnits>hemo_lborresu</redcapFieldNameUnits><redcapFieldNameStatus>hemo_lbstat</redcapFieldNameStatus></subject>
    <subject>
        <NAME>WBC</NAME>
        <loinc_code>999</loinc_code>
        <RESULT>5.4</RESULT>
        <REFERENCE_LOW/>
        <REFERENCE_HIGH/>
        <REFERENCE_UNIT/>
        <DATE_TIME_STAMP/>
        <STUDY_ID>76</STUDY_ID>
    <timestamp/><redcapFormName>cbc</redcapFormName><eventName/><formDateField>cbc_lbdtc</formDateField><formCompletedFieldName>cbc_complete</formCompletedFieldName><formImportedFieldName>cbc_nximport</formImportedFieldName><redcapFieldNameValue>wbc_lborres</redcapFieldNameValue><redcapFieldNameUnits>wbc_lborresu</redcapFieldNameUnits><redcapFieldNameStatus>wbc_lbstat</redcapFieldNameStatus></subject>
    <subject>
        <NAME>PLATELET COUNT</NAME>
        <loinc_code>1009</loinc_code>
        <RESULT>92</RESULT>
        <REFERENCE_LOW/>
        <REFERENCE_HIGH/>
        <REFERENCE_UNIT/>
        <DATE_TIME_STAMP/>
        <STUDY_ID>76</STUDY_ID>
    <timestamp/><redcapFormName>cbc</redcapFormName><eventName/><formDateField>cbc_lbdtc</formDateField><formCompletedFieldName>cbc_complete</formCompletedFieldName><formImportedFieldName>cbc_nximport</formImportedFieldName><redcapFieldNameValue>plat_lborres</redcapFieldNameValue><redcapFieldNameUnits>plat_lborresu</redcapFieldNameUnits><redcapFieldNameStatus>plat_lbstat</redcapFieldNameStatus></subject>
    <subject>
        <NAME>HEMOGLOBIN</NAME>
        <loinc_code>1534435</loinc_code>
        <RESULT>9.5</RESULT>
        <REFERENCE_LOW>12.0</REFERENCE_LOW>
        <REFERENCE_HIGH>16.0</REFERENCE_HIGH>
        <REFERENCE_UNIT>g/dL</REFERENCE_UNIT>
        <DATE_TIME_STAMP/>
        <STUDY_ID>76</STUDY_ID>
    <timestamp/><redcapFormName>cbc</redcapFormName><eventName/><formDateField>cbc_lbdtc</formDateField><formCompletedFieldName>cbc_complete</formCompletedFieldName><formImportedFieldName>cbc_nximport</formImportedFieldName><redcapFieldNameValue>hemo_lborres</redcapFieldNameValue><redcapFieldNameUnits>hemo_lborresu</redcapFieldNameUnits><redcapFieldNameStatus>hemo_lbstat</redcapFieldNameStatus></subject>
    </study>"""

        self.expect = etree.tostring(etree.fromstring(self.output))
        setup_json = proj_root+'config/setup.json'
        # parse the setup json
        self.setup = redi.read_config(setup_json)

        # initialize properties
        self.properties = {'host' : 'localhost:8051', 'path' : '/api/', "is_secure" : False,
                        'token': 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'}
        # start a server in seperate thread
        thread.start_new_thread(self.server_setup,())

    #@all_requests
    def response_content(self, environ, start_response):
      response_body = self.serverResponse
      status = '200 OK'
      response_headers = [('Content-Type', 'text/plain'),
                ('Content-Length', str(len(response_body)))]
      start_response(status, response_headers)
      body= ''  # b'' for consistency on Python 3.0
      try:
          length= int(environ.get('CONTENT_LENGTH', '0'))
      except ValueError:
          length= 0
      if length!=0:
          # got the body of the response
          body = environ['wsgi.input'].read(length)
          required_params = {'format':'xml',
                          'returnFormat':'xml',
                          'content':'record',
                          'token':'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
                          'type':'flat'}
          import re
          if  re.search(r'format\=xml',body).group() != 'format=xml' or \
              re.search(r'returnFormat\=xml',body).group() != 'returnFormat=xml' or \
              re.search(r'content\=record',body).group() != 'content=record' or \
              re.search(r'token\=AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',body).group() != 'token=AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA' or \
              re.search(r'type\=flat',body).group() != 'type=flat':
              response_body = 'NOT OK'

      #print response_body
      return [response_body]

    '''This function runs as a seperate thread.
        used to start the server at localhost:8051
    '''
    def server_setup(self):
      httpd = make_server('localhost', 8051, self.response_content)
      httpd.handle_request()

    def test_research_id_to_redcap_id_converter(self):
        redi.configure_logging()

        redi.research_id_to_redcap_id_converter(self.data, self.properties, self.setup)
        result = etree.tostring(self.data)
        self.assertEqual(self.expect, result)

    def tearDown(self):
        return()

if __name__ == "__main__":
    unittest.main()
