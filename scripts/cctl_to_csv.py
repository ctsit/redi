#!/usr/bin/env python
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
