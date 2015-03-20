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
        <ORD_VALUE>KEEP ME PLEASE</ORD_VALUE>
        <DATE_TIME_STAMP>2013-12-07 00:00:09</DATE_TIME_STAMP>
        <STUDY_ID>999-0262</STUDY_ID>
        <timestamp>2013-12-07</timestamp>
        <redcapFormName>cbc</redcapFormName>
    </subject>
    <subject>
        <NAME>PLATELET COUNT</NAME>
        <ORD_VALUE>discard 1</ORD_VALUE>
        <DATE_TIME_STAMP>2013-12-07 00:00:20</DATE_TIME_STAMP>
        <STUDY_ID>999-0262</STUDY_ID>
        <timestamp>2013-12-07</timestamp>
        <redcapFormName>cbc</redcapFormName>
    </subject>
    <subject>
        <NAME>PLATELET COUNT</NAME>
        <ORD_VALUE>discard 2</ORD_VALUE>
        <DATE_TIME_STAMP>2013-12-07 00:00:30</DATE_TIME_STAMP>
        <STUDY_ID>999-0262</STUDY_ID>
        <timestamp>2013-12-07</timestamp>
        <redcapFormName>cbc</redcapFormName>
    </subject>
    <subject>
        <NAME>WHITE BLOOD COUNT</NAME>
        <ORD_VALUE>KEEP ME TOO</ORD_VALUE>
        <DATE_TIME_STAMP>2013-12-07 00:00:10</DATE_TIME_STAMP>
        <STUDY_ID>999-0262</STUDY_ID>
        <timestamp>2013-12-07</timestamp>
        <redcapFormName>cbc</redcapFormName>
    </subject>
    <subject>
        <NAME>WHITE BLOOD COUNT</NAME>
        <ORD_VALUE>discard 3</ORD_VALUE>
        <DATE_TIME_STAMP>2013-12-07 00:00:15</DATE_TIME_STAMP>
        <STUDY_ID>999-0262</STUDY_ID>
        <timestamp>2013-12-07</timestamp>
        <redcapFormName>cbc</redcapFormName>
    </subject>
    <subject>
        <NAME>WHITE BLOOD COUNT</NAME>
        <ORD_VALUE>KEEP ME AS WELL</ORD_VALUE>
        <DATE_TIME_STAMP>2013-13-07 00:00:17</DATE_TIME_STAMP>
        <STUDY_ID>999-0262</STUDY_ID>
        <timestamp>2013-13-07</timestamp>
        <redcapFormName>cbc</redcapFormName>
    </subject>
    <subject>
        <NAME>GLUCOSE</NAME>
        <ORD_VALUE>KEEP ME!</ORD_VALUE>
        <DATE_TIME_STAMP>2013-13-07 00:00:20</DATE_TIME_STAMP>
        <STUDY_ID>999-0262</STUDY_ID>
        <timestamp>2013-13-07</timestamp>
        <redcapFormName>chemistry</redcapFormName>
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
        self.assertTrue(count == 4)

        # verify that we got the lab result with the earliest time on a given
        # date
        self.assertEqual("KEEP ME PLEASE", keep_ele.text)

        # verify that a lab result with a different name on the same date and
        # in the same form is not deleted
        keep_ele = data.xpath('//subject/ORD_VALUE')[1]
        self.assertEqual("KEEP ME TOO", keep_ele.text)

        # verify that the lab result on a different date in the same form is
        # retained
        keep_ele = data.xpath('//subject/ORD_VALUE')[2]
        self.assertEqual("KEEP ME AS WELL", keep_ele.text)

        # verify that the lab result for a different form on the same day is
        # retianed
        keep_ele = data.xpath('//subject/ORD_VALUE')[3]
        self.assertEqual("KEEP ME!", keep_ele.text)


if __name__ == "__main__":
    unittest.main()
