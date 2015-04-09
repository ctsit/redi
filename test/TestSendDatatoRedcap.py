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

    def dummy_init(*args, **kwargs):
        """This function is called in place of RedcapClient's constructor"""
        return None

    def dummy_send_data_to_redcap(*args, **kwargs):
        """No time out has occurred or function retries to send the data on 
        network connection timeout"""
        return True

    def dummy_send_data_to_redcap_timeout(*args, **kwargs):
        """retry_count has reached 10 so the function stops resending data 
        and exits gracefully"""
        return True

    @patch.multiple(redcapClient.RedcapClient, __init__=dummy_init)
    @patch.multiple(redcapClient.RedcapClient,
        send_data_to_redcap=dummy_send_data_to_redcap)
    def test_send_data_to_redcap(self):
        self.assertTrue(redcapClient.RedcapClient().send_data_to_redcap(
            self.test_data, False, 0))

    @patch.multiple(redcapClient.RedcapClient, __init__=dummy_init)
    @patch.multiple(redcapClient.RedcapClient,
        send_data_to_redcap=dummy_send_data_to_redcap)
    def test_send_data_to_redcap_retry_3(self):       
        self.assertTrue(redcapClient.RedcapClient().send_data_to_redcap(
            self.test_data, 'overwrite', 3))

    @patch.multiple(redcapClient.RedcapClient, __init__=dummy_init)
    @patch.multiple(redcapClient.RedcapClient,
        send_data_to_redcap=dummy_send_data_to_redcap_timeout)
    def test_send_data_to_redcap_retry_10(self):
        self.assertTrue(redcapClient.RedcapClient().send_data_to_redcap(
            self.test_data, 'overwrite', 10))

    def tearDown(self):
        return()

if __name__ == "__main__":
    unittest.main()
