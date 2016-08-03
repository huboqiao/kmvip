# -*- coding: utf-8 -*-
'''
Created on 2015年2月7日

@author: LiuXinwu
仓库类型列表控制器
'''
from PyQt4 import QtGui
from application.lib.Commethods import *
from application.view.storagetypelist import Ui_Dialog
from application.model.storagemodel import StorageModel
from application.controller.storagetypeadd import StorageTypeAddController
from application.controller.storagetypealter import StorageTypeAlterController
from application.lib.commodel import getDataThread

class StorageTypeListController(ControllerAction,Ui_Dialog):
    def __init__(self,parent=None):
        ControllerAction.__init__(self,parent)
        self.parent = parent
        self.model = StorageModel()
        self.pushButton_2.setEnabled(False)
        self.pushButton_3.setEnabled(False)
        self.init()
        #绑定事件
        self.connect(self.tableWidget, SIGNAL("itemClicked (QTableWidgetItem*)"), self.outSelect)
        self.connect(self.pushButton,SIGNAL('clicked()'),self.addType)
        self.connect(self.pushButton_2,SIGNAL('clicked()'),self.alterType)
        self.connect(self.tableWidget,SIGNAL(' cellDoubleClicked (int,int)'),self.alterType)
        self.connect(self.pushButton_3,SIGNAL('clicked()'),self.delType)
    
    #选择某单元格
    def outSelect(self,itme=None):
        self.pushButton_2.setEnabled(True)
        self.pushButton_3.setEnabled(True)
        self.id=self.tableWidget.item(itme.row(),0).text()
        self.name=self.tableWidget.item(itme.row(),1).text()
        self.statname=self.tableWidget.item(itme.row(),2).text()
    
    #修改仓库类型
    def alterType(self):
        win = StorageTypeAlterController(self)
        win.exec_()
    
    #删除类型
    def delType(self):
        if self.boxConfirm(u'确认框', u'您是否确定删除%s'%self.name):
            re = self.model.deleteStorageType({'id':str(self.id)})
            self.boxInfo(u'提示',re['msg'])
            #更新列表
            self.init()
            
            
    def init(self):
        #查询所有仓库类型数据
        data = {'node':'logic','act_fun':'findAllStorageType','data':''}   
        self.modell = getDataThread(data,0,"findAllStorageType")
        self.connect(self.modell,SIGNAL("findAllStorageType"),self.dealAllType)
        self.modell.start()
        
    def dealAllType(self,data):
        data = data
        if data['stat']:
            self.tableWidget.setRowCount(0)
            for i in data['data']:
                self.updateTable(i)
        else:
            self.boxInfo(u'提示',data['msg'])
    
    def updateTable(self,data):
        counts = int(self.tableWidget.rowCount()) 
        self.tableWidget.setRowCount(counts+1)
        
        id = QTableWidgetItem(self.tr(str(data['id'])))
        id.setTextAlignment(Qt.AlignCenter)
        id.setFlags(Qt.ItemIsEnabled)
        self.tableWidget.setItem(counts,0,id)
        
        name = QTableWidgetItem(self.tr(str(data['name'])))
        name.setFlags(Qt.ItemIsEnabled)
        name.setTextAlignment(Qt.AlignCenter)
        self.tableWidget.setItem(counts,1,name)
        
        if data['stat']==1:
            stat='是'
        else:
            stat='否'
        stat = QTableWidgetItem(self.tr(stat))
        stat.setTextAlignment(Qt.AlignCenter)
        stat.setFlags(Qt.ItemIsEnabled)
        self.tableWidget.setItem(counts,2,stat)
    
        cdate=time.localtime(int(data['cdate']))
        try:
            cdate=time.strftime('%Y-%m-%d %H:%M:%S',cdate)
            cdate = QTableWidgetItem(self.tr(str(cdate)))
            cdate.setTextAlignment(Qt.AlignCenter)
            cdate.setFlags(Qt.ItemIsEnabled)
            self.tableWidget.setItem(counts,3,cdate)
        except:
            cdate=time.strftime('%Y/%m/%d %H:%M:%S',cdate)
            cdate = QTableWidgetItem(self.tr(str(cdate)))
            cdate.setTextAlignment(Qt.AlignCenter)
            cdate.setFlags(Qt.ItemIsEnabled)
            self.tableWidget.setItem(counts,3,cdate)
    
    
    #添加类型
    def addType(self):
        win = StorageTypeAddController(self)
        win.exec_()