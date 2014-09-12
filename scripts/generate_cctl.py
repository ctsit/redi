#!/usr/bin/env python
""" Generates a clinical-component-to-loinc.xml from CSV """
import argparse
import csv
import StringIO
import sys


def main():
    """ Main entry point """
    parser = argparse.ArgumentParser(
        description='Generates a clinical-component-to-loinc.xml from a CSV',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="The expected format is 4-columns without headers. \n"
               "The column order is: \n"
               "\tdescription, local-code, units, loinc-code\n"
               "\n"
               "Since the third column 'units' is not used, however, a \n"
               "3-column format is also acceptable: \n"
               "\tdescription, local-code, loinc-code",
        usage='%(prog)s < mapping.csv > clinical-component-to-loinc.xml')
    parser.parse_args()

    print '<?xml version="1.0" encoding="UTF-8"?>'
    print """
    <clinical_datum>
        <version>1.0</version>
        <Description>A mapping of local clinical component identifiers to their corresponding LOINC codes</Description>
        <components>"""

    stdin_as_file = StringIO.StringIO(sys.stdin.read())
    reader = csv.reader(stdin_as_file)
    for line in reader:
        length = len(line)
        if 4 == length:
            (description, code, unit, loinc) = line[0:4]
        elif 3 == length:
            (description, code, loinc) = line[0:3]
        else:
            raise Exception('Unexpected CSV format: ' + str(line))

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
            </component>""".format(description=description,
                                   code=code,
                                   loinc=loinc.rstrip())

    print "</components>"
    print "</clinical_datum>"


if __name__ == '__main__':
    main()
