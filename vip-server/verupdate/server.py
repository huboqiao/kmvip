# -*- coding: utf-8 -*-
'''
Created on 2014/10/30


@author: huboqiao
'''
import os
import sys
from time import *
import pickle
import struct
import SocketServer
from SocketServer import StreamRequestHandler as SRH  
import json

reload(sys)
sys.setdefaultencoding('utf8')
BUFSIZE = 2048
FILEINFO_SIZE = struct.calcsize('128sI')
dpath = os.getcwd()
addr = ('124.172.220.230', 5050)

class MyServer(SRH):
    
    def handle(self):
        mip, mport = self.client_address
        v = json.load(open('config.json', 'r')).get('version') 
        VERSION = v['version']
        while True:
            data = self.request.recv(1024)
            data = pickle.loads(data)
            if data['act'] == 'checkver':
                # 鍒ゆ柇鐗堟湰鏄惁涓�鏍�
                if VERSION == data['ver']:
                    senddata = {'flag':True, 'version':VERSION}
                    fthead = pickle.dumps(senddata)
                    self.request.send(fthead)
                else:
                    senddata = {'flag':False, 'version':VERSION}
                    fthead = pickle.dumps(senddata)
                    self.request.send(fthead)
                break
            if data['act'] == 'download':
                dll = 'VIPcore.dll'
                paths = dpath + '/up/' + dll
                fhead = struct.pack('128s11I', paths, 0, 0, 0, 0, 0, 0, 0, 0, os.stat(paths).st_size, 0, 0)
                self.request.send(fhead)
                fp = open(paths, 'rb')
                while True:   
                    data = fp.read(1024)   
                    if not data:   
                        break  
                    while len(data) > 0:   
                        intSent = self.request.send(data)   
                        data = data[intSent:]   
                fp.close()
                break

class TimeLog():
    def __init__(self):
        pass
    def showlog(self, data):
        times = str(time.strftime('%Y-%m-%d %H:%M:%S'))

            
if __name__ == '__main__':
    info = '''
                        
                        version:%s    
                        server-time:%s
           '''
    times = str(strftime('%Y-%m-%d %H:%M:%S %a'))
    server = SocketServer.ThreadingTCPServer(addr, MyServer)  
    server.serve_forever() 
            
