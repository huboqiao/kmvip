#coding:utf8
'''
Created on 2015年1月28日

@author: LiuXinwu
仓库表的操作
'''

from PyQt4.QtCore import QThread
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from application.lib.commodel import Socket_model,Connection_Stock
import json
class StorageModel(Socket_model):
    def __init__(self):
        Socket_model.__init__(self)
        self.conn = Connection_Stock().getConnection()
   
    #修改仓库
    def updateStorage(self,data):
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'updateStorage','data':data}),0))
        r = self.conn.recv(self.recvBuff)
        data = json.loads(r[17:])
        return data
   
    #删除仓库        
    def deleteStorage(self,data):
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'deleteStorage','data':data}),0))
        r = self.conn.recv(self.recvBuff)
        data = json.loads(r[17:])
        return data
    
    #查询所有仓库名称
    def findAllStorageName(self):
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'findAllStorageName','data':''}),0))
        r = self.conn.recv(self.recvBuff)
        data = json.loads(r[17:])
        return data
    
    #添加仓库
    def insertStorage(self,data):
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'insertStorage','data':data}),0))
        r = self.conn.recv(self.recvBuff)
        data = json.loads(r[17:])
        return data
    
    #查询某仓库信息
    def findOneStorage(self,data):
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'findOneStorage','data':data}),0))
        r = self.conn.recv(self.recvBuff)
        data = json.loads(r[17:])
        return data
    
    #查询某仓库区域信息
    def findOneStorageQuYu(self,data):
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'findOneStorageQuYu','data':data}),0))
        r = self.conn.recv(self.recvBuff)
        data = json.loads(r[17:])
        return data
    
    #查询某仓库号数信息
    def findOneStorageHaoShu(self,data):
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'findOneStorageHaoShu','data':data}),0))
        r = self.conn.recv(self.recvBuff)
        data = json.loads(r[17:])
        return data
    
    #查询仓库类型所有名称
    def findTypeNames(self):
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'findTypeNames','data':''}),0))
        r = self.conn.recv(self.recvBuff)
        data = json.loads(r[17:])
        return data
    
    #添加仓库类型
    def insertStorageType(self,data):
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'insertStorageType','data':data}),0))
        r = self.conn.recv(self.recvBuff)
        data = json.loads(r[17:])
        return data
    
    #删除仓库类型数据
    def deleteStorageType(self,data):
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'deleteStorageType','data':data}),0))
        r = self.conn.recv(self.recvBuff)
        data = json.loads(r[17:])
        return data
    
    #查询某仓库类型数据
    def findOneStorageType(self,data):
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'findOneStorageType','data':data}),0))
        r = self.conn.recv(self.recvBuff)
        data = json.loads(r[17:])
        return data
    
    #修改一条仓库类型数据
    def updateStorageType(self,data):
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'updateStorageType','data':data}),0))
        r = self.conn.recv(self.recvBuff)
        data = json.loads(r[17:])
        return data
    
    #查询某区域的号数
    def findOneQuYuHaoShu(self,data):
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'findOneQuYuHaoShu','data':data}),0))
        r = self.conn.recv(self.recvBuff)
        data = json.loads(r[17:])
        return data
    
    #根据区域的id，查到区域的名称
    def findQuYuName(self,data):
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'findQuYuName','data':data}),0))
        r = self.conn.recv(self.recvBuff)
        data = json.loads(r[17:])
        return data
    
    #查询某仓库的所有区域数据
    def findAllQuYu(self,data):
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'findAllQuYu','data':data}),0))
        r = self.conn.recv(self.recvBuff)
        data = json.loads(r[17:])
        return data
    
    #向某仓库添加区域
    def insertQuYu(self,data):
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'insertQuYu','data':data}),0))
        r = self.conn.recv(self.recvBuff)
        data = json.loads(r[17:])
        return data
    
    #删除区域
    def deleteQuYu(self,data):
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'deleteQuYu','data':data}),0))
        r = self.conn.recv(self.recvBuff)
        data = json.loads(r[17:])
        return data
    
    #修改区域
    def updateQuYu(self,data):
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'updateQuYu','data':data}),0))
        r = self.conn.recv(self.recvBuff)
        data = json.loads(r[17:])
        return data
    
    #删除某区域的号数
    def deleteHaoShu(self,data):
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'deleteHaoShu','data':data}),0))
        r = self.conn.recv(self.recvBuff)
        data = json.loads(r[17:])
        return data
    
    #添加区域的号数
    def insertHaoShu(self,data):
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'insertHaoShu','data':data}),0))
        r = self.conn.recv(self.recvBuff)
        data = json.loads(r[17:])
        return data
    