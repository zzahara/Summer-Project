#!/usr/bin/env python
# Written by Zahara Docena

# usage: python zd_cut.py -f field [--file] [filename]

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
    parser.add_option("-f", action="append", dest="fields") # fields to cut

    (options, args) = parser.parse_args(argv)
    cut_fields_str = options.fields

def get_script_args():
    global first_line
    field_list = get_field_list()
    field_nums = ''

    script_args = ['']
    indexes = []
    field_nums = []
    
    for i in range(0, len(cut_fields_str)):
        try:
            index = field_list.index(cut_fields_str[i])
            indexes.append(index)
            field_nums.append(str(index+1))
        except IOError, e:
            if e.errno == errno.EPIPE:
                exit(0)
    try:
        write_first_line(indexes, field_list)
        script_args.append(','.join(field_nums))
    except IOError, e:
        if e.errno == errno.EPIPE:
            exit(0)      
    return script_args

def write_first_line(indexes, field_list):
    fields = []
    indexes.sort()

    for i in range(0, len(indexes)):
        x = indexes[i]
        fields.append(field_list[x])

    first_line = '\t'.join(fields)
    os.write(1, first_line)
    os.write(1,'\n')

def get_field_list():
    first_line = ''
    char = os.read(0,1)
    
    while char != '\n':
        first_line = first_line + char
        char = os.read(0,1)

    first_line = first_line.rstrip()
    field_list = first_line.split('\t')

    return field_list

def cut(script_args):
    os.execv("cut-wrapper", script_args)

# MAIN

process_args()
script_args = get_script_args()
cut(script_args)




