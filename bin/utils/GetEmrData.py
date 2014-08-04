#/usr/bin/env python
# Python module to connect to server using sftp, get raw EMR data, get log file and return possibly modified
# log file to the server

import os
import argparse
import tempfile
import pysftp
import SimpleConfigParser
import re

file_dir = os.path.dirname(os.path.realpath(__file__))
goal_dir = os.path.join(file_dir, "../")
proj_root = os.path.abspath(goal_dir) + '/'


def download_file(source, destination, server):
    try:
        server.get(source, destination)
    except IOError:
        raise Exception(source + " not found")


def upload_file(source, server):
    try:
        server.put(source)
    except Exception:
        raise Exception("Error while uploading " + source)


def data_preprocessing(input_filename, output_filename):
    # replace &, >, < with &amp;, &>;, &<;
    with open(input_filename, 'r') as file1:
        new_string = ""
        for line in file1:
            new_string = new_string + re.sub('(&)', r'&amp;', line)
            new_string = re.sub('(<)', r'&lt;', new_string)
            new_string = re.sub('(>)', r'&gt;', new_string)
    with open(output_filename, 'w') as file2:
        file2.write(new_string)


def generate_xml(input_filename, output_filename):
    input_string = proj_root + "utils/csv2xml.py --input-encoding=cp1252  --output-encoding=utf8 --header \
    --delimiter=,  --xml-declaration -tstudy -rsubject --output-file=" + output_filename + " \
    " + input_filename
    os.system(input_string)


def cleanup(file_to_delete):
    os.remove(file_to_delete)


def get_emr_data(configuration_directory_path, settings):
    # parsing settings.ini file to get server details
    sftp_server = settings.emr_sftp_server_hostname
    username = settings.emr_sftp_server_username
    password = settings.emr_sftp_server_password
    project_name = settings.emr_sftp_project_name + "/"
    data_file = settings.emr_data_file
    log_file = settings.emr_log_file
    server = pysftp.Connection(
        host=sftp_server,
        username=username,
        password=password)
    # download csv file
    download_file(
        project_name +
        data_file,
        configuration_directory_path +
        'raw.txt',
        server)
    # download log file
    download_file(
        project_name +
        log_file,
        settings.emr_log_file_destination,
        server)
    # replace certain characters with escape sequences
    data_preprocessing(
        configuration_directory_path +
        'raw.txt',
        configuration_directory_path +
        'rawEscaped.txt')
    # run csv2xml.py to generate data in xml format
    generate_xml(
        configuration_directory_path +
        'rawEscaped.txt',
        configuration_directory_path +
        'raw.xml')
    # delete rawEscaped.txt
    cleanup(configuration_directory_path + 'rawEscaped.txt')
