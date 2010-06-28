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
    parser.add_option("-t", action="store_true", dest="tp99", help="calculates tp99")
    parser.add_option("-a", action="store_true", dest="ave_load", help="calculates average load time")
    parser.add_option("-b", action="store_true", dest="bounce_rate", help="calculates bounce rate")
    parser.add_option("-s", action="store_true", dest="standard_dev", help="calculates standard deviation")
 
    (options, args) = parser.parse_args(argv)
    parserOptions = options

    if options.file != None:
        filename = options.file
        file = open(options.file, "r")

    else:
        filename = sys.stdin
        file = sys.stdin

    return options

def get_loadtimes():
    global file
    loadtimes = []
    field_list = get_field_list()

    index = field_list.index('loadtime')

    for log_line in file:
        fields = log_line.split('\t')
        loadtimes.append(int(fields[index]))

    print loadtimes
    return loadtimes


def process_file(options):
    global file
    field_list = get_field_list()
    print_fields(field_list)
    
    page = field_list.index('page')
    loadtime = field_list.index('loadtime')

    curr_page = ''
    loadtimes = []
    saved_lines = []


    for log_line in file:
        log_data = log_line.split('\t')

        if curr_page == '':
            curr_page = log_data[page]

        # same page
        if log_data[page] == curr_page:
            loadtimes.append(log_data[loadtime])
            saved_lines.append(log_line)

        # new page, so calculate stats for current page
        else:
            #print curr_page
            #print loadtimes
            
            stats = calculate_stats(options, loadtimes)
            print_lines(saved_lines, stats)

            # store new page's values
            curr_page = log_data[page]
            loadtimes = []
            saved_lines = []

            loadtimes.append(log_data[loadtime])
            saved_lines.append(log_line)

    stats = calculate_stats(options, loadtimes)
    print_lines(saved_lines, stats)

    file.close()

def print_fields(fields):
    stats = dict()

    if options.tp99:
        stats['tp99'] = 0

    if options.ave_load:
        stats['ave_load'] = 0
    
    if options.standard_dev:
        stats['standard_dev'] = 0

    for i in range(0, len(fields)-1):
        print fields[i],
        print '\t',

    keys = stats.keys()

    for i in range(0, len(keys)):
        print keys[i],

        if i != len(keys)-1:
            print '\t',

    print ' '
   

def calculate_stats(options, loadtimes):
    stats = dict()
    if options.tp99:
        tp99 = calc_tp99(loadtimes)
        #print tp99
        stats['tp99'] = tp99

    if options.ave_load:
        ave_load = calc_ave(loadtimes)
        #print ave_load
        stats['ave_load'] = ave_load
    
    if options.standard_dev:
        ave_load = calc_ave(loadtimes)
        standard_dev = calc_standard_dev(loadtimes, ave_load)
        #print standard_dev
        stats['standard_dev'] = standard_dev


    #print stats
    return stats

def print_lines(lines, stats):

    for log in lines:
        print log.rstrip(),

        keys = stats.keys()
        for i in range(0, len(keys)):
            print stats[keys[i]],

            if i != len(keys)-1:
                print '\t',
            
    
        #for key in stats.keys():
         #   print stats[key],
         #   print '\t',


        print ''
 

def get_field_list():
    global file
    first_line = file.readline()
    field_names = first_line.split('\t')
    
    return field_names

# ------------------------------------------------------------
#                     Calculating Functions
# ------------------------------------------------------------  


#def calc_tp99(values, field):

def calc_tp99(values, percentile):
    values.sort()
    group = []

    group_len = ((percentile/float(100)) * len(values))

    # round accordingly
    if group_len < 1:
        group_len = 1
    else:
        group_len = int(round(group_len))

    for i in range(0, group_len):
        group.append(values[i])

    print group
    print calc_ave(group)
    return calc_ave(group)
    
def calc_ave(values):
    sum = 0
    
    for x in values:
        val = float(x)
        sum = sum + val

    return sum/len(values)

def calc_standard_dev(values, average):
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
#options = process_args()
#process_file(options)


values = [2, 35, 543, 21, 1, 8, 42, 45, 16, 3, 79, 679]
calc_tp99(values, 90)



