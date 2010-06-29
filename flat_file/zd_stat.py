# Contact Info:
# Zahara Docena
# zahara.docena@gmail.com

# usage: zd_stat 
# http://www01.us.archive.org/~samuel/access-data.php?datecode=20100621

import re
import os
import sys
import math
from sys import argv
from optparse import OptionParser

argv
file
fileanme = ''
parser = OptionParser()


def process_args():

    # sort by page first

    global argv, parser, file
    parser.add_option("-f", "--file", action="store", dest="file", help="read from FILE") 
    parser.add_option("-c", action="store", dest="count", help="counts the size of each group", default="-")
    parser.add_option("-t", action="store", dest="tp99", help="calculates tp99", default="-")
    parser.add_option("-a", action="store", dest="ave_load", help="calculates average load time", default="-")
    parser.add_option("-b", action="store", dest="bounce_rate", help="calculates bounce rate", default="-")
    parser.add_option("-s", action="store", dest="standard_dev", help="calculates standard deviation", default="-")
    parser.add_option("-g", action="append", dest="grouping", help="calculates the statistics on the given grouping")
    parser.add_option("-d", action="store", dest="data", help="calculates the statistics of these values", default="loadtime")
 
    (options, args) = parser.parse_args(argv)
    parserOptions = options

    if options.file != None:
        filename = options.file
        file = open(options.file, "r")

    else:
        filename = sys.stdin
        file = sys.stdin

    return options


def process_file(options):
    global file
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

    for log_line in file:
        log_data = log_line.split('\t')

        # first group
        if len(current) == 0:
            current = get_current(log_data, grouped_by)

        if (in_group(log_data, grouped_by, current)):
            data.append(log_data[data_field])
            saved_lines.append(log_line)   

        # end of group so calculate stats
        else:
            #print ' ',
            #print data
            stats = calculate_stats(options, data)
            print_lines(saved_lines, stats)

            # store new group's values
            current = get_current(log_data, grouped_by)
            data = []
            saved_lines = []

            data.append(log_data[data_field])
            saved_lines.append(log_line)  

    stats = calculate_stats(options, data)
    print_lines(saved_lines, stats)

    file.close()
    

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

def print_fields(options, fields):
    stats = []

    stats.append

def print_fields(fields):
    stats = []

    if options.tp99 != '-':
        stats.append(options.tp99)

    if options.ave_load != '-':
        stats.append(options.ave_load)
    
    if options.standard_dev != '-':
        stats.append(options.standard_dev)

    if options.count != '-':
        stats.append(options.count)

    for i in range(0, len(fields)-1):
        print fields[i],
        print '\t',

    for i in range(0, len(stats)):
        print stats[i],
        
        if i != len(stats)-1:
            print '\t',

    print ''


def print_lines(lines, stats):

    for log in lines:
        print log.rstrip(),

        #keys = stats
        for i in range(0, len(stats)):
            print stats[i],

            if i != len(stats)-1:
                print '\t',

        print ''

def print_lines1(lines, stats):

    for log in lines:
        print log.rstrip(),

        for i in range(0, len(stats)):
            print stats[i]

            if i != len(stats)-1:
                print '\t',
          
        print ''
 

def get_field_list():
    global file
    first_line = file.readline()
    field_names = first_line.split('\t')
    
    return field_names

# ------------------------------------------------------------
#                Calculating Statistics Functions
# ------------------------------------------------------------  

def calculate_stats(options, values):
    stats = []
    if options.tp99 != '-':
        tp99 = calc_tp99(values, 10)
        #print tp99
        stats.append(tp99)

    if options.ave_load != '-':
        ave_load = calc_ave(values)
        #print ave_load
        stats.append(ave_load)
    
    if options.standard_dev != '-':
        standard_dev = calc_standard_dev(values)
        #print standard_dev
        stats.append(standard_dev)

    if options.count != '-':
        stats.append(len(values))

    return stats

#def calc_tp99(values, field):

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
        

    #print group
    #print calc_ave(group)
    return calc_ave(group)
    
def calc_ave(values):
    sum = 0
    
    for x in values:
        val = float(x)
        sum = sum + val

    return sum/len(values)

def calc_standard_dev(values):
    average = calc_ave(values)
    sum = 0.0

    if len(values) <= 1:
        return 0

    else:
        for x in values:
            val = float(x)
            sum = sum + math.pow((val-average), 2)

        return math.sqrt(sum/(len(values)-1))


#def calc_bounce_rate():
    

# Main
options = process_args()
process_file(options)


#values = [2, 35, 543, 21, 1, 8, 42, 45, 16, 3, 79, 679]
#calc_tp99(values, 90)

