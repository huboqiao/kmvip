#coding:utf8
'''
Created on 2014��9��27��

@author: huaan
��������
'''

from PyQt4.QtCore import QThread
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from application.lib.commodel import Socket_model,Connection_Stock
import json
class OrderAddModel(Socket_model):
    def __init__(self):
        Socket_model.__init__(self)
        self.conn = Connection_Stock().getConnection()
    
    def addOrder(self,data):
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'orderAdd','data':data}),0))
        r = self.conn.recv(self.recvBuff)
        r = self.resolveRecvdata(r)
        return json.loads(r)
    
    def queryPurchasers(self):
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'queryPurchasers','data':''}),0))
        r = self.conn.recv(self.recvBuff)
        r = self.resolveRecvdata(r)
        return json.loads(r)

    def querySuppliers(self):
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'querySupplier','data':''}),0))
        r = self.conn.recv(self.recvBuff)
        r = self.resolveRecvdata(r)
        return json.loads(r)  
    
        
    def getAllClass(self):
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'getAllClass','data':''}),0) )
        r = self.conn.recv(self.recvBuff)
        data = json.loads(r[17:])
        return data
    
    def queryClassGoods(self,data):
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'queryClassGoods','data':data}),0) )
        r = self.conn.recv(self.recvBuff)
        data = json.loads(r[17:])
        return data    
    
    def getGoodsSN(self,goodsID):
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'getGoodsSN','data':goodsID}),0) )
        r = self.conn.recv(self.recvBuff)
        data = json.loads(r[17:])
        
        return data
    
    def getOrderID(self, orderID):
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'getOrdersID','data':orderID}),0) )
        r = self.conn.recv(self.recvBuff)
        data = json.loads(r[17:])
        return data
    