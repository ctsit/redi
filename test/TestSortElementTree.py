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
import os
import logging
from lxml import etree

from redi import redi

class TestSortElementTree(unittest.TestCase):

    def setUp(self):
        redi.configure_logging('.')
        #redi.logger.setLevel(logging.DEBUG)

        # un-sorted XML file
        self.unsorted = """<?xml version="1.0" encoding="UTF-8"?>
<study>
   <subject>
        <NAME>PLATELET COUNT</NAME>
        <ORD_VALUE>123</ORD_VALUE>
        <STUDY_ID>999-0262</STUDY_ID>
        <redcapFormName>cbc</redcapFormName>
        <loinc_code>component_A</loinc_code>
        <DATE_TIME_STAMP>2013-12-03 00:00:00</DATE_TIME_STAMP>
    </subject>
    <subject>
        <NAME>PLATELET COUNT</NAME>
        <ORD_VALUE>123</ORD_VALUE>
        <STUDY_ID>999-0262</STUDY_ID>
        <redcapFormName>cbc</redcapFormName>
        <loinc_code>component_A</loinc_code>
        <DATE_TIME_STAMP>2013-12-01 00:00:00</DATE_TIME_STAMP>
    </subject>
    <subject>
        <NAME>PLATELET COUNT</NAME>
        <ORD_VALUE>123</ORD_VALUE>
        <STUDY_ID>999-0262</STUDY_ID>
        <redcapFormName>cbc</redcapFormName>
        <loinc_code>component_A</loinc_code>
        <DATE_TIME_STAMP>2013-12-01 00:12:01</DATE_TIME_STAMP>
    </subject>
    <subject>
        <NAME>PLATELET COUNT</NAME>
        <ORD_VALUE>123</ORD_VALUE>
        <STUDY_ID>999-0262</STUDY_ID>
        <redcapFormName>cbc</redcapFormName>
        <loinc_code>component_A</loinc_code>
        <DATE_TIME_STAMP>2013-12-02 00:00:00</DATE_TIME_STAMP>
    </subject>
</study>
        """

        # we expect the following sorted tree
        self.sorted_tree_keep_all_false = """<?xml version="1.0" encoding="UTF-8"?>
<study>
    <subject>
        <NAME>PLATELET COUNT</NAME>
        <ORD_VALUE>123</ORD_VALUE>
        <STUDY_ID>999-0262</STUDY_ID>
        <redcapFormName>cbc</redcapFormName>
        <loinc_code>component_A</loinc_code>
        <DATE_TIME_STAMP>2013-12-01 00:00:00</DATE_TIME_STAMP>
    </subject>
    <subject>
        <NAME>PLATELET COUNT</NAME>
        <ORD_VALUE>123</ORD_VALUE>
        <STUDY_ID>999-0262</STUDY_ID>
        <redcapFormName>cbc</redcapFormName>
        <loinc_code>component_A</loinc_code>
        <DATE_TIME_STAMP>2013-12-02 00:00:00</DATE_TIME_STAMP>
    </subject>
    <subject>
        <NAME>PLATELET COUNT</NAME>
        <ORD_VALUE>123</ORD_VALUE>
        <STUDY_ID>999-0262</STUDY_ID>
        <redcapFormName>cbc</redcapFormName>
        <loinc_code>component_A</loinc_code>
        <DATE_TIME_STAMP>2013-12-03 00:00:00</DATE_TIME_STAMP>
    </subject>
</study>
        """
        self.sorted_tree_keep_all_true = """<?xml version="1.0" encoding="UTF-8"?>
<study>
    <subject>
        <NAME>PLATELET COUNT</NAME>
        <ORD_VALUE>123</ORD_VALUE>
        <STUDY_ID>999-0262</STUDY_ID>
        <redcapFormName>cbc</redcapFormName>
        <loinc_code>component_A</loinc_code>
        <DATE_TIME_STAMP>2013-12-01 00:00:00</DATE_TIME_STAMP>
    </subject>
    <subject>
        <NAME>PLATELET COUNT</NAME>
        <ORD_VALUE>123</ORD_VALUE>
        <STUDY_ID>999-0262</STUDY_ID>
        <redcapFormName>cbc</redcapFormName>
        <loinc_code>component_A</loinc_code>
        <DATE_TIME_STAMP>2013-12-01 00:12:01</DATE_TIME_STAMP>
    </subject>
    <subject>
        <NAME>PLATELET COUNT</NAME>
        <ORD_VALUE>123</ORD_VALUE>
        <STUDY_ID>999-0262</STUDY_ID>
        <redcapFormName>cbc</redcapFormName>
        <loinc_code>component_A</loinc_code>
        <DATE_TIME_STAMP>2013-12-02 00:00:00</DATE_TIME_STAMP>
    </subject>
    <subject>
        <NAME>PLATELET COUNT</NAME>
        <ORD_VALUE>123</ORD_VALUE>
        <STUDY_ID>999-0262</STUDY_ID>
        <redcapFormName>cbc</redcapFormName>
        <loinc_code>component_A</loinc_code>
        <DATE_TIME_STAMP>2013-12-03 00:00:00</DATE_TIME_STAMP>
    </subject>
</study>
        """
        self.dirpath = tempfile.mkdtemp()


    # def test_sort_elementtree(self):
    #     tree_to_sort = etree.ElementTree(etree.fromstring(self.unsorted))
    #     # make the original test work
    #     redi.sort_element_tree(tree_to_sort, self.dirpath)
    #
    #     # TODO: create a way to test if --keep-all is True
    #     # test the keep all results functionality
    #     # redi.sort_element_tree(tree_to_sort, self.dirpath, True)
    #
    #     par = etree.XMLParser(remove_blank_text = True)
    #     clean_expect = etree.XML(self.sorted_tree, parser=par)
    #     clean_result = etree.XML(etree.tostring(tree_to_sort), parser=par)
    #     self.assertEqual(etree.tostring(clean_expect), etree.tostring(clean_result))

    def test_sort_elementtree_keep_all_true(self):
        tree_to_sort = etree.ElementTree(etree.fromstring(self.unsorted))
        # make the original test work
        redi.sort_element_tree(tree_to_sort, self.dirpath, True)

        # TODO: create a way to test if --keep-all is True
        # test the keep all results functionality
        # redi.sort_element_tree(tree_to_sort, self.dirpath, True)
        # then the log should NOT!! have the line "Remove duplicate result using key:"

        par = etree.XMLParser(remove_blank_text = True)
        clean_expect = etree.XML(self.sorted_tree_keep_all_true, parser=par)
        clean_result = etree.XML(etree.tostring(tree_to_sort), parser=par)
        self.assertEqual(etree.tostring(clean_expect), etree.tostring(clean_result))




    def test_sort_elementtree_keep_all_false(self):
        tree_to_sort = etree.ElementTree(etree.fromstring(self.unsorted))
        # make the original test work
        redi.sort_element_tree(tree_to_sort, self.dirpath, False)

        # TODO: create a way to test if --keep-all is false
        # test the keep all results functionality
        # redi.sort_element_tree(tree_to_sort, self.dirpath, False)

        # then the log should have the line "Remove duplicate result using key:"

        par = etree.XMLParser(remove_blank_text = True)
        clean_expect = etree.XML(self.sorted_tree_keep_all_false, parser=par)
        clean_result = etree.XML(etree.tostring(tree_to_sort), parser=par)
        self.assertEqual(etree.tostring(clean_expect), etree.tostring(clean_result))

    def tearDown(self):
        try:
            os.unlink(os.path.join(self.dirpath,
                "rawDataSortedBeforeCompression.xml"))
        except:
            print("setUp failed to unlink "\
                "file \'rawDataSortedBeforeCompression\'.xml")
        try:
            os.rmdir(self.dirpath)
        except OSError:
            raise LogException("Folder \'{}\' is not empty, hence cannot "\
                "be deleted.".format(self.dirpath))

if __name__ == '__main__':
    unittest.main()
