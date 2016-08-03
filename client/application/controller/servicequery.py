# -*- coding: utf-8 -*-
'''
Created on 2015年2月4日

@author: LiuXinwu
'''
from application.lib.Commethods import *
from application.view.servicequery import Ui_Dialog
import time
from application.lib.commodel import getDataThread
import application.lib.formatCheck as check

class ServiceQueryController(ControllerAction, PrintAction, Ui_Dialog):
    def __init__(self,parent=None):
        ControllerAction.__init__(self,parent)
        PrintAction.__init__(self, self.tableWidget)
        self.parent = parent
        self.setTableFormat()
        self.startQuery = True
        self.tableWidget.horizontalHeader().setResizeMode(QHeaderView.Stretch)      #铺满表格
        self.connect(self.pushButton, SIGNAL("clicked()"),self.memberQuery)
        self.connect(self.name, SIGNAL("returnPressed()"),self.memberQuery)
        self.connect(self.idcard, SIGNAL("returnPressed()"),self.memberQuery)
        self.connect(self.lineEdit_3, SIGNAL("returnPressed()"),self.memberQuery)
        self.connect(self.lineEdit, SIGNAL("returnPressed()"),self.memberQuery)
        self.connect(self.comboBox, SIGNAL("currentIndexChanged(int)"),self.memberQuery)
        self.memberQuery()
        check.stringFilter(self.lineEdit_3, "[\d\s]+$")
        check.stringFilter(self.idcard, "^[1-9]\d{5}[1-9]\d{3}((0\d)|(1[0-2]))(([0|1|2]\d)|3[0-1])\d{3}([0-9]|X)$")
        
    #查询客户冻结时间
    def memberQuery(self):
        self.tableWidget.setRowCount(0)
        if not self.startQuery:
            return
        name=str(self.name.text())
        idcard=str(self.idcard.text())
        data={'orderName':str(self.lineEdit.text()), 'name':name, 'idcard':idcard, 'noid':str(self.lineEdit_3.text()), 'type':self.comboBox.currentIndex()}
        datas={'node':'logic','act_fun':'queryService22','data':data}
        self.threadmodel = getDataThread(datas,0,"queryService22")
        self.connect(self.threadmodel,SIGNAL("queryService22"),self.getgroup)
        self.threadmodel.start()
        self.startQuery = False
            
    def getgroup(self,data):
        self.startQuery = True
        self.memberQueryInfo(data)
            
    def memberQueryInfo(self,data):
        data = data
        if data['stat']:
            self.insertTable(data['data'])
        else:
            self.boxWarning(u'提示', data['msg'])
                
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
            self.tableWidget.setItem(rowCount,0,QTableWidgetItem(u"合计：%s条记录"%len(data)))
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
        self.table_fmt_list.append({"alignment":"center","color":"black","format":"general","count":False})
        self.table_fmt_list.append({"alignment":"center","color":"black","format":"general","count":False})
        self.table_fmt_list.append({"alignment":"center","color":"black","format":"general","count":False})
        self.table_fmt_list.append({"alignment":"center","color":"black","format":"general","count":False})
        self.table_fmt_list.append({"alignment":"center","color":"black","format":"enum","count":False,"enum":['绑卡', u'挂失', u'冻结', u'注销', u'添加']})
        self.table_fmt_list.append({"alignment":"center","color":"black","format":"general","count":False})
        #需要汇总的字段
        self.countColumn = [key for key,value in enumerate(self.table_fmt_list) if value['count'] == True]
        #表格列匹配数据库字段
        self.columnName = ['id', "membername", "idcard", 'noid', 'tel', 'username', 'type', 'cdate']
        #初始化汇总字段的值为0
        self.countList = {}
        for i in self.countColumn:
            self.countList[str(i)] = 0