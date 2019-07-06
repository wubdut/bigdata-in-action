#!/usr/bin/env python
import sys

for line in sys.stdin:
    key = line.strip()
    print('%s\t%s' % (key, 1))
