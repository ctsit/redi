#!/usr/bin/env python

from __future__ import print_function, unicode_literals
from io import open
import sys
reload(sys)
sys.setdefaultencoding('utf8')

# ==============================================================================
# Conversion from CSV to XML
# ==================
#
# Legal
# ------------------
#
# This software was written by Jerzy Jalocha N <jjalocha@gmail.com>. It is
# distributed "as is" without warranty of any kind. Use at you own risk!
# The author puts no restrictions on the user of this software, except
# attribution. You are free to share, remix, and re-license it, as long as
# the original author is credited.
#
#
# Synopsis
# ------------------
#
# csv2xml.py [options] ifile
#
#
# General Options
# ------------------
#
# ifile             Input CSV file path. Mandatory argument. If a hyphen '-' is
#                   given, the script reads from STDIN.
#
# ofile             Output XML file path. If the option os absent, the script
#                   writes to STDOUT.
#
# iencoding         Input file encoding. Defaults to UTF-8.
#
# oencoding         Output file encoding. Defaults to UTF-8.
#
#
# Input Options
# ------------------
#
# delimiter         The one-character string that is used to separate the
#                   fields. It defaults to a comma ','.
#                   eg: Specifying '\t', instructs the script to read tabulator-
#                       separated files:
#                         A1[TAB]B1[TAB]C1
#
# doublequote       Controls how instances of quotechar appearing inside a field
#                   should be themselves be quoted. When True, the character is
#                   doubled. When False, the escapechar is used as a prefix to
#                   the quotechar. It defaults to True.
#
# escapechar        The escapechar removes any special meaning from the
#                   following character. It defaults to None, which disables
#                   escaping.
#                   eg: Using '!' for escaping the delimiter character:
#                         A1,B!,2,C3
#
#(lineterminator)   The reader is hard-coded to recognise either '\r' or '\n' as
#                   end-of-line, and ignores lineterminator. This behavior may
#                   change in the future.
#
# quotechar         A one-character string used to quote fields containing
#                   special characters, such as the delimiter or quotechar, or
#                   which contain new-line characters. It defaults to '"'.
#                   eg: When set to a single-quote, you can easily use the
#                       delimiter inside fields:
#                         A1,"bee,2",C3
#
# quoting           Controls when quotes should be recognised by the reader. It
#                   can take on any of the QUOTE_* constants below:
#     QUOTE_MINIMAL Default. Instructs writer objects to only quote those fields
#                   which contain special characters such as delimiter,
#                   quotechar or any of the characters in lineterminator.
#         QUOTE_ALL Instructs writer objects to quote all fields.
#  QUOTE_NONNUMERIC Instructs the reader to convert all non-quoted fields to
#                   type float.
#        QUOTE_NONE Instructs reader to perform no special processing of quote
#                   characters.
#
# skipinitialspace  When True, whitespace immediately following the delimiter is
#                   ignored. The default is False.
#                   eg: When False, 'A, B, C' is read as
#                         <field>A</field> <field> B</field> <field> C</field>.
#                       When True, it is read as
#                         <field>A</field> <field>B</field> <field> C</field>.
#
# header            This option instructs the script to read read the field
#                   names from the first file line. It defaults to False.
#                   eg: When True, if reads the following CSV input:
#                         'colA,colB,colC
#                          A1,B1,C1'
#                       And uses the first line as field element names:
#                         <colA>A1</colA> <colB>B1</colB> <colC>C1</colC>
#
#
# Output Options
# ------------------
#
# xml-declaration   This option instructs the script to write an XML
#                   declaration. It defaults to False.
#                   eg: If this option is set, the first line in the output
#                       is <?xml version="1.0" encoding="UTF-8"?>.
#
# root_elem         These three options define the element names in the output
# record_elem       XML document. They default to <document>, <record>, and
# field_elem        <field>.
#                   eg: Specifying 'table', 'row', and 'cell', the output
#                       elements become <table>, <row>, and <cell>.
#
# newline_elem      Name for the newline element. It is disabled (None) by
#                   default.
#                   eg: Specifying 'br' will output a <br/> element for each
#                       newline in a field.
#
# flat_fields       This option disables the numbering of the field elements in
#                   the XML output. It is False by default.
#                   eg: When True, a field element is output as a <field>
#                       element, instead of <field0>, <field1>, etc.
#
# indent            XML file indentation. Defaults to four spaces '    '.
#                   eg: Specifying '\t' uses a tabulator, and using ''
#                       disables indentation alltogether.
#
# linebreak         This option defines what character is used at the end of
#                   each line in the XML file. It defaults to '\n', printing
#                   a new line after each element.
#                   eg: Specifying '' instructs the script to print the whole
#                       XML document as one single line.
#
# ==============================================================================

