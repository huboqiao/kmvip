# -*- coding: utf-8 -*-
'''
Created on 2015年2月27日
客户管理模型类
@author: LiuXinwu
'''
from PyQt4.QtCore import QThread
from application.lib.commodel import Socket_model,Connection_Stock
import json
class PartyModel(Socket_model):
    def __init__(self):
        Socket_model.__init__(self)
        self.conn = Connection_Stock().getConnection()

    def add(self,name,tel,phone,email,address,man,desc,ty):
        data={'name':name,'tel':tel,'phone':phone,'email':email,'address':address,'man':man,'desc':desc,'ty':ty}
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'addParty','data':data}),0))
        r = self.conn.recv(self.recvBuff)
        r = self.resolveRecvdata(r)
        return json.loads(r)
    
    def update(self,name,tel,phone,email,address,man,desc,ty,id):
        data={"name":name,"tel":tel,"phone":phone,"email":email,"address":address,'man':man,'desc':desc,"ty":ty}
        datas={'data':data,'id':id}
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'updateParty','data':datas}),0))
        r = self.conn.recv(self.recvBuff)
        r = self.resolveRecvdata(r)
        return json.loads(r)
    
    def delete(self,partyid):
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'deleteparty','data':partyid}),0))
        r = self.conn.recv(self.recvBuff)
        r = self.resolveRecvdata(r)
        return json.loads(r)
    
    def get(self,where):
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'getparty','data':where}),0))
        r = self.conn.recv(self.recvBuff)
        r = self.resolveRecvdata(r)
        return json.loads(r)
    
    #查询供应商有无提供货物
    def querySupGoods(self,data):
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'querySupGoods','data':data}),0))
        r = self.conn.recv(self.recvBuff)
        r = self.resolveRecvdata(r)
        return json.loads(r)
