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
        
        self.redcap_error = """<?xml version="1.0" encoding="UTF-8" ?><hash><error>RedCap Error</error></hash>
        """
        self.report_data = {'errors':[]}
        self.assertTrue(redi_lib.handle_errors_in_redcap_xml_response(self.redcap_error,self.report_data))
        
    def test_handle_errors_in_redcap_xml_response_with_no_error(self):
        
        self.redcap_pass = """<?xml version="1.0" encoding="UTF-8" ?><ids><id>123-4567</id></ids>
        """
        self.report_data = {'errors':[]}
        self.assertFalse(redi_lib.handle_errors_in_redcap_xml_response(self.redcap_pass,self.report_data))
        
    def test_handle_errors_in_redcap_xml_response_with_no_errorKey_in_report_data(self):
        
        self.redcap_pass = """<?xml version="1.0" encoding="UTF-8" ?><hash><error>RedCap Error</error></hash>
        """
        self.report_data = {}
        self.assertRaises(redi.LogException,redi_lib.handle_errors_in_redcap_xml_response,self.redcap_pass,self.report_data)
        
    def tearDown(self):
        return()

if __name__ == '__main__':
    unittest.main()
