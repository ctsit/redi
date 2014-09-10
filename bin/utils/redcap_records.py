#!/usr/bin/env python
#
# This software is distributed under the BSD 3-Clause License
#
# Copyright (c) 2014, University of Florida
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the University of Florida nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE UNIVERSITY OF FLORIDA BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import sys
import argparse
import json
from redcap import Project, RedcapError

def main():

    parser = argparse.ArgumentParser(
        description='Read some data from a REDCap Project')
    parser.add_argument(
        '--token',
        dest='token',
        default='',
        required=True,
        help='Specify the authentication/authorization token that will provide access to the REDCap project')
    parser.add_argument(
        '--url',
        dest='url',
        default='',
        required=True,
        help='Specify the url of the REDCap server to connect with')
    parser.add_argument(
        '--verify_ssl',
        dest='verify_ssl',
        default=True,
        help='Specify whether the SSL cert of the REDCap server should be checked')
    parser.add_argument('-i', '--import_data', dest='import_data', default='',
                        help='Specify the input data file to load into REDCap')
    parser.add_argument(
        '-f',
        '--forms',
        dest='forms',
        default='',
        help='Specify a list of forms, separated by spaces, for which data should be returned.')
    parser.add_argument(
        '-t',
        '--type',
        choices=['json', 'csv', 'xml'],
        dest='data_type',
        default='csv',
        help='Specify the file type used as input or output. Valid types: json, csv, xml')
    parser.add_argument(
        '--fields',
        dest='fields',
        default='',
        help='Specify a list of fields, separated by spaces, for which data should be returned.')
    parser.add_argument(
        '-e',
        '--events',
        dest='events',
        default='',
        help='Specify a list of events, separated by spaces, for which data should be returned.')

    # prepare the arguments we were given
    args = vars(parser.parse_args())

    # According to http://pycap.readthedocs.org/en/latest/api.html
    # allowed data_types are: csv, json, xml
    data_type = args['data_type']

    # Turn the 'verify_ssl' parameter into the truth value we need to make a
    # REDCap connection
    if args['verify_ssl'] == 'y':
        args['verify_ssl'] = True
    else:
        args['verify_ssl'] = False

    # Attempt to connect to the REDCap project
    try:
        project = Project(args['url'], args['token'], "", args['verify_ssl'])
    except:
        print "Cannot connect to project at " + args['url'] + ' with token ' + args['token']
        quit()

    # either we export data...
    if args['import_data'] == '':
        my_forms = args['forms'].split()
        my_fields = args['fields'].split()
        my_events = args['events'].split()
        data = project.export_records(
            forms=my_forms,
            format = data_type,
            fields=my_fields,
            events=my_events,
            event_name='unique')
        if 'json' == data_type:
            print json.dumps(data, ensure_ascii=False)
        else:
            print str(data)
    else:
        # ...or we import data
        file = args['import_data']
        try:
            input = open(file, 'r')
        except IOError:
            print "Cannot open file " + file
            quit()
        if 'json' == data_type:
            json_data = json.load(input)
            response = project.import_records(json_data)
        else:
            response = project.import_records(input.read(), format = data_type)

        print response

if __name__ == '__main__':
    main()
