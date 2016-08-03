# -*- coding: utf-8 -*-
'''
Created on 2015年3月2日
对用户操作的模型
@author: LiuXinwu
'''
from PyQt4.QtCore import QThread
from application.lib.commodel import Socket_model,Connection_Stock
import json
class UserlistModel(Socket_model):
    def __init__(self):
        Socket_model.__init__(self)
        self.conn = Connection_Stock().getConnection()

    def addUser(self,data):
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'addUser','data':data}),0))
        r = self.conn.recv(self.recvBuff)
        r = self.resolveRecvdata(r)
        return json.loads(r)
    
    def modifyUser(self,data,data_info):
        data={'data':data,'datainfo':data_info}
        try:
            self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'modifyUser','data':data}),0))
            r = self.conn.recv(self.recvBuff)
            r = self.resolveRecvdata(r)
            return json.loads(r)
        except Exception as e:
            pass
    
    def delUser(self,data):
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'delUser','data':data}),0))
        r = self.conn.recv(self.recvBuff)
        r = self.resolveRecvdata(r)
        return json.loads(r)
    
    def alterMyPassword(self, data):
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'alterMyPassword','data':data}),0))
        r = self.conn.recv(self.recvBuff)
        r = self.resolveRecvdata(r)
        return json.loads(r)
        
    
