# -*- coding: utf-8 -*-
'''
Created on 2014年9月27日

@author: twc
'''
from PyQt4 import QtGui
from application.lib.Commethods import *
from application.view.pushNews import Ui_Dialog
from application.lib.commodel import getDataThread
from application.model.massage import MassageModel
import application.lib.formatCheck as check
from win32api import GetSystemMetrics

class PushNews(ControllerAction, PrintAction, Ui_Dialog):
    def __init__(self, parent=None):
        ControllerAction.__init__(self, parent)
        PrintAction.__init__(self, self.tableWidget)
        self.tableWidget_2.setEditTriggers(QAbstractItemView.CurrentChanged)
        self.setTableFormat()
        self.tableWidget_2.setRowCount(1)
        item = QTableWidgetItem('+')
        item.setTextAlignment(Qt.AlignCenter)
        self.tableWidget_2.setItem(0, 0, item)
        self.parent = parent
        size = self.geometry()
        width = GetSystemMetrics(0)
        height = GetSystemMetrics(1)
        self.move((width - size.width()) / 2, (height - size.height()) / 2) # 重置窗口位置
        self.connect(self.pushButton_2, SIGNAL("clicked()"), self.addAllMember)
        self.connect(self.pushButton_3, SIGNAL("clicked()"), self.sendMessage)
        self.connect(self.pushButton_4, SIGNAL("clicked()"), self.removeAllTels)
        
        self.connect(self.tableWidget, SIGNAL("cellDoubleClicked(int, int)"), self.addMember)
        self.connect(self.tableWidget, SIGNAL("currentCellChanged(int, int, int, int)"), self.findInTable2)
        self.connect(self.tableWidget_2, SIGNAL("cellDoubleClicked(int, int)"), self.removeTel)
        self.connect(self.tableWidget_2, SIGNAL("cellClicked(int, int)"), self.findInTable1)
        self.connect(self.tableWidget_2, SIGNAL("cellPressed(int, int)"), self.setItemBackgroundColor)
        self.connect(self.tableWidget_2, SIGNAL("cellChanged(int, int)"), self.checkInputTel)
        self.connect(self.tableWidget_2, SIGNAL("currentCellChanged(int, int, int, int)"), self.checkInputTel)
        self.queryMemberName()
    
    def clearTable1color(self):
        for r in range(self.tableWidget.rowCount()):
            self.tableWidget.item(r, 0).setBackgroundColor(Qt.white)
            self.tableWidget.item(r, 1).setBackgroundColor(Qt.white)
            self.tableWidget.item(r, 2).setBackgroundColor(Qt.white)
    
    def findInTable1(self, row, col):
        self.clearTable1color()
        for r in range(self.tableWidget.rowCount()):
            if cmp(str(self.tableWidget.item(r, 2).text()), str(self.tableWidget_2.item(row, 0).text())) == 0:
                self.tableWidget.scrollToItem(self.tableWidget.item(r, 2))
#                 self.tableWidget.item(r, 0).setBackgroundColor(QColor(51,153,255))
#                 self.tableWidget.item(r, 1).setBackgroundColor(QColor(51,153,255))
#                 self.tableWidget.item(r, 2).setBackgroundColor(QColor(51,153,255))
                self.tableWidget.setCurrentCell(r, 0)
                break
    
    def findInTable2(self, row, col):
        self.setItemBackgroundColor()
        for r in range(self.tableWidget_2.rowCount()):
            if cmp(str(self.tableWidget_2.item(r, 0).text()), str(self.tableWidget.item(row, 2).text())) == 0:
                self.tableWidget_2.scrollToItem(self.tableWidget_2.item(r, 0))
                self.tableWidget_2.item(r, 0).setBackgroundColor(QColor(51,153,255))
                break
    # 发送短信    
    def sendMessage(self):
        msg = str(self.textEdit_2.toPlainText())
        if msg.strip() == '':
            self.boxWarning(u'提示', u'请输入短信内容')
            return
        self.telsCount = self.tableWidget_2.rowCount() - 1
        if self.telsCount <= 0:
            self.boxWarning(u'提示', u'短信接收手机号至少为一个')
            return
        failCount = 0
        tels = []
        for i in range(self.telsCount):
            tels.append(str(self.tableWidget_2.item(i, 0).text()))
        
        data = {'node':'logic','act_fun':'sendCustomerMsg','data':{'tels':tels, 'content':msg}}
        self.myThread = getDataThread(data,0,"sendCustomerMsg")
        self.connect(self.myThread, SIGNAL("sendCustomerMsg"), self.sendResult)
        self.myThread.start()
    def sendResult(self, data):
        try:
            self.boxWarning(u'提示', data['msg'])
        except:
            self.boxWarning(u'提示', u'发送成功%s条，失败%s条'%(self.telsCount - data['failedCount'], data['failedCount']))
        
    # 校验输入的手机号码是否合法
    def checkInputTel(self, row, col, newRow=0, newCol=0):
        if row == self.tableWidget_2.rowCount() - 1:
            text = str(self.tableWidget_2.item(row, 0).text()).replace(' ', '')
            # 手机号码合法？
            if check.checkMobilePhone(text):
                # 号码重复
                for r in range(row):
                    if cmp(text.replace(' ', ''), str(self.tableWidget_2.item(r, 0).text()).replace(' ', '')) == 0:
                        self.tableWidget_2.item(r, 0).setText(self.tableWidget_2.item(row - 1, 0).text())
                        self.tableWidget_2.item(row - 1, 0).setText(self.tr(text))
                        self.tableWidget_2.item(row - 1, 0).setFlags(Qt.ItemIsEnabled)
                        self.tableWidget_2.item(row, 0).setText('+')
                        return
                # 号码未重复，添加一行
                self.tableWidget_2.setRowCount(row + 2)
                item = QTableWidgetItem('+')
                item.setTextAlignment(Qt.AlignCenter)
                self.tableWidget_2.setItem(row + 1, 0, item)
                self.tableWidget_2.setCurrentItem(item)
                self.tableWidget_2.item(row, 0).setFlags(Qt.ItemIsEnabled)
                self.tableWidget_2.scrollToBottom()
            else:
                self.tableWidget_2.item(row, 0).setText('+')
                self.tableWidget_2.setCurrentCell(row, 0)
