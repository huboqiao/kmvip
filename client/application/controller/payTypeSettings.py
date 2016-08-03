# -*- coding: utf-8 -*-
'''
Created on 2015年4月10日
缴费项目设置
@author: huaan
'''
from PyQt4 import QtGui
from application.lib.Commethods import *
from application.view.payTypeSettings import Ui_Dialog
from application.controller.addPayType import AddPayType
from application.controller.alterPayType import AlterPayType
from application.lib.commodel import getDataThread
from application.model.payment import Payment

class PayTypeSettings(ControllerAction,PrintAction, Ui_Dialog):
    def __init__(self,parent=None):
        ControllerAction.__init__(self,parent)
        PrintAction.__init__(self, self.tableWidget)
        self.tableWidget.horizontalHeader().setResizeMode(QHeaderView.Stretch)      #铺满表格
        self.parent=parent
        
        self.connect(self.pushButton, SIGNAL("clicked()"), self.addPayType)  # 添加缴费项目
        self.connect(self.pushButton_2, SIGNAL("clicked()"), self.alterPayType)  # 修改缴费项目
        self.connect(self.pushButton_3, SIGNAL("clicked()"), self.deletePayType)  #　删除缴费项目
        self.connect(self.tableWidget, SIGNAL('cellClicked(int, int)'), self.rowSelected)  # 选中一个缴费项目
        
        self.setTableFormat()
        self.queryPayTypes()
    # 检索所有缴费项目    
    def queryPayTypes(self):
        self.tableWidget.setRowCount(0)
        self.pushButton_2.setEnabled(False)
        self.pushButton_3.setEnabled(False)
        data = {'node':'logic','act_fun':'queryPayTypes','data':''}
        self.myThread = getDataThread(data,0,"queryPayTypes")
        self.connect(self.myThread, SIGNAL("queryPayTypes"), self.fillTypes)
        self.myThread.start()
    # 存在缴费项目则显示在表格，不存在则提示
    def fillTypes(self, data):
        data = data
        if data['stat']:
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
                    
        if len(self.countColumn)>0:
            rowCount = self.tableWidget.rowCount()
            self.tableWidget.setRowCount(rowCount+1)
            self.tableWidget.setItem(rowCount,0,QTableWidgetItem(u"合计："))
            for key,value in self.countList.items():
                item = QTableWidgetItem(str(value))
                self.tableWidget.setItem(rowCount,int(key),item)
                self.formatTableItem(item,self.table_fmt_list[int(key)])
    # 设置表格每列的格式
    def setTableFormat(self):
        #字段格式
        self.table_fmt_list = []
        self.table_fmt_list.append({"alignment":"center","color":"black","format":"general","count":False})
        self.table_fmt_list.append({"alignment":"center","color":"black","format":"general","count":False})
        self.table_fmt_list.append({"alignment":"center","color":"black","format":"enum","count":False,"enum":['未启用','启用']})
        #需要汇总的字段
        self.countColumn = [key for key,value in enumerate(self.table_fmt_list) if value['count'] == True]
        #表格列匹配数据库字段
        self.columnName = ["id","typename","stat"]
        #初始化汇总字段的值为0
        self.countList = {}
        for i in self.countColumn:
            self.countList[str(i)] = 0
    # 点击表格   
    def rowSelected(self, row, col, enable=True):
        self.typeId = self.tableWidget.item(row, 0).text()
        self.typeName = self.tableWidget.item(row, 1).text()
        self.typeStat = self.tableWidget.item(row, 2).text()
        self.pushButton_2.setEnabled(enable)
        self.pushButton_3.setEnabled(enable)
    # 添加缴费项目
    def addPayType(self):
        AddPayType(self).exec_()
    # 修改缴费项目
    def alterPayType(self):
        AlterPayType(self).exec_()
    # 删除缴费项目  
    def deletePayType(self):
        if not self.boxConfirm(u'提示', u'您确定要删除缴费项目%s'%str(self.typeName), u'删除', u'取消'):
            return
        data = {'id':str(self.typeId)}
        data = {'node':'logic','act_fun':'deletePayType','data':data}
        self.myThread = getDataThread(data,0,"deletePayType")
        self.connect(self.myThread, SIGNAL("deletePayType"), self.deleteResult)
        self.myThread.start()
    # 缴费项目删除结果    
    def deleteResult(self, data):
        if data['stat']:
            self.queryPayTypes()
        self.boxWarning(u'提示', data['msg'])