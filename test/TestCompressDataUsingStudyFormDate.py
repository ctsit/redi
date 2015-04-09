import unittest
from lxml import etree
from redi import redi
import logging
from redi import batch

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
        <ORD_VALUE>CANCEleD</ORD_VALUE>
        <STUDY_ID>262</STUDY_ID>
        <redcapFormName>form_a</redcapFormName>
        <loinc_code>component_A</loinc_code>
        <DATE_TIME_STAMP>2013-12-07 00:00:08</DATE_TIME_STAMP>
    </subject>

    <subject>
        <ORD_VALUE>KEEP_ME_PLEASE</ORD_VALUE>
        <STUDY_ID>262</STUDY_ID>
        <redcapFormName>form_a</redcapFormName>
        <loinc_code>component_A</loinc_code>
        <DATE_TIME_STAMP>2013-12-07 00:00:09</DATE_TIME_STAMP>
    </subject>

    <subject>
        <ORD_VALUE>discard_1</ORD_VALUE>
        <STUDY_ID>262</STUDY_ID>
        <redcapFormName>form_a</redcapFormName>
        <loinc_code>component_A</loinc_code>
        <DATE_TIME_STAMP>2013-12-07 00:00:20</DATE_TIME_STAMP>
    </subject>

    <subject>
        <ORD_VALUE>discard_2</ORD_VALUE>
        <STUDY_ID>262</STUDY_ID>
        <redcapFormName>form_a</redcapFormName>
        <loinc_code>component_A</loinc_code>
        <DATE_TIME_STAMP>2013-12-07 00:00:30</DATE_TIME_STAMP>
    </subject>

    <comment> ========== Date B ============ </comment>
    <subject>
        <NAME>Name_A</NAME>
        <ORD_VALUE> canceled</ORD_VALUE>
        <STUDY_ID>999</STUDY_ID>
        <redcapFormName>form_a</redcapFormName>
        <loinc_code>component_b</loinc_code>
        <DATE_TIME_STAMP>2013-13-07 07:00:00</DATE_TIME_STAMP>
    </subject>
    <subject>
        <NAME>Name_A</NAME>
        <ORD_VALUE> CANCELLED     </ORD_VALUE>
        <STUDY_ID>999</STUDY_ID>
        <redcapFormName>form_a</redcapFormName>
        <loinc_code>component_b</loinc_code>
        <DATE_TIME_STAMP>2013-13-07 08:00:00</DATE_TIME_STAMP>
    </subject>

    <subject>
        <NAME>Name_A</NAME>
        <ORD_VALUE>KEEP_A</ORD_VALUE>
        <STUDY_ID>999</STUDY_ID>
        <redcapFormName>form_a</redcapFormName>
        <loinc_code>component_b</loinc_code>
        <DATE_TIME_STAMP>2013-13-07 09:00:00</DATE_TIME_STAMP>
    </subject>

    <subject>
        <NAME>Name_A</NAME>
        <ORD_VALUE>discard_3</ORD_VALUE>
        <STUDY_ID>999</STUDY_ID>
        <redcapFormName>form_a</redcapFormName>
        <loinc_code>component_b</loinc_code>
        <DATE_TIME_STAMP>2013-13-07 10:00:00</DATE_TIME_STAMP>
    </subject>

    <comment> ========== Date C ============ </comment>
    <subject>
        <ORD_VALUE>canceled</ORD_VALUE>
        <STUDY_ID>123</STUDY_ID>
        <redcapFormName>form_c</redcapFormName>
        <loinc_code>component_c</loinc_code>
        <DATE_TIME_STAMP>2013-01-01 07:00:00</DATE_TIME_STAMP>
    </subject>

    <subject>
        <ORD_VALUE>canceLLed_2</ORD_VALUE>
        <STUDY_ID>123</STUDY_ID>
        <redcapFormName>form_c</redcapFormName>
        <loinc_code>component_c</loinc_code>
        <DATE_TIME_STAMP>2013-01-01 08:00:00</DATE_TIME_STAMP>
    </subject>

    <comment> ========== Date D ============ </comment>
    <subject>
        <ORD_VALUE>canceled</ORD_VALUE>
        <STUDY_ID>123</STUDY_ID>
        <redcapFormName>form_d</redcapFormName>
        <loinc_code>component_d</loinc_code>
        <DATE_TIME_STAMP>2013-11-11 07:00:00</DATE_TIME_STAMP>
    </subject>

</study>
"""

    def test_compress(self):
        #parser = etree.XMLParser(remove_comments = True)
        #data = etree.parse('ha.xml', parser = parser)
        data = etree.ElementTree(etree.fromstring(self.xml))
        redi.compress_data_using_study_form_date(data)
        count = len(data.xpath('//subject'))

        #batch.printxml(data)

        # verify that four components are left
        self.assertTrue(count == 4)

        # verify that we got the lab results with the earliest time
        keep_ele = data.xpath('//subject/ORD_VALUE')[0]
        self.assertEqual("KEEP_ME_PLEASE", keep_ele.text)

        keep_ele = data.xpath('//subject/ORD_VALUE')[1]
        self.assertEqual("KEEP_A", keep_ele.text)

        # verify that when there are two results canceled we keep one
        keep_ele = data.xpath('//subject/ORD_VALUE')[2]
        self.assertEqual("canceled", keep_ele.text)

        # verify that when there are only one result canceled we keep one
        keep_ele = data.xpath('//subject/ORD_VALUE')[3]
        self.assertEqual("canceled", keep_ele.text)


if __name__ == "__main__":
    unittest.main()
