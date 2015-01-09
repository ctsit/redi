'''
@author : Ruchi
email : ruchi.desai@ufl.edu

This file is to test the function send_data_to_redcap

'''
import unittest
from mock import patch, call
from redi import redi
from redi.utils import redcapClient

class TestSendDatatoRedcap(unittest.TestCase):

    def setUp(self):
        self.test_data = ''

    def dummy_send_data_to_redcap(*args, **kwargs):
        """No time out occurred or retrying"""
        return True

    def dummy_send_data_to_redcap_timeout(*args, **kwargs):
        """Time out occurred and exiting"""
        return True

    @patch.multiple(redcapClient,send_data_to_redcap=dummy_send_data_to_redcap)
    def testSendDatatoRedcapNoTimeOut(self):
        self.assertTrue(redcapClient.RedcapClient.send_data_to_redcap(data,
            False, 0)        

    @patch.multiple(redcapClient,send_data_to_redcap=dummy_send_data_to_redcap_timeout)
    def testSendDatatoRedcapNoTimeOut10(self, retry_count):        
        self.assertTrue(redcapClient.RedcapClient.send_data_to_redcap(data,
            'overwrite', 10)

    # @patch.multiple(redcapClient,
    #     send_data_to_redcap=dummy_send_data_to_redcap_timeout)
    # def testSendDatatoRedcapNoTimeOut11(self, retry_count):        
    #     self.assertTrue(redcapClient.RedcapClient.send_data_to_redcap(data,
    #         'overwrite', 11)

    def tearDown(self):
        return()

if __name__ == "__main__":
    unittest.main()
