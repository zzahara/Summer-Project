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
    parser.add_option("-f", action="append", dest="fields", help="fields to be kept in the new flat file")
    
    (options, args) = parser.parse_args(argv)
    sort_fields = options.fields
    
    return options

def process_file(options):
    field_list = get_field_list()

    # store the indexes of combining fields
    indexes = []
    for field in options.add_fields:
        indexes.append(field_list.index(field))

    #print_field_line(options.name, options.add_fields, field_list)
    print options.name
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


def print_field_line(new_field, add_fields, field_list):

    if len(field_list) > len(add_fields):
        print new_field + '\t',
    else:
        print new_field

    for i in range(0, len(field_list)):
        if other_field(add_fields, i, field_list):
            if i != len(field_list)-1:
                print field_list[i] + '\t',
            else:
                print field_list[i]

        elif i == len(field_list)-1:
            print ''

def get_field_list():
    first_line = sys.stdin.readline()
    first_line = first_line.rstrip()
    print first_line + '\t',

    field_list = first_line.split('\t')
    return strip_spaces(field_list)

def strip_spaces(list):
    for i in range(0, len(list)):
        list[i] = list[i].rstrip()
    return list

# Main
options = process_args()
process_file(options)


