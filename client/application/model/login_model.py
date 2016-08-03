# -*- coding: utf-8 -*-
'''
Created on 2014年9月25日
登录
@author: ivan
'''
from application.lib.commodel import Socket_model,Connection_Stock
import json
class LoginModel(Socket_model):
    def __init__(self):
        Socket_model.__init__(self)
        self.conn = Connection_Stock().getConnection()
    
    def login(self,u,p):
        data = {'u':str(u),'p':str(p)}
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'login','data':data}),3)) 
        r = self.conn.recv(1024)
        r = self.resolveRecvdata(r)  
        return r  