# Contact Info:
# Zahara Docena
# zahara.docena@gmail.com

# usage: sort -f field [--file] [filename]

import os
import sys
from sys import argv
from optparse import OptionParser

argv
field = ''  
fileanme = ''
parser = OptionParser()

def process_args():
    global argv, parser, field, filename
    parser.add_option("-f", action="store", dest="field")
    parser.add_option("--file", action="store", dest = "file")    
    
    (options, args) = parser.parse_args(argv)
    field = options.field
    filename = options.file

    if options.file != None:
        filename = options.file
        return open(options.file, "r")

    else:
        filename = sys.stdin
        return sys.stdin


def order_by_field345(file):
    field_list = get_field_list(file)
    field_num = field_list.index(str(field)) + 1
    
    # cut order field
    f = open('cut_one','w')
    f.close()

    # cut all except order field
    before = field_num - 1
    after = field_num + 1
    other_fields = ''
    
    if before > 0:
        other_fields = '-' + str(before)
    if after < len(field_list):
        if before > 0:
            other_fields = other_fields + ','
        other_fields = other_fields + str(after) + '-'
    

  
    args = ["cut", str(field_num), filename, "|", "cut", other_fields,]
    ret_code = subprocess.Popen(args, shell=True)
    print 'ret_code = ' + str(ret_code)
    #os.execl("cut", '', str(field_num), filename, '>', 'cut_one')

    

def order_by_field(file):
    field_list = get_field_list(file)
    field_num = field_list.index(str(field)) + 1
  
    # cut all except order field
    before = field_num - 1
    after = field_num + 1
    other_fields = ''
    
    if before > 0:
        other_fields = '-' + str(before) + ','
        
    if after < len(field_list):
        other_fields = other_fields + str(after) + '-'

    os.execl("sort", '', str(field_num), other_fields, filename)
    
def get_field_list(file):
    global field
    first_line = file.readline()
    field_names = first_line.split('\t')
    
    return field_names

# Main
file = process_args()
order_by_field(file)
sort()


