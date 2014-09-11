#!/usr/bin/env python
""" Generates a clinical-component-to-loinc.xml from a 4-column CSV """
import argparse
import sys


def main():
    """ Main entry point """
    parser = argparse.ArgumentParser(
        description='Generates a clinical-component-to-loinc.xml from a '
                    '4-column CSV',
        epilog='Expected columns are: description, local-code, units, '
               'loinc-code',
        usage='%(prog)s < mapping.csv > clinical-component-to-loinc.xml')
    parser.parse_args()

    print '<?xml version="1.0" encoding="UTF-8"?>'
    print """
    <clinical_datum>
        <version>1.0</version>
        <Description>A mapping of local clinical component identifiers to their corresponding LOINC codes</Description>
        <components>"""

    for (description, code, unit, loinc) in map(lambda x: x.rstrip().split(','), sys.stdin.readlines()):
        print """
            <component>
              <description>{description}</description>
              <source>
                <name>COMPONENT_ID</name>
                <value>{code}</value>
              </source>
              <target>
                <name>loinc_code</name>
                <value>{loinc}</value>
              </target>
            </component>""".format(description=description, code=code, loinc=loinc)

    print "</components>"
    print "</clinical_datum>"


if __name__ == '__main__':
    main()
