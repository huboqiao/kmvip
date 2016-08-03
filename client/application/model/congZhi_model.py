# -*- coding: utf8 -*-
'''
Created on 2014年10月8日

@author: huaan
'''

from PyQt4.QtCore import QThread
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from application.lib.commodel import Socket_model,Connection_Stock
import json
class ChongZhiModel(Socket_model):
    def __init__(self):
        Socket_model.__init__(self)
        self.conn = Connection_Stock().getConnection()
        
    def getCardInfo(self,cardid):
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'getCardInfo','data':{'cardid':cardid}}),0) )
        r = self.conn.recv(self.recvBuff)
        r = self.resolveRecvdata(r)
        return json.loads(r)
    
    def inRecharge(self, data):
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'inRecharge','data':data}),0) )
        r = self.conn.recv(self.recvBuff)
        r = self.resolveRecvdata(r)
        return json.loads(r)