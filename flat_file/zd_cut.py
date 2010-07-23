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
parser = OptionParser()
cut_fields_str = []

def process_args():
    global argv, cut_fields_str, filename
    parser.add_option("-f", action="append", dest="fields")

    (options, args) = parser.parse_args(argv)
    cut_fields_str = options.fields


def get_script_args():
    global first_line
    field_names = get_field_list()
    field_nums = ''

    script_args = ['']
    indexes = []

    for i in range(0, len(cut_fields_str)):
        index = field_names.index(cut_fields_str[i])
        indexes.append(index)
        field_nums = field_nums + str(index+1)
        
        if i != len(cut_fields_str)-1:
            field_nums = field_nums + ','

    write_first_line(indexes, field_names)
    
    script_args.append(field_nums)
    return script_args

def write_first_line(indexes, field_list):
    first_line = ''
    indexes.sort()
    for i in range(0, len(indexes)):
        x = indexes[i]
        os.write(1,field_list[x])

        if i != len(indexes)-1:
            os.write(1,'\t')   

    os.write(1,'\n')

def get_field_list():
    first_line = ''
    char = os.read(0,1)
    
    while char != '\n':
        first_line = first_line + char
        char = os.read(0,1)

    first_line = first_line.rstrip()
    field_names = first_line.split('\t')

    return field_names

def cut(script_args):
    os.execv("cut-wrapper", script_args)

# MAIN

process_args()
script_args = get_script_args()
cut(script_args)




