#coding:utf8
'''
Created on 2015年2月4日

@author: LiuXinwu
'''

from PyQt4.QtCore import QThread
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from application.lib.commodel import Socket_model,Connection_Stock
import json
class OrderListModel(Socket_model):
    def __init__(self):
        Socket_model.__init__(self)
        self.conn = Connection_Stock().getConnection()
        
    def queryOrderList(self):
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'getOrderList','data':''}),0) )
        r = self.conn.recv(self.recvBuff)
        data = json.loads(r[17:])
        return data
    
    def queryOrderUsername(self,data):
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'getOrderUsername','data':data}),0) )
        r = self.conn.recv(self.recvBuff)
        data = json.loads(r[17:])
        return data
    
        
    def queryOrderDetail(self,data):
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'queryOrderDetail','data':data}),0) )
        r = self.conn.recv(self.recvBuff)
        data = json.loads(r[17:])
        return data
        
            
    def delOrder(self,data):
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'deleteOrder','data':data}),0) )
        r = self.conn.recv(self.recvBuff)
        data = json.loads(r[17:])
        return data
    
    def queryApplyName(self,data):
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'queryApplyName','data':data}),0) )
        r = self.conn.recv(self.recvBuff)
        data = json.loads(r[17:])
        return data
    
    #查询商品表与订单_info表
    def queryGoodsAndOrderinfo(self,data):
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'queryGoodsAndOrderinfo','data':data}),0) )
        r = self.conn.recv(self.recvBuff)
        data = json.loads(r[17:])
        return data
    
    #查询订单表中某一订单的详情
    def getOneOrder(self,data):
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'getOneOrder','data':data}),0) )
        r = self.conn.recv(self.recvBuff)
        data = json.loads(r[17:])
        return data
    
    #查询某一订单下所有商品总价
    def querySumZongjia(self,data):
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'querySumZongjia','data':data}),0) )
        r = self.conn.recv(self.recvBuff)
        data = json.loads(r[17:])
        return data
    
    #查询符合条件的订单
    def filterOrderList(self,data):
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'filterOrderList','data':data}),0) )
        r = self.conn.recv(self.recvBuff)
        data = json.loads(r[17:])
        return data
    
    
    #查询所有用户的真实姓名及id
    def queryNickname(self):
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'queryNickname','data':''}),0) )
        r = self.conn.recv(self.recvBuff)
        data = json.loads(r[17:])
        return data
    
    
    
    
    
    