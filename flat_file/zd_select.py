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

def process_args():
    global argv

    if len(argv) != 2:
        print 'usage: python zd_select "condition"'
        return False
        
    return True

def process_file():
    global argv
    field_list = get_field_list()
    exec("include = lambda d: " + argv[1])

    for log_line in sys.stdin:
        log_line = log_line.rstrip()
        log_data = log_line.split('\t')
        line = list_to_dict(log_data, field_list)

        if include(line):
            print log_line
        


def list_to_dict(log_data, field_list):
    return_dict = dict()
    
    for i in range(0, len(field_list)):
        return_dict[field_list[i]] = log_data[i]

    return return_dict



def process_args1():
    global argv
    parser.add_option("-f", action="append", dest="fields")
    parser.add_option("-v", action="append", dest="values")

    (options, args) = parser.parse_args(argv)

    return options


def process_file1(options):
    field_list = get_field_list()
  
    values = parse_values(options)

    for log_line in sys.stdin:
        log_data = log_line.split('\t')

        if include(log_data, field_list, values):
            print_values(log_data, field_list, options)         

def print_values1(log_data, field_list, options):
    for field in options.fields:
        index = field_list.index(field)
        print log_data[index] + '\t',
    print ''

def include1(log_data, field_list, values):
    for val in values:
        index = field_list.index(val[0])

        if log_data[index] != val[1]:
           return False
           
    return True          

def parse_values1(options):
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
    first_line = sys.stdin.readline()
    first_line = first_line.rstrip('\n')

    field_list = first_line.split('\t')
    return strip_spaces(field_list)

def strip_spaces(list):
    for i in range(0, len(list)):
        list[i] = list[i].rstrip()
    return list


# Main
if process_args():
    process_file()

    
    
