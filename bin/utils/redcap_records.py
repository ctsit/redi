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
from redcap import Project, RedcapError
import re
import pprint


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
        help='Specify whether the SSL cert of the REDCap server should be checked (y/n)')
    parser.add_argument('-i', '--import_data', dest='import_data', default='',
                        help='Specify the input data file to load into REDCap')
    parser.add_argument(
        '-f',
        '--forms',
        dest='forms',
        default='',
        help='Specify a list of forms, separated by spaces, for which data should be returned.')
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

    # Turn the 'verify_ssl' parameter into the truth value we need to make a
    # REDCap connection
    if args['verify_ssl'] == 'y':
        args['verify_ssl'] = True
    elif args['verify_ssl'] == 'n':
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
            fields=my_fields,
            events=my_events,
            format='csv',
            event_name='unique')
        print str(data)
    else:  # ...or we import data
        file = args['import_data']
        try:
            input = open(file, 'r')
        except:
            print "Cannot open file " + file
            quit()
        response = project.import_records(input.read(), format='csv')
        print response

if __name__ == '__main__':
    main()
