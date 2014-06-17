'''
@author : Mohan
email : mohan88@ufl.edu

This file tests for the function create_summary_report and checks if the summary create_summary_report
has been created or not

'''
import unittest
import os
import sys
file_dir = os.path.dirname(os.path.realpath(__file__))
goal_dir = os.path.join(file_dir, "../")
proj_root = os.path.abspath(goal_dir)+'/'
sys.path.append(proj_root+'test')
sys.path.append(proj_root+'bin')

import redi
from lxml import etree
import datetime
from StringIO import StringIO
import time

class TestCreateSummaryReport(unittest.TestCase):

    def setUp(self):
    	redi.configure_logging()
        self.test_report_params = {'project': 'hcvtarget-uf',
        							'report_file_path': proj_root + 'config/report.xml',
        							'redcap_server': 'https://hostname.org'}

        self.test_report_data = {
            'total_subjects': 5,
            'form_details': {
                'Total_chemistry_Forms': 22,
        		'Total_cbc_Forms': 53
            },
        	'subject_details': {
                '60': {'cbc_Forms': 1, 'chemistry_Forms': 1},
                '61': {'cbc_Forms': 2, 'chemistry_Forms': 1},
                '63': {'cbc_Forms': 11, 'chemistry_Forms': 4},
                '59': {'cbc_Forms': 39, 'chemistry_Forms': 16}
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
        <Subject><ID>59</ID>
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
        </Subject>
        <Subject>
            <ID>60</ID>
            <forms>
                <form>
                    <form_name>cbc_Forms</form_name>
                    <form_count>1</form_count></form>
                <form>
                    <form_name>chemistry_Forms</form_name>
                    <form_count>1</form_count>
                </form>
            </forms>
        </Subject>
        <Subject><ID>61</ID>
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
        </Subject>
        <Subject>
            <ID>63</ID>
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
        </Subject>
    </subjectsDetails>
    <errors/>
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
              <xs:element name="Subject" maxOccurs="unbounded" minOccurs="0">
                <xs:complexType>
                  <xs:sequence>
                    <xs:element type="xs:byte" name="ID"/>
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
            </xs:sequence>
          </xs:complexType>
        </xs:element>
        <xs:element name="errors">
        </xs:element>
      </xs:sequence>
    </xs:complexType>
  </xs:element>
</xs:schema>''')
        return

    def test_create_summary_report(self):

        sys.path.append('config')
        self.newpath = proj_root+'config'
        self.configFolderCreatedNow = False
        if not os.path.exists(self.newpath):
            self.configFolderCreatedNow = True
            os.makedirs(self.newpath)

        result = redi.create_summary_report(self.test_report_params, self.test_report_data, self.test_alert_summary)
        result_string = etree.tostring(result)
    
        #print result_string

        xmlschema_doc = etree.parse(self.schema_str)
        xml_schema = etree.XMLSchema(xmlschema_doc)
        # validate the xml against the xsd schema
        self.assertEqual(xml_schema.validate(result), True)
        # validate the actual data in xml but strip the white space first
        parser = etree.XMLParser(remove_blank_text = True)
        clean_tree = etree.XML(self.expected_xml, parser = parser)
        self.expected_xml = etree.tostring(clean_tree)

        self.assertEqual(self.expected_xml, result_string)

    def tearDown(self):
    	# delete the created xml file
        with open(proj_root + 'config/report.xml'):
           os.remove(proj_root + 'config/report.xml')

           if self.configFolderCreatedNow:
               os.rmdir(self.newpath)

        return

if __name__ == '__main__':
    unittest.main()
