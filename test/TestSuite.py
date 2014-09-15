'''
This file creates a test suite for all the test classes.

    IMPORTANT: the imports should be updated in order to add the test to
    the test suite.
    Notes:
        - No error will be thrown if the `import` statement is missing
        - No test will be run if the `import` statement is missing even
            if we add the line `addTest(<test_class>)`
        - To run the script the user must instal a few libraries
            On a mac: pip install lxml request
'''
import unittest
from TestReadConfig import TestReadConfig
from TestWriteToFile import TestWriteToFile
from TestUpdateRedcapForm import TestUpdateRedcapForm
from TestUpdateTimestamp import TestUpdateTimestamp
from TestUpdateFormDateField import TestUpdateFormDateField
from TestUpdateFormCompletedFieldName import TestUpdateFormCompletedFieldName
from TestSortElementTree import TestSortElementTree
from TestUpdateDataFromLookup import TestUpdateDataFromLookup
from TestAddElementsToTree import TestAddElementsToTree
from TestUpdateRedcapFieldNameValueAndUnits import TestUpdateRedcapFieldNameValueAndUnits
from TestUpdateEventName import TestUpdateEventName
from TestResearchIdToRedcapId import TestResearchIdToRedcapId
from TestUpdateFormImported import TestUpdateFormImported
from TestCreateSummaryReport import TestCreateSummaryReport
from TestUpdateStatusField import TestUpdateStatusField
from TestCreateEmptyEventsForOneSubject import TestCreateEmptyEventsForOneSubject
from TestCreateEmptyEventTreeForStudy import TestCreateEmptyEventTreeForStudy
from TestCreateImportDataJson import TestCreateImportDataJson
from TestGenerateOutput import TestGenerateOutput
from TestParseAll import TestParseAll
from TestHandleREDCapResponse import TestHandleErrorsInREDCapResponse
from TestParseRawXml import TestParseRawXml
from TestValidateXmlFleAndExtractData import TestValidateXmlFleAndExtractData
from TestConvertComponentIdToLoincCode import TestConvertComponentIdToLoincCode
from TestCopyDataToPersonFormEventTree import TestCopyDataToPersonFormEventTree
from TestGetEMRData import TestGetEMRData
from TestResume import TestResume
from TestPersonFormEventsRepository import TestPersonFormEventsRepository
from TestVerifyAndCorrectCollectionDate import TestVerifyAndCorrectCollectionDate
from TestSkipBlanks import TestSkipBlanks
from TestRediEmail import TestRediEmail

class redi_suite(unittest.TestSuite):

    def suite(self):
        # create a test suite
        redi_test_suite = unittest.TestSuite()

        # add the test to the suite in the order to be tested
        redi_test_suite.addTest(TestReadConfig)
        redi_test_suite.addTest(TestWriteToFile)
        redi_test_suite.addTest(TestUpdateRedcapForm)
        redi_test_suite.addTest(TestUpdateTimestamp)
        redi_test_suite.addTest(TestUpdateFormDateField)
        redi_test_suite.addTest(TestSortElementTree)
        redi_test_suite.addTest(TestUpdateDataFromLookup)
        redi_test_suite.addTest(TestAddElementsToTree)
        redi_test_suite.addTest(TestUpdateRedcapFieldNameValueAndUnits)
        redi_test_suite.addTest(TestUpdateEventName)
        redi_test_suite.addTest(TestResearchIdToRedcapId)
        redi_test_suite.addTest(TestUpdateFormImported)
        redi_test_suite.addTest(TestCreateSummaryReport)
        redi_test_suite.addTest(TestUpdateFormCompletedFieldName)
        redi_test_suite.addTest(TestUpdateStatusField)
        redi_test_suite.addTest(TestCreateEmptyEventsForOneSubject)
        redi_test_suite.addTest(TestCreateEmptyEventTreeForStudy)
        redi_test_suite.addTest(TestVerifyAndCorrectCollectionDate)
        redi_test_suite.addTest(TestParseAll)

        # The redesign functions May 2014
        redi_test_suite.addTest(TestCreateImportDataJson)
        redi_test_suite.addTest(TestGenerateOutput)
        redi_test_suite.addTest(TestHandleErrorsInREDCapResponse)
        redi_test_suite.addTest(TestParseRawXml)
        redi_test_suite.addTest(TestValidateXmlFleAndExtractData)
        redi_test_suite.addTest(TestConvertComponentIdToLoincCode)
        redi_test_suite.addTest(TestCopyDataToPersonFormEventTree)
        redi_test_suite.addTest(TestGetEMRData)
        redi_test_suite.addTest(TestResume)
        redi_test_suite.addTest(TestPersonFormEventsRepository)
        redi_test_suite.addTest(TestSkipBlanks)
        redi_test_suite.addTest(TestRediEmail)

        # return the suite
        return unittest.TestSuite([redi_test_suite])

def main():
    unittest.main(buffer=True)


if __name__ == '__main__':
    main()
