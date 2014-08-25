import unittest
import os
import redi
import redi_lib

file_dir = os.path.dirname(os.path.realpath(__file__))
goal_dir = os.path.join(file_dir, "../")
proj_root = os.path.abspath(goal_dir)+'/'

DEFAULT_DATA_DIRECTORY = os.getcwd()

class TestHandleErrorsInREDCapResponse(unittest.TestCase):

    def setUp(self):
        redi.configure_logging(DEFAULT_DATA_DIRECTORY)
        return()


    def test_handle_errors_in_redcap_xml_response_valid_case(self):
        self.redcap_error = """{"error": "There were data validation errors","records": [{"record": "1 (1_arm_1)", "field_name": "wbc_lborres",
								"value": "5.4",
								"message": "This field is located on a form that is locked. You must first unlock this form for this record"}]}"""
        self.report_data = {'errors':[]}
        self.assertTrue(redi_lib.handle_errors_in_redcap_xml_response(self.redcap_error,self.report_data))
        
    # Below code is made obsolete because we are handling errors only in case of exceptions.We are not checking for errors in valid cases anymore.
    # def test_handle_errors_in_redcap_xml_response_with_no_error(self):
    #     #In a sucessful data import redcap returns a list of number of records imported.
    #     self.redcap_pass = """[1]"""
    #     self.report_data = {'errors':[]}
    #     self.assertFalse(redi_lib.handle_errors_in_redcap_xml_response(self.redcap_pass,self.report_data))
        
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
