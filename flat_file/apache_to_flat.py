#!/usr/bin/env python
# Written by Zahara Docena

import re
import sys
import cgi
import urlparse
import urllib
from sys import argv
from optparse import OptionParser

argv
parser = OptionParser()
# fields that will be in the flat file
#fields = ['ip', 'page', 'loadtime', 'locale', 'referrer', 'timestamp', 'status', 'useragent']

def process_args():
    global argv, parser
    parser.add_option("-f", action="append", dest="fields", help="the fields to add in the flat file")

    (options, args) = parser.parse_args(argv)
    parserOptions = options

    return options

# img_src = bug request made on analytics.js
def process_file(file, img_src, options):
    pattern = '(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) [^ ]+ [^ ]+ \[(?P<timestamp>../.../....:..:..:..) .....\] ' + '"GET (?P<bug>' + img_src + '\?[^ ]+)( HTTP/1\.\d)?" (?P<status>\d{3}) (?P<size>[^ ]+) "(?P<page>[^"]+)" "(?P<useragent>[^"]+)"'
    c = re.compile(pattern)

    total_lines = 0
    count_no_match = 0
    regex_no_match = 0
    
    print_fields(options.fields)
    for log_line in file:
        m = c.match(log_line)
        
        if m:
            page_data = m.groupdict()

            if page_data['page'] == '-':
                continue
            bug_values = get_bug_values(page_data['bug'], img_src)
            page_data.update(bug_values)

            if 'count' in bug_values and int(bug_values['count']) == len(bug_values):
                print_page_values(page_data, options.fields)
            else:
                #sys.stderr.write('COUNT DOES NOT MATCH: ' + log_line + '\n')
                count_no_match = count_no_match + 1
            
        else:
            #sys.stderr.write('REJECTING: ' + log_line + '\n')
            regex_no_match = regex_no_match + 1
            
        total_lines = total_lines + 1

    print "count didn't match: " + count_no_match
    print "regex didn't match: " + regex_no_match
    print "total lines = " + total_lines

def get_bug_values(bug, img_src):
    bug_values = cgi.parse_qs(urlparse.urlparse(bug)[4])

    for key in bug_values:
        bug_values[key] = bug_values[key][0]

    return bug_values

def get_bug_values1(bug, img_src):
    bug = bug.replace(img_src + '?', '')
    bug_values = dict(item.split("=") for item in bug.split("&"))

    return bug_values

def print_fields1(fields):
    for i in range(0, len(fields)):
        print fields[i] + '\t',
    print ''

def print_fields(fields):
    for i in range(0, len(fields)):
        if i != len(fields)-1:
            print fields[i] + '\t',
        else:
            print fields[i]
            
def print_page_values(page_data, fields):
    for i in range(0, len(fields)):
        field = fields[i]
        
        if field in page_data:
            page_data[field] = urllib.unquote(page_data[field])
            print page_data[field] + '\t',
        else:
            print '-' + '\t',
    print ''     


def print_page_values1(page_data):
    for i in range(0, len(fields)):
        field = fields[i]

        if field in page_data:
            #if field == 'referrer':
            page_data[field] = urllib.unquote(page_data[field])

            print page_data[field] + '\t',
        else:
            print '-' + '\t',
    print ''


options = process_args()
process_file(sys.stdin, '/0.gif', options)




