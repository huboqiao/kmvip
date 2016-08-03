#coding:utf8
'''
Created on 2015年1月30日

@author: huaan
仓库操作
'''

from PyQt4.QtCore import QThread
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from application.lib.commodel import Socket_model,Connection_Stock
import json
class StoreQueryModel(Socket_model):
    def __init__(self):
        Socket_model.__init__(self)
        self.conn = Connection_Stock().getConnection()
    # 检索仓库
    def queryStore(self):
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'queryStoreName2','data':''}),0) )
        r = self.conn.recv(self.recvBuff)
        data = json.loads(r[17:])
        return data
    # 根据仓库ID检索区域
    def queryAllRegionByStoreId(self, storeId):
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'queryAllRegionByStoreId','data':storeId}),0) )
        r = self.conn.recv(self.recvBuff)
        data = json.loads(r[17:])
        return data
    # 根据区域ID检索号数
    def queryAllSerialNumberByRegionId(self, regionId):
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'queryAllSerialNumberByRegionId','data':regionId}),0) )
        r = self.conn.recv(self.recvBuff)
        data = json.loads(r[17:])
        return data
    # 检索仓库类别
    def queryStoreType(self):
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'queryStoreType','data':''}),0) )
        r = self.conn.recv(self.recvBuff)
        data = json.loads(r[17:])
        return data