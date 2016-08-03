# -*- coding: utf-8 -*-
'''
Created on 2014年6月11日

@author: chenyong
'''
import hashlib
from application.lib.Commethods import *
from application.view.pwdt import Ui_Dialog
from application.controller.fingerWindow import FingerWindow
import application.lib.formatCheck as check

class MyLineEdit(QLineEdit):
    def __init__(self, *args):
        QLineEdit.__init__(self, *args)

    def event(self, event):
        if (event.type()==QEvent.KeyPress) and (event.key()==Qt.Key_Return):
            self.emit(SIGNAL("returnPressed"))
            return True
        return QLineEdit.event(self, event)

class PwdtContorller(ControllerAction,Ui_Dialog):
    def __init__(self,parent=None, title=u'修改密码'):
        ControllerAction.__init__(self,parent,title)
        self.parent = parent
        self.pwdPassed = False
        self.fingers = self.parent.fingers
        self.green = QPalette()
        self.green.setColor(QPalette().WindowText, Qt.green)
        self.red = QPalette()
        self.red.setColor(QPalette().WindowText, Qt.red)
        self.connect(self.lineEdit, SIGNAL("returnPressed()"),self.checkPwd)
        self.connect(self.lineEdit_2, SIGNAL("returnPressed()"),self.nextPwd)
        self.connect(self.lineEdit_3, SIGNAL("returnPressed()"),self.towPwd)
        self.connect(self.pushButton, SIGNAL('clicked()'), self.checkFinger)
        self.connect(self.pushButton_2, SIGNAL('clicked()'), self.towPwd)
        
    def checkFinger(self):
        self.pwdPassed = False
        self.label_4.setText(u'待验证')
        self.label_4.setPalette(self.red)
        FingerWindow(self).exec_()

    def checkPwd(self,data=''):
        if type(data) == type({}):
            if data['stat'] == 1:
                self.pwdPassed = True
                self.label_4.setText(u'已验证')
                self.label_4.setPalette(self.green)
                self.lineEdit_2.setFocus(True)
                return
            else:
                self.pwdPassed = False
                self.label_4.setText(u'待验证')
                self.label_4.setPalette(self.red)
                self.boxWarning(u'提示', u'您的指纹不正确，请重新匹配或选择密码验证！')
            return
        pwd = self.lineEdit.text()
        if pwd:
            pwds=hashlib.md5()
            pwds.update(str(pwd))
            pwd = pwds.hexdigest()
            if self.parent.password == str(pwd):
                self.pwdPassed = True
                self.label_4.setText(u'已验证')
                self.label_4.setPalette(self.green)
                self.lineEdit_2.setFocus(True)
                return
            else:
                self.boxWarning(u'提示', u'原密码不正确！')
                self.label_4.setText(u'待验证')
                self.label_4.setPalette(self.red)
                self.lineEdit.setText('')
                self.lineEdit.setFocus(True)
                return
        else:
            if not self.pwdPassed:
                self.lineEdit.setText('')
                self.lineEdit.setFocus(True)
    
    def nextPwd(self):
        if self.lineEdit_2.text():
            self.lineEdit_3.setFocus(True)
        else:
            self.lineEdit_2.setFocus(True)
            self.boxWarning(u'提示',u'密码不能为空')
    
    def towPwd(self):
        if not self.pwdPassed:
            self.boxWarning(u'提示', u'请输入原密码或验证客户指纹！')
            return 
        pwd1 = str(self.lineEdit_2.text())
        try:
            int(pwd1)
            if len(pwd1) != 6:
                self.boxWarning(u'提示', u'请输入六位数字新密码！')
                return
        except:
            self.boxWarning(u'提示', u'请输入六位数字新密码！')
            return
            
            
        pwd2 = str(self.lineEdit_3.text())
        if pwd2 != pwd1:
            self.boxInfo(u'提示', u'二次密码不一致，请重新输入！')
            self.lineEdit_3.setText('')
            self.lineEdit_3.setFocus(True)
            return
        else:
            if self.boxConfirm(u'修改密码', u'您将要修改金荣卡密码，请牢记您的新密码！', u'确定', u'取消'):
                self.parent.postPwd(pwd1)
                self.close()
            