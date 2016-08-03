#coding:utf8
'''
Created on 2014年9月28日

@author: huaan

'''

from application.lib.commodel import Socket_model,Connection_Stock
import json
class QuxianModel(Socket_model):
    def __init__(self):
        Socket_model.__init__(self)
        self.conn = Connection_Stock().getConnection()
        
    def getMemberInfo(self,cardid):
        data = {'cardid':cardid,'act':''}
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'getMemberInfo','data':data}),0) )
        r = self.conn.recv(self.recvBuff)
        r = self.resolveRecvdata(r)
        return json.loads(r)
    
    def pwdCheck(self, data):
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'pwdCheck','data':data}),0) )
        r = self.conn.recv(self.recvBuff)
        r = self.resolveRecvdata(r)
        return json.loads(r)
    
    def pwdCheckzz(self, data):
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'pwdCheckzz','data':data}),0) )
        r = self.conn.recv(self.recvBuff)
        r = self.resolveRecvdata(r)
        return json.loads(r)
    
    def frozenCard(self, data):
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'frozenCard','data':data}),0) )
        r = self.conn.recv(self.recvBuff)
        r = self.resolveRecvdata(r)
        return json.loads(r)       
    
    def quxian(self, data):
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'insertTaking','data':data}),0) )
        r = self.conn.recv(self.recvBuff)
        r = self.resolveRecvdata(r)
        return json.loads(r)   