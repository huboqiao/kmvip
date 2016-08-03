# -*- coding: utf-8 -*-
'''
Created on 2015年2月27日

@author: LiuXinwu
'''
from PyQt4 import QtGui
from application.lib.Commethods import *
from application.view.membermanageradd import Ui_Dialog
from application.model.party_model import PartyModel
from PyQt4.Qt import SIGNAL


class MemberManagerAddController(ControllerAction,Ui_Dialog):
    def __init__(self,parent=None):
        ControllerAction.__init__(self,parent)
        self.parent = parent
        
        if self.parent.eid:
            self.setWindowTitle(u"修改：")
        else:
            self.setWindowTitle(u"添加")
        self.model=PartyModel()
        
        self.connect(self.pushButton,SIGNAL("clicked()"),self.addParty)
        self.connect(self.pushButton_2,SIGNAL("clicked()"),self.cancle)
        
        self.init()
        
    
    def addParty(self):
        if not self.lineEdit.text():
            self.boxWarning(u'提示',u'供应商名称不能为空！')
            self.lineEdit.setFocus(True)
            return
        if not self.lineEdit_3.text():
            self.boxWarning(u'提示',u'手机号码不能为空！')
            self.lineEdit_3.setFocus(True)
            return
        try:
            int(self.lineEdit_3.text())
        except:
            self.boxWarning(u'提示',u'手机只能填写数字！')
            self.lineEdit_3.clear()
            self.lineEdit_3.setFocus(True)
            return
        name=str(self.lineEdit.text())
        tel=str(self.lineEdit_2.text())
        phone=str(self.lineEdit_3.text())
        email=str(self.lineEdit_4.text())
        address=str(self.lineEdit_5.text())
        man=str(self.lineEdit_6.text())
        desc=str(self.lineEdit_7.text())
        ty=self.comboBox.currentIndex()
        
        if ty == 0:
            ty = str(1)
        else:
            ty = str(0)
        
        if self.parent.eid:
            json=self.model.update(name,tel,phone,email,address,man,desc,ty,str(self.parent.eid))
            if json['stat']==False:
                self.boxWarning(u'提示',u'修改失败！')
                return
            else :
                self.boxInfo(u'提示',u'修改成功！')
                self.parent.query()
                self.parent.pushButton_3.setEnabled(False)
                self.parent.pushButton_4.setEnabled(False)
                self.close()
        else:
            json=self.model.add(name,tel,phone,email,address,man,desc,ty)
            
            if json['stat']==False:
                self.boxWarning(u'提示',u'添加失败！')
                return
            else :
                self.boxInfo(u'提示',u'添加成功！')
                self.parent.query()
                self.close()
            
    def cancle(self):
        self.close()     
        self.parent.pushButton_3.setEnabled(False)
        self.parent.pushButton_4.setEnabled(False)

    def init(self):
        if self.parent.eid:
            self.lineEdit.setText(self.parent.ename)
            self.lineEdit_2.setText(self.parent.etel)
            self.lineEdit_3.setText(self.parent.ephone)
            self.lineEdit_4.setText(self.parent.eemail)
            self.lineEdit_5.setText(self.parent.eaddress)
            self.lineEdit_6.setText(self.parent.eman)
            self.lineEdit_7.setText(self.parent.edesc)
            self.comboBox.setCurrentIndex(0)
            if str(self.parent.ety)=='是':
                self.comboBox.setCurrentIndex(1)