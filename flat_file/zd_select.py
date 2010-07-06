# Contact Info:
# Zahara Docena
# zahara.docena@gmail.com

import re
import os
import sys
import math
from sys import argv
from optparse import OptionParser


argv
parser = OptionParser()

def process_args():
    global argv, file
    parser.add_option("-f", action="append", dest="fields")
    parser.add_option("-v", action="append", dest="values")
    parser.add_option("--file", action="store", dest = "file")

    (options, args) = parser.parse_args(argv)

    if options.file != None:
        filename = options.file
        file = open(options.file, "r")

    else:
        filename = sys.stdin
        file = sys.stdin

    return options


def process_file(options):
    field_list = get_field_list()
  
    values = parse_values(options)

    for log_line in file:
        log_data = log_line.split('\t')

        if include(log_data, field_list, values):
            print_values(log_data, field_list, options)
            

def print_values(log_data, field_list, options):
    for field in options.fields:
        index = field_list.index(field)
        print log_data[index] + '\t',
    print ''

def include(log_data, field_list, values):
    for val in values:
        index = field_list.index(val[0])

        if log_data[index] != val[1]:
           return False
           
    return True          

def parse_values(options):
    values = []
    
    for x in options.values:
        print x
        split = x.split('=')
        values.append((split[0], split[1]))

    print values     
    return values

def is_num(string):
    float_pattern = "[0-9]+\.[0-9]+"
    int_pattern = "[0-9]+"
    
    c_float = re.compile(float_pattern)
    c_int = re.compile(int_pattern)
    
    if c_int.match(string) or c_float.match(string):
        return True
    return False

def get_field_list():
    global file
    first_line = file.readline()
    first_line = first_line.rstrip('\n')
    return first_line.split('\t')


options = process_args()
process_file(options)

    
    
