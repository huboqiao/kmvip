# -*- coding: utf-8 -*-
'''
Created on 2014年9月28日
绑定卡
@author: huann
'''
import json
from application.lib.commodel import Socket_model,Connection_Stock
class OpenCardModel(Socket_model):
    def __init__(self):
        Socket_model.__init__(self)
        self.conn = Connection_Stock().getConnection()
    
    def bindCard(self,userid,card,pwd,addid=''):
        data = {'user_id':userid,'card':card,'pwd':pwd,'addid':addid}
        
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'bindCard','data':data}),0))
        r = self.conn.recv(self.recvBuff)
        r = self.resolveRecvdata(r)
        print r
        return json.loads(r)        