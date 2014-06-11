'''
@author : Radha
email : rkandula@ufl.edu

This file is to test the function send_data_to_redcap of bin/redi.py
This file should be run from the project level folder (one level up from /bin)

'''
import unittest
import os
import sys
file_dir = os.path.dirname(os.path.realpath(__file__))
goal_dir = os.path.join(file_dir, "../")
proj_root = os.path.abspath(goal_dir)+'/'
sys.path.append(proj_root+'test')
sys.path.append(proj_root+'bin')

from wsgiref.simple_server import make_server
import requests
import redi
import thread

class TestSendDatatoRedcap(unittest.TestCase):

    def setUp(self):
        # configure logging
        redi.configure_logging()
        # start a server in seperate thread
        thread.start_new_thread(self.server_setup,())

    #@all_requests
    def response_content(self, environ, start_response):
        response_body = 'OK'
        status = '200 OK'
        response_headers = [('Content-Type', 'text/plain'),
                  ('Content-Length', str(len(response_body)))]
        start_response(status, response_headers)
        body= ''  # b'' for consistency on Python 3.0
        try:
            length= int(environ.get('CONTENT_LENGTH', '0'))
        except ValueError:
            length= 0
        if length!=0:
            # got the body of the response
            body = environ['wsgi.input'].read(length)
            required_params = {'returnContent':'ids',
                            'format':'csv',
                            'data':'',
                            'returnFormat':'xml',
                            'overwriteBehavior':'normal',
                            'content':'record',
                            'token':'4CE405878D219CFA5D3ADF7F9AB4E8ED',
                            'type':'eav'}
            import re
            if re.search(r'returnContent\=ids',body).group() != 'returnContent=ids' or \
                re.search(r'format\=csv',body).group() != 'format=csv' or \
                re.search(r'data\=',body).group() != 'data=' or \
                re.search(r'returnFormat\=xml',body).group() != 'returnFormat=xml' or \
                re.search(r'overwriteBehavior\=normal',body).group() != 'overwriteBehavior=normal' or \
                re.search(r'content\=record',body).group() != 'content=record' or \
                re.search(r'token\=4CE405878D219CFA5D3ADF7F9AB4E8ED',body).group() != 'token=4CE405878D219CFA5D3ADF7F9AB4E8ED' or \
                re.search(r'type\=eav',body).group() != 'type=eav':
                response_body = 'NOT OK'

        #print response_body
        return [response_body]

    '''This function runs as a seperate thread.
        used to start the server at localhost:8051
    '''
    def server_setup(self):
        httpd = make_server('localhost', 8051, self.response_content)
        httpd.handle_request()

    '''This is the test function which runs independent of server
        it makes call to the function in test 'testSendDatatoRedcap'
        and tests for the response returned by the mock server

    '''
    def testSendDatatoRedcap(self):
        # the test properties except the localhost are intentionally
        # blanked out just to test the posting of content to the server
        # mentioned in variable test_data
        test_properties = {'host' : 'localhost:8051',
                        'path' : '', "is_secure" : '',
                        'token': '4CE405878D219CFA5D3ADF7F9AB4E8ED'}

        global test_data
        test_data = ''
        # This is the actual send_data_to_redcap function in test
        returned = redi.send_data_to_redcap(test_properties,data=test_data,
                        token=test_properties['token'])
        #print returned
        # checking for the response from the server started with the expected
        # data from user side
        assert returned == 'OK'

    def tearDown(self):
        return()

if __name__ == "__main__":
    unittest.main()
