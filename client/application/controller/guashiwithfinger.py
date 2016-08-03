# -*- coding: utf-8 -*-
'''
Created on 2015年3月22日

@author: LiuXinwu
'''
from PyQt4 import QtGui
from application.lib.Commethods import *
from application.view.password import Ui_Dialog
from application.controller.fingerWindow import FingerWindow
from application.model.guashi_model import GuashiModel
from application.model.quxian_model import QuxianModel

class GuaShiWithFinger(ControllerAction,Ui_Dialog):
    def __init__(self,parent=None):
        ControllerAction.__init__(self,parent)
        self.parent = parent
        self.fingers = parent.fingers
        self.model = GuashiModel()
        self.model2 = QuxianModel()
        self.connect(self.lineEdit, SIGNAL("returnPressed()"), self.getPwd)    #获取用户输入的密码
        self.connect(self.pushButton, SIGNAL("clicked()"), self.checkFinger)    #输入用户指纹验证

    def checkFinger(self):
        win = FingerWindow(self)
        win.exec_() 
        
    def getPwd(self):
        pwd=self.lineEdit.text()
        if pwd=='':
            self.boxWarning(u'提示',u'请输入密码！')
            self.lineEdit.setFocus()
        else:
            recvData = self.model2.pwdCheck({'cardid':str(self.parent.noid), 'pwd':str(pwd)})
            self.checkPwd(recvData)
                
    #密码验证结果
    def checkPwd(self,data):
        if data['stat'] == 1:
            #密码验证正确，挂失
            self.close()
            self.parent.gart(True)
        else:
            self.parent.pwdNum += 1
            if self.parent.pwdNum == 5:
                #密码连续输错五次
                isFrozen = self.model.frozenCard(str(self.parent.noid))
                if isFrozen['stat'] == 1:
                    self.boxWarning(u'提示', u'连续5次输入错误密码！已冻结该会员卡。')
                    self.close()
                    self.parent.pushButton_9.setEnabled(False)#不能正常挂失
                else:
                    self.boxInfo('失败', isFrozen['msg'])
            else:
                msg=data['msg']+u'还有（'+str(5-self.parent.pwdNum)+u'）次机会'
                self.boxWarning(u'提示',msg)
                self.lineEdit.setText('')
                self.lineEdit.setFocus(True)
    #此卡密码已锁定
    def cardShop(self,data):
        if data:
            self.boxWarning(u'提示',u'您连续输错密码五次现已锁定！')
            self.close()
            self.parent.close()
        else:
            self.boxWarning(u'提示',u'您连续输错密码过多,此次操作不能进行！')
            self.close()
            self.parent.close()
            
            
            
        
        
    