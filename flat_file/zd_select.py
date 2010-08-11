#!/usr/bin/env python

# Copyright 2010 Internet Archive
# Written by Zahara Docena
# This program is distributed under the terms of the GNU General Public License v3
# see: http://www.gnu.org/licenses/gpl.txt 

# Input: flat file (must include the selected fields in the condition)
# Output: flat file (with lines that satisfy the given condition)

# Example: ./zd_select.py "d['loadtime'] > 100"

# Input:
# ip                         page               loadtime
# 0.29.113.149          www.yoursite.com         6789
# 0.29.113.149          www.yoursite.com         56
# ...

# Output:
# ip                         page               loadtime
# 0.29.113.149          www.yoursite.com         6789

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

    print '\t'.join(field_list)
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

    for i in range(0, len(field_list)):
        return_dict[field_list[i]] = log_data[i]

    return return_dict

def get_field_list():
    first_line = sys.stdin.readline()
    first_line = first_line.rstrip('\n')
    
    field_list = first_line.split('\t')
    return field_list

def strip_spaces(list):
    for i in range(0, len(list)):
        list[i] = list[i].rstrip()
    return list


# Main
if process_args():
    process_file()

    
    
