import unittest
from lxml import etree
from redi import redi
import logging

class TestCompressDataUsingStudyFormDate(unittest.TestCase):

    def setUp(self):
        # silence logger during testing
        #redi.configure_logging('.')
        redi.logger = logging.getLogger('redi')
        redi.logger.addHandler(logging.NullHandler())

        self.xml = """<?xml version="1.0" encoding="UTF-8"?>
<study>

    <comment> ========== Date A ============ </comment>
    <subject>
        <NAME>Name_A</NAME>
        <ORD_VALUE>KEEP_ME_PLEASE</ORD_VALUE>
        <STUDY_ID>262</STUDY_ID>
        <redcapFormName>form_a</redcapFormName>
        <loinc_code>component_A</loinc_code>
        <DATE_TIME_STAMP>2013-12-07 00:00:09</DATE_TIME_STAMP>
    </subject>

    <subject>
        <NAME>Name_A</NAME>
        <ORD_VALUE>discard_1</ORD_VALUE>
        <STUDY_ID>262</STUDY_ID>
        <redcapFormName>form_a</redcapFormName>
        <loinc_code>component_A</loinc_code>
        <DATE_TIME_STAMP>2013-12-07 00:00:20</DATE_TIME_STAMP>
    </subject>

    <subject>
        <NAME>Name_A</NAME>
        <ORD_VALUE>discard_2</ORD_VALUE>
        <STUDY_ID>262</STUDY_ID>
        <redcapFormName>form_a</redcapFormName>
        <loinc_code>component_A</loinc_code>
        <DATE_TIME_STAMP>2013-12-07 00:00:30</DATE_TIME_STAMP>
    </subject>

    <comment> ========== Date B ============ </comment>
    <subject>
        <NAME>Name_A</NAME>
        <ORD_VALUE>KEEP_A</ORD_VALUE>
        <STUDY_ID>999</STUDY_ID>
        <redcapFormName>form_a</redcapFormName>
        <loinc_code>component_A</loinc_code>
        <DATE_TIME_STAMP>2013-13-07 09:00:00</DATE_TIME_STAMP>
    </subject>
    <subject>
        <NAME>Name_A</NAME>
        <ORD_VALUE>discard_3</ORD_VALUE>
        <STUDY_ID>999</STUDY_ID>
        <redcapFormName>form_a</redcapFormName>
        <loinc_code>component_A</loinc_code>
        <DATE_TIME_STAMP>2013-13-07 10:00:00</DATE_TIME_STAMP>
    </subject>
</study>
"""

    def test_compress(self):
        #parser = etree.XMLParser(remove_comments = True)
        #data = etree.parse('ha.xml', parser = parser)
        data = etree.ElementTree(etree.fromstring(self.xml))
        redi.compress_data_using_study_form_date(data)
        count = len(data.xpath('//subject'))

        #from redi import batch
        #batch.printxml(data)

        # verify that three components are left
        self.assertTrue(count == 2)


        # verify that we got the lab results with the earliest time
        keep_ele = data.xpath('//subject/ORD_VALUE')[0]
        self.assertEqual("KEEP_ME_PLEASE", keep_ele.text)

        keep_ele = data.xpath('//subject/ORD_VALUE')[1]
        self.assertEqual("KEEP_A", keep_ele.text)


if __name__ == "__main__":
    unittest.main()
