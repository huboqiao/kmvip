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

class AlterPayType(ControllerAction, Ui_Dialog):
    def __init__(self, parent=None):
        ControllerAction.__init__(self, parent)
        self.title = u'修改缴费项目'
        self.parent = parent
        size = self.geometry()
        width = GetSystemMetrics(0)
        height = GetSystemMetrics(1)
        self.move((width - size.width()) / 2, (height - size.height()) / 2) # 重置窗口位置
        self.lineEdit.setText(self.parent.typeName)
        self.comboBox.setCurrentIndex(cmp(u'未启用', str(self.parent.typeStat).decode('utf-8')))
        
        self.connect(self.lineEdit, SIGNAL("returnPressed()"), self.alterPayType)  # 名称输入完毕
        self.connect(self.pushButton, SIGNAL("clicked()"), self.alterPayType)  # 修改缴费项目
    # 检查缴费项目是否为空
    def checkTypename(self):
        self.typeName = str(self.lineEdit.text()).strip()
        if self.typeName == '':
            self.boxWarning(u'提示', u'缴费项目名称不能为空')
            self.lineEdit.setFocus()
            return False
        return True
    # 添加缴费项目   
    def alterPayType(self):
        if not self.checkTypename():
            return
        if not self.boxConfirm(u'提示', u'请确认对缴费项目%s的更改'%str(self.parent.typeName), u'修改', u'取消'):
            return
        data = {'typename':self.typeName,'stat':self.comboBox.currentIndex(), 'id':str(self.parent.typeId)}
        data = {'node':'logic','act_fun':'alterPayType','data':data}
        self.myThread = getDataThread(data,0,"alterPayType")
        self.connect(self.myThread, SIGNAL("alterPayType"), self.alterResult)
        self.myThread.start()
    # 缴费项目修改结果
    def alterResult(self, data):
        if data['stat']:
            self.parent.queryPayTypes()
            self.close()
        self.boxWarning(u'提示', data['msg'])