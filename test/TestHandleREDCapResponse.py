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
import os
from redi import redi
from redi import upload

DEFAULT_DATA_DIRECTORY = os.getcwd()

class TestHandleErrorsInREDCapResponse(unittest.TestCase):

    def setUp(self):
        redi.configure_logging(DEFAULT_DATA_DIRECTORY)
        self.study_id = 123


    def test_handle_errors_in_redcap_xml_response_records(self):
        """
        Test the correctness of function
        upload.handle_errors_in_redcap_xml_response()
        """
        self.report_data = {
                'errors':[]
            }

        self.redcap_error = """{
            "error": "There were data validation errors",
            "records": [
                    {
                        "record": "1 (1_arm_1)",
                        "field_name": "wbc_lborres",
                        "value": "5.4",
                        "message": "This field is located on a form that is locked."
                    },
                    {
                        "record": "1 (1_arm_1)",
                        "field_name": "wbc_x",
                        "value": "5.5",
                        "message": "This field is located on a form that is locked."
                    }

                ]
            }"""

        # Verify that the report_data contains the error
        # after calling `handle_errors_in_redcap_xml_response`
        upload.handle_errors_in_redcap_xml_response(self.study_id, self.redcap_error, self.report_data)
        self.assertTrue(2 == len(self.report_data['errors']))


    def test_handle_errors_in_redcap_xml_response_fields(self):
        """
        Test the correctness of function
        upload.handle_errors_in_redcap_xml_response()
        """
        self.report_data = {
                'errors':[]
            }

        self.redcap_error = """{
            'error': 'The following fields were not found in the project',
            'fields': ['hcv_im_supplb_vborres', 'hcv_im_nxtrust', 'hcv_im_supplb_lbnote']
        }"""

        upload.handle_errors_in_redcap_xml_response(self.study_id, self.redcap_error, self.report_data)
        self.assertTrue(1 == len(self.report_data['errors']))


        self.redcap_error = """{
            'error': "Missing subjects",
            'subjects': ['1', '2']
        }"""


        upload.handle_errors_in_redcap_xml_response(self.study_id, self.redcap_error, self.report_data)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
