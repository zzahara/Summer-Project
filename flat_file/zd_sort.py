# Contact Info:
# Zahara Docena
# zahara.docena@gmail.com

# usage: python zd_sort.py -f field [--file] [filename]
# usage: python zd_sort.py -f field1 -f field2 ... [-n] [field#] [--field] [filename]
# e.g. python zd_sort.py -f page -f loadtime -n 2 ... (will 1st sort by page, 2nd sort by loadtime numerically for same pages)

import os
import sys
from sys import argv
from optparse import OptionParser

argv
first_line = ''
sort_fields = []
parser = OptionParser()

def process_args():
    global argv, parser, file, filename, sort_fields
    parser.add_option("-f", action="append", dest="fields")
    parser.add_option("-n", action="store", dest="numeric", default=-2)
    
    (options, args) = parser.parse_args(argv)
    sort_fields = options.fields

    return options

def get_field_nums(options):
    global sort_fields, filename
    field_names = get_field_list()

    script_args = []
    script_args.append('')
    length = len(sort_fields)

    for i in range(0, length):
        index = field_names.index(sort_fields[i])
        #print sort_fields[i] + " = " + str(index)
        
        other_option = ''
        if int(options.numeric) == i+1:
            other_option = 'n'

        if length > 1 and i != length-1:
            script_args.append('-k')
            script_args.append(str(index+1) + ',' + str(index+1) + other_option)

        else:
            script_args.append('-k')
            script_args.append(str(index+1) + other_option)

    return script_args

def get_field_list():
    global first_line

    char = os.read(0,1)
    first_line = ''
    
    while char != '\n':
        first_line = first_line + char
        char = os.read(0,1)

    
    field_names = first_line.split('\t')

    return field_names

def sort(script_args):
    global first_line
    os.write(1,first_line + '\n')
    os.execv("sort-wrapper", script_args)


# Main
options = process_args()
script_args = get_field_nums(options)
sort(script_args)
