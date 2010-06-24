# Contact Info:
# Zahara Docena
# zahara.docena@gmail.com

# usage: ./zd_cut.py -f field [--file] [filename]

import os
import sys
import optparse
from sys import argv
from optparse import OptionParser

argv
filename = ''
parser = OptionParser()
cut_fields_str = []

def process_args():
    global argv, cut_fields_str, filename
    parser.add_option("-f", action="append", dest="fields")
    parser.add_option("--file", action="store", dest = "file")

    (options, args) = parser.parse_args(argv)
    cut_fields_str = options.fields
    print cut_fields_str
    
    if options.file != None:
        filename = options.file
        return open(options.file, "r")

    else:
        filename = sys.stdin
        return sys.stdin

def get_field_nums(file):

    first_line = file.readline()
    field_names = first_line.split('\t')
    print field_names

    cut_fields_int = ''

    for i in range(0, len(cut_fields_str)):
        index = field_names.index(cut_fields_str[i])
        cut_fields_int = cut_fields_int + str(index+1)
        
        if i != len(cut_fields_str)-1:
            cut_fields_int = cut_fields_int + ','

    return cut_fields_int

def cut(field_nums):
    os.execl("cut", '', field_nums, filename)

# MAIN

file = process_args()
field_nums = get_field_nums(file)
cut(field_nums)




