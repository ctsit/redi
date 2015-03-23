#!/usr/bin/env python

# Contributors:
# Christopher P. Barnes <senrabc@gmail.com>
# Andrei Sura: github.com/indera
# Mohan Das Katragadda <mohan.das142@gmail.com>
# Philip Chase <philipbchase@gmail.com>
# Ruchi Vivek Desai <ruchivdesai@gmail.com>
# Taeber Rapczak <taeber@ufl.edu>
# Josh Hanna <josh@hanna.io>
# Copyright (c) 2015, University of Florida
# All rights reserved.
#
# Distributed under the BSD 3-Clause License
# For full text of the BSD 3-Clause License see http://opensource.org/licenses/BSD-3-Clause

""" Converts clinical-component-to-loinc.xml to CSV """

import argparse
import sys
from xml.etree import ElementTree


def main():
    """ Main entry point """
    parser = argparse.ArgumentParser(
        description='Converts clinical-component-to-loinc.xml to CSV',
        usage='%(prog)s < clinical-component-to-loinc.xml')
    parser.parse_args()

    clinical_datum = ElementTree.fromstring(sys.stdin.read())

    for component in clinical_datum.findall('.//component'):
        print "{description}, {code}, {loinc}".format(
            description=component.findtext('description'),
            code=component.findtext('source/value'),
            loinc=component.findtext('target/value'))


if __name__ == '__main__':
    main()
