#!/usr/bin/env python
# Written by Zahara Docena

import sys
from sys import argv

total_file = open(argv[1])
flat_file = open(argv[2])

total = float(total_file.readline())
bounces = 0

for line in flat_file:
    line = line.strip()
    
    if line.startswith('1'):
        bounces = bounces + 1
    else:
        break
        
print total
print bounces  

bounce_rate = (bounces/total)*100
print "bounce rate = " + str(bounce_rate) + '%'
