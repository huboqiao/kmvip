# -*- coding: utf-8 -*-
'''
Created on 2015年1月31日

@author: LiuXinwu
'''
from PyQt4.QtCore import QThread
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from application.lib.commodel import Socket_model,Connection_Stock
import json
class CustomerModel(Socket_model):
    def __init__(self):
        Socket_model.__init__(self)
        self.conn = Connection_Stock().getConnection()
    
    #查询客户卡的状态,密码,显示卡号
    def findCustomerCardStat(self,data):
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'findCustomerCardStat','data':data}),0))
        r = self.conn.recv(self.recvBuff)
        data = json.loads(r[17:])
        return data
    
    #查询客户的状态
    def findCustomerStat(self,data):
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'findCustomerStat','data':data}),0))
        r = self.conn.recv(self.recvBuff)
        data = json.loads(r[17:])
        return data
        
    def getMemberInfo2(self,data):
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'getMemberInfo2','data':data}),0))
        r = self.conn.recv(self.recvBuff)
        data = json.loads(r[17:])
        return data
    
    #查询客户（customer）信息
    def findOneCustomer(self,data):
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'findOneCustomer','data':data}),0))
        r = self.conn.recv(self.recvBuff)
        data = json.loads(r[17:])
        return data
    
    #查询客户(customerinfo)信息
    def findOneCustomerAdditional(self,data):
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'findOneCustomerAdditional','data':data}),0))
        r = self.conn.recv(self.recvBuff)
        data = json.loads(r[17:])
        return data
    
    #查询客户绑定的卡,用客户ID查
    def findCardWithUid(self,data):
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'findCardWithUid','data':data}),0))
        r = self.conn.recv(self.recvBuff)
        data = json.loads(r[17:])
        return data
    
    #查询此卡是否在数据库中已激活
    def findCardExists(self,data):
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'findCardExists','data':data}),0))
        r = self.conn.recv(self.recvBuff)
        data = json.loads(r[17:])
        return data
    
    #为用户绑定此卡
    def bindCardForCustomer(self,data):
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'bindCardForCustomer','data':data}),0))
        r = self.conn.recv(self.recvBuff)
        data = json.loads(r[17:])
        return data
    
    
    #为用户挂失此卡
    def guashiCardForCustomer(self,data):
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'guashiCardForCustomer','data':data}),0))
        r = self.conn.recv(self.recvBuff)
        data = json.loads(r[17:])
        return data
    
    #查询最近一次交易内容
    def findOneLog(self,data):
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'findOneLog','data':data}),0))
        r = self.conn.recv(self.recvBuff)
        data = json.loads(r[17:])
        return data
    
    #更新客户状态
    def updateCustomerStat(self,data):
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'updateCustomerStat','data':data}),0))
        r = self.conn.recv(self.recvBuff)
        data = json.loads(r[17:])
        return data
    
    