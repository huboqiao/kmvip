# -*- coding: utf-8 -*-
'''
Created on 2014年6月11日

@author: chenyong
'''
from PyQt4 import QtGui
from application.lib.Commethods import *
from application.view.bank import Ui_Dialog
from application.controller.prints import PrintContorller


class BankController(ControllerAction,Ui_Dialog):
    def __init__(self,parent=None):
        ControllerAction.__init__(self,parent)
        self.setupUi(self)
        self.parent=parent
        
        self.connect(self.lineEdit, SIGNAL("returnPressed()"), self.inputBankId)      #输入银行转账流水号
        parentWin = parent.parent.parent.geometry()
        size = self.geometry()#此处的geometry()首字母必须要小写，否则无法测试通过。
        self.move((parentWin.width()-size.width())/2,(parentWin.height()-size.height())/4)
        
    def inputBankId(self):
        bankid=str(self.lineEdit.text())
        if bankid=='':
            self.boxWarning(u'提示', u'银行卡流水号不能为空！')
            return
                
        else:
            try:
                self.close()
                self.appdata['perspective'].callRemote('upInRechargeBankNo',self.parent,self.parent.noid,bankid)
            except:
                self.boxWarning(u'提示', u'连接服务器超时，请重新登录！')
