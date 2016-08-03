# -*- coding: utf-8 -*-
'''
Created on 2015年1月31日
开卡
@author: huaan
'''
from PyQt4 import QtGui
from application.lib.Commethods import *
from application.view.opencard import Ui_Dialog
from application.model.opencard_model import OpenCardModel
from application.controller.addcard import AddcardContorller
import time
import hashlib

class OpenCardContorller(ControllerAction,Ui_Dialog):
    def __init__(self,parent=None):
        ControllerAction.__init__(self,parent)
        self.parent=parent
        self.title = u'新用户绑卡'
        self.aCard = ''
#         self.setupUi(self)
        self.connect(self.card, SIGNAL("returnPressed()"), self.inputCard)        #刷入会员卡
        self.connect(self.pwd, SIGNAL("returnPressed()"), self.inputPwd)          #输入密码
        self.connect(self.pwd2, SIGNAL("returnPressed()"), self.inputPwd2)        #输入密码
        self.connect(self.pushButton, SIGNAL("clicked()"), self.inputPwd2)
        self.connect(self.pushButton_2, SIGNAL("clicked()"), self.newCard)
        
    def newCard(self):
        if AddcardContorller(self).exec_():
            self.card.setText(self.tr(self.aCard))
            self.inputCard()
    #刷入会员卡
    def inputCard(self):
        self.pwd.setFocus()
        
    #输入第一次密码
    def inputPwd(self):
        if len(self.pwd.text()) != 6:
            self.boxWarning(u'提示',u'密码必须为六位数字！')
            self.pwd.setFocus()
        else:
            self.pwd2.setFocus()
    #输入第二次密码
    def inputPwd2(self):
        if self.pwd2.text()=='':
            self.boxWarning(u'提示',u'确认密码不能为空！')
        elif str(self.pwd.text())!=str(self.pwd2.text()):
            self.boxWarning(u'提示',u'两次密码不一致！')
            self.pwd2.setFocus()
        else:
            if len(self.pwd2.text())!=6:
                self.boxWarning(u'提示',u'密码必须为六位！')
                return
            pwd=hashlib.md5()
            pwd.update(str(self.pwd2.text()))
            pwd.hexdigest()
            
            model = OpenCardModel()
            data = model.bindCard(str(self.parent.user_id),str(self.card.text()),str(pwd.hexdigest()),self.appdata['user']['user_id'])
            try:
                if data['stat'] == 1:
                    self.bindOk()
                else:
                    self.bindError()
                    self.boxWarning(u'提示', data['msg'].decode('utf8'))
            except:
                self.boxWarning(u'提示',u'该卡处于【'+data.decode('utf8')+'】')
    #绑定卡成功关闭窗口
    def bindOk(self):
        self.boxInfo(unicode('提示', 'utf8'), unicode('绑定成功', 'utf8'))
        self.close()
        ControllerAction.closeTab(self.parent)
    
    #绑定卡不成功
    def bindError(self):
        self.card.setText('')
        self.pwd.setText('')
        self.pwd2.setText('')
        self.card.setFocus()
        
        
     