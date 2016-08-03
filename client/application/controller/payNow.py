# -*- coding: utf-8 -*-
'''
Created on 2015年4月10日

@author: huaan
'''
from PyQt4 import QtGui
from application.lib.Commethods import *
from application.view.payNow import Ui_Dialog
from application.lib.commodel import getDataThread
from application.controller.payNowPassword import PayNowPassword
from win32api import GetSystemMetrics

class PayNow(ControllerAction, Ui_Dialog):
    def __init__(self, parent=None, title=''):
        ControllerAction.__init__(self, parent)
        self.title = title
        self.parent = parent
        self.payMethod = 1
        
        size = self.geometry()
        width = GetSystemMetrics(0)
        height = GetSystemMetrics(1)
        self.move((width - size.width()) / 2, (height - size.height()) / 2) # 重置窗口位置
        
        if cmp(title, u'单据详情') == 0:
            self.label_8.hide()
            self.radioButton.hide()
            self.radioButton_2.hide()
            self.radioButton_3.hide()
            self.pushButton.hide()
            self.pushButton_2.setText(self.tr(u'确    定'))
        
        self.lineEdit.setText(self.tr(self.parent.toPayRecord[0]['noid']))
        self.lineEdit_2.setText(self.tr(self.parent.toPayRecord[0]['typename']))
        self.lineEdit_3.setText(self.tr(self.parent.toPayRecord[0]['cdate']))
#         self.lineEdit_4.setText(self.tr(self.parent.toPayRecord[0]['adder']))
        
        data = {'node':'logic','act_fun':'getMemberInfoss','data':{'idCard':self.parent.toPayRecord[0]['idcard']}}
        self.myThread = getDataThread(data,0,"getMemberInfoss")
        self.connect(self.myThread, SIGNAL("getMemberInfoss"), self.setStoregaSite)
        self.myThread.start()
        
        self.lineEdit_5.setText(self.tr(self.parent.toPayRecord[0]['membername']))
        self.lineEdit_6.setText(self.tr(str(self.parent.toPayRecord[0]['amount'])))
        self.lineEdit_7.setText(self.tr(self.parent.toPayRecord[0]['edate']))
        
        self.connect(self.pushButton_2, SIGNAL("clicked()"), self.close)
        self.connect(self.pushButton, SIGNAL("clicked()"), self.payNow)    # 去付款  
        self.connect(self.radioButton, SIGNAL("pressed()"), self.payMethodChanged)
        self.connect(self.radioButton_2, SIGNAL("pressed()"), self.payMethodChanged)
        self.connect(self.radioButton_3, SIGNAL("pressed()"), self.payMethodChanged)
        
    # 填写租赁地址    
    def setStoregaSite(self, data):
        if data['stat']:
            if str(data['data'][0]['isstorage']) == '0':
                self.lineEdit_4.setText(u'该类型客户无仓位')
            else:
                storeSite = self.tr(str(data['data'][0]['storename']))
                self.lineEdit_4.setText(storeSite)
        
    # 变更付款方式
    def payMethodChanged(self):
        if self.sender() == self.radioButton:
            self.parent.payAct = 1
        elif self.sender() == self.radioButton_2:
            self.parent.payAct = 2
        else:
            self.parent.payAct = 3
            
    # 金荣卡转账前验证密码
    def payNow(self):
        if self.parent.payAct == 2:
            self.fingers = ['dsafd']
            self.pwdNum = 0
            PayNowPassword(self).exec_()
        else:
            self.accept()
    # 密码或指纹验证通过
    def pwdOk(self):
        self.accept()
        