#coding:utf8
'''
Created on 2014年9月28日

@author: huaan
设置利率
'''

from PyQt4.QtCore import QThread
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from application.lib.commodel import Socket_model,Connection_Stock
import json
class MemberQueryModel(Socket_model):
    def __init__(self):
        Socket_model.__init__(self)
        self.conn = Connection_Stock().getConnection()
        
    def queryMember(self, data):
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'queryMember','data':data}),0) )
        r = self.conn.recv(self.recvBuff)
        r = self.resolveRecvdata(r)
        return json.loads(r)
    
    def getMemberInfosss(self, data):
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'getMemberInfosss','data':data}),0) )
        r = self.conn.recv(self.recvBuff)
        r = self.resolveRecvdata(r)
        return json.loads(r)
    
    def queryUserCard(self, IDcard):
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'queryUserCard','data':IDcard}),0) )
        r = self.conn.recv(self.recvBuff)
        r = self.resolveRecvdata(r)
        return json.loads(r)