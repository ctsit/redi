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
sys.path.append(proj_root + 'bin/')
import redi
from lxml import etree


class TestWriteToFile(unittest.TestCase):
    def setUp(self):
        redi.configure_logging()
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
        <Component_ID>1810650</Component_ID>
        <Reference_Unit>g/dL</Reference_Unit>
        <Reference_Low>3.5</Reference_Low>
        <Reference_High>5.0</Reference_High>
        <Result_Value>3.9</Result_Value>
    </subject>
    <subject>
        <Study_Id>001-0001</Study_Id>
        <Study_Start>09/11/18</Study_Start>
        <Collection_Date>04/18/19</Collection_Date>
        <Collection_Time>11:57</Collection_Time>
        <Qualifying_Result>Y</Qualifying_Result>
        <Study_Stop>04/14/20</Study_Stop>
        <Component_Name>ALKALINE PHOSPHATASE</Component_Name>
        <Component_ID>1525848</Component_ID>
        <Reference_Unit>U/L</Reference_Unit>
        <Reference_Low>35</Reference_Low>
        <Reference_High>129</Reference_High>
        <Result_Value>112</Result_Value>
    </subject>
</study>
"""

    '''  '''

    # this is a function to test the writeElementTreetoFile function.
    # we called it with input file and tried to write the element tree to an XML file
    def testWriteElementTreetoFile(self):
        import xml.etree.ElementTree as ET
        tree = etree.ElementTree(etree.fromstring(self.test_raw_xml))
        root = tree.getroot()
        redi.write_element_tree_to_file(tree,'testWriteFile.xml')
        assert os.path.exists('testWriteFile.xml') == 1
        os.remove('testWriteFile.xml')

if __name__ == "__main__":
    unittest.main()
