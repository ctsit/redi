import json
import unittest
import tempfile
import os
import sys
file_dir = os.path.dirname(os.path.realpath(__file__))
goal_dir = os.path.join(file_dir, "../")
proj_root = os.path.abspath(goal_dir)+'/'
sys.path.append(proj_root + 'bin/')
import redi

class TestReadConfig(unittest.TestCase):

    def setUp(self):
        self.setupFile = tempfile.mkstemp()
        self.input = """{ "job_owner_name": "John Doe",
    "job_email": "johndoe@example.org",
    "data_provider_name": "Jane Doe",
    "data_provider_email": "janedoe@example.org",
    "smtp_host_for_outbound_mail": "smtp.example.org",
    "system_log_file": "log/redi",

    "translation_table_file": "TestTranslationTable.xml",
    "form_events_file": "TestFormEvents.xml",
    "raw_xml_file": "TestRaw.xml",

    "subject_map_header": "studyID, mrn, facilityCode, startDate, endDate\\n",
    "redcap_uri": "https://example.org/redcap/api/",
    "token": "ABCDEF878D219CFA5D3ADF7F9AB12345" }"""
        f = open(self.setupFile[1], 'r+')
        f.write(self.input)
        
        f.close()
        self.files = ['TestTranslationTable.xml', 'TestFormEvents.xml',
            'TestRaw.xml']
        for file in self.files:
            try:
                f = open(proj_root+file, "w+")
            except:
                print("setUp failed to create file '" + file + "'")

    def test_readConfig(self):
        self.setup = redi.read_config(self.setupFile[1])
        self.assertEqual(self.setup['system_log_file'], "log/redi")
        self.assertEqual(self.setup['translation_table_file'],
            "TestTranslationTable.xml")
        self.assertEqual(self.setup['form_events_file'], "TestFormEvents.xml")
        self.assertEqual(self.setup['raw_xml_file'], "TestRaw.xml")
        self.assertEqual(self.setup['redcap_uri'],
            "https://example.org/redcap/api/")
        self.assertEqual(self.setup['token'],
            "ABCDEF878D219CFA5D3ADF7F9AB12345")
        self.assertEqual(self.setup['smtp_host_for_outbound_mail'],
            "smtp.example.org")

    def tearDown(self):
        os.unlink(self.setupFile[1])
        for file in self.files:
            try:
                os.unlink(proj_root+file)
            except:
                print("setUp failed to unlink file '" + file + "'")

        return()

if __name__ == '__main__':
    unittest.main()
