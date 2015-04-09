#!/usr/bin/env python

# Contributors:
# Christopher P. Barnes <senrabc@gmail.com>
# Andrei Sura: github.com/indera
# Mohan Das Katragadda <mohan.das142@gmail.com>
# Philip Chase <philipbchase@gmail.com>
# Ruchi Vivek Desai <ruchivdesai@gmail.com>
# Taeber Rapczak <taeber@ufl.edu>
# Nicholas Rejack <nrejack@ufl.edu>
# Josh Hanna <josh@hanna.io>
# Copyright (c) 2014-2015, University of Florida
# All rights reserved.
#
# Distributed under the BSD 3-Clause License
# For full text of the BSD 3-Clause License see http://opensource.org/licenses/BSD-3-Clause

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