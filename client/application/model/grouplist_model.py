# -*- coding: utf-8 -*-
'''
Created on 2015年3月2日
绑卡
@author: LiuXinwu
'''
from application.lib.commodel import Socket_model,Connection_Stock
import json
class GroupListModel(Socket_model):
    def __init__(self):
        Socket_model.__init__(self)
        self.conn = Connection_Stock().getConnection()
        
        
    def getPower(self,data=''):
        
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'getPow2','data':data}),0) )
        r = self.conn.recv(self.recvBuff)
        r = self.resolveRecvdata(r)
        return json.loads(r)
    
    def deletePower(self,id): 
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'delGroup','data':id}),0))
        r = self.conn.recv(self.recvBuff)
        r = self.resolveRecvdata(r)
        return json.loads(r)
    
    def groupAdd(self,data): 
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'addGroup','data':data}),0))
        r = self.conn.recv(self.recvBuff)
        r = self.resolveRecvdata(r)
        return json.loads(r)
    
    
    def editPower(self,data): 
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'editGroup','data':data}),0))
        r = self.conn.recv(self.recvBuff)
        r = self.resolveRecvdata(r)
        return str(r)
    
    def getGroupInfo(self,groupid):
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'getGroupInfo','data':groupid}),0))
        r = self.conn.recv(self.recvBuff)
        r = self.resolveRecvdata(r)
        return str(r)
    
