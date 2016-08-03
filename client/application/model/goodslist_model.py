#coding:utf8
'''
Created on 2014年9月25日

@author: ivan
取现
'''
from PyQt4.QtCore import QThread
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from application.lib.commodel import Socket_model,Connection_Stock
class GoodslistModel(Socket_model,QThread):
    def __init__(self):
        Socket_model.__init__(self)
        QThread.__init__(self)
        self.conn = Connection_Stock().getConnection()
        try:
           self.appdata['perspective'].callRemote('goodlist',self,'','','','')
           #self.conn.sendall(self.sendData("{'node':'capital','act_fun':'getMemberinfo','data':"+cardid+"}",0))
        except:
            pass
        self.data = ''
    
    def run(self):
        while True:
            try:
                message = self.conn.recv(1024)
                self.data += self.resolveRecvdata(message)
                if len(message) < 1024:
                    self.emit(SIGNAL("report"),self.cardStat(eval(self.data)))
                    break
            except:
                self.emit(SIGNAL("report"),self.cardStat('error'))
                break
                
    def cardStat(self,data):
        if data == 'error':
            return {'stat':False,'msg':u'网络连接失败，请重新连接'}
        try:
            stat = data['cardstat']
            if stat == 1:
                return {'stat':True,'data':data}
            elif stat == 2:
                return {'stat':False,'msg':u'该卡处于注销状态，无法使用'}
            elif stat == 0:
                return {'stat':False,'msg':u'该卡未绑定用户，无法使用'}
            else:
                return {'stat':False,'msg':u'该卡处于冻结状态，无法使用'}
        except:
            return {'stat':False,'msg':u'卡号不正确'}

