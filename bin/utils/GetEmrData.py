"""
Python module to connect to server using sftp, get raw EMR data, get log file
and return possibly modified log file to the server.
"""

import os
import csv
from xml.sax import saxutils

import pysftp

from csv2xml import openio, Writer


class EmrConnectionDetails(object) :
    """
    Encapsulate the settings specific for Emr SFTP connections
    @see #get_emr_data()
    """
    def __init__(self,
            emr_server,
            emr_username,
            emr_password,
            emr_project_name,
            emr_data_file) :

        self.server                 = emr_server
        self.username               = emr_username
        self.password               = emr_password
        self.project_name           = emr_project_name
        self.data_file              = emr_data_file


#============================
# Module level functions
#============================

def download_file(source, destination, server, username, password):
    with pysftp.Connection(host=server, username=username, password=password) as sftp:
        sftp.get(source, destination)


def data_preprocessing(input_filename, output_filename):
    # replace &, >, < with &amp;, &>;, &<;
    with open(input_filename, 'r') as raw, open(output_filename, 'w') as processed:
        for line in raw:
            processed.write(saxutils.escape(line))


def generate_xml(input_filename, output_filename):

    # generate_xml now replicates the functionality from the
    # "__name__ == '__main__'" code block of csv2xml.py. This allows us to use
    # it like another module in our project without having to call os.system().
    class Arguments:
        pass
    args = Arguments()

    # Set the properties which we used to pass as command line arguments
    args.iencoding = 'cp1252'
    args.oencoding = 'utf8'
    args.header = True,
    args.delimiter = ','
    args.declaration = True
    args.root_elem = 'study'
    args.record_elem = 'subject'
    args.ofile = output_filename
    args.ifile = input_filename

    # Now configure the defaults that would've been set if we were to execute
    # csv2xml.py from the command line.
    args.linebreak = u'\n'
    args.escapechar = None
    args.indent = u'    '
    args.quoting = csv.QUOTE_MINIMAL
    args.skipinitialspace = False
    args.field_elem = u'field'
    args.flat_fields = False
    args.doublequote = True
    args.quotechar = '"'
    args.newline_elem = None

    # WARNING! The rest of this function is copied verbatim from csv2xml.py.
    # There should be no differences between these blocks of code whatsoever.
    # TODO: Replace csv2xml.py entirely?
    csv.register_dialect('custom',
                         delimiter=args.delimiter,
                         doublequote=args.doublequote,
                         escapechar=args.escapechar,
                         quotechar=args.quotechar,
                         quoting=args.quoting,
                         skipinitialspace=args.skipinitialspace)
    with openio(args.ifile, mode='r', encoding=args.iencoding,
                newline='') as ifile:
        csvreader = csv.reader(ifile, dialect='custom')
        if args.header:
            args.header = next(csvreader)
        with openio(args.ofile, 'w', args.oencoding) as ofile:
            writer = Writer(ofile, args)
            writer.write_file(csvreader)


def cleanup(file_to_delete):
    os.remove(file_to_delete)


def get_emr_data(configuration_directory_path, props):
    """
    @param configuration_directory_path : string
    @param props                        : EmrConnectionDetails object
    """

    project_name    = props.project_name + "/"
    data_file       = props.data_file
    configuration_directory_path = configuration_directory_path + "/"

    # download csv file
    download_file(
        project_name + data_file,
        configuration_directory_path + 'raw.txt',
        props.server, props.username, props.password)

    # replace certain characters with escape sequences
    data_preprocessing(
        configuration_directory_path + 'raw.txt',
        configuration_directory_path + 'rawEscaped.txt')

    # run csv2xml.py to generate data in xml format
    generate_xml(
        configuration_directory_path + 'rawEscaped.txt',
        configuration_directory_path + 'raw.xml')

    # delete rawEscaped.txt
    cleanup(configuration_directory_path + 'rawEscaped.txt')
