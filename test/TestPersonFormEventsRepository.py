import unittest
import tempfile

from lxml import etree

from redi.redi import PersonFormEventsRepository


class TestPersonFormEventsRepository(unittest.TestCase):

    def test_delete(self):
        with tempfile.NamedTemporaryFile(delete=False) as temp:
            service = PersonFormEventsRepository(temp.name)
            service.delete()

    def test_fetch(self):
        with tempfile.NamedTemporaryFile() as temp:
            temp.write('<test>42</test>')
            temp.seek(0)

            service = PersonFormEventsRepository(temp.name)
            xml = service.fetch()
            self.assertEquals(42, int(xml.xpath('//test')[0].text))

    def test_store(self):
        class MockLogger(object):
            @staticmethod
            def debug(*args):
                MockLogger.message = repr(args)

        with tempfile.NamedTemporaryFile() as temp:
            xml = etree.fromstring('<test>42</test>').getroottree()
            service = PersonFormEventsRepository(temp.name, MockLogger())

            service.store(xml)

            self.assertTrue('<test>42</test>' in open(temp.name).read())
            self.assertIsNotNone(MockLogger.message)