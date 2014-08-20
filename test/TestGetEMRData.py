import unittest
import shutil
import tempfile
import pysftp
from mock import patch
import utils.GetEmrData as GetEmrData
from utils.GetEmrData import EmrConnectionDetails


class TestGetEMRData(unittest.TestCase):

    def _noop(*args, **kwargs):
        pass

    @patch.multiple(pysftp, Connection=_noop)
    @patch.multiple(GetEmrData, download_file=_noop, upload_file=_noop)
    def test_get_emr_data(self):
        temp_folder = tempfile.mkdtemp('/')
        input_string = '''"NAME","COMPONENT_ID","RESULT","REFERENCE_UNIT","DATE_TIME_STAMP","STUDY_ID"
"RNA","1905","<5","IU/mL","1907-05-21 05:50:00","999-0059"
"EGFR","1740200","eGFR result is => 60 ml/min/1.73M2","ml/min/1.73M2","1903-11-27 15:13:00","999-0059"
"HEMATOCRIT","1534436",">27&<30","%","","999-0059"'''
        with open(temp_folder+"raw.txt", 'w+') as f:
            f.write(input_string)

        props = EmrConnectionDetails('fake.server',
            'username',
            'password',
            'tmp',
            'output.csv'
            )

        GetEmrData.get_emr_data(temp_folder, props)

        with open(temp_folder + 'raw.xml') as f:
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
        shutil.rmtree(temp_folder)
