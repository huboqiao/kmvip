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

class AlterPayment(ControllerAction, Ui_Dialog):
    def __init__(self, parent=None):
        ControllerAction.__init__(self, parent)
        self.title = u'修改单据'
        self.parent = parent

        size = self.geometry()
        width = GetSystemMetrics(0)
        height = GetSystemMetrics(1)
        self.move((width - size.width()) / 2, (height - size.height()) / 2) # 重置窗口位置
        
        self.initData()
        
        self.connect(self.pushButton_2, SIGNAL("clicked()"), self.close)
        self.connect(self.pushButton, SIGNAL("clicked()"), self.alterPayment)
        self.connect(self.pushButton_3, SIGNAL("clicked()"), self.queryMemberName)
    # 初始化数据    
    def initData(self):   
        self.typeIds = []
        for payType in self.parent.types:
            self.typeIds.append(payType['id'])
            self.comboBox.addItem(self.tr(payType['typename'])) 
        self.comboBox.setCurrentIndex(self.typeIds.index(self.parent.selectedRecord['typeid']))
        self.dateEdit.setCalendarPopup(True)
        self.dateEdit_2.setCalendarPopup(True)
        self.dateEdit.setDate(QDate.fromString(self.tr(self.parent.selectedRecord['cdate']), 'yyyy/MM/dd'))
        self.dateEdit_2.setDate(QDate.fromString(self.tr(self.parent.selectedRecord['edate']), 'yyyy/MM/dd'))
        self.lineEdit.setText(self.tr(self.parent.selectedRecord['noid']))
        self.lineEdit_2.setText(self.tr(self.parent.selectedRecord['membername']))
        self.lineEdit_3.setText(self.tr(str(self.parent.selectedRecord['amount'])))
        check.stringFilter(self.lineEdit_3, '\d+(\.\d{2})?$')
        data = {'node':'logic','act_fun':'getMemberInfoss','data':{'idCard':self.parent.selectedRecord['idcard']}}
        self.myThread = getDataThread(data,0,"getMemberInfoss")
        self.connect(self.myThread, SIGNAL("getMemberInfoss"), self.setStoregaSite)
        self.myThread.start()
        self.lineEdit_5.setText(self.tr(self.parent.selectedRecord['txt']))
    # 填写租赁地址    
    def setStoregaSite(self, data):
        data = data
        if data['stat']:
            self.memberInfos = data['data'][0]
            if str(data['data'][0]['isstorage']) == '0':
                self.lineEdit_4.setText(u'该类型客户无仓位')
            else:
                storeSite = self.tr(str(data['data'][0]['storename']))
                self.lineEdit_4.setText(storeSite)
    # 查找用户
    def queryMemberName(self):
        if QueryMemberName(self).exec_():
            print self.memberInfos
            self.lineEdit.setText(self.tr(self.memberInfos['noid']))
            self.lineEdit_2.setText(self.tr(self.memberInfos['membername']))
            try:
                storeSite = self.tr(str(self.memberInfos['storename']))
                self.lineEdit_4.setText(storeSite)
            except:
                self.lineEdit_4.setText(u'该类型客户无仓位')
            self.lineEdit_3.setFocus(True)

    # 修改待缴费单  
    def alterPayment(self):
        try:
#             self.memberInfos = {}
            self.memberInfos['payMoney'] = str(self.lineEdit_3.text())
            self.memberInfos['startDate'] = str(self.dateEdit.text())
            self.memberInfos['endDate'] = str(self.dateEdit_2.text())
            self.memberInfos['payType'] = self.parent.types[self.comboBox.currentIndex()]['id']
            self.memberInfos['txt'] = str(self.lineEdit_5.text())
#             try:
            self.memberInfos['cid'] = self.memberInfos['id']
#             except:
#                 self.memberInfos['cid'] = self.parent.selectedRecord['cid']
            self.memberInfos['id'] = self.parent.selectedRecord['id']
            try:
                if float(self.memberInfos['payMoney']) <= 0:
                    self.boxWarning(msg=u'缴费金额需大于0')
                    self.lineEdit_3.setFocus()
                    return
                self.memberInfos['txt'] = self.memberInfos['txt'].replace('null', 'Null')
            except:
                self.lineEdit_3.setFocus()
                return
            print self.memberInfos
            data = {'node':'logic','act_fun':'alterPayment','data':self.memberInfos}
            self.myThread = getDataThread(data,0,"alterPayment")
            self.connect(self.myThread, SIGNAL("alterPayment"), self.alterResult)
            self.myThread.start()
        except Exception as e:
            print e
            
    def alterResult(self, data):
        data = data
        self.boxWarning(u'提示', data['msg'])
        if data['stat']:
            self.accept()
        