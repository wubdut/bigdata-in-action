#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
run_map.py
'''
from hadooptool import Job
from wordmapreduce import WordMapper, WordReducer          
if __name__ == "__main__":
    mapper = WordMapper()
    reducer = WordReducer()
     
    job = Job(mapper, reducer, 1000000, 'input/', 'output/')
     
    job.runMapper()
