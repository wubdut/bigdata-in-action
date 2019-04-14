#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
hadooptool
'''
from abc import ABCMeta, abstractmethod
import multiprocessing
from time import time
from filetool import getFileByte, listAllFilesUnderDir, makeDir, delAllFilesUnderDir, readLines, readLinesOfFiles,\
    writeLines

TEMP_DIR = 'temp/'
    

class Shuffle(object):
    __metaclass__ = ABCMeta
    @abstractmethod
    def partition(self):
        pass
    @abstractmethod
    def sort(self):
        pass
    
    
class Mapper(object):
    __metaclass__ = ABCMeta
    @abstractmethod
    def do(self, lines):
        pass


class Reducer(object):
    __metaclass__ = ABCMeta
    @abstractmethod
    def do(self, lines):
        pass


class Task(multiprocessing.Process):
    def run(self):
        print('start ' + multiprocessing.current_process().name)
        start = time()
        self.tasker.do( self.lines)
        end = time()
        print('end %s: %.3f s' % (multiprocessing.current_process().name, end-start))
    def __init__(self, tasker, lines):
        multiprocessing.Process.__init__(self)
        self.tasker = tasker
        self.lines = lines


class Job(object):
                
    def __init__( self, mapper, reducer, mem_size_limit, input_dir, output_dir ):
        self.mapper = mapper
        self.reducer = reducer
        self.memSizeLimit = mem_size_limit
        self.inputDir = input_dir
        self.outputDir = output_dir
        
    def runMapper(self):
        # 创建目录 #
        makeDir(TEMP_DIR)
        # ---END--- #
        # 清空数据目录 #
        delAllFilesUnderDir(TEMP_DIR)
        # ----END---- #
        fileList = []
        fileTotalByte = 0
        taskList = []
        for file in listAllFilesUnderDir(self.inputDir):
            fileByte = getFileByte(self.inputDir+file)
            if fileTotalByte + fileByte > self.memSizeLimit:
                taskList.append( Task( self.mapper, readLinesOfFiles(fileList) ) )
                fileList = []
                fileTotalByte = 0
            fileList.append(self.inputDir+file)
            fileTotalByte = fileTotalByte + fileByte
        if len(fileList) > 0:
            taskList.append( Task( self.mapper, readLinesOfFiles(fileList) ) )
        for task in taskList:
            task.start()
            
    def runReducer(self):
        fileList = []
        fileTotalByte = 0
        taskList = []
        for file in listAllFilesUnderDir(TEMP_DIR):
            fileByte = getFileByte(TEMP_DIR+file)
            if fileTotalByte + fileByte > self.memSizeLimit:
                taskList.append( Task( self.reducer, readLinesOfFiles(fileList) ) )
                fileList = []
                fileTotalByte = 0
            fileList.append(TEMP_DIR+file)
            fileTotalByte = fileTotalByte + fileByte
        if len(fileList) > 0:
            taskList.append( Task( self.reducer, readLinesOfFiles(fileList) ) )
        for task in taskList:
            task.start()
            
    def filtOutput(self, top = 10, oper = lambda x : int(x.split('\t')[1][:-1]), rev = True):
        # 创建目录 #
        makeDir(self.outputDir)
        # ---END--- #
        # 清空数据目录 #
        delAllFilesUnderDir(self.outputDir)
        # ----END---- #
        lines = readLines(TEMP_DIR + 'data.out')
        lines.sort(key = oper, reverse = rev)
        
        writeLines(self.outputDir + 'data.out', lines)
        
        print("# \tkey\tvalue\n")
        for index in range(top):
            print(str(index+1) + ".\t" +lines[index].strip())
