#coding:utf8
'''
Created on 2015年2月6日

@author: LiuXinwu
操作商品类别表的模型
'''
import json
from application.lib.commodel import Socket_model,Connection_Stock,getDataThread
class GoodsModel(Socket_model):
    def __init__(self):
        Socket_model.__init__(self)
        self.conn = Connection_Stock().getConnection()
    
    #获取商品所有类别
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
    
    def addClass(self,data):
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'addClass','data':data}),0) )
        r = self.conn.recv(self.recvBuff)
        data = json.loads(r[17:])
        return data
    
    #修改商品类别
    def editClass(self,data):
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'editClass','data':data}),0) )
        r = self.conn.recv(self.recvBuff)
        data = json.loads(r[17:])
        return data   
     
    def delClass(self,data):
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'delClass','data':data}),0) )
        r = self.conn.recv(self.recvBuff)
        data = json.loads(r[17:])
        return data
       
    #为类别添加商品
    def addGoods(self,data):
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'addGoods','data':data}),0) )
        r = self.conn.recv(self.recvBuff)
        data = json.loads(r[17:])
        
        return data  
    
    #修改商品信息
    def editGoods(self,data):
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'editGoods','data':data}),0) )
        r = self.conn.recv(self.recvBuff)
        data = json.loads(r[17:])
        
        return data
         
    #删除商品
    def delGoods(self,data):
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'delGoods','data':data}),0) )
        r = self.conn.recv(self.recvBuff)
        data = json.loads(r[17:])
        
        return data

        
        