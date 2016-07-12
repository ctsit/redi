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
import logging
import shutil
import tempfile
import pysftp
from mock import patch
from redi.utils import GetEmrData
from redi.utils.GetEmrData import EmrFileAccessDetails

import time
from subprocess import Popen

# Try to silence extra info
logging.getLogger("paramico").addHandler(logging.NullHandler)
logging.getLogger("pysftp").addHandler(logging.NullHandler)

class TestGetEMRData(unittest.TestCase):

    def setUp(self):
        pass


    def _noop(*args, **kwargs):
        pass


    @patch.multiple(pysftp, Connection=_noop)
    @patch.multiple(GetEmrData, download_files=_noop)
    def test_get_emr_data(self):
        """
        This test verifies only that the csv file on the sftp server
        can be transformed to an xml file.
        Note: This test is not concerned with testing the sftp communication"""
        temp_folder = tempfile.mkdtemp('/')
        temp_txt_file = os.path.join(temp_folder, "raw.txt")
        temp_escaped_file = os.path.join(temp_folder, "rawEscaped.txt")
        temp_xml_file = os.path.join(temp_folder, "raw.xml")

        input_string = '''"NAME","COMPONENT_ID","RESULT","REFERENCE_UNIT","DATE_TIME_STAMP","STUDY_ID"
"RNA","1905","<5","IU/mL","1907-05-21 05:50:00","999-0059"
"EGFR","1740200","eGFR result is => 60 ml/min/1.73M2","ml/min/1.73M2","1903-11-27 15:13:00","999-0059"
"HEMATOCRIT","1534436",">27&<30","%","","999-0059"'''

        with open(temp_txt_file, 'w+') as f:
            f.write(input_string)

        props = EmrFileAccessDetails(
            emr_sftp_project_name='/',
            emr_download_list='raw.csv',
            emr_host='localhost',
            emr_username='admin',
            emr_password='admin',
            emr_port='7788',
            emr_private_key=None,
            emr_private_key_pass=None,
            )

        GetEmrData.get_emr_data(temp_folder, props)
        GetEmrData.data_preprocessing(temp_txt_file, temp_escaped_file)
        GetEmrData.generate_xml(temp_escaped_file, temp_xml_file)

        with open(temp_xml_file) as f:
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

    @unittest.skip("Unconditional skipping: test fails under pysftp 0.2.9")
    def test_pysftp_using_rsa_key(self):

        """
        Starts a sftp server and transfers a file
        to verify the connection using a private key.

        Notes:
            - Disble this test if running on the Travis VM fails
                by adding one of the following annotations:
                @unittest.skip("Unconditional skipping")
                @unittest.skipIf(os.getenv('CI', '') > '', reason='Travis VM')
            - Dependency: `sudo easy_install sftpserver`
        """

        # Using a temp folder does not work for some reason
        #temp_folder = tempfile.mkdtemp('/')
        temp_folder = "."
        key_file = os.path.join(temp_folder, 'unittest_pysftp_rsa_key')
        key_file = create_rsa_key(key_file)

        source_file = os.path.join(temp_folder, 'source_file')
        source_file = create_sample_file(source_file)

        # At this point the destination file is empty
        destination_file = os.path.join(temp_folder, 'destination_file')
        proc = None

        try:
            sftp_cmd = "sftpserver --host localhost -p 7788 -l DEBUG -k " + key_file
            proc = Popen(sftp_cmd, shell=True)
            time.sleep(1) # let the server start

            try:
                # this block depends on a running sftp server
                connection_info = get_connection_info(key_file)
                connection_info['port'] = int(connection_info['port'])
                with pysftp.Connection(**connection_info) as sftp:
                    logging.info("User %s connected to sftp server %s" % \
                        (connection_info['username'], connection_info['host']))
                    #print sftp.listdir('.')
                    sftp.get(source_file, destination_file)
            except Exception as e:
                logging.error("Problem connecting to: %s due error: %s" % \
                        (connection_info['host'], e))
        except Exception as e:
            logging.error("Problem starting sftp server due error: %s for file: %s" % \
                    (e, destination_file))
        finally:
            if proc:
                proc.terminate()

        with open(destination_file) as fresh_file:
            actual = fresh_file.read()
            self.assertEqual(actual, "SFTP TEST")

        # Cleanup created files
        os.remove(source_file)
        os.remove(destination_file)
        os.remove(key_file)
        os.remove(key_file +".pub")


def create_rsa_key(rsa_key_file):
    """Create a RSA private key pair to be used by sftp"""
    if not os.path.isfile(rsa_key_file):
        cmd = "ssh-keygen -q -t rsa -N '' -f " + rsa_key_file
        proc = Popen(cmd, shell=True)
        time.sleep(1)
        proc.terminate()
    else:
        logging.warn("RSA key file already exists: %s" % rsa_key_file)

    return rsa_key_file


def create_sample_file(sample_file):
    """ Create a sample file to be transfered ofe sftp"""
    if not os.path.isfile(sample_file):
        try:
            f = open(sample_file, 'w+')
            f.write("SFTP TEST")
            f.flush()
            f.close()
        except IOError as (errno, strerror):
            logging.error("I/O error({0}): {1}".format(errno, strerror))
    else:
        logging.info("Sample file %s already exists" % sample_file)
    return sample_file


def get_connection_info(private_key):
    """Return a dictionary of parameters for creating a sftp connection"""
    access_details = EmrFileAccessDetails(
        emr_sftp_project_name='/',
        emr_download_list='raw.csv',
        emr_host='localhost',
        emr_username='admin',
        emr_password='admin',
        emr_port='7788',
        emr_private_key=private_key,
        emr_private_key_pass=None,
    )

    connection_info = dict(access_details.__dict__)
    # delete unnecessary elements form the dictionary
    del connection_info['sftp_project_name']
    del connection_info['download_list']
    return connection_info


if __name__ == '__main__':
    unittest.main()
