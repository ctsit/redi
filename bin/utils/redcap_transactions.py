import logging
import httplib
from urllib import urlencode
import os
import sys
from lxml import etree
# This addresses the issues with relative paths
file_dir = os.path.dirname(os.path.realpath(__file__))
goal_dir = os.path.join(file_dir, "../../")
proj_root = os.path.abspath(goal_dir)+'/'
sys.path.insert(0, proj_root+'bin')


class redcap_transactions:
    """A class for getting data from redcap instace"""
    def __init__(self):
        self.data = []
        self.params = {}
        
    def init_redcap_interface(self, setup, redcap_uri, logger):
        '''This function initializes the variables requrired to get data from redcap
        interface. This reads the data from the setup.json and fills the dict
        with required properties.
        Mohan'''
        logger.info('Initializing redcap interface')
        host = ''
        path = ''
        token = setup['token']

        if redcap_uri is None:
            host = '127.0.0.1:8998'
            path = '/redcap/api/'
        if token is None:
            token = '4CE405878D219CFA5D3ADF7F9AB4E8ED'

        uri_list = redcap_uri.split('//')
        http_str = ''
        if uri_list[0] == 'https:':
            is_secure = True
        else:
            is_secure = False
        after_httpstr_list = uri_list[1].split('/', 1)
        host = http_str + '//' + after_httpstr_list[0]
        host = after_httpstr_list[0]
        path = '/' + after_httpstr_list[1]
        properties = {'host' : host, 'path' : path, "is_secure" : is_secure,
                                'token': token}

        logger.info("redcap interface initialzed")
        return properties

    def get_data_from_redcap(self, properties, token, logger, formtype, format_param='xml',
            type_param='flat', return_format='xml'):
        '''This function gets data from redcap using POST method
        for getting person index data formtype='Person_Index' must be passed as argument
        for getting redcap data formtype='RedCap' must be passed as argument

        '''
        logger.info('getting data from redcap')
        params = {}
        if token != '':
            params['token'] = token
        else:
            params['token'] = properties['token']
        params['content'] = 'record'
        params['format'] = format_param
        params['type'] = type_param
        params['returnFormat'] = return_format
        params['fields'] = properties['fields']

        if properties['is_secure'] is True:
            redcap_connection = httplib.HTTPSConnection(properties['host'])
        else:
            redcap_connection = httplib.HTTPConnection(properties['host'])
        logger.debug('getting data from path : %s', properties['path'])
        redcap_connection.request('POST', properties['path'], urlencode(params),
            {'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'text/plain'})
        response_buffer = redcap_connection.getresponse()
        returned = response_buffer.read()
        logger.info('***********RESPONSE RECEIVED FROM REDCAP***********')
        logger.debug(returned)
        redcap_connection.close()
        return returned

    def get_redcap_connection(self,properties, token, format_param='csv',
        type_param='eav', overwrite_behavior='normal', return_content='ids',
        return_format='xml'):
        '''This function sends data to redcap using POST method

        '''
        params = {}
        if token != '':
            self.params['token'] = token
        else:
            self.params['token'] = properties['token']
        self.params['content'] = 'record'
        self.params['format'] = format_param
        self.params['type'] = type_param
        self.params['overwriteBehavior'] = overwrite_behavior
        self.params['returnContent'] = return_content
        self.params['returnFormat'] = return_format

        if properties['is_secure'] is True:
            redcap_connection = httplib.HTTPSConnection(properties['host'])
        else:
            redcap_connection = httplib.HTTPConnection(properties['host'])
    
        return redcap_connection   

    def send_data(self, redcap_connection, properties, data, logger):
        self.params['data'] = data
        redcap_connection.request('POST', properties['path'], urlencode(self.params),
            {'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'text/plain'})
        response_buffer = redcap_connection.getresponse()
        returned = response_buffer.read()
        #print(returned)
        logger.info('***********RESPONSE RECEIVED FROM REDCAP***********')
        logger.debug(returned)
        return returned
