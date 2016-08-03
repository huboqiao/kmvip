#coding:utf8
'''
Created on 2015年3月9日

@author: LiuXinwu

'''

from application.lib.commodel import Socket_model,Connection_Stock
import json
class SearchStockModel(Socket_model):
    def __init__(self):
        Socket_model.__init__(self)
        self.conn = Connection_Stock().getConnection()
        
    def queryCustomer(self,data):
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'queryCustomer','data':data}),0) )
        r = self.conn.recv(self.recvBuff)
        r = self.resolveRecvdata(r)
        return json.loads(r)
        
    def queryStockById(self,data):
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'queryStockById','data':data}),0) )
        r = self.conn.recv(self.recvBuff)
        r = self.resolveRecvdata(r)
        return json.loads(r)