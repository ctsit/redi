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
import os
import sys
from lxml import etree
from StringIO import StringIO
import time
from redi import redi
from redi import report

DEFAULT_DATA_DIRECTORY = os.getcwd()

class TestCreateSummaryReport(unittest.TestCase):
    """
    Unit test for `redi.create_summary_report()`
    """

    def setUp(self):
        """
        Prepare data structures
        """
        redi.configure_logging(DEFAULT_DATA_DIRECTORY)
        self.test_report_params = {
            'project': 'hcvtarget-uf',
            'report_file_path': os.path.join(DEFAULT_DATA_DIRECTORY, 'unittest_report.xml'),
            'redcap_uri': 'https://hostname.org',
            'is_sort_by_lab_id': True,
            }

        self.test_report_data = {
            'total_subjects': 5,
            'form_details': {
                'Total_chemistry_Forms': 22,
                'Total_cbc_Forms': 53
            },
            'subject_details': {
                '60': {'cbc_Forms': 1, 'chemistry_Forms': 1, 'lab_id': '999-0060'},
                '61': {'cbc_Forms': 2, 'chemistry_Forms': 1, 'lab_id': '999-0061'},
                '63': {'cbc_Forms': 11, 'chemistry_Forms': 4, 'lab_id': '999-0063'},
                '59': {'cbc_Forms': 39, 'chemistry_Forms': 16, 'lab_id': '999-0059'}
            },
            'errors' : [],
        }

        self.test_alert_summary = {
            'multiple_values_alert': [
                'This is multiple values alert 1',
                'This is multiple values alert 2',
                'This is multiple values alert 3'],
            'max_event_alert': [
                'This is max event alert 1',
                'This is max event alert 2',
                'This is max event alert 3']
        }

        self.specimen_taken_time_summary = {'total': 15, 'blank': 3}
        self.duration_dict = {
            'all' : {
                'start': "2014-01-01 00:00:00",
                'end': "2014-01-01 00:00:01",
            }
        }

        self.expected_xml = '''
<report>
    <header>
        <project>hcvtarget-uf</project>
        <date>'''+time.strftime("%m/%d/%Y")+'''</date>
        <redcapServerAddress>https://hostname.org</redcapServerAddress>
    </header>
    <summary>
        <subjectCount>5</subjectCount>
        <forms>
            <form>
                <form_name>Total_cbc_Forms</form_name>
                <form_count>53</form_count>
            </form>
            <form>
                <form_name>Total_chemistry_Forms</form_name>
                <form_count>22</form_count>
            </form>
        </forms>
    </summary>
    <alerts>
        <tooManyForms>
        <eventAlert>
            <message>This is max event alert 1</message>
        </eventAlert>
        <eventAlert>
            <message>This is max event alert 2</message>
        </eventAlert>
        <eventAlert>
            <message>This is max event alert 3</message>
        </eventAlert>
        </tooManyForms>
        <tooManyValues>
            <valuesAlert>
                <message>This is multiple values alert 1</message>
            </valuesAlert>
            <valuesAlert>
                <message>This is multiple values alert 2</message>
            </valuesAlert>
            <valuesAlert><message>This is multiple values alert 3</message>
        </valuesAlert></tooManyValues>
    </alerts>
    <subjectsDetails>
        <subject>
        <redcap_id>59</redcap_id>
        <forms>
            <form>
                <form_name>cbc_Forms</form_name>
                <form_count>39</form_count>
            </form>
            <form>
                <form_name>chemistry_Forms</form_name>
                <form_count>16</form_count>
            </form>
        </forms>
        <lab_id>999-0059</lab_id>
        </subject>
        <subject>
            <redcap_id>60</redcap_id>
            <forms>
                <form>
                    <form_name>cbc_Forms</form_name>
                    <form_count>1</form_count></form>
                <form>
                    <form_name>chemistry_Forms</form_name>
                    <form_count>1</form_count>
                </form>
            </forms>
            <lab_id>999-0060</lab_id>
        </subject>
        <subject>
            <redcap_id>61</redcap_id>
            <forms>
                <form>
                    <form_name>cbc_Forms</form_name>
                    <form_count>2</form_count>
                </form>
                <form>
                    <form_name>chemistry_Forms</form_name>
                    <form_count>1</form_count>
                </form>
            </forms>
            <lab_id>999-0061</lab_id>
        </subject>
        <subject>
            <redcap_id>63</redcap_id>
            <forms>
                <form>
                    <form_name>cbc_Forms</form_name>
                    <form_count>11</form_count>
                </form>
                <form>
                    <form_name>chemistry_Forms</form_name>
                    <form_count>4</form_count>
                </form>
            </forms>
            <lab_id>999-0063</lab_id>
        </subject>
    </subjectsDetails>
    <errors/>
    <summaryOfSpecimenTakenTimes>
        <total>15</total>
        <blank>3</blank>
        <percent>20.0</percent>
    </summaryOfSpecimenTakenTimes>
    <sort_details_by>lab_id</sort_details_by>
    <time_all_start>00:00:00</time_all_start>
    <time_all_end>00:00:01</time_all_end>
    <time_all_diff>0:00:01</time_all_diff>
</report>'''

        self.schema_str = StringIO('''\
            <xs:schema attributeFormDefault="unqualified" elementFormDefault="qualified" xmlns:xs="http://www.w3.org/2001/XMLSchema">
  <xs:element name="report">
    <xs:complexType>
      <xs:sequence>
        <xs:element name="header">
          <xs:complexType>
            <xs:sequence>
              <xs:element type="xs:string" name="project"/>
              <xs:element type="xs:string" name="date"/>
              <xs:element type="xs:string" name="redcapServerAddress"/>
            </xs:sequence>
          </xs:complexType>
        </xs:element>
        <xs:element name="summary">
          <xs:complexType>
            <xs:sequence>
              <xs:element type="xs:byte" name="subjectCount"/>
              <xs:element name="forms">
                <xs:complexType>
                  <xs:sequence>
                    <xs:element name="form" maxOccurs="unbounded" minOccurs="0">
                      <xs:complexType>
                        <xs:sequence>
                          <xs:element type="xs:string" name="form_name"/>
                          <xs:element type="xs:byte" name="form_count"/>
                        </xs:sequence>
                      </xs:complexType>
                    </xs:element>
                  </xs:sequence>
                </xs:complexType>
              </xs:element>
            </xs:sequence>
          </xs:complexType>
        </xs:element>
        <xs:element name="alerts">
          <xs:complexType>

             <xs:sequence>
              <xs:element name="tooManyForms">
                <xs:complexType>
                  <xs:sequence>
                    <xs:element name="eventAlert" maxOccurs="unbounded" minOccurs="0">
                      <xs:complexType>
                        <xs:sequence>
                          <xs:element type="xs:string" name="message"/>
                        </xs:sequence>
                      </xs:complexType>
                    </xs:element>
                  </xs:sequence>
                </xs:complexType>
              </xs:element>

              <xs:element name="tooManyValues">
                <xs:complexType>
                  <xs:sequence>
                    <xs:element name="valuesAlert" maxOccurs="unbounded" minOccurs="0">
                      <xs:complexType>
                        <xs:sequence>
                          <xs:element type="xs:string" name="message"/>
                        </xs:sequence>
                      </xs:complexType>
                    </xs:element>
                  </xs:sequence>
                </xs:complexType>
              </xs:element>
            </xs:sequence>
          </xs:complexType>
        </xs:element>
        <xs:element name="subjectsDetails">
          <xs:complexType>
            <xs:sequence>
              <xs:element name="subject" maxOccurs="unbounded" minOccurs="0">
                <xs:complexType>
                  <xs:sequence>
                    <xs:element type="xs:int" name="redcap_id"/>
                    <xs:element name="forms">
                      <xs:complexType>
                        <xs:sequence>
                          <xs:element name="form" maxOccurs="unbounded" minOccurs="0">
                            <xs:complexType>
                              <xs:sequence>
                                <xs:element type="xs:string" name="form_name"/>
                                <xs:element type="xs:byte" name="form_count"/>
                              </xs:sequence>
                            </xs:complexType>
                          </xs:element>
                        </xs:sequence>
                      </xs:complexType>
                    </xs:element>
                    <xs:element type="xs:string" name="lab_id"/>
                  </xs:sequence>
                </xs:complexType>
              </xs:element>
            </xs:sequence>
          </xs:complexType>
        </xs:element>
        <xs:element name="errors">
        </xs:element>
        <xs:element name="summaryOfSpecimenTakenTimes">
          <xs:complexType>
            <xs:sequence>
              <xs:element type="xs:byte" name="total"/>
              <xs:element type="xs:byte" name="blank"/>
              <xs:element type="xs:float" name="percent"/>
            </xs:sequence>
          </xs:complexType>
        </xs:element>
        <xs:element name="sort_details_by"></xs:element>
        <xs:element name="time_all_start"></xs:element>
        <xs:element name="time_all_end"></xs:element>
        <xs:element name="time_all_diff"></xs:element>
      </xs:sequence>
    </xs:complexType>
  </xs:element>
</xs:schema>''')
        return

    def test_create_summary_report(self):
        """
        Validates the summary xml structure using xsd
        Validate the summary xml content
        """
        sys.path.append('config')

        class MockWriter(object):
            def __call__(self, *args, **kwargs):
                #expected call: write(tree, report_file_path)
                self.result = args[0]
        writer = MockWriter()

        creator = report.ReportCreator(
            self.test_report_params['report_file_path'],
            self.test_report_params['project'],
            self.test_report_params['redcap_uri'],
            self.test_report_params['is_sort_by_lab_id'],
            writer)

        creator.create_report(self.test_report_data, self.test_alert_summary,
                              self.specimen_taken_time_summary, self.duration_dict)

        result = writer.result
        result_string = etree.tostring(result)
        #print result_string
        xmlschema_doc = etree.parse(self.schema_str)
        xml_schema = etree.XMLSchema(xmlschema_doc)
        # validate the xml against the xsd schema
        self.assertEqual(xml_schema.validate(result), True)

        # validate the actual data in xml but strip the white space first
        parser = etree.XMLParser(remove_blank_text=True)
        clean_tree = etree.XML(self.expected_xml, parser=parser)
        self.expected_xml = etree.tostring(clean_tree)
        self.assertEqual(self.expected_xml, result_string)

    def tearDown(self):
        # delete the created xml file
        try:
            os.remove(self.test_report_params['report_file_path'])
        except:
            pass

if __name__ == '__main__':
    unittest.main()
