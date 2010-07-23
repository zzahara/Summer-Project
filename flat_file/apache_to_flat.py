#!/usr/bin/env python
# Written by Zahara Docena


import re
import sys
from sys import argv

argv
# fields that will be in the flat file
fields = ['user', 'page', 'loadtime', 'locale', 'referrer', 'timestamp', 'status', 'useragent']

# img_src = bug request made on analytics.js
def process_file(file, img_src):
    pattern = '(?P<user>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) [^ ]+ [^ ]+ \[(?P<timestamp>../.../....:..:..:..) .....\] ' + '"GET (?P<bug>' + img_src + '\?[^ ]+)[^"]+" (?P<status>\d{3}) (?P<size>[^ ]+) "(?P<page>[^"]+)" "(?P<useragent>[^"]+)"'
    c = re.compile(pattern)

    print_fields()
    for log_line in file:
        m = c.match(log_line)
        
        if m:
            page_data = m.groupdict()

            if page_data['page'] == '-':
                continue
            bug_values = get_bug_values(page_data['bug'], img_src)
            page_data.update(bug_values)

            print_page_values(page_data)
                
        #else:
          #  sys.stderr.write('REJECTING: ' + log_line + '\n')

def get_bug_values(bug, img_src):
    end = bug.replace(img_src + '?', '')
    bug_values = dict(item.split("=") for item in end.split("&"))

    return bug_values

def print_fields():
    for i in range(0, len(fields)):
        print fields[i] + '\t',
    print ''

def print_page_values(page_data):
    for i in range(0, len(fields)):
        field = fields[i]
        print page_data[field] + '\t',
    print ''


process_file(sys.stdin, '/0.gif')




