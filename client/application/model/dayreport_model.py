#coding:utf8
'''
Created on 2014年9月25日

@author: ivan

'''
import json
from application.lib.commodel import Socket_model,Connection_Stock,getDataThread
class DayreportModel(Socket_model):
    def __init__(self):
        Socket_model.__init__(self)
        self.conn = Connection_Stock().getConnection()
    
    def getUser(self):
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'queryUser','data':''}),0) )
        r = self.conn.recv(self.recvBuff)
        data = json.loads(r[17:])
        return data[0]
        