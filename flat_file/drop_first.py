#!/usr/bin/env python
import sys

# read first line from stdin and discard it
first_line = sys.stdin.readline()

# print all other lines
for line in sys.stdin:
    print line,
