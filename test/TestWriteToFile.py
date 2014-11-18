import unittest
import os
from lxml import etree
from redi import redi

DEFAULT_DATA_DIRECTORY = os.getcwd()

class TestWriteToFile(unittest.TestCase):

    """ Variables setup """
    def setUp(self):
        redi.configure_logging(DEFAULT_DATA_DIRECTORY)
        self.test_raw_xml = """<?xml version='1.0' encoding='US-ASCII'?>
<study>
    <subject>
        <Study_Id>001-0001</Study_Id>
        <Study_Start>09/11/18</Study_Start>
        <Collection_Date>04/18/19</Collection_Date>
        <Collection_Time>11:57</Collection_Time>
        <Qualifying_Result>Y</Qualifying_Result>
        <Study_Stop>04/14/20</Study_Stop>
        <Component_Name>ALBUMIN</Component_Name>
        <loinc_code>1810650</loinc_code>
        <Reference_Unit>g/dL</Reference_Unit>
        <Reference_Low>3.5</Reference_Low>
        <Reference_High>5.0</Reference_High>
        <Result_Value>3.9</Result_Value>
    </subject>
</study>
"""

    def test_write_element_tree_to_file(self):
        """ Test the correctness of function
        redi.write_element_tree_to_file()
        """
        tree = etree.ElementTree(etree.fromstring(self.test_raw_xml))
        root = tree.getroot()
        redi.write_element_tree_to_file(tree, 'testWriteFile.xml')
        assert os.path.exists('testWriteFile.xml') == 1
        os.remove('testWriteFile.xml')

if __name__ == "__main__":
    unittest.main()
