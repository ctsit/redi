'''
@author : Radha
email : rkandula@ufl.edu

This file is to test the function writeElementTreetoFile of bin/redi.py
This file should be run from the project level folder (one level up from /bin)

'''
import unittest
import sys
import os
file_dir = os.path.dirname(os.path.realpath(__file__))
goal_dir = os.path.join(file_dir, "../")
proj_root = os.path.abspath(goal_dir)+'/'
sys.path.append(proj_root + 'bin')
import redi
from lxml import etree


class TestGenerateRedcapEAV(unittest.TestCase):
    def setUp(self):
        redi.configure_logging()
        self.test_form_data = {'cbc': 'cbc_complete', 'chemistry': 'chemistry_complete'}
        self.expect = """record,redcap_event_name,field_name,value\n001-0001,"3_arm_1",hemo_lborres,12.3\n001-0001,"3_arm_1",hemo_lborresu,"g/dL"\n001-0001,"3_arm_1",plat_lborres,92\n001-0001,"3_arm_1",plat_lborresu,"thou/cu mm"\n001-0001,"3_arm_1",neut_lborres,52.8\n001-0001,"3_arm_1",neut_lborresu,"%"\n001-0001,"3_arm_1",anc_lbstat,"NOT_DONE"\n001-0001,"3_arm_1",lym_lbstat,"NOT_DONE"\n001-0001,"3_arm_1",lymce_lbstat,"NOT_DONE"\n001-0001,"3_arm_1",wbc_lbstat,"NOT_DONE"\n001-0001,"3_arm_1",cbc_lbdtc,"1908-08-11"\n001-0001,"3_arm_1",cbc_complete,2\n001-0001,"3_arm_1",cbc_nximport,"Y"\n"""
        self.output_date_format = "%Y-%m-%d"
        self.test_xml = """<?xml version='1.0' encoding='US-ASCII'?>
        <study>
            <subject>
        <NAME>WHITE BLOOD CELL COUNT</NAME>
        <COMPONENT_ID>1577876</COMPONENT_ID>
        <ORD_VALUE>6.0</ORD_VALUE>
        <REFERENCE_LOW>4.0</REFERENCE_LOW>
        <REFERENCE_HIGH>10.0</REFERENCE_HIGH>
        <REFERENCE_UNIT>thou/cu mm</REFERENCE_UNIT>
        <SPECIMN_TAKEN_TIME>1908-08-11 10:05:00</SPECIMN_TAKEN_TIME>
        <STUDY_ID>001-0001</STUDY_ID>
    <timestamp>1908-08-11</timestamp><redcapFormName>cbc</redcapFormName><eventName>3_arm_1</eventName><formDateField>cbc_lbdtc</formDateField><formCompletedFieldName>cbc_complete</formCompletedFieldName><formImportedFieldName>cbc_nximport</formImportedFieldName><redcapFieldNameValue>wbc_lborres</redcapFieldNameValue><redcapFieldNameUnits>wbc_lborresu</redcapFieldNameUnits><redcapFieldNameStatus>wbc_lbstat</redcapFieldNameStatus></subject>
    <subject>
        <NAME>HEMOGLOBIN</NAME>
        <COMPONENT_ID>1534435</COMPONENT_ID>
        <ORD_VALUE>12.3</ORD_VALUE>
        <REFERENCE_LOW>12.0</REFERENCE_LOW>
        <REFERENCE_HIGH>16.0</REFERENCE_HIGH>
        <REFERENCE_UNIT>g/dL</REFERENCE_UNIT>
        <SPECIMN_TAKEN_TIME>1908-08-11 10:05:00</SPECIMN_TAKEN_TIME>
        <STUDY_ID>001-0001</STUDY_ID>
    <timestamp>1908-08-11</timestamp><redcapFormName>cbc</redcapFormName><eventName>3_arm_1</eventName><formDateField>cbc_lbdtc</formDateField><formCompletedFieldName>cbc_complete</formCompletedFieldName><formImportedFieldName>cbc_nximport</formImportedFieldName><redcapFieldNameValue>hemo_lborres</redcapFieldNameValue><redcapFieldNameUnits>hemo_lborresu</redcapFieldNameUnits><redcapFieldNameStatus>hemo_lbstat</redcapFieldNameStatus></subject>
    <subject>
        <NAME>PLATELET COUNT</NAME>
        <COMPONENT_ID>1009</COMPONENT_ID>
        <ORD_VALUE>92</ORD_VALUE>
        <REFERENCE_LOW>150</REFERENCE_LOW>
        <REFERENCE_HIGH>450</REFERENCE_HIGH>
        <REFERENCE_UNIT>thou/cu mm</REFERENCE_UNIT>
        <SPECIMN_TAKEN_TIME>1908-08-11 10:05:00</SPECIMN_TAKEN_TIME>
        <STUDY_ID>001-0001</STUDY_ID>
    <timestamp>1908-08-11</timestamp><redcapFormName>cbc</redcapFormName><eventName>3_arm_1</eventName><formDateField>cbc_lbdtc</formDateField><formCompletedFieldName>cbc_complete</formCompletedFieldName><formImportedFieldName>cbc_nximport</formImportedFieldName><redcapFieldNameValue>plat_lborres</redcapFieldNameValue><redcapFieldNameUnits>plat_lborresu</redcapFieldNameUnits><redcapFieldNameStatus>plat_lbstat</redcapFieldNameStatus></subject>
    <subject>
        <NAME>NEUTROPHILS RELATIVE PERCENT</NAME>
        <COMPONENT_ID>1539315</COMPONENT_ID>
        <ORD_VALUE>52.8</ORD_VALUE>
        <REFERENCE_LOW>40.0</REFERENCE_LOW>
        <REFERENCE_HIGH>80.0</REFERENCE_HIGH>
        <REFERENCE_UNIT>%</REFERENCE_UNIT>
        <SPECIMN_TAKEN_TIME>1908-08-11 10:05:00</SPECIMN_TAKEN_TIME>
        <STUDY_ID>001-0001</STUDY_ID>
    <timestamp>1908-08-11</timestamp><redcapFormName>cbc</redcapFormName><eventName>3_arm_1</eventName><formDateField>cbc_lbdtc</formDateField><formCompletedFieldName>cbc_complete</formCompletedFieldName><formImportedFieldName>cbc_nximport</formImportedFieldName><redcapFieldNameValue>neut_lborres</redcapFieldNameValue><redcapFieldNameUnits>neut_lborresu</redcapFieldNameUnits><redcapFieldNameStatus>neut_lbstat</redcapFieldNameStatus></subject>
        </study>
        """
        self.translationTableXml = '''<rediFieldMap>
    <clinicalComponent>
        <clinicalComponentId>1577876</clinicalComponentId>
        <clinicalComponentName>WHITE BLOOD CELL COUNT</clinicalComponentName>
        <redcapFormName>cbc</redcapFormName>
        <redcapFieldNameValue>wbc_lborres</redcapFieldNameValue>
        <redcapFieldNameValueDescriptiveText>WBC</redcapFieldNameValueDescriptiveText>
        <redcapFieldNameUnits>wbc_lborresu</redcapFieldNameUnits>
        <redcapFieldNameUnitsDescriptiveText>WBC units</redcapFieldNameUnitsDescriptiveText>
        <redcapFieldNameStatus>wbc_lbstat</redcapFieldNameStatus>
        <lbtest>Leukocytes</lbtest>
        <lbtestcd>WBC</lbtestcd>
    </clinicalComponent>
    <clinicalComponent>
        <clinicalComponentId>999</clinicalComponentId>
        <clinicalComponentName>WBC</clinicalComponentName>
        <redcapFormName>cbc</redcapFormName>
        <redcapFieldNameValue>wbc_lborres</redcapFieldNameValue>
        <redcapFieldNameValueDescriptiveText>WBC</redcapFieldNameValueDescriptiveText>
        <redcapFieldNameUnits>wbc_lborresu</redcapFieldNameUnits>
        <redcapFieldNameUnitsDescriptiveText>WBC units</redcapFieldNameUnitsDescriptiveText>
        <redcapFieldNameStatus>wbc_lbstat</redcapFieldNameStatus>
        <lbtest>Leukocytes</lbtest>
        <lbtestcd>WBC</lbtestcd>
    </clinicalComponent>
    <clinicalComponent>
        <clinicalComponentId>913</clinicalComponentId>
        <clinicalComponentName>NEUTROPHILS</clinicalComponentName>
        <redcapFormName>cbc</redcapFormName>
        <redcapFieldNameValue>neut_lborres</redcapFieldNameValue>
        <redcapFieldNameValueDescriptiveText>Neutrophils</redcapFieldNameValueDescriptiveText>
        <redcapFieldNameUnits>neut_lborresu</redcapFieldNameUnits>
        <redcapFieldNameUnitsDescriptiveText>Neutrophils units</redcapFieldNameUnitsDescriptiveText>
        <redcapFieldNameStatus>neut_lbstat</redcapFieldNameStatus>
        <lbtest>Neutrophils/Leukocytes</lbtest>
        <lbtestcd>NEUTLE</lbtestcd>
    </clinicalComponent>
    <clinicalComponent>
        <clinicalComponentId>1539315</clinicalComponentId>
        <clinicalComponentName>NEUTROPHILS RELATIVE PERCENT</clinicalComponentName>
        <redcapFormName>cbc</redcapFormName>
        <redcapFieldNameValue>neut_lborres</redcapFieldNameValue>
        <redcapFieldNameValueDescriptiveText>Neutrophils</redcapFieldNameValueDescriptiveText>
        <redcapFieldNameUnits>neut_lborresu</redcapFieldNameUnits>
        <redcapFieldNameUnitsDescriptiveText>Neutrophils units</redcapFieldNameUnitsDescriptiveText>
        <redcapFieldNameStatus>neut_lbstat</redcapFieldNameStatus>
        <lbtest>Neutrophils/Leukocytes</lbtest>
        <lbtestcd>NEUTLE</lbtestcd>
    </clinicalComponent>
    <clinicalComponent>
        <clinicalComponentId>1558101</clinicalComponentId>
        <clinicalComponentName>NEUTROPHILS ABSOLUTE COUNT</clinicalComponentName>
        <redcapFormName>cbc</redcapFormName>
        <redcapFieldNameValue>anc_lborres</redcapFieldNameValue>
        <redcapFieldNameValueDescriptiveText>ANC</redcapFieldNameValueDescriptiveText>
        <redcapFieldNameUnits>anc_lborresu</redcapFieldNameUnits>
        <redcapFieldNameUnitsDescriptiveText>ANC units</redcapFieldNameUnitsDescriptiveText>
        <redcapFieldNameStatus>anc_lbstat</redcapFieldNameStatus>
        <lbtest>Absolute Neutrophil Count</lbtest>
        <lbtestcd>NEUT</lbtestcd>
    </clinicalComponent>
    <clinicalComponent>
        <clinicalComponentId>1009</clinicalComponentId>
        <clinicalComponentName>PLATELET COUNT</clinicalComponentName>
        <redcapFormName>cbc</redcapFormName>
        <redcapFieldNameValue>plat_lborres</redcapFieldNameValue>
        <redcapFieldNameValueDescriptiveText>Platelet count</redcapFieldNameValueDescriptiveText>
        <redcapFieldNameUnits>plat_lborresu</redcapFieldNameUnits>
        <redcapFieldNameUnitsDescriptiveText>Platelet units</redcapFieldNameUnitsDescriptiveText>
        <redcapFieldNameStatus>plat_lbstat</redcapFieldNameStatus>
        <lbtest>Platelets</lbtest>
        <lbtestcd>PLAT</lbtestcd>
    </clinicalComponent>
    <clinicalComponent>
        <clinicalComponentId>1577116</clinicalComponentId>
        <clinicalComponentName>PLATELET COUNT</clinicalComponentName>
        <redcapFormName>cbc</redcapFormName>
        <redcapFieldNameValue>plat_lborres</redcapFieldNameValue>
        <redcapFieldNameValueDescriptiveText>Platelet count</redcapFieldNameValueDescriptiveText>
        <redcapFieldNameUnits>plat_lborresu</redcapFieldNameUnits>
        <redcapFieldNameUnitsDescriptiveText>Platelet units</redcapFieldNameUnitsDescriptiveText>
        <redcapFieldNameStatus>plat_lbstat</redcapFieldNameStatus>
        <lbtest>Platelets</lbtest>
        <lbtestcd>PLAT</lbtestcd>
    </clinicalComponent>
    <clinicalComponent>
        <clinicalComponentId>1534444</clinicalComponentId>
        <clinicalComponentName>LYMPHOCYTES ABSOLUTE COUNT</clinicalComponentName>
        <redcapFormName>cbc</redcapFormName>
        <redcapFieldNameValue>lym_lborres</redcapFieldNameValue>
        <redcapFieldNameValueDescriptiveText>Lymphocytes (absolute)</redcapFieldNameValueDescriptiveText>
        <redcapFieldNameUnits>lym_lborresu</redcapFieldNameUnits>
        <redcapFieldNameUnitsDescriptiveText>Lymphocytes units</redcapFieldNameUnitsDescriptiveText>
        <redcapFieldNameStatus>lym_lbstat</redcapFieldNameStatus>
        <lbtest>lym_lbtest</lbtest>
        <lbtestcd>lym_lbtestcd</lbtestcd>
    </clinicalComponent>
    <clinicalComponent>
        <clinicalComponentId>918</clinicalComponentId>
        <clinicalComponentName>LYMPHOCYTES</clinicalComponentName>
        <redcapFormName>cbc</redcapFormName>
        <redcapFieldNameValue>lymce_lborres</redcapFieldNameValue>
        <redcapFieldNameValueDescriptiveText>Lymphocytes (%)</redcapFieldNameValueDescriptiveText>
        <redcapFieldNameUnits>lymce_lborresu</redcapFieldNameUnits>
        <redcapFieldNameUnitsDescriptiveText>Lymphocytes (%) units</redcapFieldNameUnitsDescriptiveText>
        <redcapFieldNameStatus>lymce_lbstat</redcapFieldNameStatus>
        <lbtest>lymce_lbtest</lbtest>
        <lbtestcd>lymce_lbtestcd</lbtestcd>
    </clinicalComponent>
    <clinicalComponent>
        <clinicalComponentId>1534435</clinicalComponentId>
        <clinicalComponentName>HEMOGLOBIN</clinicalComponentName>
        <redcapFormName>cbc</redcapFormName>
        <redcapFieldNameValue>hemo_lborres</redcapFieldNameValue>
        <redcapFieldNameValueDescriptiveText>Hemoglobin</redcapFieldNameValueDescriptiveText>
        <redcapFieldNameUnits>hemo_lborresu</redcapFieldNameUnits>
        <redcapFieldNameUnitsDescriptiveText>Hemoglobin units</redcapFieldNameUnitsDescriptiveText>
        <redcapFieldNameStatus>hemo_lbstat</redcapFieldNameStatus>
        <lbtest>hemo_lbtest</lbtest>
        <lbtestcd>hemo_lbtestcd</lbtestcd>
    </clinicalComponent>
    <clinicalComponent>
        <clinicalComponentId>1534076</clinicalComponentId>
        <clinicalComponentName>BILIRUBIN TOTAL</clinicalComponentName>
        <redcapFormName>chemistry</redcapFormName>
        <redcapFieldNameValue>tbil_lborres</redcapFieldNameValue>
        <redcapFieldNameValueDescriptiveText>Total Bilirubin</redcapFieldNameValueDescriptiveText>
        <redcapFieldNameUnits>tbil_lborresu</redcapFieldNameUnits>
        <redcapFieldNameUnitsDescriptiveText>Total Bilirubin units</redcapFieldNameUnitsDescriptiveText>
        <redcapFieldNameStatus>tbil_lbstat</redcapFieldNameStatus>
        <lbtest>Total Bilirubin</lbtest>
        <lbtestcd>BILI</lbtestcd>
    </clinicalComponent>
    <clinicalComponent>
        <clinicalComponentId>1558221</clinicalComponentId>
        <clinicalComponentName>BILIRUBIN DIRECT</clinicalComponentName>
        <redcapFormName>chemistry</redcapFormName>
        <redcapFieldNameValue>dbil_lborres</redcapFieldNameValue>
        <redcapFieldNameValueDescriptiveText>Direct Bilirubin</redcapFieldNameValueDescriptiveText>
        <redcapFieldNameUnits>dbil_lborresu</redcapFieldNameUnits>
        <redcapFieldNameUnitsDescriptiveText>Direct Bilirubin units</redcapFieldNameUnitsDescriptiveText>
        <redcapFieldNameStatus>dbil_lbstat</redcapFieldNameStatus>
        <lbtest>Total Bilirubin</lbtest>
        <lbtestcd>BILI</lbtestcd>
    </clinicalComponent>

    <clinicalComponent>
        <clinicalComponentId>1525870</clinicalComponentId>
        <clinicalComponentName>ALT (SGPT)</clinicalComponentName>
        <redcapFormName>chemistry</redcapFormName>
        <redcapFieldNameValue>alt_lborres</redcapFieldNameValue>
        <redcapFieldNameValueDescriptiveText>Serum ALT</redcapFieldNameValueDescriptiveText>
        <redcapFieldNameUnits>alt_lborresu</redcapFieldNameUnits>
        <redcapFieldNameUnitsDescriptiveText>Serum ALT units</redcapFieldNameUnitsDescriptiveText>
        <redcapFieldNameStatus>alt_lbstat</redcapFieldNameStatus>
        <lbtest>Alanine Aminotransferase</lbtest>
        <lbtestcd>ALT</lbtestcd>
    </clinicalComponent>

    <clinicalComponent>
        <clinicalComponentId>1526000</clinicalComponentId>
        <clinicalComponentName>AST (SGOT)</clinicalComponentName>
        <redcapFormName>chemistry</redcapFormName>
        <redcapFieldNameValue>ast_lborres</redcapFieldNameValue>
        <redcapFieldNameValueDescriptiveText>Serum AST</redcapFieldNameValueDescriptiveText>
        <redcapFieldNameUnits>ast_lborresu</redcapFieldNameUnits>
        <redcapFieldNameUnitsDescriptiveText>Serum AST units</redcapFieldNameUnitsDescriptiveText>
        <redcapFieldNameStatus>ast_lbstat</redcapFieldNameStatus>
        <lbtest>Aspartate Aminotransferase</lbtest>
        <lbtestcd>AST</lbtestcd>
    </clinicalComponent>

    <clinicalComponent>
        <clinicalComponentId>1810650</clinicalComponentId>
        <clinicalComponentName>ALBUMIN</clinicalComponentName>
        <redcapFormName>chemistry</redcapFormName>
        <redcapFieldNameValue>alb_lborres</redcapFieldNameValue>
        <redcapFieldNameValueDescriptiveText>Albumin</redcapFieldNameValueDescriptiveText>
        <redcapFieldNameUnits>alb_lborresu</redcapFieldNameUnits>
        <redcapFieldNameUnitsDescriptiveText>Albumin units</redcapFieldNameUnitsDescriptiveText>
        <redcapFieldNameStatus>alb_lbstat</redcapFieldNameStatus>
        <lbtest>Albumin</lbtest>
        <lbtestcd>ALB</lbtestcd>
    </clinicalComponent>

    <clinicalComponent>
        <clinicalComponentId>1526296</clinicalComponentId>
        <clinicalComponentName>CREATININE</clinicalComponentName>
        <redcapFormName>chemistry</redcapFormName>
        <redcapFieldNameValue>creat_lborres</redcapFieldNameValue>
        <redcapFieldNameValueDescriptiveText>Creatinine</redcapFieldNameValueDescriptiveText>
        <redcapFieldNameUnits>creat_lborresu</redcapFieldNameUnits>
        <redcapFieldNameUnitsDescriptiveText>Creatinine units</redcapFieldNameUnitsDescriptiveText>
        <redcapFieldNameStatus>creat_lbstat</redcapFieldNameStatus>
        <lbtest>Creatinine</lbtest>
        <lbtestcd>CREAT</lbtestcd>
    </clinicalComponent>

    <clinicalComponent>
        <clinicalComponentId>1510655</clinicalComponentId>
        <clinicalComponentName>GLUCOSE</clinicalComponentName>
        <redcapFormName>chemistry</redcapFormName>
        <redcapFieldNameValue>gluc_lborres</redcapFieldNameValue>
        <redcapFieldNameValueDescriptiveText>Glucose</redcapFieldNameValueDescriptiveText>
        <redcapFieldNameUnits>gluc_lborresu</redcapFieldNameUnits>
        <redcapFieldNameUnitsDescriptiveText>Glucose units</redcapFieldNameUnitsDescriptiveText>
        <redcapFieldNameStatus>gluc_lbstat</redcapFieldNameStatus>
        <lbtest></lbtest>
        <lbtestcd></lbtestcd>
    </clinicalComponent>

    <clinicalComponent>
        <clinicalComponentId>968</clinicalComponentId>
        <clinicalComponentName>GLUCOSE</clinicalComponentName>
        <redcapFormName>chemistry</redcapFormName>
        <redcapFieldNameValue>gluc_lborres</redcapFieldNameValue>
        <redcapFieldNameValueDescriptiveText>Glucose</redcapFieldNameValueDescriptiveText>
        <redcapFieldNameUnits>gluc_lborresu</redcapFieldNameUnits>
        <redcapFieldNameUnitsDescriptiveText>Glucose units</redcapFieldNameUnitsDescriptiveText>
        <redcapFieldNameStatus>gluc_lbstat</redcapFieldNameStatus>
        <lbtest></lbtest>
        <lbtestcd></lbtestcd>
    </clinicalComponent>

    <clinicalComponent>
        <clinicalComponentId>1534081</clinicalComponentId>
        <clinicalComponentName>POTASSIUM</clinicalComponentName>
        <redcapFormName>chemistry</redcapFormName>
        <redcapFieldNameValue>k_lborres</redcapFieldNameValue>
        <redcapFieldNameValueDescriptiveText>Potassium</redcapFieldNameValueDescriptiveText>
        <redcapFieldNameUnits>k_lborresu</redcapFieldNameUnits>
        <redcapFieldNameUnitsDescriptiveText>Potassium units</redcapFieldNameUnitsDescriptiveText>
        <redcapFieldNameStatus>k_lbstat</redcapFieldNameStatus>
        <lbtest></lbtest>
        <lbtestcd></lbtestcd>
    </clinicalComponent>

    <clinicalComponent>
        <clinicalComponentId>971</clinicalComponentId>
        <clinicalComponentName>POTASSIUM</clinicalComponentName>
        <redcapFormName>chemistry</redcapFormName>
        <redcapFieldNameValue>k_lborres</redcapFieldNameValue>
        <redcapFieldNameValueDescriptiveText>Potassium</redcapFieldNameValueDescriptiveText>
        <redcapFieldNameUnits>k_lborresu</redcapFieldNameUnits>
        <redcapFieldNameUnitsDescriptiveText>Potassium units</redcapFieldNameUnitsDescriptiveText>
        <redcapFieldNameStatus>k_lbstat</redcapFieldNameStatus>
        <lbtest></lbtest>
        <lbtestcd></lbtestcd>
    </clinicalComponent>

    <clinicalComponent>
        <clinicalComponentId>1534098</clinicalComponentId>
        <clinicalComponentName>SODIUM</clinicalComponentName>
        <redcapFormName>chemistry</redcapFormName>
        <redcapFieldNameValue>sodium_lborres</redcapFieldNameValue>
        <redcapFieldNameValueDescriptiveText>Sodium</redcapFieldNameValueDescriptiveText>
        <redcapFieldNameUnits>sodium_lborresu</redcapFieldNameUnits>
        <redcapFieldNameUnitsDescriptiveText>Sodium units</redcapFieldNameUnitsDescriptiveText>
        <redcapFieldNameStatus>sodium_lbstat</redcapFieldNameStatus>
        <lbtest>Sodium</lbtest>
        <lbtestcd>SODIUM</lbtestcd>
    </clinicalComponent>

    <clinicalComponent>
        <clinicalComponentId>1810583</clinicalComponentId>
        <clinicalComponentName>INR</clinicalComponentName>
        <redcapFormName>inr</redcapFormName>
        <redcapFieldNameValue>inr_lborres</redcapFieldNameValue>
        <redcapFieldNameValueDescriptiveText>INR</redcapFieldNameValueDescriptiveText>
        <redcapFieldNameStatus>inr_lbstat</redcapFieldNameStatus>
        <lbtest>Prothrombin Intl. Normalized Ratio</lbtest>
        <lbtestcd>INR</lbtestcd>
    </clinicalComponent>

    <clinicalComponent>
        <clinicalComponentId>1526776</clinicalComponentId>
        <clinicalComponentName>INR</clinicalComponentName>
        <redcapFormName>inr</redcapFormName>
        <redcapFieldNameValue>inr_lborres</redcapFieldNameValue>
        <redcapFieldNameValueDescriptiveText>INR</redcapFieldNameValueDescriptiveText>
        <redcapFieldNameStatus>inr_lbstat</redcapFieldNameStatus>
        <lbtest>Prothrombin Intl. Normalized Ratio</lbtest>
        <lbtestcd>INR</lbtestcd>
    </clinicalComponent>

</rediFieldMap>
 '''




    def testGenerateRedcapEAV(self):
        # check if there exists an eav already in the path

        sys.path.append('config')
        newpath = proj_root+'config'
        configFolderCreatedNow = False
        if not os.path.exists(newpath): 
            configFolderCreatedNow = True
            os.makedirs(newpath)
        if os.path.isfile(proj_root+'config/redcap.eav'):
            #print "already exists"
            # if it exists then delete it
            os.remove(proj_root+'config/redcap.eav')
        # build element tree from the test xml in setup
        translational_table_tree = etree.ElementTree(etree.fromstring(self.translationTableXml))
        redi.translational_table_tree = translational_table_tree
        tree = etree.ElementTree(etree.fromstring(self.test_xml))

        # run the actual function to test
        redi.generate_redcap_eav(tree, self.test_form_data, self.output_date_format)
        try:
            read_data = open(proj_root+'config/redcap.eav', 'r')
            lines = read_data.readlines()
            content = ''
            for line in lines:
                content+=line
            self.assertEqual(self.expect, content)
        except Exception, e:
            raise e
        
        with open(proj_root+'config/redcap.eav'):
            os.remove(proj_root+'config/redcap.eav')
            if configFolderCreatedNow:
                os.rmdir(newpath)

if __name__ == "__main__":
    unittest.main()
