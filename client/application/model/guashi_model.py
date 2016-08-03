# -*- coding: utf-8 -*-
'''
Created on 2015年3月3日
@author: LiuXinwu
'''
from PyQt4.QtCore import QThread
from application.lib.commodel import Socket_model,Connection_Stock
import json
class GuashiModel(Socket_model):
    def __init__(self):
        Socket_model.__init__(self)
        self.conn = Connection_Stock().getConnection()

    def checkMember(self,idcard):
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'getMemberinfo','data':idcard}),0))
        r = self.conn.recv(self.recvBuff)
        r = self.resolveRecvdata(r)
        return json.loads(r)
    
    def lossCard(self,data):
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'lossCard','data':data}),0))
        r = self.conn.recv(self.recvBuff)
        r = self.resolveRecvdata(r)
        return json.loads(r)
    
    def findAllFingerOneCard(self,data):
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'getMemberInfo1','data':data}),0))
        r = self.conn.recv(self.recvBuff)
        r = self.resolveRecvdata(r)
        return json.loads(r)
    
    def frozenCard(self, data):
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'frozenCard','data':data}),0) )
        r = self.conn.recv(self.recvBuff)
        r = self.resolveRecvdata(r)
        return json.loads(r)
    
    
    