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
import shutil
import os

from redi import redi
from redi.utils import SimpleConfigParser

class TestReadConfig(unittest.TestCase):

    def setUp(self):
        _configure_redi_logger()

    def test_read_config(self):
        configuration_directory = tempfile.mkdtemp()
        try:
            files = ['TestTranslationTable.xml', 'TestFormEvents.xml',
                     'TestRaw.xml', 'TestResearchIdToRedcapId.xml',
                     'TestComponentToLoincCode.xml']

            for path in files:
                open(os.path.join(configuration_directory, path), 'a').close()

            # SHALL NOT raise exceptions
            redi.read_config(None, configuration_directory, files)

        finally:
            shutil.rmtree(configuration_directory)

    def test_read_config_missing_file_exits(self):
        kwargs = {
            "config_file": None,
            "configuration_directory": "/path/to/missing/folder",
            "file_list": ["doesn't matter, not a file"]
        }
        self.assertRaises(SystemExit, redi.read_config, **kwargs)


    def test_to_bool(self):
        """
        Verify we can convert properly the boolean strings
        """
        self.assertRaises(ValueError, SimpleConfigParser.to_bool, (None))
        self.assertRaises(ValueError, SimpleConfigParser.to_bool, (True))
        self.assertRaises(ValueError, SimpleConfigParser.to_bool, (False))
        self.assertTrue(SimpleConfigParser.to_bool('true'))
        self.assertTrue(SimpleConfigParser.to_bool('t'))
        self.assertTrue(SimpleConfigParser.to_bool('1'))
        self.assertTrue(SimpleConfigParser.to_bool('y'))

        self.assertFalse(SimpleConfigParser.to_bool('false'))
        self.assertFalse(SimpleConfigParser.to_bool('f'))
        self.assertFalse(SimpleConfigParser.to_bool('0'))
        self.assertFalse(SimpleConfigParser.to_bool('n'))

    def test_settings(self):
        settings = SimpleConfigParser.SimpleConfigParser()

        # write settings to a file and then read them right back
        with tempfile.NamedTemporaryFile() as t:
            t.write("""translation_table_file = TestTranslationTable.xml
form_events_file = TestFormEvents.xml
raw_xml_file = TestRaw.xml
research_id_to_redcap_id = TestResearchIdToRedcapId.xml
component_to_loinc_code_xml = TestComponentToLoincCode.xml
redcap_uri = https://example.org/redcap/api/
token = ABCDEF878D219CFA5D3ADF7F9AB12345
smtp_host_for_outbound_mail = smtp.example.org
redcap_support_receiver_email = jdoe@example.com
smtp_port_for_outbound_mail = 22
emr_sftp_server_hostname = TESTSERVER
emr_sftp_server_username = user
emr_sftp_server_password = pswd
emr_sftp_project_name = sample
emr_data_file = data.csv
include_rule_errors_in_report = False
verify_ssl = False
""")
            t.seek(0)
            settings.read(t.name)

        settings.set_attributes()

        self.assertEqual(settings.translation_table_file,
                         "TestTranslationTable.xml")
        self.assertEqual(settings.form_events_file,
                         "TestFormEvents.xml")
        self.assertEqual(settings.raw_xml_file,
                         "TestRaw.xml")
        self.assertEqual(settings.redcap_uri,
                         "https://example.org/redcap/api/")
        self.assertEqual(settings.token,
                         "ABCDEF878D219CFA5D3ADF7F9AB12345")
        self.assertEqual(settings.smtp_host_for_outbound_mail,
                         "smtp.example.org")

        self.assertFalse(settings.include_rule_errors_in_report)
        self.assertFalse(settings.verify_ssl)

def _configure_redi_logger():
    class MockLogger(object):
        def error(self, *args, **kwargs):
            pass

    redi.logger = MockLogger()

if __name__ == "__main__":
    unittest.main()
