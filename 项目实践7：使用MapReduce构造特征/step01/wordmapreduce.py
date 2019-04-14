#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
wordmapreduce.py
'''
import string
from filetool import writeOneLine, getWriteOneLineHandle
from hadooptool import Mapper, Reducer, Job, Shuffle, TEMP_DIR


class WordShuffle(Shuffle):
    def __init__(self):
        self.partitionPathHandlerDict = {}
        for ch in string.ascii_lowercase:
            self.partitionPathHandlerDict[ch] = getWriteOneLineHandle(TEMP_DIR + 'partition_' + ch)
            
    def partition(self, key, value):
        key2 = key.strip("[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）:：；;]+").lower()
        if (key2[:1] >= 'a' and key2[:1] <= 'z'):
            writeOneLine(self.partitionPathHandlerDict[key2[:1]], ('%s\t%s' % (key2, value)))
    
    def sort(self, lines):
        lines.sort(key=lambda x:x.split('\t')[0])
        
    def __del__(self):
        for key in self.partitionPathHandlerDict:
            self.partitionPathHandlerDict[key].close()

class WordMapper(Mapper):
    def do(self, lines):
        print('WordMapper')
        wordShuffle = WordShuffle()
        for line in lines:
            line = line.strip()
            words = line.split()
            for word in words:
                wordShuffle.partition(word, 1)
        
        
class WordReducer(Reducer):
    
    def do(self, lines):
        print('WordReducer')
        
        file_handler = getWriteOneLineHandle(TEMP_DIR + 'data.out')
        wordShuffle = WordShuffle()
        wordShuffle.sort(lines)
        
        current_word = None
        current_count = 0
        word = None
        
        for line in lines:
            line = line.strip()
            word, count = line.split('\t', 1)
            try:
                count = int(count)
            except ValueError:
                continue
            if current_word == word:
                current_count += count
            else:
                if current_word:
                    writeOneLine(file_handler, ('%s\t%s' % (current_word, current_count)))
                current_count = count
                current_word = word
        
        if current_word == word:
            writeOneLine(file_handler, ('%s\t%s' % (current_word, current_count)))
            
        file_handler.close()
            


