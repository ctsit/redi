import unittest
import os
from lxml import etree
import redi

file_dir = os.path.dirname(os.path.realpath(__file__))
goal_dir = os.path.join(file_dir, "../")
proj_root = os.path.abspath(goal_dir)+'/'

DEFAULT_DATA_DIRECTORY = os.getcwd()

class TestCopyDataToPersonFormEventTree(unittest.TestCase):

    def setUp(self):
        redi.configure_logging(DEFAULT_DATA_DIRECTORY, False)
        self.form_event_tree = """<?xml version='1.0' encoding='US-ASCII'?>
        <redcapProject>
        <name>Project</name>
        <form>
		<name>cbc</name>
		<formDateField>cbc_lbdtc</formDateField>
		<formCompletedFieldName>cbc_complete</formCompletedFieldName>
		<formImportedFieldName>cbc_nximport</formImportedFieldName>
        <formCompletedFieldValue>2</formCompletedFieldValue>
        <formImportedFieldValue>Y</formImportedFieldValue>
		<event>
    		<name>1_arm_1</name>
		</event>
		
		
        </form>
        <form>
            <name>chemistry</name>
            <formDateField>chem_lbdtc</formDateField>
            <formCompletedFieldName>chemistry_complete</formCompletedFieldName>
            <formImportedFieldName>chem_nximport</formImportedFieldName>
            <formCompletedFieldValue>2</formCompletedFieldValue>
            <formImportedFieldValue>Y</formImportedFieldValue>
            <event>
		        <name>1_arm_1</name>
		    </event>
		
		
        </form>

	    <form>
		    <name>inr</name>
		    <formDateField>inr_lbdtc</formDateField>
		    <formCompletedFieldName>inr_complete</formCompletedFieldName>
		    <formImportedFieldName>inr_nximport</formImportedFieldName>
            <formCompletedFieldValue>2</formCompletedFieldValue>
            <formImportedFieldValue>Y</formImportedFieldValue>
		    <event>
		    <name>1_arm_1</name>
		    </event>
		
	       </form>
	
        </redcapProject>
        """
        self.data_form_event_tree = etree.ElementTree(etree.fromstring(self.form_event_tree))
        return()

    def test_copy_data_with_blank_reference_unit(self):

        self.person_form_event_tree = """<person_form_event><person><study_id>123</study_id><all_form_events><form>
        <name>cbc</name>
        <event>
            <name>1_arm_1</name>
            <field><name>hemo_lborres</name><value/></field>
            <field><name>hemo_lborresu</name><value/></field>
            <field><name>cbc_complete</name><value/></field>
            <field><name>cbc_nximport</name><value/></field></event>
        </form>
        </all_form_events></person></person_form_event>
        """
        self.data_person_form_event_tree = etree.ElementTree(etree.fromstring(self.person_form_event_tree))

        self.one_subject = """<?xml version='1.0' encoding='US-ASCII'?>
            <study>
            <subject>
            <NAME>TestSubject</NAME>
            <RESULT>987</RESULT>
            <REFERENCE_UNIT/>
            <STUDY_ID>123</STUDY_ID>
            <timestamp>1906-12-25</timestamp>
            <redcapFormName>cbc</redcapFormName>
            <eventName>1_arm_1</eventName>
            <formDateField>cbc_lbdtc</formDateField>
            <formCompletedFieldName>cbc_complete</formCompletedFieldName>
            <formImportedFieldName>cbc_nximport</formImportedFieldName>
            <redcapFieldNameValue>hemo_lborres</redcapFieldNameValue>
            <redcapFieldNameUnits>hemo_lborresu</redcapFieldNameUnits>
            <redcapFieldNameStatus>hemo_lbstat</redcapFieldNameStatus></subject>
        </study>
            """
        self.data_one_subject= etree.ElementTree(etree.fromstring(self.one_subject))
        self.result = etree.tostring(redi.copy_data_to_person_form_event_tree(self.data_one_subject,self.data_person_form_event_tree,self.data_form_event_tree))

        self.output = """<person_form_event><person><study_id>123</study_id><all_form_events><form>
        <name>cbc</name>
        <event>
            <name>1_arm_1</name>
            <field><name>hemo_lborres</name><value>987</value></field>
            <field><name>hemo_lborresu</name><value/></field>
            <field><name>cbc_complete</name><value>2</value></field>
            <field><name>cbc_nximport</name><value>Y</value></field></event>
        </form>
        </all_form_events></person></person_form_event>"""

        self.expect = etree.tostring(etree.fromstring(self.output))
        self.assertEqual(self.expect, self.result)

    def test_copy_data_to_person_form_event_tree_one_person(self):
        
        self.person_form_event_tree = """<person_form_event><person><study_id>123</study_id><all_form_events><form>
        <name>cbc</name>
        <event>
            <name>1_arm_1</name>
            <field><name>hemo_lborres</name><value/></field>
            <field><name>hemo_lborresu</name><value/></field>
            <field><name>cbc_complete</name><value/></field>
            <field><name>cbc_nximport</name><value/></field></event>
        </form>    
        </all_form_events></person></person_form_event>
        """
        self.data_person_form_event_tree = etree.ElementTree(etree.fromstring(self.person_form_event_tree))
        
        self.one_subject = """<?xml version='1.0' encoding='US-ASCII'?>
            <study>
            <subject>
            <NAME>TestSubject</NAME>
            <RESULT>987</RESULT>
            <REFERENCE_UNIT>g/dL</REFERENCE_UNIT>
            <STUDY_ID>123</STUDY_ID>
        <timestamp>1906-12-25</timestamp>
        <redcapFormName>cbc</redcapFormName>
        <eventName>1_arm_1</eventName>
        <formDateField>cbc_lbdtc</formDateField>
        <formCompletedFieldName>cbc_complete</formCompletedFieldName>
        <formImportedFieldName>cbc_nximport</formImportedFieldName>
        <redcapFieldNameValue>hemo_lborres</redcapFieldNameValue>
        <redcapFieldNameUnits>hemo_lborresu</redcapFieldNameUnits>
        <redcapFieldNameStatus>hemo_lbstat</redcapFieldNameStatus></subject>
        </study>
            """
        self.data_one_subject= etree.ElementTree(etree.fromstring(self.one_subject))
        self.result = etree.tostring(redi.copy_data_to_person_form_event_tree(self.data_one_subject,self.data_person_form_event_tree,self.data_form_event_tree))
        
        self.output = """<person_form_event><person><study_id>123</study_id><all_form_events><form>
        <name>cbc</name>
        <event>
            <name>1_arm_1</name>
            <field><name>hemo_lborres</name><value>987</value></field>
            <field><name>hemo_lborresu</name><value>g/dL</value></field>
            <field><name>cbc_complete</name><value>2</value></field>
            <field><name>cbc_nximport</name><value>Y</value></field></event>
        </form>    
        </all_form_events></person></person_form_event>"""
        
        self.expect = etree.tostring(etree.fromstring(self.output))
        self.assertEqual(self.expect, self.result)

    def test_copy_data_to_person_form_event_tree_two_persons(self):
        
        self.person_form_event_tree = """<person_form_event><person><study_id>456</study_id><all_form_events>
		<form>
		    <name>inr</name>
		    <event>
		    <name>1_arm_1</name>
		    <field><name>inr_lbdtc</name><value/></field>
		    <field><name>inr_complete</name><value/></field>
            <field><name>inr_nximport</name><value/></field></event>
		
	       </form>
	
        </all_form_events></person>
        <person><study_id>123</study_id><all_form_events><form>
        		<name>cbc</name>
        		<event>
            		<name>1_arm_1</name>
        		    <field><name>hemo_lborres</name><value></value></field>
                    <field><name>cbc_complete</name><value/></field>
                    <field><name>cbc_nximport</name><value/></field></event>
        		</form>	
                </all_form_events></person>
        
        </person_form_event>
        """
        self.data_person_form_event_tree = etree.ElementTree(etree.fromstring(self.person_form_event_tree))
        self.two_subjects = """<?xml version='1.0' encoding='US-ASCII'?>
            <study>
            <subject>
            <NAME>TestSubject</NAME>
            <RESULT>987</RESULT>
            <REFERENCE_UNIT>g/dL</REFERENCE_UNIT>
            <STUDY_ID>123</STUDY_ID>
        <timestamp>1906-12-25</timestamp><redcapFormName>cbc</redcapFormName><eventName>1_arm_1</eventName><formDateField>cbc_lbdtc</formDateField><formCompletedFieldName>cbc_complete</formCompletedFieldName><formImportedFieldName>cbc_nximport</formImportedFieldName><redcapFieldNameValue>hemo_lborres</redcapFieldNameValue><redcapFieldNameUnits>hemo_lborresu</redcapFieldNameUnits><redcapFieldNameStatus>hemo_lbstat</redcapFieldNameStatus></subject>
            <subject>
            <NAME>TestSubject_2</NAME>
            <RESULT>123</RESULT>
            <REFERENCE_UNIT>g/dL</REFERENCE_UNIT>
            <STUDY_ID>456</STUDY_ID>
        <timestamp>1906-12-25</timestamp><redcapFormName>inr</redcapFormName><eventName>1_arm_1</eventName><formDateField>inr_lbdtc</formDateField><formCompletedFieldName>inr_complete</formCompletedFieldName><formImportedFieldName>inr_nximport</formImportedFieldName><redcapFieldNameValue>hemo_lborres</redcapFieldNameValue><redcapFieldNameUnits>hemo_lborresu</redcapFieldNameUnits><redcapFieldNameStatus>hemo_lbstat</redcapFieldNameStatus></subject>
        
        </study>
            """
        self.data_two_subjects= etree.ElementTree(etree.fromstring(self.two_subjects))
        self.result = etree.tostring(redi.copy_data_to_person_form_event_tree(self.data_two_subjects,self.data_person_form_event_tree,self.data_form_event_tree))
        self.output = """<person_form_event><person><study_id>456</study_id><all_form_events>
		<form>
		    <name>inr</name>
		    <event>
		    <name>1_arm_1</name>
		    <field><name>inr_lbdtc</name><value>1906-12-25</value></field>
		    <field><name>inr_complete</name><value>2</value></field>
            <field><name>inr_nximport</name><value>Y</value></field></event>
		
	       </form>
	
        </all_form_events></person>
        <person><study_id>123</study_id><all_form_events><form>
        		<name>cbc</name>
        		<event>
            		<name>1_arm_1</name>
        		    <field><name>hemo_lborres</name><value>987</value></field>
                    <field><name>cbc_complete</name><value>2</value></field>
                    <field><name>cbc_nximport</name><value>Y</value></field></event>
        		</form>	
                </all_form_events></person>
        
        </person_form_event>"""
        
        self.expect = etree.tostring(etree.fromstring(self.output))
        self.assertEqual(self.expect, self.result)
        
    def test_copy_data_to_person_form_event_tree_zero_forms(self):
        
        self.person_form_event_tree = """<person_form_event><person><study_id>456</study_id>
        </person>
        
        </person_form_event>
        """
        self.data_person_form_event_tree = etree.ElementTree(etree.fromstring(self.person_form_event_tree))
        self.zero_form = """<?xml version='1.0' encoding='US-ASCII'?>
            <study>
            <subject>
            <NAME>TestSubject_2</NAME>
            <RESULT>123</RESULT>
            <REFERENCE_UNIT>g/dL</REFERENCE_UNIT>
            <STUDY_ID>456</STUDY_ID>
        <timestamp>1906-12-25</timestamp><redcapFormName>inr</redcapFormName><eventName>1_arm_1</eventName><formDateField>inr_lbdtc</formDateField><formCompletedFieldName>inr_complete</formCompletedFieldName><formImportedFieldName>inr_nximport</formImportedFieldName><redcapFieldNameValue>hemo_lborres</redcapFieldNameValue><redcapFieldNameUnits>hemo_lborresu</redcapFieldNameUnits><redcapFieldNameStatus>hemo_lbstat</redcapFieldNameStatus></subject>
        
        </study>
            """
        self.data_zero_form= etree.ElementTree(etree.fromstring(self.zero_form))
        self.assertRaises(Exception,redi.copy_data_to_person_form_event_tree,self.data_zero_form,self.data_person_form_event_tree,self.data_form_event_tree)
        
        
    def test_copy_data_to_person_form_event_tree_two_forms(self):
        
        self.person_form_event_tree = """<person_form_event><person><study_id>456</study_id><all_form_events>
		<form>
		    <name>cbc</name>
		    <event>
		    <name>1_arm_1</name>
		    <field><name>cbc_lbdtc</name><value/></field>
            <field><name>cbc_complete</name><value/></field>
            <field><name>cbc_nximport</name><value/></field></event>
		    </form>
            <form>
		    <name>inr</name>
		    <event>
		    <name>1_arm_1</name>
		    <field><name>inr_lbdtc</name><value/></field>
		    <field><name>inr_complete</name><value/></field>
            <field><name>inr_nximport</name><value/></field>
            </event>
		    </form>
	    </all_form_events></person></person_form_event>
        """
        self.data_person_form_event_tree = etree.ElementTree(etree.fromstring(self.person_form_event_tree))
        self.two_subjects = """<?xml version='1.0' encoding='US-ASCII'?>
            <study>
            <subject>
            <NAME>TestSubject_2</NAME>
            <RESULT>987</RESULT>
            <REFERENCE_UNIT>g/dL</REFERENCE_UNIT>
            <STUDY_ID>456</STUDY_ID>
        <timestamp>1906-12-26</timestamp><redcapFormName>cbc</redcapFormName><eventName>1_arm_1</eventName><formDateField>cbc_lbdtc</formDateField><formCompletedFieldName>cbc_complete</formCompletedFieldName><formImportedFieldName>cbc_nximport</formImportedFieldName><redcapFieldNameValue>hemo_lborres</redcapFieldNameValue><redcapFieldNameUnits>hemo_lborresu</redcapFieldNameUnits><redcapFieldNameStatus>hemo_lbstat</redcapFieldNameStatus></subject>
            <subject>
            <NAME>TestSubject_2</NAME>
            <RESULT>123</RESULT>
            <REFERENCE_UNIT>g/dL</REFERENCE_UNIT>
            <STUDY_ID>456</STUDY_ID>
        <timestamp>1906-12-25</timestamp><redcapFormName>inr</redcapFormName><eventName>1_arm_1</eventName><formDateField>inr_lbdtc</formDateField><formCompletedFieldName>inr_complete</formCompletedFieldName><formImportedFieldName>inr_nximport</formImportedFieldName><redcapFieldNameValue>hemo_lborres</redcapFieldNameValue><redcapFieldNameUnits>hemo_lborresu</redcapFieldNameUnits><redcapFieldNameStatus>hemo_lbstat</redcapFieldNameStatus></subject>
        
        </study>
            """
        self.data_two_subjects= etree.ElementTree(etree.fromstring(self.two_subjects))
        self.result = etree.tostring(redi.copy_data_to_person_form_event_tree(self.data_two_subjects,self.data_person_form_event_tree,self.data_form_event_tree))
        self.output = """<person_form_event><person><study_id>456</study_id><all_form_events>
		<form>
		    <name>cbc</name>
		    <event>
		    <name>1_arm_1</name>
		    <field><name>cbc_lbdtc</name><value>1906-12-26</value></field>
            <field><name>cbc_complete</name><value>2</value></field>
            <field><name>cbc_nximport</name><value>Y</value></field></event>
		    </form>
            <form>
		    <name>inr</name>
		    <event>
		    <name>1_arm_1</name>
		    <field><name>inr_lbdtc</name><value>1906-12-25</value></field>
		    <field><name>inr_complete</name><value>2</value></field>
            <field><name>inr_nximport</name><value>Y</value></field>
            </event>
		    </form>
	    </all_form_events></person></person_form_event>"""
        
        self.expect = etree.tostring(etree.fromstring(self.output))
        self.assertEqual(self.expect, self.result)

    def test_copy_data_to_person_form_event_tree_two_events(self):
        
        self.person_form_event_tree = """<person_form_event><person><study_id>456</study_id><all_form_events>
		<form>
		    <name>inr</name>
		    <event>
		    <name>1_arm_1</name>
		    <field><name>inr_lbdtc</name><value/></field>
		    <field><name>inr_complete</name><value/></field>
            <field><name>inr_nximport</name><value/></field>
            </event>
		    <event>
		    <name>2_arm_1</name>
		    <field><name>inr_lbdtc</name><value/></field>
		    <field><name>inr_complete</name><value/></field>
            <field><name>inr_nximport</name><value/></field>
            </event>
           </form>
	    </all_form_events></person></person_form_event>
        """
        self.data_person_form_event_tree = etree.ElementTree(etree.fromstring(self.person_form_event_tree))
        self.two_subjects = """<?xml version='1.0' encoding='US-ASCII'?>
            <study>
            <subject>
            <NAME>TestSubject_2</NAME>
            <RESULT>987</RESULT>
            <REFERENCE_UNIT>g/dL</REFERENCE_UNIT>
            <STUDY_ID>456</STUDY_ID>
        <timestamp>1906-12-26</timestamp><redcapFormName>inr</redcapFormName><eventName>1_arm_1</eventName><formDateField>inr_lbdtc</formDateField><formCompletedFieldName>inr_complete</formCompletedFieldName><formImportedFieldName>inr_nximport</formImportedFieldName><redcapFieldNameValue>hemo_lborres</redcapFieldNameValue><redcapFieldNameUnits>hemo_lborresu</redcapFieldNameUnits><redcapFieldNameStatus>hemo_lbstat</redcapFieldNameStatus></subject>
            <subject>
            <NAME>TestSubject_2</NAME>
            <RESULT>123</RESULT>
            <REFERENCE_UNIT>g/dL</REFERENCE_UNIT>
            <STUDY_ID>456</STUDY_ID>
        <timestamp>1906-12-25</timestamp><redcapFormName>inr</redcapFormName><eventName>2_arm_1</eventName><formDateField>inr_lbdtc</formDateField><formCompletedFieldName>inr_complete</formCompletedFieldName><formImportedFieldName>inr_nximport</formImportedFieldName><redcapFieldNameValue>hemo_lborres</redcapFieldNameValue><redcapFieldNameUnits>hemo_lborresu</redcapFieldNameUnits><redcapFieldNameStatus>hemo_lbstat</redcapFieldNameStatus></subject>
        
        </study>
            """
        self.data_two_subjects= etree.ElementTree(etree.fromstring(self.two_subjects))
        # print "Testing Test case"
        self.result = etree.tostring(redi.copy_data_to_person_form_event_tree(self.data_two_subjects,self.data_person_form_event_tree,self.data_form_event_tree))
        self.output = """<person_form_event><person><study_id>456</study_id><all_form_events>
		<form>
		    <name>inr</name>
		    <event>
		    <name>1_arm_1</name>
		    <field><name>inr_lbdtc</name><value>1906-12-26</value></field>
		    <field><name>inr_complete</name><value>2</value></field>
            <field><name>inr_nximport</name><value>Y</value></field>
            </event>
		    <event>
		    <name>2_arm_1</name>
		    <field><name>inr_lbdtc</name><value>1906-12-25</value></field>
		    <field><name>inr_complete</name><value>2</value></field>
            <field><name>inr_nximport</name><value>Y</value></field>
            </event>
           </form>
	    </all_form_events></person></person_form_event>"""
        
        self.expect = etree.tostring(etree.fromstring(self.output))
        self.assertEqual(self.expect, self.result)
        
    def test_form_date_field_pair(self):
        
        self.person_form_event_tree = """<person_form_event><person><study_id>456</study_id><all_form_events>
		<form>
		    <name>inr</name>
		    <event>
		    <name>1_arm_1</name>
		    <field><name>inr_lbdtc</name><value/></field></event>
		</form>
	    </all_form_events></person></person_form_event>
        """
        self.data_person_form_event_tree = etree.ElementTree(etree.fromstring(self.person_form_event_tree))
        self.form_date_field = """<?xml version='1.0' encoding='US-ASCII'?>
            <study>
            <subject>
            <NAME>TestSubject_2</NAME>
            <RESULT>987</RESULT>
            <REFERENCE_UNIT>g/dL</REFERENCE_UNIT>
            <STUDY_ID>456</STUDY_ID>
        <timestamp>1906-12-26</timestamp><redcapFormName>inr</redcapFormName><eventName>1_arm_1</eventName><formCompletedFieldName>cbc_complete</formCompletedFieldName><formImportedFieldName>cbc_nximport</formImportedFieldName><redcapFieldNameValue>hemo_lborres</redcapFieldNameValue><redcapFieldNameUnits>hemo_lborresu</redcapFieldNameUnits><redcapFieldNameStatus>hemo_lbstat</redcapFieldNameStatus></subject>
            
        </study>
            """
        self.data_form_date_field= etree.ElementTree(etree.fromstring(self.form_date_field))
        self.form_date_value_field = """<?xml version='1.0' encoding='US-ASCII'?>
            <study>
            <subject>
            <NAME>TestSubject_2</NAME>
            <RESULT>987</RESULT>
            <REFERENCE_UNIT>g/dL</REFERENCE_UNIT>
            <STUDY_ID>456</STUDY_ID>
        <redcapFormName>inr</redcapFormName><eventName>1_arm_1</eventName><formCompletedFieldName>cbc_complete</formCompletedFieldName><formDateField>cbc_lbdtc</formDateField><formImportedFieldName>cbc_nximport</formImportedFieldName><redcapFieldNameValue>hemo_lborres</redcapFieldNameValue><redcapFieldNameUnits>hemo_lborresu</redcapFieldNameUnits><redcapFieldNameStatus>hemo_lbstat</redcapFieldNameStatus></subject>
            
        </study>
            """
        self.data_form_date_value_field= etree.ElementTree(etree.fromstring(self.form_date_value_field))
        
        self.assertRaises(Exception,redi.copy_data_to_person_form_event_tree,self.data_form_date_field,self.data_person_form_event_tree,self.data_form_event_tree)
        self.assertRaises(Exception,redi.copy_data_to_person_form_event_tree,self.data_form_date_value_field,self.data_person_form_event_tree,self.data_form_event_tree)
        
    def test_redcap_field_name_pair(self):
        
        self.person_form_event_tree = """<person_form_event><person><study_id>456</study_id><all_form_events>
		<form>
		    <name>inr</name>
		    <event>
		    <name>1_arm_1</name>
		    <field><name>inr_lbdtc</name><value/></field></event>
		</form>
	    </all_form_events></person></person_form_event>
        """
        self.data_person_form_event_tree = etree.ElementTree(etree.fromstring(self.person_form_event_tree))
        self.redcap_field_name = """<?xml version='1.0' encoding='US-ASCII'?>
            <study>
            <subject>
            <NAME>TestSubject_2</NAME>
            <RESULT>987</RESULT>
            <REFERENCE_UNIT>g/dL</REFERENCE_UNIT>
            <STUDY_ID>456</STUDY_ID>
        <timestamp>1906-12-26</timestamp><redcapFormName>inr</redcapFormName><eventName>1_arm_1</eventName><formCompletedFieldName>cbc_complete</formCompletedFieldName><formImportedFieldName>cbc_nximport</formImportedFieldName><redcapFieldNameUnits>hemo_lborresu</redcapFieldNameUnits><redcapFieldNameStatus>hemo_lbstat</redcapFieldNameStatus></subject>
            
        </study>
            """
        self.data_redcap_field_name= etree.ElementTree(etree.fromstring(self.redcap_field_name))
        self.redcap_value_field = """<?xml version='1.0' encoding='US-ASCII'?>
            <study>
            <subject>
            <NAME>TestSubject_2</NAME>
            <REFERENCE_UNIT>g/dL</REFERENCE_UNIT>
            <STUDY_ID>456</STUDY_ID>
        <redcapFormName>inr</redcapFormName><eventName>1_arm_1</eventName><formCompletedFieldName>cbc_complete</formCompletedFieldName><formDateField>cbc_lbdtc</formDateField><formImportedFieldName>cbc_nximport</formImportedFieldName><redcapFieldNameValue>hemo_lborres</redcapFieldNameValue><redcapFieldNameUnits>hemo_lborresu</redcapFieldNameUnits><redcapFieldNameStatus>hemo_lbstat</redcapFieldNameStatus></subject>
            
        </study>
            """
        self.data_redcap_value_field= etree.ElementTree(etree.fromstring(self.redcap_value_field))
        self.assertRaises(Exception,redi.copy_data_to_person_form_event_tree,self.data_redcap_field_name,self.data_person_form_event_tree,self.data_form_event_tree)
        self.assertRaises(Exception,redi.copy_data_to_person_form_event_tree,self.data_redcap_value_field,self.data_person_form_event_tree,self.data_form_event_tree)
        
    def test_redcap_field_units_pair(self):
        
        self.person_form_event_tree = """<person_form_event><person><study_id>456</study_id><all_form_events>
		<form>
		    <name>inr</name>
		    <event>
		    <name>1_arm_1</name>
		    <field><name>inr_lbdtc</name><value/></field></event>
		</form>
	    </all_form_events></person></person_form_event>
        """
        self.data_person_form_event_tree = etree.ElementTree(etree.fromstring(self.person_form_event_tree))
        self.redcap_field_units_name = """<?xml version='1.0' encoding='US-ASCII'?>
            <study>
            <subject>
            <NAME>TestSubject_2</NAME>
            <RESULT>987</RESULT>
            <REFERENCE_UNIT>g/dL</REFERENCE_UNIT>
            <STUDY_ID>456</STUDY_ID>
        <timestamp>1906-12-26</timestamp><redcapFormName>inr</redcapFormName><eventName>1_arm_1</eventName><formDateField>cbc_lbdtc</formDateField><formCompletedFieldName>cbc_complete</formCompletedFieldName><redcapFieldNameValue>hemo_lborres</redcapFieldNameValue><formImportedFieldName>cbc_nximport</formImportedFieldName><redcapFieldNameStatus>hemo_lbstat</redcapFieldNameStatus></subject>
            
        </study>
            """
        self.data_redcap_field_units_name= etree.ElementTree(etree.fromstring(self.redcap_field_units_name))
        self.redcap_units_value_field = """<?xml version='1.0' encoding='US-ASCII'?>
            <study>
            <subject>
            <NAME>TestSubject_2</NAME>
            <RESULT>987</RESULT>
            <STUDY_ID>456</STUDY_ID>
        <timestamp>1906-12-26</timestamp><redcapFormName>inr</redcapFormName><eventName>1_arm_1</eventName><formCompletedFieldName>cbc_complete</formCompletedFieldName><formDateField>cbc_lbdtc</formDateField><formImportedFieldName>cbc_nximport</formImportedFieldName><redcapFieldNameValue>hemo_lborres</redcapFieldNameValue><redcapFieldNameUnits>hemo_lborresu</redcapFieldNameUnits><redcapFieldNameStatus>hemo_lbstat</redcapFieldNameStatus></subject>
            
        </study>
            """
        self.data_redcap_units_value_field= etree.ElementTree(etree.fromstring(self.redcap_units_value_field))
        self.assertRaises(Exception,redi.copy_data_to_person_form_event_tree,self.data_redcap_field_units_name,self.data_person_form_event_tree,self.data_form_event_tree)
        self.assertRaises(Exception,redi.copy_data_to_person_form_event_tree,self.data_redcap_units_value_field,self.data_person_form_event_tree,self.data_form_event_tree)
        
    def test_Form_Completed_Field(self):
        self.form_event_tree = """<?xml version='1.0' encoding='US-ASCII'?>
        <redcapProject>
        <name>Project</name>
        <form>
		    <name>inr</name>
		    <formDateField>inr_lbdtc</formDateField>
		    <formCompletedFieldName>inr_complete</formCompletedFieldName>
		    <formImportedFieldName>inr_nximport</formImportedFieldName>
            <formCompletedFieldValue></formCompletedFieldValue>
            <formImportedFieldValue>Y</formImportedFieldValue>
		    <event>
		    <name>1_arm_1</name>
		    </event>
		
	       </form>
	
        </redcapProject>
        """
        self.data_form_event_tree = etree.ElementTree(etree.fromstring(self.form_event_tree))
        
        self.person_form_event_tree = """<person_form_event><person><study_id>456</study_id><all_form_events>
		<form>
		    <name>inr</name>
		    <event>
		    <name>1_arm_1</name>
		    <field><name>inr_lbdtc</name><value/></field>
		    <field><name>inr_complete</name><value/></field>
            <field><name>inr_nximport</name><value/></field>
            </event>
            
		</form>
	    </all_form_events></person></person_form_event>
        """
        self.data_person_form_event_tree = etree.ElementTree(etree.fromstring(self.person_form_event_tree))
        self.Form_Completed_Field = """<?xml version='1.0' encoding='US-ASCII'?>
            <study>
            <subject>
            <NAME>TestSubject_2</NAME>
            <RESULT>987</RESULT>
            <REFERENCE_UNIT>g/dL</REFERENCE_UNIT>
            <STUDY_ID>456</STUDY_ID>
        <timestamp>1906-12-26</timestamp><redcapFormName>inr</redcapFormName><eventName>1_arm_1</eventName><formDateField>inr_lbdtc</formDateField><formCompletedFieldName>inr_complete</formCompletedFieldName><redcapFieldNameValue>hemo_lborres</redcapFieldNameValue><formImportedFieldName>inr_nximport</formImportedFieldName><redcapFieldNameUnits>hemo_lborresu</redcapFieldNameUnits><redcapFieldNameStatus>hemo_lbstat</redcapFieldNameStatus></subject>
            
        </study>
            """
        self.data_Form_Completed_Field= etree.ElementTree(etree.fromstring(self.Form_Completed_Field))
        self.assertRaises(Exception,redi.copy_data_to_person_form_event_tree,self.data_Form_Completed_Field,self.data_person_form_event_tree,self.data_form_event_tree)
        
    def test_Form_Imported_Field(self):
        self.form_event_tree = """<?xml version='1.0' encoding='US-ASCII'?>
        <redcapProject>
        <name>Project</name>
        <form>
		    <name>inr</name>
		    <formDateField>inr_lbdtc</formDateField>
		    <formCompletedFieldName>inr_complete</formCompletedFieldName>
		    <formImportedFieldName>inr_nximport</formImportedFieldName>
            <formCompletedFieldValue>2</formCompletedFieldValue>
            <formImportedFieldValue></formImportedFieldValue>
		    <event>
		    <name>1_arm_1</name>
		    </event>
		
	       </form>
	
        </redcapProject>
        """
        self.data_form_event_tree = etree.ElementTree(etree.fromstring(self.form_event_tree))
        self.person_form_event_tree = """<person_form_event><person><study_id>456</study_id><all_form_events>
		<form>
		    <name>inr</name>
		    <event>
		    <name>1_arm_1</name>
		    <field><name>inr_lbdtc</name><value/></field>
		    <field><name>inr_complete</name><value/></field>
            <field><name>inr_nximport</name><value/></field>
            </event>
		</form>
	    </all_form_events></person></person_form_event>
        """
        self.data_person_form_event_tree = etree.ElementTree(etree.fromstring(self.person_form_event_tree))
        self.Form_Imported_Field = """<?xml version='1.0' encoding='US-ASCII'?>
            <study>
            <subject>
            <NAME>TestSubject_2</NAME>
            <RESULT>987</RESULT>
            <REFERENCE_UNIT>g/dL</REFERENCE_UNIT>
            <STUDY_ID>456</STUDY_ID>
        <timestamp>1906-12-26</timestamp><redcapFormName>inr</redcapFormName><eventName>1_arm_1</eventName><formCompletedFieldName>inr_complete</formCompletedFieldName><formDateField>inr_lbdtc</formDateField><redcapFieldNameValue>hemo_lborres</redcapFieldNameValue><formImportedFieldName>inr_nximport</formImportedFieldName><redcapFieldNameUnits>hemo_lborresu</redcapFieldNameUnits><redcapFieldNameStatus>hemo_lbstat</redcapFieldNameStatus></subject>
            
        </study>
            """
        self.data_Form_Imported_Field =  etree.ElementTree(etree.fromstring(self.Form_Imported_Field))
        self.assertRaises(Exception,redi.copy_data_to_person_form_event_tree,self.data_Form_Imported_Field,self.data_person_form_event_tree,self.data_form_event_tree)
        
    def tearDown(self):
        return()

if __name__ == '__main__':
    unittest.main()
