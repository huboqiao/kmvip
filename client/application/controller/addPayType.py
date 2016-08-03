# -*- coding: utf-8 -*-
'''
Created on 2015年4月10日

@author: huaan
'''
from PyQt4 import QtGui
from application.lib.Commethods import *
from application.view.addPayType import Ui_Dialog
from application.lib.commodel import getDataThread
from application.model.payment import Payment
from win32api import GetSystemMetrics

class AddPayType(ControllerAction, Ui_Dialog):
    def __init__(self, parent=None):
        ControllerAction.__init__(self, parent)
        self.title = u'添加缴费项目'
        self.parent = parent
        size = self.geometry()
        width = GetSystemMetrics(0)
        height = GetSystemMetrics(1)
        self.move((width - size.width()) / 2, (height - size.height()) / 2) # 重置窗口位置
        self.connect(self.lineEdit, SIGNAL("returnPressed()"), self.addPayType)  # 名称输入完毕
        self.connect(self.pushButton, SIGNAL("clicked()"), self.addPayType)  # 添加缴费项目
    # 检查缴费项目是否为空
    def checkTypename(self):
        self.typeName = str(self.lineEdit.text()).strip()
        if self.typeName == '':
            self.boxWarning(u'提示', u'缴费项目名称不能为空')
            self.lineEdit.setFocus()
            return False
        return True
    # 添加缴费项目   
    def addPayType(self):
        if not self.checkTypename():
            return
        data = {'typename':self.typeName,'stat':self.comboBox.currentIndex()}
        data = {'node':'logic','act_fun':'addPayType','data':data}
        self.myThread = getDataThread(data,0,"addPayType")
        self.connect(self.myThread, SIGNAL("addPayType"), self.addResult)
        self.myThread.start()
    # 缴费项目添加结果    
    def addResult(self, data):
        self.boxWarning(u'提示', data['msg'])
        if data['stat']:
            self.parent.queryPayTypes()
            self.close()
