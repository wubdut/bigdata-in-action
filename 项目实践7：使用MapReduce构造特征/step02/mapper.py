#!/usr/bin/env python
"""
mapper.py
"""

import sys
line1 = sys.stdin.readline()
for line in sys.stdin:
    line = line.strip()
    keys = line.split(',')
    print '%s\t%s' % (keys[7], 1)
