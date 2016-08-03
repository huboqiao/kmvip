# -*- coding: utf-8 -*-
'''
Created on 2015年2月3日

@author: huaan
'''
from PyQt4 import QtGui
from application.lib.Commethods import *
from application.view.alterPassword import Ui_Dialog
from application.controller.fingerWindow import FingerWindow
from application.model.cardeditpwd_model import CardEidtPwdModel


class AlterPasswordController(ControllerAction,Ui_Dialog):
    def __init__(self,parent=None):
        ControllerAction.__init__(self,parent)
        self.parent = parent
        
        self.connect(self.pushButton, SIGNAL('clicked()'), self.getIDCardNumber)
        self.connect(self.pushButton_2, SIGNAL('clicked()'), self.checkFinger)
        self.connect(self.pushButton_3, SIGNAL('clicked()'), self.getBasicInfos)
        
    def getIDCardNumber(self):
        pass 
    
    def checkFinger(self):
        pass
    
    def getBasicInfos(self):
        pass
    
    
    #验证会员密码后获取客户信息   
    def getMemberInfo(self):
        cardid=str(self.lineEdit_2.text())
        if cardid:
            json=CardEidtPwdModel().getCardInfo(cardid)
            if json['stat']==-1:
                self.boxWarning(u'提示',json['msg'])
                self.lineEdit_2.selectAll()
                return
            
            self.GetCardInfo(json)
            
        else:
            self.boxWarning(u'提示',u'请刷入要取现的会员卡！')
        