#!/usr/bin/env python
# Written by Zahara Docena

# calculates the sum of the selected fields and creates a new field

import os
import sys
from sys import argv
from optparse import OptionParser

argv
parser = OptionParser()

def process_args():
    global argv, parser
    parser.add_option("-n", action="store", dest="name", help="name of new field")
    parser.add_option("-a", action="append", dest="add_fields", help="fields to add")
    
    (options, args) = parser.parse_args(argv)
    return options

def process_file(options):
    field_list = get_field_list()

    # store the indexes of the fields to add
    indexes = []
    for field in options.add_fields:
        indexes.append(field_list.index(field))

    print_field_line(options.name, field_list)
    for log_line in sys.stdin:
        log_line = log_line.rstrip()
        log_data = log_line.split('\t')

        print log_line + '\t',
        print_sum(log_data, options.add_fields, field_list)           
    
def print_sum(log_data, sum_fields, field_list):
    new_sum = 0

    for field in sum_fields:
        index = field_list.index(field)
        if log_data[index] != '-':
            new_sum = new_sum + int(log_data[index])

    print str(new_sum)

def print_field_line(new_field, field_list):
    field_list.append(new_field)
    print '\t'.join(field_list)

def print_field_line1(new_field, add_fields, field_list):

    fields = []
    fields.append(new_field)
    
    for i in range(0, len(field_list)):
        if other_field(add_fields, i, field_list):
            fields.append(field_list[i])

    print '\t'.join(fields)

def get_field_list():
    first_line = sys.stdin.readline()
    first_line = first_line.rstrip()

    field_list = first_line.split('\t')
    return strip_spaces(field_list)

def strip_spaces(list):
    for i in range(0, len(list)):
        list[i] = list[i].rstrip()
    return list

# Main
options = process_args()
process_file(options)


