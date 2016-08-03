# -*- coding: utf-8 -*-
'''
Created on 2015年2月6日

@author: LiuXinwu
供应商列表控制器
'''
from PyQt4 import QtGui
from application.lib.Commethods import *
from application.view.suppliers import Ui_suppliersList
from application.lib.commodel import  getDataThread
import time

class SuppliersController(ControllerAction,Ui_suppliersList):
    def __init__(self,parent = None):
        ControllerAction.__init__(self,parent)
        self.parent = parent
        self.suppliersTable.horizontalHeader().setResizeMode(QHeaderView.Stretch)      #铺满表格
        #绑定事件
        self.connect(self.lineEdit, SIGNAL('returnPressed()'), self.suppliersQuery)
        self.connect(self.lineEdit_2, SIGNAL('returnPressed()'), self.suppliersQuery)
        self.connect(self.lineEdit_3, SIGNAL('returnPressed()'), self.suppliersQuery)
        self.connect(self.lineEdit_4, SIGNAL('returnPressed()'), self.suppliersQuery)
        self.connect(self.pushButton, SIGNAL('clicked()'), self.suppliersQuery)
        self.suppliersQuery()
    #查询供应商信息
    def suppliersQuery(self):
        self.suppliersTable.setRowCount(0)
        cidData = str(self.lineEdit.text())
        cid = cidData.strip()
        cmembernameData = str(self.lineEdit_2.text())
        cmembername = cmembernameData.strip()
        snameData = str(self.lineEdit_3.text())
        sname = snameData.strip()
        quyuData = str(self.lineEdit_4.text())
        quyu = quyuData.strip()
        wheres = {'supplierID':str(cid),
                  'supplierName':str(cmembername),
                  'storageName':str(sname),
                  'storageQuyu':str(quyu)
                  }
        data = {'node':'logic','act_fun':'findSuppliers', 'data':wheres}
        self.thread = getDataThread(data,0,"showData")
        self.connect(self.thread,SIGNAL("showData"),self.showSuppliersInTable)
        self.thread.start()
            
    #列表显示供应商信息
    def showSuppliersInTable(self,data):
        try:
            if data['state'] != True:
                self.boxWarning(u'提示',data['msg'])
                return
            suppliers = data['data']
            counts = len(suppliers)
            self.suppliersTable.setRowCount(counts)
            for row in range(0, counts):
                supplier = suppliers[row]
                if supplier['stat'] == 1:
                    self.userState = u'正常'
                elif supplier['stat'] == 2:
                    self.userState = u'冻结'
                else :
                    self.userState = u'注销'
                
                id = QTableWidgetItem(self.tr(str(supplier['id'])))
                id.setTextAlignment(Qt.AlignCenter|Qt.AlignVCenter)
                id.setFlags(Qt.ItemIsEnabled)
                self.suppliersTable.setItem(row, 0, id)
                
                membername = QTableWidgetItem(self.tr(str(supplier['membername'].decode('utf8'))))
                membername.setTextAlignment(Qt.AlignCenter|Qt.AlignVCenter)
                membername.setFlags(Qt.ItemIsEnabled)
                self.suppliersTable.setItem(row, 1, membername)
                
                name = QTableWidgetItem(self.tr(str(supplier['name'].decode('utf8'))))
                name.setFlags(Qt.ItemIsEnabled)
                self.suppliersTable.setItem(row, 2, name)
                
                quyu = QTableWidgetItem(self.tr(str(supplier['q.name'].decode('utf8'))))
                quyu.setTextAlignment(Qt.AlignCenter|Qt.AlignVCenter)
                quyu.setFlags(Qt.ItemIsEnabled)
                self.suppliersTable.setItem(row, 3, quyu) 
                
                haoshu = QTableWidgetItem(self.tr(str(supplier['h.name'])))
                haoshu.setTextAlignment(Qt.AlignCenter|Qt.AlignVCenter)
                haoshu.setFlags(Qt.ItemIsEnabled)
                self.suppliersTable.setItem(row, 4, haoshu)
                
                userState = QTableWidgetItem(self.tr(str(self.userState)))
                userState.setTextAlignment(Qt.AlignCenter|Qt.AlignVCenter)
                userState.setFlags(Qt.ItemIsEnabled)
                self.suppliersTable.setItem(row, 5, userState)
                
        except:
            self.boxWarning(u'提示', u'系统错误，请联系技术人员。')