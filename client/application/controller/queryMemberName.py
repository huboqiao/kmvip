# -*- coding: utf-8 -*-
'''
Created on 2015年4月15日
查找要缴费的人员
@author: huaan
'''
from PyQt4 import QtGui
from application.lib.Commethods import *
from application.view.queryMemberName import Ui_Dialog
from application.model.memberQuery import MemberQueryModel
from application.lib.commodel import getDataThread
from application.lib.Commethods import *
from application.lib.commodel import *
from win32api import GetSystemMetrics
import application.lib.formatCheck as check

class QueryMemberName(ControllerAction, PrintAction, Ui_Dialog):
    def __init__(self, parent=None):
        ControllerAction.__init__(self, parent)
        self.parent = parent
        self.title = u'查找用户'
        PrintAction.__init__(self, self.tableWidget)
        size = self.geometry()
        width = GetSystemMetrics(0)
        height = GetSystemMetrics(1)
        self.move((width - size.width()) / 2, (height - size.height()) / 2 + 25) # 重置窗口位置
        self.tableWidget.horizontalHeader().setResizeMode(QHeaderView.Stretch)      #铺满表格
        self.setTableFormat()
        
        self.connect(self.lineEdit, SIGNAL("returnPressed()"), self.queryMemberName)  # 回车事件
        self.connect(self.lineEdit_2, SIGNAL("returnPressed()"), self.queryMemberName)  # 回车事件
        self.connect(self.lineEdit_3, SIGNAL("returnPressed()"), self.queryMemberName)  # 回车事件
        self.connect(self.pushButton, SIGNAL("clicked()"), self.queryMemberName)  # 点击事件
        self.connect(self.tableWidget, SIGNAL("cellDoubleClicked(int, int)"), self.selectName)  # 双击单元格
        self.queryMemberName()
        check.stringFilter(self.lineEdit_2, "[\d\s]+$")
        check.stringFilter(self.lineEdit_3, "^[1-9]\d{5}[1-9]\d{3}((0\d)|(1[0-2]))(([0|1|2]\d)|3[0-1])\d{3}([0-9]|X)$")
    # 重写键盘事件响应方法
    def keyPressEvent(self, event):
        # 过滤大小键盘回车事件
        if event.key() in (Qt.Key_Enter, Qt.Key_Return):
            if self.tableWidget.currentItem() is not None:
                self.selectName(self.tableWidget.currentRow())
            else:
                return QDialog.keyPressEvent(self, event)
    
    def selectName(self, row):
        self.parent.memberInfos = self.members[row]
        self.accept()
    # 根据条件查询数据
    def queryMemberName(self):
        self.tableWidget.setCurrentItem(None)
        data = {'name': str(self.lineEdit.text()).strip(), 
                'card':str(self.lineEdit_2.text()).strip(), 
                'idCard':str(self.lineEdit_3.text()).strip()}
#         recvData = MemberQueryModel().getMemberInfosss(data)
#         self.getSearchResults(recvData)
        data = {'node':'logic','act_fun':'getMemberBaseInfo','data':data}
        self.myThread = getDataThread(data,0,"getMemberBaseInfo")
        self.connect(self.myThread, SIGNAL("getMemberBaseInfo"), self.getSearchResults)
        self.myThread.start()
#         self.myThread.deleteLater()
    # 查询结果处理
    def getSearchResults(self, data):
        data = data
        self.tableWidget.setRowCount(0)
        if not data['stat']:
            self.boxWarning(u'提示', data['msg'])
        else:
            self.members = data['data']
            self.insertTable(data['data'])
            self.lineEdit.setFocus()
    
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
        self.columnName = ["membername","noid","idcard"]
        #初始化汇总字段的值为0
        self.countList = {}
        for i in self.countColumn:
            self.countList[str(i)] = 0