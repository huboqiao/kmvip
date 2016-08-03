# -*- coding: utf-8 -*-
'''
Created on 2015年2月2日

@author: LiuXinwu
'''
from PyQt4 import QtGui
from application.lib.Commethods import *
from application.view.linkcard import Ui_Dialog
from application.model.customermodel import CustomerModel
import hashlib

class LinkCardController(ControllerAction,Ui_Dialog):
    def __init__(self,parent=None):
        ControllerAction.__init__(self,parent)
        self.parent = parent
        self.id = self.parent.id
        #实例化model
        self.model = CustomerModel()
        #绑定事件
        self.connect(self.pushButton,SIGNAL('clicked()'),self.tiJiao)
    
    #验证密码是否一致
    def validate(self):
        noid = str(self.lineEdit.text())
        #卡号不能为空
        if noid.strip():
            pass
        else:
            self.lineEdit.setFocus(True)
            self.boxInfo(u'提示',u'请填写卡号！')
            return False
        try:
            int(noid)
        except:
            self.lineEdit.clear()
            self.lineEdit.setFocus(True)
            self.boxInfo(u'提示',u'卡号只能由数字组成！')
            return False
        
        #密码1不能为空
        pwd1 = str(self.lineEdit_2.text())
        if pwd1.strip():
            pass
        else:
            self.lineEdit_2.setFocus(True)
            self.boxInfo(u'提示',u'请填写密码！')
            return False
        
        #密码2不能为空
        pwd2 = str(self.lineEdit_3.text())
        if pwd2.strip():
            pass
        else:
            self.lineEdit_3.setFocus(True)
            self.boxInfo(u'提示',u'请填写确认密码！')
            return False
        
        #输入密码
        if pwd1==pwd2:
            if len(pwd1)!=6:
                self.lineEdit_2.clear()
                self.lineEdit_3.clear()
                self.lineEdit_2.setFocus(True)
                self.boxInfo(u'提示',u'密码只能为六位数字组成！')
                return False
            else:
                pass
        else:
            self.lineEdit_2.clear()
            self.lineEdit_3.clear()
            self.lineEdit_2.setFocus(True)
            self.boxInfo(u'提示',u'两次密码输入不一致，请重新输入！')
            return False
        
        return True
        
        
    def tiJiao(self):
        if self.validate():
            #获得表单数据
            pnoid = str(self.lineEdit.text())
            noid = pnoid.strip()
            #pwd = str(self.lineEdit_2.text())
            cid = str(self.id)
            pwd=hashlib.md5()
            pwd.update(str(self.lineEdit_2.text()))
            pwd.hexdigest()
            
            #先查询该卡是否已录入到数据库中
            cardExists = self.model.findCardExists({'cnoid':str(noid)})
            if cardExists['stat']:
                #更新数据库
                re = self.model.bindCardForCustomer({'cid':cid,'cnoid':str(noid),'pwd':str(pwd.hexdigest()),'uid':self.appdata['user']['user_id']})
                self.boxInfo(u'提示',re['msg'])
                print '是执行这个'
                self.close()
                self.parent.closeTab()
            else:
                self.boxInfo(u'提示',cardExists['msg'])
        else:
            pass
        