#!/usr/bin/env python
# Written by Zahara Docena

import re
import os
import sys
import errno
import math
from sys import argv
from optparse import OptionParser


argv

def process_args():
    global argv

    if len(argv) != 2:
        print 'usage: ./zd_select "condition"'
        return False
        
    return True

def process_file():
    global argv
    field_list = get_field_list()
    exec("include = lambda d: " + argv[1])

    for log_line in sys.stdin:
        try:
            log_line = log_line.rstrip()
            log_data = log_line.split('\t')
            line = list_to_dict(log_data, field_list)
        
            if include(line):
                print log_line

        except IOError, e:
            if e.errno == errno.EPIPE:
                exit(0)       


def list_to_dict(log_data, field_list):
    return_dict = dict()

    #print log_data
    for i in range(0, len(field_list)):
        return_dict[field_list[i]] = log_data[i]

    return return_dict

def get_field_list():
    first_line = sys.stdin.readline()
    first_line = first_line.rstrip('\n')
    print first_line
    
    field_list = first_line.split('\t')
    return strip_spaces(field_list)

def strip_spaces(list):
    for i in range(0, len(list)):
        list[i] = list[i].rstrip()
    return list


# Main
if process_args():
    process_file()

    
    
