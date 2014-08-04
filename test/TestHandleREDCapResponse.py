import json
import unittest
import tempfile
import os
import sys

from lxml import etree

sys.path.append('bin/')
import redi
import redi_lib

class TestHandleErrorsInREDCapResponse(unittest.TestCase):

    def setUp(self):
        redi.configure_logging()
        return()


    def test_handle_errors_in_redcap_xml_response_with_error(self):
        
        self.redcap_error = """{"error": "There were data validation errors","records": [{"record": "1 (1_arm_1)", "field_name": "wbc_lborres",
								"value": "5.4",
								"message": "This field is located on a form that is locked. You must first unlock this form for this record"}]}"""
        self.report_data = {'errors':[]}
        self.assertTrue(redi_lib.handle_errors_in_redcap_xml_response(self.redcap_error,self.report_data))
        
    def test_handle_errors_in_redcap_xml_response_with_no_error(self):
        #In a sucessful data import redcap returns a list of number of records imported.
        self.redcap_pass = """[1]"""
        self.report_data = {'errors':[]}
        self.assertFalse(redi_lib.handle_errors_in_redcap_xml_response(self.redcap_pass,self.report_data))
        
    def test_handle_errors_in_redcap_xml_response_with_no_errorKey_in_report_data(self):
        
        self.redcap_pass = """{"error": "There were data validation errors","records": [{"record": "1 (1_arm_1)", "field_name": "wbc_lborres",
								"value": "5.4",
								"message": "This field is located on a form that is locked. You must first unlock this form for this record"}]}"""
        self.report_data = {}
        self.assertTrue(redi_lib.handle_errors_in_redcap_xml_response(self.redcap_pass,self.report_data))
        
    def tearDown(self):
        return()

if __name__ == '__main__':
    unittest.main()
