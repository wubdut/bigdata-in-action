#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
filetool.python

Created on 2019年1月5日

@author: wubin
'''
import os
import linecache

def makeDir(dir_path):
    isExist = os.path.exists(dir_path)
    if not isExist:
        os.makedirs(dir_path)
        print(dir_path+' 创建成功')
        return True
    else:
        print(dir_path+' 目录已存在')
        return False
    
def listAllFilesUnderDir(dir_path):
    files= os.listdir(dir_path)
    s = []
    for file in files:
        s.append(file)
    return s
    
def delAllFilesUnderDir(dir_path):
    for file in listAllFilesUnderDir(dir_path):
        os.unlink(dir_path + file)
        
def getLineInFile(file_path, line_num):
    return linecache.getline(file_path, line_num)

def fileExist(file_path):
    return os.path.exists(file_path)

def getFileByte(file_path):
    fsize = os.path.getsize(file_path)
    return round(fsize,2)



def getWriteOneLineHandle(file_path):
    return open(file_path, 'a', encoding='utf-8')

    
def writeOneLine(file_handler, context):
    file_handler.write(context+'\n')
    
    
    
def readLines(file_path):
    f = open(file_path,"r", encoding='utf-8', errors = 'ignore')
    data = f.readlines()
    f.close()
    return data

def writeLines(file_path, lines):
    f = open(file_path, 'w', encoding='utf-8')
#     lines = [line+"\n" for line in lines]
    f.writelines(lines)
    f.close()

def readLinesOfFiles(file_list):
    lines = []
    for file_path in file_list:
        lines = lines + readLines(file_path)
    return lines


if __name__ == "__main__":
    pass
    