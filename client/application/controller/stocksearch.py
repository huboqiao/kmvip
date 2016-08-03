# -*- coding: utf-8 -*-
'''
Created on 2015年3月9日

@author: LiuXinwu
'''
from PyQt4 import QtGui
from application.lib.Commethods import *
from application.view.searchstock import Ui_Dialog
from application.model.searchstock_model import SearchStockModel
from application.lib.commodel import getDataThread

class StockSearchController(ControllerAction,Ui_Dialog):
    def __init__(self,parent=None):
        ControllerAction.__init__(self,parent)
        self.parent = parent
        
        self.startQuery = True
        
        self.tableWidget.horizontalHeader().setResizeMode(QHeaderView.Stretch)          #铺满表格
        self.tableWidget_2.horizontalHeader().setResizeMode(QHeaderView.Stretch)        #铺满表格
        
        self.connect(self.pushButton,SIGNAL("clicked()"),self.queryCustomer)            #查询客户
        self.connect(self.lineEdit,SIGNAL("returnPressed()"),self.queryCustomer)        #查询客户
        self.connect(self.tableWidget,SIGNAL("cellClicked (int,int)"),self.queryStockById)
        
        self.getCustomer({"membername":""})
        
    def queryCustomer(self):
        membername = unicode(str(self.lineEdit.text()))
        self.getCustomer({'membername':membername})
    
    def getCustomer(self,where):
        if not self.startQuery :
            return
        
        data = {'node':'logic','act_fun':'queryCustomer','data':where}   
        self.modell = getDataThread(data,0,"queryCustomer")
        self.connect(self.modell,SIGNAL("queryCustomer"),self.afterqueryCustomer)
        self.modell.start()
        self.startQuery = False

         
    def afterqueryCustomer(self,data):
        self.startQuery = True
        self.resultIDs = []
        self.tableWidget.setRowCount(0)
        self.label_3.setText("")
        self.tableWidget_2.setRowCount(0)
        if data['stat']:
            #更新表格
            self.updateTable(data['data'])
        else:
            self.boxWarning(u'msg',data['msg'].decode('utf8'))
         
    def updateTable(self,data):
        #如果只有一条记录，查询stock
            
        for v in data:
            self.updateRow(v)
            self.resultIDs.append(v['id']);
        if len(data) == 1:
            self.queryStockById(0,0)
            
    def updateRow(self,data):  
        counts = int(self.tableWidget.rowCount()) 
        self.tableWidget.setRowCount(counts+1)
        
        membername = QTableWidgetItem(self.tr(str(data['membername'])))
        membername.setFlags(Qt.ItemIsEnabled)
        cardid = QTableWidgetItem(self.tr(str(data['cardid'])))
        cardid.setFlags(Qt.ItemIsEnabled)
        
        self.tableWidget.setItem(counts,0,membername)
        self.tableWidget.setItem(counts,1,cardid)
    
    def queryStockById(self,row,column):
        if not self.startQuery :
            return
        customerId = str(self.resultIDs[row])
        name = self.tableWidget.item(row,0).text()
        self.label_3.setText(name)
             
        data = {'node':'logic','act_fun':'queryStockById','data':{"uid":customerId}}   
        self.modell = getDataThread(data,0,"queryStockById")
        self.connect(self.modell,SIGNAL("queryStockById"),self.afterqueryStockById)
        self.modell.start()
        self.startQuery = False
        
        
      
    def afterqueryStockById(self,data):
        self.startQuery = True
        self.tableWidget_2.setRowCount(0)
        if data['stat']:
            self.updateStockTable(data['data'])
        
    def updateStockTable(self,data): 
        for v in data:
            self.updateStockRow(v)
    
    def updateStockRow(self,data):

        counts = int(self.tableWidget_2.rowCount()) 
        self.tableWidget_2.setRowCount(counts+1)
        
        goods_id = QTableWidgetItem(self.tr(str(data['goods_id'])))
        goods_id.setFlags(Qt.ItemIsEnabled)
        goodsname = QTableWidgetItem(self.tr(str(data['pname'])))
        goodsname.setFlags(Qt.ItemIsEnabled)
        goods_numbers = QTableWidgetItem(self.tr(str(data['goods_numbers'])))
        goods_numbers.setFlags(Qt.ItemIsEnabled)
        unit = QTableWidgetItem(self.tr(str(data['unit'])))
        unit.setFlags(Qt.ItemIsEnabled)
        
        self.tableWidget_2.setItem(counts,0,goods_id)
        self.tableWidget_2.setItem(counts,1,goodsname)
        self.tableWidget_2.setItem(counts,2,goods_numbers)
        self.tableWidget_2.setItem(counts,3,unit)
        