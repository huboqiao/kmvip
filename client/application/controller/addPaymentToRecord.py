# -*- coding: utf-8 -*-
'''
Created on 2015年4月15日

@author: huaan
'''
from PyQt4 import QtGui
from application.lib.Commethods import *
from application.view.addPayment import Ui_Dialog
from application.lib.commodel import getDataThread
from application.controller.queryMemberName import QueryMemberName
from application.model.memberModel import MemberModel
import application.lib.formatCheck as check
from win32api import GetSystemMetrics

class AddPaymentToRecord(ControllerAction, Ui_Dialog):
    def __init__(self, parent=None):
        ControllerAction.__init__(self, parent)
        self.title = u'缴费项目手动录入'
        self.parent = parent
        self.memberInfos = ''
        
        for payType in parent.types:
            self.comboBox.addItem(self.tr(payType['typename']))
        
        self.dateEdit.setCalendarPopup(True)
        self.dateEdit_2.setCalendarPopup(True)
        date = QDate().currentDate()
        self.dateEdit.setDate(date)
        date = date.addDays(-date.day())
        self.dateEdit_2.setDate(date)
        self.lineEdit_3.setText('0.00')
        check.stringFilter(self.lineEdit_3, '\d+(\.\d{2})?$')
        
        size = self.geometry()
        width = GetSystemMetrics(0)
        height = GetSystemMetrics(1)
        self.move((width - size.width()) / 2, (height - size.height()) / 2) # 重置窗口位置
        
        self.connect(self.lineEdit_3, SIGNAL("textChanged(QString)"), self.autoFillTxt)
        self.connect(self.comboBox, SIGNAL("currentIndexChanged(QString)"), self.autoFillTxt)
        self.connect(self.dateEdit_2, SIGNAL("editingFinished()"), self.latestDateChanged)
        self.connect(self.pushButton_2, SIGNAL("clicked()"), self.close)
        self.connect(self.pushButton, SIGNAL("clicked()"), self.addPaymentRecord)
        self.connect(self.pushButton_3, SIGNAL("clicked()"), self.queryMemberName)
        
    def latestDateChanged(self):
        if self.dateEdit.date().__ge__(self.dateEdit_2.date()):
            if type(self.focusWidget()) == QtGui.QLineEdit:
                self.boxWarning(u'提示', u'最后缴费期限必须晚于录单时间')
                self.dateEdit_2.setFocus()
                return False
        return True
        
    def autoFillTxt(self, txt):
        if self.sender() == self.lineEdit_3:
            if str(txt) == '':
                return
        text = u'%s年%s月份%s%s元'
        temp = (self.dateEdit.date().year(),
                self.dateEdit.date().month(),
                str(self.comboBox.currentText()),
                str(self.lineEdit_3.text()))
        self.lineEdit_5.setText(self.tr(text%temp))
    # 查找用户
    def queryMemberName(self):
        if QueryMemberName(self).exec_():
            self.lineEdit.setText(self.tr(self.memberInfos['noid']))
            self.lineEdit_2.setText(self.tr(self.memberInfos['membername']))
            if str(self.memberInfos['storename']) == '':
                self.lineEdit_4.setText(u'该类型客户无仓位')
            else:
                storeSite = self.tr(str(self.memberInfos['storename']))
                self.lineEdit_4.setText(storeSite)
            self.lineEdit_3.setFocus(True)

    # 添加待缴费单  
    def addPaymentRecord(self):
        if not self.latestDateChanged():
            return
        try:
            self.memberInfos['payMoney'] = str(self.lineEdit_3.text())
            self.memberInfos['startDate'] = str(self.dateEdit.text())
            self.memberInfos['endDate'] = str(self.dateEdit_2.text())
            self.memberInfos['payType'] = self.parent.types[self.comboBox.currentIndex()]['id']
            self.memberInfos['txt'] = str(self.lineEdit_5.text())
            try:
                if float(self.memberInfos['payMoney']) <= 0:
                    self.boxWarning(msg=u'缴费金额需大于0')
                    self.lineEdit_3.setFocus()
                    return
                self.memberInfos['txt'] = self.memberInfos['txt'].replace('null', 'Null')
            except:
                self.lineEdit_3.setFocus()
                return
            self.parent.toAddRecordData = self.memberInfos
            if self.boxConfirm(u'提示', u'请确认待缴费单信息，点击“确定”按钮完成添加'):
                self.accept()
        except Exception as e:
            print e