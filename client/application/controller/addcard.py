# -*- coding: utf-8 -*-
'''
Created on 2014年9月27日

@author: twc
'''
from PyQt4 import QtGui
from application.lib.Commethods import *
from application.view.addcard import Ui_Dialog
from application.model.addcard_model import AddCardModel
from win32api import GetSystemMetrics
import application.lib.formatCheck as check

class AddcardContorller(ControllerAction, Ui_Dialog):
    def __init__(self, parent=None):
        ControllerAction.__init__(self, parent)
        self.parent = parent
        size = self.geometry()
        width = GetSystemMetrics(0)
        height = GetSystemMetrics(1)
        self.move((width - size.width()) / 2, (height - size.height()) / 2) # 重置窗口位置
        
        self.connect(self.lineEdit, SIGNAL("returnPressed()"), self.addcard)  # 回车事件
        self.connect(self.lineEdit_2, SIGNAL("returnPressed()"), self.addcardto)  # 回车事件
        self.connect(self.pushButton, SIGNAL("clicked()"), self.addcardto)  # 回车事件
        self.model = AddCardModel()
        check.stringFilter(self.lineEdit, "[\d\s]+$")
        check.stringFilter(self.lineEdit_2, "[\d\s]+$")
   
    # 添加会员卡    
    def addcard(self):
        try:
            self.cardid = int(str(self.lineEdit.text()))
            self.lineEdit_2.setFocus()
        except:
            self.boxWarning(u'提示', u'请输入正确的会员卡号')
            self.lineEdit.setFocus()
            
    # 进行添加
    def addcardto(self):
        try:
            self.cardid = long(str(self.lineEdit.text()))
            self.cardid1 = long(str(self.lineEdit_2.text()))
        except:
            self.boxWarning(u'提示', u'请输入正确的纯数字会员卡号')
            self.lineEdit.setFocus()
        
        else:
            data = self.model.sendCard(self.cardid, self.cardid1, self.appdata['user']['user_id'])
            if data['stat'] == -1:
                self.boxWarning(u'提示', data['msg'].decode('utf8'))
            if data['stat'] == 1:
                self.boxWarning(u'提示', u'添加会员卡成功')
                self.label_2.setText(self.tr(str(self.lineEdit.text()) + data['msg'].decode('utf8')))
        #         self.label_2.setText(self.tr(str(self.lineEdit.text()) + '会员卡添加成功'))
                try:
                    self.parent.aCard = str(self.lineEdit_2.text())
                    self.accept()
                except:
                    self.lineEdit.setText('')
                    self.lineEdit_2.setText('')
                    self.lineEdit.setFocus()
        
    def addCardError(self):
        self.boxWarning(u'提示', u'会员卡已存在')
        self.label_2.setText('')
        self.lineEdit.setText('')
        self.lineEdit_2.setText('')
        self.lineEdit.setFocus()
   
    def addCardSucces(self):
        self.boxWarning(u'提示', u'添加会员卡成功')
#         self.label_2.setText(self.tr(str(self.lineEdit.text()) + '会员卡添加成功'))
        try:
            self.parent.aCard = str(self.lineEdit_2.text())
            self.accept()
        except:
            self.lineEdit.setText('')
            self.lineEdit_2.setText('')
            self.lineEdit.setFocus()
       
