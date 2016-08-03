# -*- coding: utf-8 -*-
'''
Created on 2014年9月25日
登录
@author: ivan
'''

import time,json
from PyQt4.QtCore import QThread
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from socket import AF_INET,SOCK_STREAM,socket
from thread import start_new
import struct,ConfigParser

class Socket_model:
    def __init__(self):
        self.recvBuff=2097152   #最大接收字节
        pass
              
    
    def sendData(self,sendstr,commandId):
        '''发送数据'''
        HEAD_0 = chr(0)
        HEAD_1 = chr(0)
        HEAD_2 = chr(0)
        HEAD_3 = chr(0)
        ProtoVersion = chr(0)
        ServerVersion = 0
        sendstr = sendstr
        data = struct.pack('!sssss3I',HEAD_0,HEAD_1,HEAD_2,\
                           HEAD_3,ProtoVersion,ServerVersion,\
                           len(sendstr)+4,commandId)
        senddata = data+sendstr
        return senddata
    
    def resolveRecvdata(self,data):
        '''解析数据'''
        head = struct.unpack('!sssss3I',data[:17])
        length = head[6]
        data = data[17:17+length]
        return data
    
    def receiveMessage(self,conn): 
        '''接收消息'''
        while 1:
            message = conn.recv(1024)
            message = self.resolveRecvdata(message)
            print message

class Connection_Stock( object ):
    '''单列socket连接'''
    instance = None
    def __init__(self):
        pass
            
    @staticmethod
    def getConnection():
        if (Connection_Stock.instance == None):
            cf = ConfigParser.ConfigParser()
            cf.read('config.ini')
            host = cf.get('server', 'ip')        
            port = int(cf.get('server', 'port'))  
            
            client = socket(AF_INET,SOCK_STREAM)
            client.connect((host,port))
            Connection_Stock.instance = client
        return Connection_Stock.instance        

class getDataThread(Socket_model,QThread):
    '''
        @data 发送数据 dict
        @pid  服务端PID
        @singal 信号
    '''
    def __init__(self,data,pid,singal):
        Socket_model.__init__(self)
        QThread.__init__(self)
        self.conn = Connection_Stock().getConnection()
        self.conn.sendall(self.sendData(json.dumps(data),pid))
        self.singal = singal
        self.data = ''
        
    def run(self):
        while True:
            message = self.conn.recv(1024)
            self.data += message
            if self.data.find('#end') != -1:
                mdata = self.data[17:]
                try:
                    data = json.loads(mdata.replace('null', '"null"'))
                except:
                    mdata = self.data
                    print mdata
                    #data = json.loads(mdata.replace('null', '"null"'))
                self.emit(SIGNAL(self.singal),(data[0]))
                break
        
    