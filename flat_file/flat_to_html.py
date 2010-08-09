#!/usr/bin/env python
# Written by Zahara Docena

# Input: flat file
# Output: html file

import os
import sys

def process_file():
    field_list = get_field_list()
    print_table_header(field_list)

    for log_line in sys.stdin:
        log_line = log_line.rstrip()
        log_data = log_line.split('\t')
        print_table_row(log_data)

    print '</table>'

def get_field_list():
    first_line = sys.stdin.readline()
    first_line = first_line.rstrip()

    field_list = first_line.split('\t')
    return field_list

def print_table_header(fields):
    print '<table border="1" cellpadding="5" cellspacing="5" width="100%">'
    print '<tr>'
    
    for x in fields:
        print '<th>' + str(x) + '</th>'

    print '</tr>'

def print_table_row(log_data):
    print '<tr>'

    for x in log_data:
        print '<td width="20%">' + str(x) + '</td>'

    print '</tr>'


# Main
process_file()