import csv
import sys
from optparse import OptionParser, OptionGroup

# Replace s by r in text.


def replace(text, s, r):
    return r.join(text.split(s))

# NOTE: If you modify this script, and the need arises to re-use sys.stdin
#       or sys.stdout, uncomment the following.
#
# Never close STDIN and STDOUT.
# def do_not_close(exc_type, exc_value, traceback):
#    pass
#sys.stdin.__exit__ = do_not_close
#sys.stdout.__exit__ = do_not_close

# Open a file or standard input/output from a unified interface.


def openio(filename, mode, encoding, newline=None):
    if filename == '-':       # Hyphen is commonly used to designate stdin/out.
        filename = None       # Use filename = None for stdin/out.
    if filename:
        return open(filename, mode=mode, encoding=encoding, newline=newline)
    elif mode == 'r':
        return sys.stdin
    elif mode == 'w':
        return sys.stdout
    else:
        raise ValueError("mode not recognized")

# Sometimes we need to print linebreak elements to the output document, in place
# of the real linebreaks in the input document. Sometimes we just keep print
# out the unmodified field content.


def field_subst_factory(newline):
    newline_tag = '<{0}/>'.format(newline)

    def text_replace(field):
        return replace(field, '\n', newline_tag)

    def text_keep(field):
        return field
    if newline:
        return text_replace
    else:
        return text_keep

# This class handles all the creating of the XML file.


class Writer:

    def __init__(self, ofile, args):
        self.file = ofile
        self.args = args
        self.newline_subst = field_subst_factory(args.newline_elem)
        if args.header:
            self.fieldname = self.__fieldname_header
        elif args.flat_fields:
            self.fieldname = self.__fieldname_flat
        else:
            self.fieldname = self.__fieldname_indexed

    def write_file(self, data):
        if self.args.declaration:
            declaration = ('<?xml version="1.0" encoding="{0}"?>'.
                           format(self.args.oencoding))
            self.write(declaration)
        self.write("<{0}>".format(self.args.root_elem))
        for record in data:
            self.write_record(record)
        self.write("</{0}>".format(self.args.root_elem))

    def write_record(self, record):
        self.write("{0}<{1}>".
                   format(self.args.indent, self.args.record_elem))
        for index, field in enumerate(record):
            self.write_field(field, index)
        self.write("{0}</{1}>".
                   format(self.args.indent, self.args.record_elem))

    def write_field(self, field, index):
        self.write("{0}{0}<{1}>{2}</{1}>".
                   format(self.args.indent, self.fieldname(index),
                          self.newline_subst(field)))

    def write(self, text):
        print(text, file=self.file, end=self.args.linebreak)

    def __fieldname_header(self, index):
        return self.args.header[index]

    def __fieldname_flat(self, index):
        return self.args.field_elem

    def __fieldname_indexed(self, index):
        return self.args.field_elem + str(index)

# Custom callback function for the command-line parser.
# Store tabs and newlines as "real" tabs and newlines.


def cleanup_callback(option, opt, value, parser):
    result = replace(value, '\\n', '\n')
    result = replace(result, '\\t', '\t')
    setattr(parser.values, option.dest, result)

# Parse the huge amount of command-line options.


