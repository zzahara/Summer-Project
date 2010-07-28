#!/usr/bin/env python
# Written by Zahara Docena

import sys
from sys import argv

total_file = open(argv[1])
flat_file = open(argv[2])

total = float(total_file.readline())
count = 0

for line in flat_file:
    array = line.split()
    count = int(array[0])
    percentage = (count/total) * 100

    print '  ' + "%6.3f%%" % (percentage) + '\t' + array[1]


