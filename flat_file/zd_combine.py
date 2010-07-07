# Contact Info:
# Zahara Docena
# zahara@archive.org
# zahara.docena@gmail.com

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

    print_field_line(options.name, options.fields)
    for log_line in sys.stdin:
        log_data = log_line.split('\t')

        print_combined(log_data, options.combine, field_list)
        print_other_fields(log_data, options.fields, field_list)

def print_other_fields(log_data, fields, field_list):
    for i in range(0, len(fields)):
        index = field_list.index(fields[i])
        print log_data[index],

        if i != len(fields)-1:
            print '\t',
    print ''

def print_combined(log_data, combine_fields, field_list):
    new_string = ''

    for field in combine_fields:
        index = field_list.index(field)
        new_string = new_string + log_data[index]

    print new_string + '\t',

def print_field_line(new_field, fields):

    print new_field,
    if len(fields) != 0:
        print '\t',
    
    for i in range(0, len(fields)):
        print fields[i],
       
        if i != len(fields)-1:
            print '\t',
    print ''

def get_field_list():
    first_line = sys.stdin.readline()
    first_line = first_line.rstrip('\n')
    return first_line.split('\t')


# Main
options = process_args()
process_file(options)


