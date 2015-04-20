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
# Copyright (c) 2015, University of Florida
# All rights reserved.
#
# Distributed under the BSD 3-Clause License
# For full text of the BSD 3-Clause License see http://opensource.org/licenses/BSD-3-Clause
"""
SimpleConfigParser

Simple configuration file parser: Python module to parse configuration files
without sections. Based on ConfigParser from the standard library.

Author: Philippe Lagadec

Project website: http://www.decalage.info/python/configparser

Inspired from an idea posted by Fredrik Lundh:
http://mail.python.org/pipermail/python-dev/2002-November/029987.html

Usage: see end of source code and http://docs.python.org/library/configparser.html
"""

__author__ = 'Philippe Lagadec'
__version__ = '0.02'

#--- LICENSE ------------------------------------------------------------------

# The SimpleConfigParser Python module is copyright (c) Philippe Lagadec 2009-2010
#
# By obtaining, using, and/or copying this software and/or its associated
# documentation, you agree that you have read, understood, and will comply with
# the following terms and conditions:
#
# Permission to use, copy, modify, and distribute this software and its
# associated documentation for any purpose and without fee is hereby granted,
# provided that the above copyright notice appears in all copies, and that both
# that copyright notice and this permission notice appear in supporting
# documentation, and that the name of the author not be used in advertising or
# publicity pertaining to distribution of the software without specific,
# written prior permission.
#
# THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE, INCLUDING
# ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL
# THE AUTHOR BE LIABLE FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL DAMAGES OR
# ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER
# IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

#-------------------------------------------------------------------------
# CHANGELOG
# 2009-02-12 v0.01 PL: - initial version
# 2010-03-15 v0.02 PL: - updated tests and comments

#-------------------------------------------------------------------------
# TODO:
# - implement read() using the base class code

#=== IMPORTS ==================================================================

import ConfigParser
import StringIO
import logging
import os
import sys
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

#=== CONSTANTS ================================================================

# section name for options without section:
NOSECTION = 'NOSECTION'

DEFAULT_MESSAGE_NO_VALUE = "Required parameter '{0}' does not have a"\
                           " value in {1}."

DEFAULT_MESSAGE = "\nPlease set it with the appropriate value. Refer to "\
                  "config-example/settings.ini for assistance.\nProgram "\
                  "will now terminate..."

# Dictionary containing required file-related parameters along with custom
# message to be displayed in case of error
required_files_dict = {
    "raw_xml_file": "\nIt should specify the name of the file containing raw"\
    " data. ",
    "translation_table_file": "\nIt should specify the name of the required "\
    "xml file containing translation table. ",
    "form_events_file": "\nIt should specify the name of the required xml "\
    "file containing empty form events. ",
    "research_id_to_redcap_id": "\nIt should specify the name of the xml "\
    "file containing mapping of research ids to redcap ids. ",
    "component_to_loinc_code_xml": "\nIt should specify the name of the "\
    "required xml file  containing a mapping of clinical component ids to "\
    "loinc codes. "
}

required_server_parameters_list = [
    'redcap_uri',
    'token',
    'redcap_support_receiver_email',
    'smtp_host_for_outbound_mail',
    'smtp_port_for_outbound_mail',
    'emr_sftp_server_hostname',
    'emr_sftp_server_username',
    'emr_sftp_project_name',
    'emr_data_file']

# Dictionary containing optional parameters along with their default values
optional_parameters_dict = {
    "report_file_path": "report.xml",
    "input_date_format": "%Y-%m-%d %H:%M:%S",
    "output_date_format": "%Y-%m-%d",
    "report_file_path2": "report.html",
    "sender_email": "please-do-not-reply@example.com",
    "project": "DEFAULT_PROJECT",
    "rules": {},
    "preprocessors": {},
    "batch_warning_days": 13,
    "rate_limiter_value_in_redcap": 600,
    "batch_info_database": "redi.db",
    "send_email": 'N',
    "receiver_email": "test@example.com",
    "verify_ssl": True,
    "replace_fields_in_raw_data_xml": None,
    "include_rule_errors_in_report": False,
    "redcap_support_sender_email": 'please-do-not-reply@example.com',
    "emr_sftp_server_port": 22,
    "emr_sftp_server_password": None,
    "emr_sftp_server_private_key": None,
    "emr_sftp_server_private_key_pass": None,
    "is_sort_by_lab_id": True,
    "max_retry_count": 10,
}

class ConfigurationError(Exception):
    pass

#=== CLASSES ==================================================================

