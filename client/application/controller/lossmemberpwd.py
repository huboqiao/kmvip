# -*- coding: utf-8 -*-
'''
Created on 2015年3月4日

@author: LiuXinwu
'''
from PyQt4 import QtGui
from application.lib.Commethods import *
from application.view.password2 import Ui_Dialog
from application.controller.grants import GrantContorller
import hashlib

class LossMemberPwdContorller(ControllerAction,Ui_Dialog):
    def __init__(self,data,parent=None):
        ControllerAction.__init__(self,parent)
        self.parent = parent
        self.data=data
        self.connect(self.lineEdit, SIGNAL("returnPressed()"), self.checkPwd)    #验证密码
    
    #验证密码
    def checkPwd(self):
        pwd = str(self.lineEdit.text())
        if pwd:
            password=hashlib.md5()
            password.update(pwd)
            if str(password.hexdigest())==(self.data.customerPwd):
                self.close()
                win=GrantContorller(self.data)
                win.exec_()
            else:
                self.boxWarning(u'提示',u'密码错误')
        else:
            self.boxWarning(u'提示',u'请输入密码！')
            

    
        
