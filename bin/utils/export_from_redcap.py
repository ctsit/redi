#!/usr/bin/env python

import sys
import urllib
import httplib
import argparse

# example usage: ./export_records.py token=<token> content=record format=xml
# ./export_records.py token=727D123244B55048136834EEB796D86E content=record format=csv

# export records
# export_records.py token=727D123244B55048136834EEB796D86E content=record format=csv type=flat forms=demographics
# export_records.py token=727D123244B55048136834EEB796D86E content=record format=csv type=eav forms=cbc

# Set the url and path to the API
host = '127.0.0.1:8998'
path = '/redcap/api/'

def main():

   parser = argparse.ArgumentParser(description='Read some data from a REDCap Project')
   parser.add_argument('--token', dest='token', default='727D123244B55048136834EEB796D86E',
                      help='Specify the authentication/authorization token that will provide access to the REDCap project')
   parser.add_argument('--content', dest='content', default='record',
                      help='Specify the kind of data to return')
   parser.add_argument('--format', dest='format', default='csv',
                      help='Specify the format for the returned data: csv, json, xml')
   parser.add_argument('--type', dest='type', default='eav',
                      help='Specify the type for the returned data: eav, flat')
   parser.add_argument('--forms', dest='forms',
                      help='Specify the forms whose values should be to returned')
   parser.add_argument('--fields', dest='fields',
                      help='Specify the fields whose values should be to returned')

   args = vars(parser.parse_args())

   c = httplib.HTTPConnection(host)
   c.request('POST', path, urllib.urlencode(args), {'Content-Type': 'application/x-www-form-urlencoded'})
   r = c.getresponse()
   print(r.read())
   c.close()

if __name__ == '__main__':
   main()
