#coding:utf8
'''
Created on 2015年4月10日

@author: huaan

'''

from application.lib.commodel import Socket_model,Connection_Stock
import json
class Payment(Socket_model):
    def __init__(self):
        Socket_model.__init__(self)
        self.conn = Connection_Stock().getConnection()
        
    def addPayType(self, data):
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'addPayType','data':data}),0) )
        r = self.conn.recv(self.recvBuff)
        r = self.resolveRecvdata(r)
        return json.loads(r)
    
    def alterPayType(self, data):
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'alterPayType','data':data}),0) )
        r = self.conn.recv(self.recvBuff)
        r = self.resolveRecvdata(r)
        return json.loads(r)
    
    def deletePayType(self, data):
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'deletePayType','data':data}),0) )
        r = self.conn.recv(self.recvBuff)
        r = self.resolveRecvdata(r)
        return json.loads(r)
    
    def addPayment(self, data):
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'addPayment','data':data}),0) )
        r = self.conn.recv(self.recvBuff)
        r = self.resolveRecvdata(r)
        return json.loads(r)