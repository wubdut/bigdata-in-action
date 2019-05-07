#!/usr/bin/env python
"""mapper.py"""

import sys,datetime
for line in sys.stdin:
    line = line.strip()
    keys = line.split(',')
    try:
        today = datetime.datetime.strptime('20'+keys[2][:6],'%Y%m%d')
    except:
        pass
    if keys[1] == '0':
        print ('%s\t%s' % (keys[11]+','+keys[8]+','+keys[14]+','+keys[9]+','+today.strftime('%Y%m%d')+','+'t0', 1))
    elif keys[1] == '1':
        print ('%s\t%s' % (keys[11]+','+keys[8]+','+keys[14]+','+keys[9]+','+today.strftime('%Y%m%d')+','+'t1', 1))
        print ('%s\t%s' % (keys[11]+','+keys[8]+','+keys[14]+','+keys[9]+','+(today+datetime.timedelta(days=1)).strftime('%Y%m%d')+','+'p1', 1))
        print ('%s\t%s' % (keys[11]+','+keys[8]+','+keys[14]+','+keys[9]+','+(today+datetime.timedelta(days=1)).strftime('%Y%m%d')+','+'p7', 1))
        print ('%s\t%s' % (keys[11]+','+keys[8]+','+keys[14]+','+keys[9]+','+(today+datetime.timedelta(days=2)).strftime('%Y%m%d')+','+'p7', 1))
        print ('%s\t%s' % (keys[11]+','+keys[8]+','+keys[14]+','+keys[9]+','+(today+datetime.timedelta(days=3)).strftime('%Y%m%d')+','+'p7', 1))
        print ('%s\t%s' % (keys[11]+','+keys[8]+','+keys[14]+','+keys[9]+','+(today+datetime.timedelta(days=4)).strftime('%Y%m%d')+','+'p7', 1))
        print ('%s\t%s' % (keys[11]+','+keys[8]+','+keys[14]+','+keys[9]+','+(today+datetime.timedelta(days=5)).strftime('%Y%m%d')+','+'p7', 1))
        print ('%s\t%s' % (keys[11]+','+keys[8]+','+keys[14]+','+keys[9]+','+(today+datetime.timedelta(days=6)).strftime('%Y%m%d')+','+'p7', 1))
        print ('%s\t%s' % (keys[11]+','+keys[8]+','+keys[14]+','+keys[9]+','+(today+datetime.timedelta(days=7)).strftime('%Y%m%d')+','+'p7', 1))

