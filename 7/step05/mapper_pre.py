#!/usr/bin/env python
"""mapper.py"""

import sys,datetime
for line in sys.stdin:
    line = line.strip()
    keys = line.split(',')
    print ('%s\t%s' % ('device_id:'+keys[11], 1))
    print ('%s\t%s' % ('app_id:'+keys[8], 1))
    print ('%s\t%s' % ('app_domain:'+keys[9], 1))
