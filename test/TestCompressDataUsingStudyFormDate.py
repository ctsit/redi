import unittest
from lxml import etree
from redi import redi
import logging


class TestCompressDataUsingStudyFormDate(unittest.TestCase):

    def setUp(self):
         # silence logger during testing
        redi.logger = logging.getLogger('redi')
        redi.logger.addHandler(logging.NullHandler())

        self.xml = """<?xml version="1.0" encoding="UTF-8"?>
<study>
    <subject>
        <NAME>PLATELET COUNT</NAME>
        <ORD_VALUE> KEEP ME PLEASE </ORD_VALUE>
        <DATE_TIME_STAMP>2013-12-07 00:00:09</DATE_TIME_STAMP>
        <STUDY_ID>999-0262</STUDY_ID>
        <timestamp>2013-12-07</timestamp>
        <redcapFormName>cbc</redcapFormName>
    </subject>
    <subject>
        <NAME>PLATELET COUNT</NAME>
        <ORD_VALUE> discard 1 </ORD_VALUE>
        <DATE_TIME_STAMP>2013-12-07 00:00:10</DATE_TIME_STAMP>
        <STUDY_ID>999-0262</STUDY_ID>
        <timestamp>2013-12-07</timestamp>
        <redcapFormName>cbc</redcapFormName>
    </subject>
    <subject>
        <NAME>PLATELET COUNT</NAME>
        <ORD_VALUE> discard 2 </ORD_VALUE>
        <DATE_TIME_STAMP>2013-12-07 00:00:20</DATE_TIME_STAMP>
        <STUDY_ID>999-0262</STUDY_ID>
        <timestamp>2013-12-07</timestamp>
        <redcapFormName>cbc</redcapFormName>
    </subject>
</study>
"""

    def test_compress(self):
        #parser = etree.XMLParser(remove_comments = True)
        #data = etree.parse('ha.xml', parser = parser)
        data = etree.ElementTree(etree.fromstring(self.xml))
        redi.compress_data_using_study_form_date(data)
        count = len(data.xpath('//subject'))
        keep_ele = data.xpath('//subject/ORD_VALUE')[0]

        # verify that only one subject element is left
        self.assertTrue(count == 1)

        # verify that we got the lab result with the earliest time on a given date
        self.assertTrue("KEEP ME PLEASE", keep_ele.text)
        #print etree.tostring(data, pretty_print = True)


if __name__ == "__main__":
    unittest.main()
