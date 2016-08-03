#coding:utf8
'''
Created on 2014年10月09日

@author: tang

'''

from application.lib.commodel import Socket_model, Connection_Stock
import json
class GrantsModel(Socket_model):
    def __init__(self):
        Socket_model.__init__(self)
        self.conn = Connection_Stock().getConnection()
        
    def getGrantsFinger(self, groupId):
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'getGrantsFinger','data':groupId}),0) )
        r = self.conn.recv(self.recvBuff)
        r = self.resolveRecvdata(r)
        return json.loads(r)