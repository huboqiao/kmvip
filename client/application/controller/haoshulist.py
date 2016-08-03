# -*- coding: utf-8 -*-
'''
Created on 2015年2月11日

@author: LiuXinwu
'''
from PyQt4 import QtGui
from application.lib.Commethods import *
from application.view.haoshulist import Ui_Dialog
from application.model.storagemodel import StorageModel
from application.controller.addhaoshu import AddHaoShuController
from application.lib.commodel import getDataThread


class HaoShuListController(ControllerAction,Ui_Dialog):
    def __init__(self,parent=None):
        ControllerAction.__init__(self,parent)
        self.parent = parent
        self.quyuId = self.parent.quyuid
        self.pushButton_2.setEnabled(False)
        #定义数据
        self.haoshuIdList = []
        #实例化model
        self.model = StorageModel()
        self.initData()
        #绑定事件
        self.connect(self.tableWidget, SIGNAL("itemClicked (QTableWidgetItem*)"), self.outSelect)
        self.connect(self.pushButton_2,SIGNAL('clicked()'),self.delHaoShu)
        self.connect(self.pushButton,SIGNAL('clicked()'),self.addHaoShu)
    
    #打开添加号数窗口
    def addHaoShu(self):
        win = AddHaoShuController(self)
        win.exec_()
        
        
    #删除选中的号数
    def delHaoShu(self):
        print self.haoshuid,'号数的id'
        if self.boxConfirm(u'提示',u'您确定要删除号数%s'%self.haoshuname):
            #删除号数数据
            re = self.model.deleteHaoShu({'id':str(self.haoshuid)})
            self.boxInfo(u'提示：',re['msg'])
            self.initData()
        else:
            #什么都不干
            pass
            
        
        
    #选择某单元格
    def outSelect(self,itme=None):
        self.pushButton_2.setEnabled(True)
        self.haoshuid=self.haoshuIdList[itme.row()]
        self.haoshuname = str(self.tableWidget.item(itme.row(),0).text())
    
    #初始化填充表格
    def initData(self):
        data = {'node':'logic','act_fun':'findAllHaoShu','data':{'qid':str(self.quyuId)}}   
        self.modell = getDataThread(data,0,"findAllHaoShu")
        self.connect(self.modell,SIGNAL("findAllHaoShu"),self.dealData)
        self.modell.start()
        
        
    def dealData(self,data):
        if data['stat']:
            #清楚历史数据
            self.haoshuIdList = []
            self.tableWidget.setRowCount(0) 
            for i in data['data']:
                self.haoshuIdList.append(i['id'])
                self.updateTable(i)
        else:
            self.boxWarning(u'警示：',data['msg'])
        
    #更新表格
    def updateTable(self,data):
        counts = int(self.tableWidget.rowCount()) 
        self.tableWidget.setRowCount(counts+1)
        #区域名称
        name = QTableWidgetItem(self.tr(str(data['name'])))
        name.setFlags(Qt.ItemIsEnabled)
        name.setTextAlignment(Qt.AlignCenter|Qt.AlignVCenter)
        self.tableWidget.setItem(counts,0,name)
        
        #启用状态
        if str(data['stat'])=='0':
            stat='未启用'
        else:
            stat='启用'
        stat = QTableWidgetItem(self.tr(stat))
        stat.setFlags(Qt.ItemIsEnabled)
        stat.setTextAlignment(Qt.AlignCenter|Qt.AlignVCenter)
        self.tableWidget.setItem(counts,1,stat)
        
        #创建或修改日期
        cdate=time.localtime(int(data['cdate']))
        try:
            cdate=time.strftime('%Y-%m-%d ',cdate)
            cdate = QTableWidgetItem(self.tr(str(cdate)))
            cdate.setFlags(Qt.ItemIsEnabled)
            cdate.setTextAlignment(Qt.AlignCenter|Qt.AlignVCenter)
            self.tableWidget.setItem(counts,2,cdate)
        except:
            cdate=time.strftime('%Y/%m/%d ',cdate)
            cdate = QTableWidgetItem(self.tr(str(cdate)))
            cdate.setFlags(Qt.ItemIsEnabled)
            cdate.setTextAlignment(Qt.AlignCenter|Qt.AlignVCenter)
            self.tableWidget.setItem(counts,2,cdate)
    
        
        
        