#         else:
#             
#             self.findInTable1(row, col)
    # 添加所有客户手机号    
    def addAllMember(self):
        for row in range(self.tableWidget.rowCount()):
            self.addMember(row, 2)
    # 清空接收手机号表背景颜色        
    def setItemBackgroundColor(self, row = 0, col = 0, color = Qt.white):
        for row in range(self.tableWidget_2.rowCount() - 1):
            self.tableWidget_2.item(row, 0).setBackgroundColor(color)
    # 移除所有接收手机号
    def removeAllTels(self):
        self.tableWidget_2.setRowCount(1)
        item = QTableWidgetItem('+')
        item.setTextAlignment(Qt.AlignCenter)
        self.tableWidget_2.setItem(0, 0, item)
    # 移除一个接收手机号  
    def removeTel(self, row, col):
        self.setItemBackgroundColor()
        if row == self.tableWidget_2.rowCount() - 1:
            return
        self.tableWidget_2.removeRow(row)
    # 添加一个客户手机号
    def addMember(self, row, col):
        telsRowCount = self.tableWidget_2.rowCount()
        tel = self.tableWidget.item(row, 2).text()
        self.setItemBackgroundColor()
        # 手机号码合法？
        if check.checkMobilePhone(str(tel)) is None:
            self.boxWarning(u'提示', u'该用户手机号格式不正确')
            self.tableWidget.setCurrentCell(row,col)
            return
        for r in range(telsRowCount - 1):
            # 手机号已经存在跳转到该号所在行
            if cmp(str(tel).replace(' ', ''), str(self.tableWidget_2.item(r, 0).text()).replace(' ', '')) == 0:
                self.tableWidget_2.scrollToItem(self.tableWidget_2.item(r, 0))
                self.tableWidget_2.item(r, 0).setBackgroundColor(QColor(51,153,255))
                return
        # 手机号未出现在接收号码表中，该手机号插入倒数第1行
        item = QTableWidgetItem(tel)
        item.setFlags(Qt.ItemIsEnabled)
        item.setBackgroundColor(QColor(51,153,255))
        item.setTextAlignment(Qt.AlignCenter)
        self.tableWidget_2.setItem(telsRowCount - 1, 0, item)
        # 手机号未出现在接收号码表中，添加1空行
        self.tableWidget_2.setRowCount(telsRowCount + 1)
        item = QTableWidgetItem('+')
        item.setTextAlignment(Qt.AlignCenter)
        self.tableWidget_2.setItem(telsRowCount, 0, item)
        # 滚动到最后一行
        self.tableWidget_2.scrollToBottom()
        
    # 根据条件查询数据
    def queryMemberName(self):
        data = {'node':'logic','act_fun':'getMemberBaseInfo','data':{'stat':''}}
        self.myThread = getDataThread(data,0,"getMemberBaseInfo")
        self.connect(self.myThread, SIGNAL("getMemberBaseInfo"), self.getSearchResults)
        self.myThread.start()
    # 查询结果处理
    def getSearchResults(self, data):
        data = data
        self.tableWidget.setRowCount(0)
        if not data['stat']:
            self.boxWarning(u'提示', data['msg'])
        else:
            self.insertTable(data['data'])
            
    # 插入数据到表格
    def insertTable(self,data):
        self.tableWidget.setRowCount(len(data))
        for i,value in enumerate(data):
            for j in range(self.tableWidget.columnCount()):
                item = QTableWidgetItem(unicode(str(value[self.columnName[j]])))
                self.formatTableItem(item,self.table_fmt_list[j])
                self.tableWidget.setItem(i,j,item)
                if j in self.countColumn:
                    self.countList[str(j)] += value[self.columnName[j]]
                    
    # 设置表格每列的格式
    def setTableFormat(self):
        #字段格式
        self.table_fmt_list = []
        self.table_fmt_list.append({"alignment":"center","color":"black","format":"general","count":False})
        self.table_fmt_list.append({"alignment":"center","color":"black","format":"general","count":False})
        self.table_fmt_list.append({"alignment":"center","color":"black","format":"general","count":False})
        #需要汇总的字段
        self.countColumn = [key for key,value in enumerate(self.table_fmt_list) if value['count'] == True]
        #表格列匹配数据库字段
        self.columnName = ["membername","noid","tel"]
        #初始化汇总字段的值为0
        self.countList = {}
        for i in self.countColumn:
            self.countList[str(i)] = 0
            
