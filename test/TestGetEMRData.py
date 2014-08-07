import unittest
import os
import tempfile
import pysftp
from mock import patch
import utils.GetEmrData as GetEmrData
import utils.SimpleConfigParser as SimpleConfigParser


class TestGetEMRData(unittest.TestCase):
	
	def setUp(self):
		self.temp_folder = tempfile.mkdtemp('/')
		input_string = '''"NAME","COMPONENT_ID","RESULT","REFERENCE_UNIT","DATE_TIME_STAMP","STUDY_ID"
"RNA","1905","<5","IU/mL","1907-05-21 05:50:00","999-0059"
"EGFR","1740200","eGFR result is => 60 ml/min/1.73M2","ml/min/1.73M2","1903-11-27 15:13:00","999-0059"
"HEMATOCRIT","1534436",">27&<30","%","","999-0059"'''
		with open(self.temp_folder+"raw.txt", 'w+') as f:
			f.write(input_string)
		settings_input = '''system_log_file = log/log.txt
emr_sftp_server_hostname = fake.server
emr_sftp_server_username = username
emr_sftp_server_password = password
emr_sftp_project_name = tmp
emr_data_file = output.csv
emr_log_file = log.txt
emr_log_file_destination = log/log.txt'''
		with open(self.temp_folder+"temp_settings.ini", 'w+') as cf:
			cf.write(settings_input)
		self.settings = SimpleConfigParser.SimpleConfigParser()
		self.settings.read(self.temp_folder+"temp_settings.ini")
		self.settings.set_attributes()

	def dummy_connect(host, username, password):
		pass

	def dummy_download(source, destination, server):
		pass

	def dummy_upload(source, server):
		pass

	@patch.multiple(pysftp, Connection=dummy_connect)
	@patch.multiple(GetEmrData, download_file=dummy_download, upload_file=dummy_upload)

	def test_get_emr_data(self):		
		GetEmrData.get_emr_data(self.temp_folder, self.settings)
		with open(self.temp_folder + 'raw.xml') as f:
			result = f.read()
		expected = '''<?xml version="1.0" encoding="utf8"?>
<study>
    <subject>
        <NAME>RNA</NAME>
        <COMPONENT_ID>1905</COMPONENT_ID>
        <RESULT>&lt;5</RESULT>
        <REFERENCE_UNIT>IU/mL</REFERENCE_UNIT>
        <DATE_TIME_STAMP>1907-05-21 05:50:00</DATE_TIME_STAMP>
        <STUDY_ID>999-0059</STUDY_ID>
    </subject>
    <subject>
        <NAME>EGFR</NAME>
        <COMPONENT_ID>1740200</COMPONENT_ID>
        <RESULT>eGFR result is =&gt; 60 ml/min/1.73M2</RESULT>
        <REFERENCE_UNIT>ml/min/1.73M2</REFERENCE_UNIT>
        <DATE_TIME_STAMP>1903-11-27 15:13:00</DATE_TIME_STAMP>
        <STUDY_ID>999-0059</STUDY_ID>
    </subject>
    <subject>
        <NAME>HEMATOCRIT</NAME>
        <COMPONENT_ID>1534436</COMPONENT_ID>
        <RESULT>&gt;27&amp;&lt;30</RESULT>
        <REFERENCE_UNIT>%</REFERENCE_UNIT>
        <DATE_TIME_STAMP></DATE_TIME_STAMP>
        <STUDY_ID>999-0059</STUDY_ID>
    </subject>
</study>
'''
		self.assertEqual(result, expected)

	def tearDown(self):
		os.remove(self.temp_folder + "raw.txt")
		os.remove(self.temp_folder + "raw.xml")
		os.remove(self.temp_folder + "temp_settings.ini")
		try:
			os.rmdir(self.temp_folder)
		except OSError:
			raise LogException("Folder " + self.temp_folder + "is not empty, hence cannot be deleted.")

if __name__ == "__main__":
    unittest.main()
