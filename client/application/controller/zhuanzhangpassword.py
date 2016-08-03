# -*- coding: utf-8 -*-
'''
Created on 2014年6月11日

@author: ivan
'''
from PyQt4 import QtGui
from application.lib.Commethods import *
from application.lib.finger import *
from application.controller.fingerWindow import FingerWindow
from application.view.password import Ui_Dialog
from application.model.quxian_model import QuxianModel

class ZhuanZhangPasswordContorller(ControllerAction, Ui_Dialog):
    def __init__(self,parent=None):
        ControllerAction.__init__(self,parent)
       
        self.parent = parent
        self.fingers = parent.fingers
        self.model = QuxianModel()
        self.connect(self.lineEdit, SIGNAL("returnPressed()"), self.getPwd)   # 获取用户输入的密码
        self.connect(self.pushButton, SIGNAL("clicked()"), self.checkFinger)  # 选择指纹验证
    
    def checkFinger(self):
        FingerWindow(self).exec_()
    
    def getPwd(self):
        pwd=self.lineEdit.text()
        if pwd=='':
            self.boxWarning(u'提示',u'请输入密码！')
            self.lineEdit.setFocus()
        else:
            self.model = QuxianModel()
            recvData = self.model.pwdCheckzz({'cardid':str(self.parent.cardid.text()), 'pwd':str(pwd)})
            self.checkPwd(recvData)
                
    # 密码验证结果
    def checkPwd(self,data):
        if data['stat'] == 1:
            self.boxWarning(u'提示', u'客户指纹匹配成功，请主管验证指纹授权')
            self.parent.pwdOk(self)
        elif data['stat'] == 2:
            self.boxWarning(u'提示', u'密码通过，请主管验证指纹授权！')
            self.parent.pwdOk(self)
        else:
            self.parent.pwdNum += 1
            if self.parent.pwdNum == 5:
                # 密码连续输错五次
                datas = {'cid':self.parent.zcid, 'noid': str(self.parent.zccard), 'uid': self.appdata['user']['user_id']}
                isFrozen = self.model.frozenCard(datas)
                if isFrozen['stat'] == 1:
                    self.boxWarning(u'提示', u'连续5次输入错误密码！已冻结该会员卡。')
                    self.close()
                    ControllerAction.closeTab(self.parent)
#                     self.parent.commandLinkButton_2.setEnabled(False)
                else:
                    self.boxInfo('失败', isFrozen['msg'])
            else:
                msg=data['msg']+u'还有（'+str(5-self.parent.pwdNum)+u'）次机会'
                self.boxWarning(u'提示',msg)
                self.lineEdit.setText('')
                self.lineEdit.setFocus(True)
                
    # 此卡密码已锁定
    def cardShop(self,data):
        if data:
            self.boxWarning(u'提示',u'您连续输错密码五次现已锁定！')
            self.close()
            self.parent.close()
        else:
            self.boxWarning(u'提示',u'您连续输错密码过多,此次操作不能进行！')
            self.close()
            self.parent.close()
