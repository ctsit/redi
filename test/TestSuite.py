'''
@author : Radha
email : rkandula@ufl.edu

This file creates a test suite for all the test classes.

'''

import unittest


'''
    IMPORTANT: the imports should be updated in order to add the test to
    the test suite.
    note: No error will be thrown if the import is not done, at the same
    time test also will not be run even we addTest(<test_class>)
'''
from lxml import etree
from TestLog import TestLog
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
from TestGenerateRedcapEAV import TestGenerateRedcapEAV
from TestSendDatatoRedcap import TestSendDatatoRedcap
from TestUpdateFormImported import TestUpdateFormImported
from TestCreateSummaryReport import TestCreateSummaryReport


class redi_suite(unittest.TestSuite):

    def suite(self):
        # create a test suite
        redi_test_suite = unittest.TestSuite()
        redi_test_suite = unittest.TestLoader().\
        loadTestsFromTestCase(TestLog)

        # add the test to the suite in the order to be tested
        redi_test_suite.addTest(TestLog)
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
        redi_test_suite.addTest(TestGenerateRedcapEAV)
        redi_test_suite.addTest(TestSendDatatoRedcap)
        redi_test_suite.addTest(TestUpdateFormImported)
        redi_test_suite.addTest(TestCreateSummaryReport)
        redi_test_suite.addTest(TestUpdateFormCompletedFieldName)

        # return the suite
        return unittest.TestSuite([redi_test_suite])

def main():
    unittest.main(buffer=True)
    

if __name__ == '__main__':
    main()

