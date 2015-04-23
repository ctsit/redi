# Contributors:
# Christopher P. Barnes <senrabc@gmail.com>
# Andrei Sura: github.com/indera
# Mohan Das Katragadda <mohan.das142@gmail.com>
# Philip Chase <philipbchase@gmail.com>
# Ruchi Vivek Desai <ruchivdesai@gmail.com>
# Taeber Rapczak <taeber@ufl.edu>
# Josh Hanna <josh@hanna.io>
# Copyright (c) 2015, University of Florida
# All rights reserved.
#
# Distributed under the BSD 3-Clause License
# For full text of the BSD 3-Clause License see http://opensource.org/licenses/BSD-3-Clause

__copyright__ = "Copyright 2015, University of Florida"
__license__ = "BSD 3-Clause"

import unittest
from StringIO import StringIO

from lxml import etree

import cancel
from redi.form import Form

FIELD_NAME = "test_field_name"
TEST_FIELD_VALUE1 = "CANCELLED"
TEST_FIELD_VALUE2 = "CANCELED"
TEST_FIELD_VALUE3 = "CANCEL"
TEST_FIELD_VALUE4 = "s0meJUnk"
TEST_FIELD_VALUE5 = " "
TEST_FIELD_VALUE6 = ""

class TestCancelRuleProcessing(unittest.TestCase):

    def test_cancel_present(self):
        data = ("<person_form_event><person><study_id>9001</study_id><all_form_events><form>"
                "  <name>Best. Form. Ever.</name>"
                "  <event>"
                "    <name>The Event</name>"
                "    <field>"
                "      <name>The Field</name>"
                "      <value>some value</value>"
                "    </field>"
                "    <field>"
                "      <name>{0}</name>"
                "      <value>{1}</value>"
                "    </field>"
                "  </event>"
                "</form></all_form_events></person></person_form_event>"
                .format(FIELD_NAME, TEST_FIELD_VALUE3))
        tree = parse_xml_from_string(data)

        form = cancel.run_rules(tree)

        self.check_form(form, FIELD_NAME, expected_value='')

    def test_cancelled_present(self):
        data = ("<person_form_event><person><study_id>9001</study_id><all_form_events><form>"
                "  <name>Best. Form. Ever.</name>"
                "  <event>"
                "    <name>The Event</name>"
                "    <field>"
                "      <name>The Field</name>"
                "      <value>some value</value>"
                "    </field>"
                "    <field>"
                "      <name>{0}</name>"
                "      <value>{1}</value>"
                "    </field>"
                "  </event>"
                "</form></all_form_events></person></person_form_event>"
                .format(FIELD_NAME, TEST_FIELD_VALUE1))
        tree = parse_xml_from_string(data)

        form = cancel.run_rules(tree)

        self.check_form(form, FIELD_NAME, expected_value='')

    def test_canceled_present(self):
        data = ("<person_form_event><person><study_id>9001</study_id><all_form_events><form>"
                "  <name>Best. Form. Ever.</name>"
                "  <event>"
                "    <name>The Event</name>"
                "    <field>"
                "      <name>The Field</name>"
                "      <value>some value</value>"
                "    </field>"
                "    <field>"
                "      <name>{0}</name>"
                "      <value>{1}</value>"
                "    </field>"
                "  </event>"
                "</form></all_form_events></person></person_form_event>"
                .format(FIELD_NAME, TEST_FIELD_VALUE2))
        tree = parse_xml_from_string(data)

        form = cancel.run_rules(tree)

        self.check_form(form, FIELD_NAME, expected_value='')


    def test_cancel_not_present(self):
        data = ("<person_form_event><person><study_id>9001</study_id><all_form_events><form>"
                "  <name>Best. Form. Ever.</name>"
                "  <event>"
                "    <name>The Event</name>"
                "    <field>"
                "      <name>The Field</name>"
                "      <value>some value</value>"
                "    </field>"
                "    <field>"
                "      <name>{0}</name>"
                "      <value>{1}</value>"
                "    </field>"
                "  </event>"
                "</form></all_form_events></person></person_form_event>"
                .format(FIELD_NAME, TEST_FIELD_VALUE4))
        tree = parse_xml_from_string(data)

        form = cancel.run_rules(tree)

        self.check_form(form, FIELD_NAME, expected_value=TEST_FIELD_VALUE4)

    def test_cancel_not_present_space_present(self):
        data = ("<person_form_event><person><study_id>9001</study_id><all_form_events><form>"
                "  <name>Best. Form. Ever.</name>"
                "  <event>"
                "    <name>The Event</name>"
                "    <field>"
                "      <name>The Field</name>"
                "      <value>some value</value>"
                "    </field>"
                "    <field>"
                "      <name>{0}</name>"
                "      <value>{1}</value>"
                "    </field>"
                "  </event>"
                "</form></all_form_events></person></person_form_event>"
                .format(FIELD_NAME, TEST_FIELD_VALUE5))
        tree = parse_xml_from_string(data)

        form = cancel.run_rules(tree)

        self.check_form(form, FIELD_NAME, expected_value=TEST_FIELD_VALUE5)

    def test_cancel_with_no_value(self):
        data = ("<person_form_event><person><study_id>9001</study_id><all_form_events><form>"
                "  <name>Best. Form. Ever.</name>"
                "  <event>"
                "    <name>The Event</name>"
                "    <field>"
                "      <name>The Field</name>"
                "      <value>some value</value>"
                "    </field>"
                "    <field>"
                "      <name>{0}</name>"
                "      <value>{1}</value>"
                "    </field>"
                "  </event>"
                "</form></all_form_events></person></person_form_event>"
                .format(FIELD_NAME, TEST_FIELD_VALUE6))
        tree = parse_xml_from_string(data)

        form = cancel.run_rules(tree)

        self.check_form(form, FIELD_NAME, expected_value=TEST_FIELD_VALUE6)


    def check_form(self, form, field_name, expected_value):
        for event in form.events():
            for field in event.fields():
                #print field.name+" - "+field_name+" - "+field.value
                if field.name == field_name:
                    self.assertEquals(field.value, expected_value)

def parse_xml_from_string(xml):
    return etree.parse(StringIO(xml))
