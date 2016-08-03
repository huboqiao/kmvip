#coding:utf8
'''
Created on 2014年10月30日

@author: ivan

'''
from __future__ import division
import os
import sys
import ast
import time
import pickle
import struct
from socket import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *

class VerCheck( QThread ):
    '''检查版本'''
    def __init__(self,ini,act,ver,parent=None):
        super(VerCheck,self).__init__()
        
        self.host = ini.get('ver','ip')
        self.port = int(ini.get('ver','port'))
        self.sock = socket(AF_INET,SOCK_STREAM,0)
        
        self.act = act
        self.ver = ver
        try:
            self.sock.connect((self.host,self.port))
        except:
            print 'socket error'
        
    
    def run(self):
        data = {'act':self.act,'ver':self.ver}
        data = pickle.dumps(data)
        self.sock.send(data)#发送文件基本信息数据  
        
        serverdata = self.sock.recv(1024)
        result = pickle.loads(serverdata)
        self.emit(SIGNAL("checkver"),result)
        self.sock.close()



class Download( QThread ):
    def __init__(self,ini,act,parent=None):
        super(Download,self).__init__()
        self.host = ini.get('ver','ip')
        self.port = int(ini.get('ver','port'))
        self.sock = socket(AF_INET,SOCK_STREAM,0)
        self.act = act
        try:
            self.sock.connect((self.host,self.port))
            self.mutex = QMutex()
            data = {'act':self.act}
            data = pickle.dumps(data)
            self.sock.send(data)#发送文件基本信息数据          
            FILEINFO_SIZE=struct.calcsize('128s32sI8s')
            fhead = self.sock.recv(FILEINFO_SIZE)
            filename,temp1,filesize,temp2=struct.unpack('128s32sI8s',fhead)
            #result = pickle.loads(serverdata)
    
            self.filename = os.getcwd()+'/VIPcore.dll'
            self.fp = open(self.filename,'wb')
            self.restsize = filesize
            self.lens = filesize
        except Exception as e:
            print e
        self.stoped = False       
        
        
    #下载数据
    def run(self):
        while True:
            if self.stoped:
                return
            if self.restsize <= 0:
                self.fp.close()
                self.sock.close()
                break
            filedata = self.sock.recv(1024)
            self.fp.write(filedata)
            self.restsize = int(self.restsize) - int(len(filedata))
            #计算完成百分比
            load = float('%.3f'%( 1 - (int(self.restsize) / int(self.lens)))) * 100
            loaddata = {'load':load}
            self.emit(SIGNAL("download"),loaddata)
            time.sleep(0.001)
        
