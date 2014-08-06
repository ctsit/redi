import unittest
import os
from lxml import etree
import redi

file_dir = os.path.dirname(os.path.realpath(__file__))
goal_dir = os.path.join(file_dir, "../")
proj_root = os.path.abspath(goal_dir)+'/'


class TestCreateEmptyEventTreeForStudy(unittest.TestCase):

    def setUp(self):
        self.all_form_events = """<all_form_events><form>
		<name>cbc</name>
		<event>
    		<name>1_arm_1</name>
		<field><name>lymce_lborres</name><value/></field><field><name>lymce_lborresu</name><value/></field><field><name>hemo_lborresu</name><value/></field><field><name>cbc_lbdtc</name><value/></field><field><name>cbc_nximport</name><value/></field><field><name>lymce_lbstat</name><value/></field><field><name>cbc_complete</name><value/></field><field><name>hemo_lbstat</name><value/></field><field><name>hemo_lborres</name><value/></field></event>
		
		
        </form>
        <form>
            <name>chemistry</name>
            <event>
		        <name>1_arm_1</name>
		    <field><name>k_lborres</name><value/></field><field><name>chem_lbdtc</name><value/></field><field><name>sodium_lborresu</name><value/></field><field><name>k_lbstat</name><value/></field><field><name>sodium_lbstat</name><value/></field><field><name>chem_nximport</name><value/></field><field><name>chemistry_complete</name><value/></field><field><name>k_lborresu</name><value/></field><field><name>sodium_lborres</name><value/></field></event>
		
		
        </form>

	    <form>
		    <name>inr</name>
		    <event>
		    <name>1_arm_1</name>
		    <field><name>inr_lbdtc</name><value/></field><field><name>inr_complete</name><value/></field><field><name>inr_nximport</name><value/></field></event>
		
	       </form>
	
        </all_form_events>
        """
        
        self.data_all_form_events= etree.ElementTree(etree.fromstring(self.all_form_events))
        
        return()


    def test_create_empty_event_tree_for_study_for_zero_subjects(self):
        redi.configure_logging(proj_root+'log/redi.log')
        self.zero_subjects = """<?xml version='1.0' encoding='US-ASCII'?>
        <study></study>
        """
        self.data_zero_subjects = etree.ElementTree(etree.fromstring(self.zero_subjects))
        self.assertRaises(Exception,redi.create_empty_event_tree_for_study,self.data_zero_subjects,self.data_all_form_events)
        
    def test_create_empty_event_tree_for_study_for_one_subjects(self):
        redi.configure_logging(proj_root+'log/redi.log')
        self.one_subject = """<?xml version='1.0' encoding='US-ASCII'?>
            <study>
            <subject>
            <NAME>TestSubject</NAME>
            <loinc_code>123456</loinc_code>
            <RESULT>123</RESULT>
            <REFERENCE_LOW>12.3</REFERENCE_LOW>
            <REFERENCE_HIGH>12.3</REFERENCE_HIGH>
            <REFERENCE_UNIT>g/dL</REFERENCE_UNIT>
            <DATE_TIME_STAMP/>
            <STUDY_ID>123</STUDY_ID>
        <timestamp/><redcapFormName>cbc</redcapFormName><eventName/><formDateField>cbc_lbdtc</formDateField><formCompletedFieldName>cbc_complete</formCompletedFieldName><formImportedFieldName>cbc_nximport</formImportedFieldName><redcapFieldNameValue>hemo_lborres</redcapFieldNameValue><redcapFieldNameUnits>hemo_lborresu</redcapFieldNameUnits><redcapFieldNameStatus>hemo_lbstat</redcapFieldNameStatus></subject>
        </study>
            """
        self.data_one_subject= etree.ElementTree(etree.fromstring(self.one_subject))
        
        self.output_one_subject = """<person_form_event><person><study_id>123</study_id><all_form_events><form>
		<name>cbc</name>
		<event>
    		<name>1_arm_1</name>
		<field><name>lymce_lborres</name><value/></field><field><name>lymce_lborresu</name><value/></field><field><name>hemo_lborresu</name><value/></field><field><name>cbc_lbdtc</name><value/></field><field><name>cbc_nximport</name><value/></field><field><name>lymce_lbstat</name><value/></field><field><name>cbc_complete</name><value/></field><field><name>hemo_lbstat</name><value/></field><field><name>hemo_lborres</name><value/></field></event>
		
		
        </form>
        <form>
            <name>chemistry</name>
            <event>
		        <name>1_arm_1</name>
		    <field><name>k_lborres</name><value/></field><field><name>chem_lbdtc</name><value/></field><field><name>sodium_lborresu</name><value/></field><field><name>k_lbstat</name><value/></field><field><name>sodium_lbstat</name><value/></field><field><name>chem_nximport</name><value/></field><field><name>chemistry_complete</name><value/></field><field><name>k_lborresu</name><value/></field><field><name>sodium_lborres</name><value/></field></event>
		
		
        </form>

	    <form>
		    <name>inr</name>
		    <event>
		    <name>1_arm_1</name>
		    <field><name>inr_lbdtc</name><value/></field><field><name>inr_complete</name><value/></field><field><name>inr_nximport</name><value/></field></event>
		
	       </form>
	
        </all_form_events></person></person_form_event>
        """
        self.expect_one_subject = etree.tostring(etree.fromstring(self.output_one_subject))
        
        self.result = etree.tostring(redi.create_empty_event_tree_for_study(self.data_one_subject,self.data_all_form_events))
        self.assertEqual(self.expect_one_subject, self.result)
       
    def test_create_empty_event_tree_for_study_for_two_subjects(self):
        redi.configure_logging(proj_root+'log/redi.log')
        self.two_subjects = """<?xml version='1.0' encoding='US-ASCII'?>
            <study>
                <subject>
                <NAME>TestSubject_1</NAME>
                <loinc_code>123456</loinc_code>
                <RESULT>123</RESULT>
                <REFERENCE_LOW>12.3</REFERENCE_LOW>
                <REFERENCE_HIGH>12.3</REFERENCE_HIGH>
                <REFERENCE_UNIT>g/dL</REFERENCE_UNIT>
                <DATE_TIME_STAMP/>
                <STUDY_ID>123</STUDY_ID>
            <timestamp/><redcapFormName>cbc</redcapFormName><eventName/><formDateField>cbc_lbdtc</formDateField><formCompletedFieldName>cbc_complete</formCompletedFieldName><formImportedFieldName>cbc_nximport</formImportedFieldName><redcapFieldNameValue>hemo_lborres</redcapFieldNameValue><redcapFieldNameUnits>hemo_lborresu</redcapFieldNameUnits><redcapFieldNameStatus>hemo_lbstat</redcapFieldNameStatus></subject>
            <subject>
            <NAME>TestSubject_2</NAME>
            <loinc_code>123456</loinc_code>
            <RESULT>123</RESULT>
            <REFERENCE_LOW>12.3</REFERENCE_LOW>
            <REFERENCE_HIGH>12.3</REFERENCE_HIGH>
            <REFERENCE_UNIT>g/dL</REFERENCE_UNIT>
            <DATE_TIME_STAMP/>
            <STUDY_ID>1234</STUDY_ID>
        <timestamp/><redcapFormName>cbc</redcapFormName><eventName/><formDateField>cbc_lbdtc</formDateField><formCompletedFieldName>cbc_complete</formCompletedFieldName><formImportedFieldName>cbc_nximport</formImportedFieldName><redcapFieldNameValue>hemo_lborres</redcapFieldNameValue><redcapFieldNameUnits>hemo_lborresu</redcapFieldNameUnits><redcapFieldNameStatus>hemo_lbstat</redcapFieldNameStatus></subject>
        </study>
            """
        self.data_two_subjects= etree.ElementTree(etree.fromstring(self.two_subjects))
        
        self.output_two_subjects = """<person_form_event><person><study_id>1234</study_id><all_form_events><form>
		<name>cbc</name>
		<event>
    		<name>1_arm_1</name>
		<field><name>lymce_lborres</name><value/></field><field><name>lymce_lborresu</name><value/></field><field><name>hemo_lborresu</name><value/></field><field><name>cbc_lbdtc</name><value/></field><field><name>cbc_nximport</name><value/></field><field><name>lymce_lbstat</name><value/></field><field><name>cbc_complete</name><value/></field><field><name>hemo_lbstat</name><value/></field><field><name>hemo_lborres</name><value/></field></event>
		
		
        </form>
        <form>
            <name>chemistry</name>
            <event>
		        <name>1_arm_1</name>
		    <field><name>k_lborres</name><value/></field><field><name>chem_lbdtc</name><value/></field><field><name>sodium_lborresu</name><value/></field><field><name>k_lbstat</name><value/></field><field><name>sodium_lbstat</name><value/></field><field><name>chem_nximport</name><value/></field><field><name>chemistry_complete</name><value/></field><field><name>k_lborresu</name><value/></field><field><name>sodium_lborres</name><value/></field></event>
		
		
        </form>

	    <form>
		    <name>inr</name>
		    <event>
		    <name>1_arm_1</name>
		    <field><name>inr_lbdtc</name><value/></field><field><name>inr_complete</name><value/></field><field><name>inr_nximport</name><value/></field></event>
		
	       </form>
	
        </all_form_events></person><person><study_id>123</study_id><all_form_events><form>
		<name>cbc</name>
		<event>
    		<name>1_arm_1</name>
		<field><name>lymce_lborres</name><value/></field><field><name>lymce_lborresu</name><value/></field><field><name>hemo_lborresu</name><value/></field><field><name>cbc_lbdtc</name><value/></field><field><name>cbc_nximport</name><value/></field><field><name>lymce_lbstat</name><value/></field><field><name>cbc_complete</name><value/></field><field><name>hemo_lbstat</name><value/></field><field><name>hemo_lborres</name><value/></field></event>
		
		
        </form>
        <form>
            <name>chemistry</name>
            <event>
		        <name>1_arm_1</name>
		    <field><name>k_lborres</name><value/></field><field><name>chem_lbdtc</name><value/></field><field><name>sodium_lborresu</name><value/></field><field><name>k_lbstat</name><value/></field><field><name>sodium_lbstat</name><value/></field><field><name>chem_nximport</name><value/></field><field><name>chemistry_complete</name><value/></field><field><name>k_lborresu</name><value/></field><field><name>sodium_lborres</name><value/></field></event>
		
		
        </form>

	    <form>
		    <name>inr</name>
		    <event>
		    <name>1_arm_1</name>
		    <field><name>inr_lbdtc</name><value/></field><field><name>inr_complete</name><value/></field><field><name>inr_nximport</name><value/></field></event>
		
	       </form>
	
        </all_form_events></person></person_form_event>
        """
        self.expect_two_subjects = etree.tostring(etree.fromstring(self.output_two_subjects))
        
        self.result = etree.tostring(redi.create_empty_event_tree_for_study(self.data_two_subjects,self.data_all_form_events))
        self.assertEqual(self.expect_two_subjects, self.result)

    def tearDown(self):
        return()

if __name__ == '__main__':
    unittest.main()
