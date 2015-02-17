import unittest
from lxml import etree
from redi import redi

class TestSortElementTree(unittest.TestCase):

    def setUp(self):
        #redi.configure_logging('.')

        # un-sorted XML file
        self.unsorted = """<?xml version="1.0" encoding="UTF-8"?>
<study>
   <subject>
        <NAME>PLATELET COUNT</NAME>
        <DATE_TIME_STAMP>2013-12-02 00:00:00</DATE_TIME_STAMP>
        <STUDY_ID>999-0262</STUDY_ID>
        <timestamp>2013-12-07</timestamp>
        <redcapFormName>cbc</redcapFormName>
    </subject>
 
    <subject>
        <NAME>PLATELET COUNT</NAME>
        <DATE_TIME_STAMP>2013-12-03 00:00:00</DATE_TIME_STAMP>
        <STUDY_ID>999-0262</STUDY_ID>
        <timestamp>2013-12-07</timestamp>
        <redcapFormName>cbc</redcapFormName>
    </subject>
    <subject>
        <NAME>PLATELET COUNT</NAME>
        <DATE_TIME_STAMP>2013-12-01 00:00:00</DATE_TIME_STAMP>
        <STUDY_ID>999-0262</STUDY_ID>
        <timestamp>2013-12-07</timestamp>
        <redcapFormName>cbc</redcapFormName>
    </subject>
</study>"""

        # we expect the following sorted tree
        self.sorted_tree = """<?xml version="1.0" encoding="UTF-8"?>
<study>
    <subject>
        <NAME>PLATELET COUNT</NAME>
        <DATE_TIME_STAMP>2013-12-01 00:00:00</DATE_TIME_STAMP>
        <STUDY_ID>999-0262</STUDY_ID>
        <timestamp>2013-12-07</timestamp>
        <redcapFormName>cbc</redcapFormName>
    </subject>
    <subject>
        <NAME>PLATELET COUNT</NAME>
        <DATE_TIME_STAMP>2013-12-02 00:00:00</DATE_TIME_STAMP>
        <STUDY_ID>999-0262</STUDY_ID>
        <timestamp>2013-12-07</timestamp>
        <redcapFormName>cbc</redcapFormName>
    </subject>
    <subject>
        <NAME>PLATELET COUNT</NAME>
        <DATE_TIME_STAMP>2013-12-03 00:00:00</DATE_TIME_STAMP>
        <STUDY_ID>999-0262</STUDY_ID>
        <timestamp>2013-12-07</timestamp>
        <redcapFormName>cbc</redcapFormName>
    </subject>
</study>"""


    def test_sort_elementtree(self):
        tree_to_sort = etree.ElementTree(etree.fromstring(self.unsorted))
        redi.sort_element_tree(tree_to_sort)

        par = etree.XMLParser(remove_blank_text = True)
        clean_expect = etree.XML(self.sorted_tree, parser=par)
        clean_result = etree.XML(etree.tostring(tree_to_sort), parser=par)
        self.assertEqual(etree.tostring(clean_expect), etree.tostring(clean_result))

if __name__ == '__main__':
    unittest.main()