class SimpleConfigParser(ConfigParser.RawConfigParser):

    """
    Simple configuration file parser: based on ConfigParser from the standard
    library, slightly modified to parse configuration files without sections.

    Inspired from an idea posted by Fredrik Lundh:
    http://mail.python.org/pipermail/python-dev/2002-November/029987.html
    """

    def read(self, filename):
        if not os.path.exists(filename):
            logger.exception("Cannot find settings file: {0}. Program will "\
                             "now terminate...".format(filename))
            sys.exit()

        self.filename = filename
        text = open(filename).read()
        f = StringIO.StringIO("[%s]\n" % NOSECTION + text)
        self.readfp(f, filename)

    def getoption(self, option):
        'get the value of an option'
        opt_as_string = self.get(NOSECTION, option)
        try:
            # if the conversion to boolean fails we keep the string value
            opt_as_bool = to_bool(opt_as_string)
            return opt_as_bool
        except ValueError:
            pass
        return opt_as_string

    def getoptionslist(self):
        'get a list of available options'
        return self.options(NOSECTION)

    def hasoption(self, option):
        """
        return True if an option is available, False otherwise.
        (NOTE: do not confuse with the original has_option)
        """
        return self.has_option(NOSECTION, option)

    def set_attributes(self):
        # Check if configuration file is empty
        if not self.getoptionslist():
            message = "ERROR: Configuration file '{0}' is empty! Program "\
                      "will now terminate...".format(self.filename)
            logger.error(message)
            sys.exit()

        else:
            self.check_parameters()


    def check_parameters(self):
        """
        handle required and default optional_parameters_dict
        """
        # check for required file parameters
        # handled separately as these need a custom message to be displayed
        for option in required_files_dict:
            if not self.hasoption(option) or self.getoption(option) == "":
                message = DEFAULT_MESSAGE_NO_VALUE.format(option, \
                    self.filename) + required_files_dict[option] +\
                     DEFAULT_MESSAGE
                logger.error(message)
                sys.exit()
            else:
                setattr(self, option, self.getoption(option))

        # check for required server and emr parameters
        for option in required_server_parameters_list:
            if not self.hasoption(option) or self.getoption(option) == "":
                message = DEFAULT_MESSAGE_NO_VALUE.format(option, \
                    self.filename) + DEFAULT_MESSAGE
                logger.error(message)
                sys.exit()
            else:
                logger.debug("Setting required parameter {} = {} "\
                        .format(option, self.getoption(option)))
                setattr(self, option, self.getoption(option))

        # check for receiver email if send_email = 'Y'
        if self.hasoption('send_email') and self.getoption('send_email'):
            if not self.hasoption('receiver_email') or \
            self.getoption('receiver_email') == "":
                message = DEFAULT_MESSAGE_NO_VALUE.format(option, \
                    self.filename) + DEFAULT_MESSAGE
                logger.error(message)
                sys.exit()

        # set optional parameters with default values if missing
        for option in optional_parameters_dict:
            if not self.hasoption(option) or self.getoption(option) == "":
                logger.warn("Parameter '{0}' in {1} does not have"\
                " a value. Default value '{2}' applied.".format(option, \
                    self.filename, optional_parameters_dict[option]))
                setattr(self, option, optional_parameters_dict[option])
            else:
                setattr(self, option, self.getoption(option))

#=== End class ================================================================
def to_bool(value):
    """
    Helper function for translating strings into booleans
    @see test/TestReadConfig.py
    """
    valid = {
        'true':  True,  't': True,  '1': True,  'y' : True,
        'false': False, 'f': False, '0': False, 'n' : False
        }

    if not isinstance(value, str):
        raise ValueError('Cannot check boolean value. Not a string.')

    lower_value = value.lower()
    if lower_value in valid:
        return valid[lower_value]
    else:
        raise ValueError('Not a boolean string: "%s"' % value)

#=== MAIN =====================================================================

if __name__ == '__main__':
    # simple tests when launched as a script instead of imported as module:

    ##cp = ConfigParser.ConfigParser()
    # this raises an exception:
    # ConfigParser.MissingSectionHeaderError: File contains no section headers.
    # cp.read('config_without_section.ini')

    print 'SimpleConfigParser tests:'

    filename = 'sample_config_no_section.ini'
    cp = SimpleConfigParser()
    print 'Parsing %s...' % filename
    cp.read(filename)

    print 'Sections:', cp.sections()
    # print cp.items(NOSECTION)
    print 'getoptionslist():', cp.getoptionslist()
    for option in cp.getoptionslist():
        print "getoption('%s') = '%s'" % (option, cp.getoption(option))
    print "hasoption('wrongname') =", cp.hasoption('wrongname')

    print
    print "Print out options by attribute instead of recursing the list"
    cp.set_attributes()
    print cp.option1
    print cp.option2
