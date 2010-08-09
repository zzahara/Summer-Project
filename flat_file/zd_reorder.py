#!/usr/bin/env python
# Written by Zahara Docena

# Input: flat file
# Output: flat file (with the columns reordered)

# Example: ./zd_reorder.py -f count -f page

# Input:
# page          count     locale
# website.com   6791      en-us
# ...

# Output:
# count     page
# 6791      website.com
# ...

import os
import sys
import errno
from sys import argv
from optparse import OptionParser

argv
parser = OptionParser()

def process_args():
    global argv, parser
    parser.add_option("-f", action="append", dest="fields", help="new order of the field columns")

    (options, args) = parser.parse_args(argv)
    return options

def process_file(options):
    field_list = get_field_list()

    indexes = []
    for field in options.fields:
        indexes.append(field_list.index(field))

    print_field_line(options.fields)
    for log_line in sys.stdin:
        try:
            log_line = log_line.rstrip()
            log_data = log_line.split('\t') 
            print_line(log_data, indexes)
        except IOError, e:
            if e.errno == errno.EPIPE:
                exit(0)

def print_line(log_data, indexes):
    values = []
    for i in indexes:
        values.append(log_data[i])

    print '\t'.join(values)

def print_field_line(fields):
    print '\t'.join(fields)

def get_field_list():
    first_line = sys.stdin.readline()
    first_line = first_line.rstrip()

    field_list = first_line.split('\t')
    return field_list

# Main
options = process_args()
process_file(options)


