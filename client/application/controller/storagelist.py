# -*- coding: utf-8 -*-
'''
Created on 2015年1月28日

@author: LiuXinwu
'''
from PyQt4 import QtGui
from application.lib.Commethods import *
from application.view.storagelist import Ui_Dialog
from application.controller.addstorage import AddStorageController
from application.controller.alterstorage import AlterStorageController
from application.model.storagemodel import StorageModel
from application.lib.commodel import getDataThread

import time

class StorageList(ControllerAction,Ui_Dialog):
    def __init__(self,parent=None):
        ControllerAction.__init__(self,parent)
        self.tableWidget.horizontalHeader().setResizeMode(QHeaderView.Stretch)      #铺满表格
        self.parent=parent
        self.startQuery = True
        self.storageModel = StorageModel()
        self.connect(self.pushButton, SIGNAL("clicked()"),self.storageAdd)
        self.connect(self.pushButton_2, SIGNAL("clicked()"),self.storageEdit)
        self.connect(self.pushButton_3, SIGNAL("clicked()"),self.storageDel)
        self.connect(self.tableWidget, SIGNAL("itemClicked (QTableWidgetItem*)"), self.outSelect)
        self.connect(self.tableWidget, SIGNAL("cellDoubleClicked(int,int)"), self.storageEdit)
        self.init()
    
    #初始化数据
    def init(self):
        
        if not self.startQuery:
            return
        try:
            data = {'node':'logic','act_fun':'findAllStorage','data':''}   
            self.modell = getDataThread(data,0,"findAllStorage")
            self.connect(self.modell,SIGNAL("findAllStorage"),self.queryStore)
            self.modell.start()
            self.startQuery = False
        except:
            self.boxWarning(u'提示', u'连接服务器超时，请重新登录！')
            
    def queryStore(self,re):
        re = re
        self.startQuery = True
        if re['stat'] ==1:
            self.storeInfo(re['data'])
        else:
            self.tableWidget.setRowCount(0)#清除数据
            self.boxInfo(u'提示',u'没有仓库信息，请添加！')
            
    #接收到所有的冷库信息
    def storeInfo(self,data):
        self.tableWidget.setRowCount(0) 
        self.pushButton_2.setEnabled(False) #修改按钮
        self.pushButton_3.setEnabled(False) #删除按钮
        if data:
            for i in range(len(data)):
                self.updateTable(data[i])
            
    #更新表格
    def updateTable(self,data):
        counts = int(self.tableWidget.rowCount()) 
        self.tableWidget.setRowCount(counts+1)
        id = QTableWidgetItem(self.tr(str(data['id'])))
        id.setTextAlignment(Qt.AlignCenter)
        id.setFlags(Qt.ItemIsEnabled)
        name = QTableWidgetItem(self.tr(str(data['name'])))
        name.setFlags(Qt.ItemIsEnabled)
        name.setTextAlignment(Qt.AlignCenter)
        try:
            cdate=time.localtime(int(data['cdate']))
            cdate=time.strftime('%Y-%m-%d ',cdate)
            cdate = QTableWidgetItem(self.tr(str(cdate)))
            cdate.setFlags(Qt.ItemIsEnabled)
        except:
            cdate=time.localtime(int(data['cdate']))
            cdate=time.strftime('%Y/%m/%d ',cdate)
            cdate = QTableWidgetItem(self.tr(str(cdate)))
            cdate.setFlags(Qt.ItemIsEnabled)
        
        cdate.setTextAlignment(Qt.AlignCenter)
        if str(data['stat'])=='0':
            stat='未启用'
        else:
            stat='启用'
        stat = QTableWidgetItem(self.tr(stat))
        stat.setTextAlignment(Qt.AlignCenter|Qt.AlignVCenter)
        stat.setFlags(Qt.ItemIsEnabled)
        self.tableWidget.setItem(counts,0,id)
        self.tableWidget.setItem(counts,1,name)
        self.tableWidget.setItem(counts,2,cdate)
        self.tableWidget.setItem(counts,3,stat)
    
    #选择某单元格
    def outSelect(self,itme=None):
        self.id=self.tableWidget.item(itme.row(),0).text()
        self.name=self.tableWidget.item(itme.row(),1).text()
        self.statname=self.tableWidget.item(itme.row(),3).text()
        self.pushButton_2.setEnabled(True)
        self.pushButton_3.setEnabled(True)
            
        
    #添加冷库
    def storageAdd(self):
        win=AddStorageController(self)
        win.exec_()
        
    #修改冷库
    def storageEdit(self):
        win=AlterStorageController(self)
        win.exec_()
        
    #删除冷库
    def storageDel(self):
        if self.boxConfirm(u'提示',u'您确定要删除仓库%s'%self.name):
            try:
                re = self.storageModel.deleteStorage({'id':str(self.id)})
                self.delInfo(re)
            except:
                self.boxWarning(u'提示', u'连接服务器超时，请重新登录！')
        else:
            pass
              
    #删除结果信息
    def delInfo(self,data):
        self.init()
        if data['stat']:
            self.boxInfo(u'提示',u'删除冷库成功！')
        else:
            self.boxInfo(u'提示',data['msg'])
    

    
 