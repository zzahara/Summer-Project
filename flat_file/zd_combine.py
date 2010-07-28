#!/usr/bin/env python
# Written by Zahara Docena

# combines fields into a new field, useful for computing bounce rate

import os
import sys
from sys import argv
from optparse import OptionParser

argv
parser = OptionParser()

def process_args():
    global argv, parser
    parser.add_option("-n", action="store", dest="name", help="name of new field")
    parser.add_option("-c", action="append", dest="combine", help="fields to combine in the order entered")
    parser.add_option("-f", action="append", dest="fields", help="fields to be kept in the new flat file")
    
    (options, args) = parser.parse_args(argv)
    sort_fields = options.fields
    
    return options

def process_file(options):
    field_list = get_field_list()

    # store the indexes of combining fields
    indexes = []
    for field in options.combine:
        indexes.append(field_list.index(field))

    print_field_line(options.name, options.combine, field_list)
    for log_line in sys.stdin:
        log_line = log_line.rstrip('\n')
        log_data = log_line.split('\t')

        print_combined(log_data, options.combine, field_list)
        print_other_fields(log_data, options.combine, field_list)

def print_other_fields(log_data, combined, field_list):
    for i in range(0, len(field_list)):

        if other_field(combined, i, field_list):
            if i != len(field_list)-1:
                print log_data[i] + '\t',
            else:
                print log_data[i]

        elif i == len(field_list)-1:
            print ''

def other_field(combined, field, field_list):
    for x in combined:
        if field == field_list.index(x):
            return False

    return True
            
    
def print_combined(log_data, combine_fields, field_list):
    new_string = ''

    for field in combine_fields:
        print 'field: ' + field
        print field_list
        index = field_list.index(field)
        
        new_string = new_string + log_data[index]

    print new_string + '\t',

def print_field_line(new_field, combine, field_list):

    if len(field_list) > len(combine):
        print new_field + '\t',
    else:
        print new_field

    for i in range(0, len(field_list)):
        if other_field(combine, i, field_list):
            if i != len(field_list)-1:
                print field_list[i] + '\t',
            else:
                print field_list[i]

        elif i == len(field_list)-1:
            print ''

def get_field_list():
    first_line = sys.stdin.readline()
    first_line = first_line.rstrip('\n')

    field_list = first_line.split('\t')
    return strip_spaces(field_list)

def strip_spaces(list):
    for i in range(0, len(list)):
        list[i] = list[i].rstrip()
    return list

# Main
options = process_args()
process_file(options)