def parse_cmdline():
    usage = "usage: %prog [options] IFILE"
    parser = OptionParser(usage)
    parser.set_defaults(iencoding='UTF-8',
                        oencoding='UTF-8',
                        delimiter=b',',
                        doublequote=True,
                        quotechar=b'"',
                        quoting=csv.QUOTE_MINIMAL,
                        skipinitialspace=False,
                        header=False,
                        declaration=False,
                        root_elem='root',
                        record_elem='record',
                        field_elem='field',
                        flat_fields=False,
                        indent='    ',
                        linebreak='\n')
    parser.add_option('-o', '--output-file', dest='ofile',
                      help="save to file OFILE")
    parser.add_option('-c', '--input-encoding', dest='iencoding',
                      help="input file encoding")
    parser.add_option('-C', '--output-encoding', dest='oencoding',
                      help="output file encoding")

    igroup = OptionGroup(parser, "CSV Dialect Options")
    igroup.add_option('-d', '--delimiter', dest='delimiter', type='str',
                      action='callback', callback=cleanup_callback,
                      help="a one-character string used to separate fields")
    igroup.add_option('-b', '--no-doublequote', action='store_false',
                      dest='doublequote',
                      help="controls how instances of quotechar appearing "
                      "inside a field should be themselves be quoted")
    igroup.add_option('-e', '--escapechar',
                      help="the escapechar removes any special meaning from "
                      "the following character")
    igroup.add_option('-q', '--quotechar',
                      help="A one-character string used to quote fields "
                      "containing special characters")
    igroup.add_option('--quote-all', dest='quoting',
                      action='store_const', const=csv.QUOTE_ALL,
                      help="quote all field (READER?)")
    igroup.add_option('--quote-minimal', dest='quoting',
                      action='store_const', const=csv.QUOTE_MINIMAL,
                      help="quote only special characters (WRITER?)")
    igroup.add_option('--quote-nonnumeric', dest='quoting',
                      action='store_const', const=csv.QUOTE_NONNUMERIC,
                      help="convert all non-quoted fields to type float")
    igroup.add_option('--quote-none', dest='quoting',
                      action='store_const', const=csv.QUOTE_NONE,
                      help="perform no special processing of quote characters")
    igroup.add_option('-s', '--skipinitialspace', action='store_true',
                      help="if whitespace immediately following the delimiter "
                      "should be ignored")
    igroup.add_option('-a', '--header', action='store_true',
                      help="read field names from file")

    ogroup = OptionGroup(parser, "XML Dialect Options")
    ogroup.add_option('-x', '--xml-declaration', dest='declaration',
                      action='store_true',
                      help="whether to output an XML declaration")
    ogroup.add_option('-t', '--root-element', dest='root_elem',
                      help="name of the root element")
    ogroup.add_option('-r', '--record-element', dest='record_elem',
                      help="name of the record-level element")
    ogroup.add_option('-f', '--field-element', dest='field_elem',
                      help="name of the field-level element")
    ogroup.add_option('-n', '--newline-element', dest='newline_elem',
                      help="name of the line break element")
    ogroup.add_option('-l', '--flat-fields', action='store_true',
                      help="disable field element numbering")
    ogroup.add_option('-i', '--indent', dest='indent', type='str',
                      action='callback', callback=cleanup_callback,
                      help="indentation")
    ogroup.add_option('-k', '--linebreak', dest='linebreak', type='str',
                      action='callback', callback=cleanup_callback,
                      help="line break character in output file")

    parser.add_option_group(igroup)
    parser.add_option_group(ogroup)
    options, args = parser.parse_args()
    if len(args) != 1:
        parser.error("incorrect number of arguments")
    options.ifile = args[0]
    return options

# The main processing code.
if __name__ == '__main__':
    args = parse_cmdline()
    csv.register_dialect('custom',
                         delimiter=args.delimiter,
                         doublequote=args.doublequote,
                         escapechar=args.escapechar,
                         quotechar=args.quotechar,
                         quoting=args.quoting,
                         skipinitialspace=args.skipinitialspace)
    with openio(args.ifile, mode='r', encoding=args.iencoding,
                newline='') as ifile:
        csvreader = csv.reader(ifile, dialect='custom')
        if args.header:
            args.header = next(csvreader)
        with openio(args.ofile, 'w', args.oencoding) as ofile:
            writer = Writer(ofile, args)
            writer.write_file(csvreader)
