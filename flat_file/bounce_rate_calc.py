#!/usr/bin/env python
# Written by Zahara Docena

import sys
from sys import argv

file1 = open(argv[1])
file2 = open(argv[2])

total = float(file1.readline())
bounces = 0

for line in file2:
    line = line.strip()
    
    if line.startswith('1'):
        bounces = bounces + 1
    else:
        break
        
#print total
#print bounces  

bounce_rate = (bounces/total)*100
print "bounce rate = " + str(bounce_rate) + '%'
