#coding:utf8
'''
Created on 2014年10月09日

@author: tang

'''

from application.lib.commodel import Socket_model,Connection_Stock
import json
class CardEidtPwdModel(Socket_model):
    def __init__(self):
        Socket_model.__init__(self)
        self.conn = Connection_Stock().getConnection()
        
    def getCardInfo(self, cardid):
        data={'cardid':cardid}
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'getCardInfo','data':data}),0) )
        r = self.conn.recv(self.recvBuff)
        r = self.resolveRecvdata(r)
        return json.loads(r)
    
    
    def upCardPwd(self, cardid,pwd):
        data={'cardid':cardid,'pwd':pwd}
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'updateCardPwd','data':data}),0) )
        r = self.conn.recv(self.recvBuff)
        r = self.resolveRecvdata(r)
        return json.loads(r)