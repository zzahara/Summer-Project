#!/usr/bin/env python
# Written by Zahara Docena
# usage: zd_stat 
# http://www01.us.archive.org/~samuel/access-data.php?datecode=20100621

import re
import os
import sys
import math
from sys import argv
from optparse import OptionParser

argv
parser = OptionParser()


def process_args():
    global argv, parser
    parser.add_option("-c", action="store", dest="count", help="counts the size of each group", default="-")
    parser.add_option("-t", action="store", dest="tp99", help="calculates tp99", default="-")
    parser.add_option("-a", action="store", dest="ave", help="calculates average load time", default="-")
    parser.add_option("-b", action="store", dest="bounce_rate", help="calculates bounce rate", default="-")
    parser.add_option("-s", action="store", dest="standard_dev", help="calculates standard deviation", default="-")
    parser.add_option("-g", action="append", dest="grouping", help="calculates the statistics on the given grouping")
    parser.add_option("-d", action="store", dest="data", help="calculates the statistics of these values", default="loadtime")
 
    (options, args) = parser.parse_args(argv)
    #parserOptions = options

    return options


def process_file(options):
    field_list = get_field_list()
    print_fields(field_list)

    # store the indexes of grouping fields
    grouped_by = []
    for field in options.grouping:
        grouped_by.append(field_list.index(field))
    
    data_field = field_list.index(options.data)

    current = [] # current field values of the current group
    data = [] # data the statistics will be computed over
    saved_lines = [] # log lines in the current group

    for log_line in sys.stdin:
        log_line = log_line.rstrip()
        log_data = log_line.split('\t')

        # first group
        if len(current) == 0:
            current = get_current(log_data, grouped_by)

        if in_group(log_data, grouped_by, current):
            data.append(log_data[data_field])
            saved_lines.append(log_line)           
        else:
            # end of group so calculate stats
            stats = calculate_stats(options, data)
            print_lines(saved_lines, stats)

            # store new group's values
            current = get_current(log_data, grouped_by)
            data = []
            saved_lines = []

            data.append(log_data[data_field])
            saved_lines.append(log_line)  

    # last group
    stats = calculate_stats(options, data)
    print_lines(saved_lines, stats)


# gets the field values of the current group
def get_current(log_data, grouped_by):
    current = []

    for field_index in grouped_by:
        value = log_data[field_index]
        current.append(value)

    #print current
    return current

# verifies if a log line belongs in the current group
def in_group(log_data, grouped_by, current):
    i = 0
    for field_num in grouped_by:

        if log_data[field_num] != current[i]:
            return False
            
        i = i + 1

    return True


# ------------------------------------------------------------
#                Printing Functions
# ------------------------------------------------------------  


def print_fields(fields):
    stats = []

    if options.tp99 != '-':
        stats.append(options.tp99)

    if options.ave != '-':
        stats.append(options.ave)
    
    if options.standard_dev != '-':
        stats.append(options.standard_dev)

    if options.count != '-':
        stats.append(options.count)

    print '\t'.join(fields) + '\t',
    print '\t'.join(stats)


def print_lines(lines, stats):

    for log in lines:
        print log.rstrip() + '\t',
        print '\t'.join(stats)

def get_field_list():
    first_line = sys.stdin.readline()
    first_line = first_line.rstrip()
    field_names = first_line.split('\t')
    
    return field_names

# ------------------------------------------------------------
#                Calculating Statistics Functions
# ------------------------------------------------------------  

def calculate_stats(options, values):
    stats = []
    if options.tp99 != '-':
        tp99 = calc_tp99(values, 10)
        stats.append(str(tp99))

    if options.ave != '-':
        ave = calc_ave(values)
        stats.append(str(ave))
    
    if options.standard_dev != '-':
        standard_dev = calc_standard_dev(values)
        stats.append(str(standard_dev))

    if options.count != '-':
        stats.append(str(len(values)))

    return stats

def calc_tp99(values, percentile):
    group = []

    group_len = ((percentile/float(100)) * len(values))

    # round accordingly
    if group_len < 1:
        group_len = 1
    else:
        group_len = int(round(group_len))

    for i in range(0, group_len):
        group.append(values[i])
        
    return calc_ave(group)
    
def calc_ave(values):
    sum = 0
    for x in values:
        if x != '-':
            val = float(x)
            sum = sum + val

    ret_val = sum/len(values)

    if ret_val == 0:
        return '-'
    return ret_val

def calc_standard_dev(values):
    average = calc_ave(values)
    sum = 0.0

    if len(values) <= 1:
        return 0

    else:
        for x in values:
            if x != '-':
                val = float(x)
                sum = sum + math.pow((val-average), 2)

        return math.sqrt(sum/(len(values)-1))

# Main
options = process_args()
process_file(options)


