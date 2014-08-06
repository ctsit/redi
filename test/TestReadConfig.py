import unittest
import tempfile
import os
import redi
import utils.SimpleConfigParser as SimpleConfigParser

class TestReadConfig(unittest.TestCase):

    def setUp(self):
        self.setupFile = tempfile.mkstemp()
        self.input = """job_owner_name = John Doe\njob_email = johndoe@example.org\ndata_provider_name = Jane Doe\ndata_provider_email = janedoe@example.org\nsmtp_host_for_outbound_mail = smtp.example.org\nsystem_log_file = log/redi\ntranslation_table_file = TestTranslationTable.xml\nform_events_file = TestFormEvents.xml\nraw_xml_file = TestRaw.xml\nsubject_map_header = studyID, mrn, facilityCode, startDate, endDate\\n\nredcap_uri = https://example.org/redcap/api/\ntoken = ABCDEF878D219CFA5D3ADF7F9AB12345"""
        f = open(self.setupFile[1], 'r+')
        f.write(self.input)
        
        f.close()
        last_slash = self.setupFile[1].rfind("/")
        self.configuration_directory = self.setupFile[1][:last_slash]+"/"
        self.files = ['TestTranslationTable.xml', 'TestFormEvents.xml',
            'TestRaw.xml']
        for file in self.files:
            try:
                f = open(self.configuration_directory+file, "w+")
            except:
                print("setUp failed to create file '" + file + "'")

    def test_readConfig(self):
        settings = SimpleConfigParser.SimpleConfigParser()
        settings.read(self.setupFile[1])
        settings.set_attributes()
        redi.read_config(self.setupFile[1],self.configuration_directory,settings)
        self.assertEqual(settings.system_log_file, "log/redi")
        self.assertEqual(settings.translation_table_file,
            "TestTranslationTable.xml")
        self.assertEqual(settings.form_events_file, "TestFormEvents.xml")
        self.assertEqual(settings.raw_xml_file, "TestRaw.xml")
        self.assertEqual(settings.redcap_uri,
            "https://example.org/redcap/api/")
        self.assertEqual(settings.token,
            "ABCDEF878D219CFA5D3ADF7F9AB12345")
        self.assertEqual(settings.smtp_host_for_outbound_mail,
            "smtp.example.org")

    def tearDown(self):
        os.unlink(self.setupFile[1])
        for file in self.files:
            try:
                os.unlink(self.configuration_directory+file)
            except:
                print("setUp failed to unlink file '" + file + "'")

        return()

if __name__ == '__main__':
    unittest.main()
