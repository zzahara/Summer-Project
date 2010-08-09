# Contact Info:
# Zahara Docena
# zahara.docena@gmail.com

import os
import sys
from sys import argv
from optparse import OptionParser

argv
file
fileanme = ''
parser = OptionParser()
fields = []

error_codes = ['404']

def process_args():
    global argv, parser, file, fields, filename
    parser.add_option("-f", "--file", action="store", dest="file", help="read from FILE") 
        
    (options, args) = parser.parse_args(argv)
    
    if options.file != None:
        filename = options.file
        file = open(options.file, "r")

    else:
        filename = 'sys.stdin'
        file = sys.stdin

    fields = get_field_list(file)

def most_popular_page():
    global file, fields
    max_count = 0
    popular_page = ''

    curr_page = ''
    curr_count = 0
    page = field_num('page')
    for log_line in file:
        log_data = log_line.split('\t')

        if curr_page == '':
            curr_page = log_data[page]

        # same page
        if log_data[page] == curr_page:
            curr_count = curr_count + 1

        # new page, stop count
        else:
            if curr_count > max_count:
                max_count = curr_count
                popular_page = curr_page
                
            curr_page = log_data[page]

    return popular_page
    
#def top_5_pages():
    



#def worst_5_pages():







def sort(script_args):
    os.execv("zd_sort.py", script_args)  


def status_codes():

    for log_line in file:
        log_data = log_line.split('\t')

        if 

def top_5_referrer():
    field_list = get_field_list()
    ref = field_list.index9'referrer')

    curr_ref = ''
    counts = dict()

    for log_line in file:
        log_data = log_line.split('\t')

        if (log_data[ref] == curr_ref):
            counts[curr_ref] = counts[curr_ref] + 1

        else:
            curr_ref = log_data[ref]
            counts[curr_ref] = 0

    items = counts.items()
    items.sort(sortfunc)
    items.reverse

    file.close()

    print 'Top 5 Referrers Pages:'
    for i in range(5):
        print items[i]

    

def top_5_error():

    # sort by 1) page 2) status code
    # perform count
    #print filename

    #sort_args = ['', '-f', 'page', '-f', 'status', '-n', '2', '--file', filename]
    #sort(sort_args)

    field_list = get_field_list()
    page = field_list.index('page')
    status = field_list.index('status')
    
    curr_page = ''
    counts = dict()
   
    for log_line in file:
        log_data = log_line.split('\t')

        if (log_data[page] == curr_page && is_error(log_data[status])):
            counts[curr_page] = counts[curr_page] + 1

        else:
            curr_page = log_data[page]
            counts[curr_page] = 0

    items = counts.items()
    items.sort(sortfunc)
    items.reverse

    file.close()

    print 'Top 5 Error Pages:'
    for i in range(5):
        print items[i]

    
def sortfunc(x,y):
    return cmp(x[1], y[1])
    
        
def is_error(status):
    global error_codes

    for x in error_codes:
        if status == x:
            return true

    return false
        
# verifies if a log line belongs in the current group
def in_group(log_data, grouped_by, current):
    i = 0
    for field_num in grouped_by:

        if log_data[field_num] != current[i]:
            return False
            
        i = i + 1

    return True

# gets the field values of the current group
def get_current(log_data, grouped_by):
    current = []

    for field_index in grouped_by:
        value = log_data[field_index]
        current.append(value)

    #print current
    return current       
    
def report():
    

    

def get_field_list(file):
    first_line = file.readline()
    first_line = first_line.rstrip('\n')
    field_names = first_line.split('\t')
    

    return field_names

def field_num(name):
    global fields
    print fields
    return fields.index(name)


process_args()
print most_popular_page()
top_5_error()


