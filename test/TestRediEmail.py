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

import unittest
import smtplib
from mock import patch, call
from redi import redi
from redi.utils.rawxml import RawXml
from redi.utils import redi_email


class TestRediEmail(unittest.TestCase):
    """
    Check functions in the `utils/redi_email` module
    To run individually:
        $ PYTHONPATH=redi python test/TestRediEmail.py
    """

    def setUp(self):
        """ Prepare the settings objects"""
        settings = {
            'smtp_host_for_outbound_mail': "a.com",
            'smtp_port_for_outbound_mail': 1234,
            'redcap_support_sender_email': "support@example.com",
            'redcap_support_receiver_email': "a@example.com b@example.com",
            'redcap_uri': "http://example.com",
            'batch_warning_days': 13,
            'sender_email': 'report_sender@example.com',
            'receiver_email': 'rep_a@example.com rep_b@example.com',
            'project': 'TEST SITE',
            }
        self.settings = type("", (), settings)()
        self.email_settings = redi.get_email_settings(self.settings)
        self.raw_xml = RawXml('', __file__)


    def test_get_email_settings(self):
        """Check if we picked proper values from the global settings"""
        ese = self.email_settings

        self.assertEqual(ese['smtp_host_for_outbound_mail'], "a.com")
        self.assertEqual(ese['smtp_port_for_outbound_mail'], 1234)
        self.assertEqual(ese['redcap_support_sender_email'], \
                "support@example.com")
        self.assertEqual(ese['redcap_support_receiving_list'], \
                ["a@example.com", "b@example.com"])
        self.assertEqual(ese['redcap_uri'], "http://example.com")
        self.assertEqual(ese['batch_warning_days'], 13)
        self.assertEqual(ese['batch_report_sender_email'], \
                "report_sender@example.com")
        self.assertEqual(ese['batch_report_receiving_list'], \
                ["rep_a@example.com", "rep_b@example.com"])
        self.assertEqual(ese['site_name'], "TEST SITE")

    def dummy_send_success(*args, **kwargs):
        """Skip sending email"""
        return True

    def dummy_send_failed(*args, **kwargs):
        """Skip sending email"""
        return False

    @patch.multiple(redi_email, send_email=dummy_send_success)
    def test_success(self):
        """ Verify return true when email is sent"""
        ese = self.email_settings
        self.assertTrue(redi_email.send_email_redcap_connection_error(ese))
        self.assertTrue(redi_email.send_email_input_data_unchanged(ese, self.raw_xml))

    @patch.multiple(redi_email, send_email=dummy_send_failed)
    def test_failed(self):
        """ Verify return false when email is not sent"""
        ese = self.email_settings
        self.assertFalse(redi_email.send_email_redcap_connection_error(ese))
        self.assertFalse(redi_email.send_email_input_data_unchanged(ese, self.raw_xml))

    @patch("smtplib.SMTP")
    def test_mime_email(self, mock_smtp):
        """ Mock the sendmail function """
        ese = self.email_settings
        instance = mock_smtp.return_value
        instance.sendmail.return_value = {}
        refused_list = redi_email.send_email_data_import_completed(ese)
        self.assertIsInstance(refused_list, dict)
        self.assertEqual(refused_list, {})

    @patch("smtplib.SMTP")
    def test_mime_email_exception(self, mock_smtp):
        """ Mock the sendmail exception """
        ese = self.email_settings
        instance = mock_smtp.return_value
        instance.sendmail.side_effect = smtplib.SMTPRecipientsRefused({})
        self.assertRaises(smtplib.SMTPRecipientsRefused,\
                redi_email.send_email_data_import_completed, ese)
        self.assertEqual(instance.sendmail.call_count, 1)

    def tearDown(self):
        """ Remove dictionary"""
        self.email_settings.clear()

if __name__ == '__main__':
    unittest.main()
