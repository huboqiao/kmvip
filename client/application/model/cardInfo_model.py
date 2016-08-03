#coding:utf8
'''
Created on 2014年9月27日

@author: huaan
设置利率
'''

from PyQt4.QtCore import QThread
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from application.lib.commodel import Socket_model,Connection_Stock
import json
class CardInfo(Socket_model):
    def __init__(self):
        Socket_model.__init__(self)
        self.conn = Connection_Stock().getConnection()
        
    def getCardInfo(self, uid):
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'queryUserCard','data':{'uid':uid}}),0) )
        r = self.conn.recv(self.recvBuff)
        r = self.resolveRecvdata(r)
        return json.loads(r)