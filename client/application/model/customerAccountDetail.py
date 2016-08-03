#coding:utf8
'''
Created on 2014年10月25日

@author: huaan
'''

from PyQt4.QtCore import QThread
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from application.lib.commodel import Socket_model,Connection_Stock
import json
class CustomerAccountActivityModel(Socket_model):
    def __init__(self):
        Socket_model.__init__(self)
        self.conn = Connection_Stock().getConnection()
    
    def getCardCurrentAmount(self,cardID):
        self.conn.sendall(self.sendData(json.dumps({'node':'capital','act_fun':'getCardCurrentAmount','data':cardID}),0))
        r = self.conn.recv(self.recvBuff)
        r = self.resolveRecvdata(r)
        return json.loads(r)
    
    def getCardRecord(self,data):
        self.conn.sendall(self.sendData(json.dumps({'node':'capital','act_fun':'cardRecord','data':data}),0))
        r = self.conn.recv(self.recvBuff)
        r = self.resolveRecvdata(r)
        return json.loads(r)

    def getCardIDFromNoID(self,data):
        self.conn.sendall(self.sendData(json.dumps({'node':'capital','act_fun':'getCardIDFromNoID','data':data}),0))
        r = self.conn.recv(self.recvBuff)
        r = self.resolveRecvdata(r)
        return json.loads(r)
    
    def balanceBeforeTime(self,data):
        self.conn.sendall(self.sendData(json.dumps({'node':'capital','act_fun':'balanceBeforeTime','data':data}),0))
        r = self.conn.recv(self.recvBuff)
        r = self.resolveRecvdata(r)
        return json.loads(r)