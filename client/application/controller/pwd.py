# -*- coding: utf-8 -*-
'''
Created on 2014年6月11日

@author: chenyong
'''
from application.lib.Commethods import *
from application.view.pwd import Ui_Dialog

class PwdContorller(ControllerAction,Ui_Dialog):
    def __init__(self,parent=None,title=u'修改密码'):
        ControllerAction.__init__(self,parent,title)
        self.parent = parent
        
        self.connect(self.lineEdit, SIGNAL("returnPressed()"),self.nextPwd)
        self.connect(self.lineEdit_2, SIGNAL("returnPressed()"),self.towPwd)

    
    def nextPwd(self):
        if self.lineEdit.text():
            self.lineEdit_2.setFocus()
        else:
            self.lineEdit.setFocus()
            self.boxWarning(u'提示',u'密码不能为空')
    
    def towPwd(self):
        pwd1 = str(self.lineEdit.text())
        pwd2 = str(self.lineEdit_2.text()) 
        try:
            int(pwd1)
            if len(pwd1) < 6:
                self.boxWarning(u'提示',u'请输入不小于6位的新密码')
                self.lineEdit.setFocus()
                return
        except:
            self.boxWarning(u'提示',u'请输入不小于6位的新数字密码')
            self.lineEdit.setFocus()
            return
            
                
        if pwd2 != pwd1:
            self.boxInfo(u'提示', u'二次密码不一致，请重新输入！')
            self.lineEdit_2.setText('')
            self.lineEdit_2.setFocus()
        else:
            if self.boxConfirm(u'修改密码', u'您将要修改金荣卡密码，请牢记您的新密码！', u'确定', u'取消'):
                self.parent.postPwd(pwd1)
                self.close()