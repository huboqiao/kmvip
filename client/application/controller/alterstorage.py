# -*- coding: utf-8 -*-
'''
Created on 2015年1月29日

@author: LiuXinwu
'''
from PyQt4 import QtGui
from application.lib.Commethods import *
from application.view.editstorage import Ui_Dialog
from application.model.storagemodel import StorageModel
from application.controller.addquyu import AddQuYuController
from application.controller.haoshulist import HaoShuListController
from application.controller.alterquyu import AlterQuYuController
from application.lib.commodel import getDataThread

class AlterStorageController(ControllerAction,Ui_Dialog):
    def __init__(self,parent=None):
        ControllerAction.__init__(self,parent)
        self.tableWidget.horizontalHeader().setResizeMode(QHeaderView.Stretch)      #铺满表格
        self.parent = parent
        self.id = self.parent.id
        self.pushButton_2.setEnabled(False)
        self.pushButton_3.setEnabled(False)
        self.pushButton_4.setEnabled(False)
        #实例化model
        self.model = StorageModel()
        self.comboBox.setEditable(False)
        #初始化数据
        self.quyuIdList = []
        self.init()
        #绑定事件
        self.connect(self.lineEdit,SIGNAL('returnPressed ()'),self.editStorage)
        self.connect(self.pushButton_5,SIGNAL('clicked()'),self.editStorage)
        self.connect(self.pushButton,SIGNAL('clicked()'),self.addQuYu)
        self.connect(self.pushButton_2,SIGNAL('clicked()'),self.alterQuYu)
        self.connect(self.pushButton_3,SIGNAL('clicked()'),self.delQuYu)
        self.connect(self.tableWidget, SIGNAL("itemClicked (QTableWidgetItem*)"), self.outSelect)
        self.connect(self.tableWidget, SIGNAL("cellDoubleClicked (int,int)"), self.openHaoShu)
        self.connect(self.pushButton_4, SIGNAL("clicked()"), self.openHaoShu)
        
    #打开区域的号数列表窗口
    def openHaoShu(self):
        win = HaoShuListController(self)
        win.exec_()
    
    #选择某单元格
    def outSelect(self,itme=None):
        self.pushButton_2.setEnabled(True)
        self.pushButton_3.setEnabled(True)
        self.pushButton_4.setEnabled(True)
        self.quyuid=self.quyuIdList[itme.row()]
        self.quyuname=self.tableWidget.item(itme.row(),0).text()
        self.quyustatname=self.tableWidget.item(itme.row(),1).text()
    
    #删除区域 
    def delQuYu(self):
        if self.boxConfirm(u'提示',u'您确定要删除区域%s'%self.quyuname):
            re = self.model.deleteQuYu({'id':str(self.quyuid)})
            self.boxInfo(u'提示：',re['msg'])
            self.init()
        else:
            pass
        
    #打开修改区域界面
    def alterQuYu(self):
        win = AlterQuYuController(self)
        win.exec_()
        
        
    #打开添加区域窗口
    def addQuYu(self):  
        win = AddQuYuController(self)
        win.exec_()
        
    #验证名称是否可行
    def validateName(self):
        namestr = str(self.lineEdit.text())
        name = namestr.strip()
        if self.stoname==name:
            #无意改变名称
            return True
        else:
            #有意改变名称
            if len(name)==0:
                self.boxInfo('提示：',u'仓库名称不能为空！')
                self.lineEdit.setFocus(True)
                return False
            else:
                #不能取已存在的仓库名称
                nameData = self.model.findAllStorageName()
                if nameData['stat']:
                    for i in nameData['data']:
                        if i['name']==name:
                            self.boxInfo(u'提示',u'名称已被占用，请重新输入！')
                            self.lineEdit.clear()
                            self.lineEdit.setFocus(True)
                            return False
            return True
                        
    #修改仓库名称
    def editStorage(self):
        if self.validateName():
            namestr = str(self.lineEdit.text())
            name = namestr.strip()
            stat = self.comboBox.currentIndex()
            if stat == 0:
                stat = 1
            else:
                stat = 0
            #修改仓库基本信息
            re = self.model.updateStorage({'id':str(self.id),'name':str(name),'stat':str(stat)})
            self.boxInfo(u'提示：',re['msg'])
            self.parent.init()
            self.close()
        else:
            #什么都不干
            pass
        
    
    #初始化填充表格
    def init(self):
        #查询仓库基本信息
        storageData = self.model.findOneStorage({'id':str(self.id)})
        self.stoname = storageData['data']['name']
        self.lineEdit.setText(self.tr(str(self.stoname)))
        xx = storageData['data']['stat']
        if xx == 1:
            self.comboBox.setCurrentIndex(0)
        else:
            self.comboBox.setCurrentIndex(1)
            
        
        
        data = {'node':'logic','act_fun':'findAllQuYu','data':{'sid':str(self.id)}}   
        self.modell = getDataThread(data,0,"findAllQuYu")
        self.connect(self.modell,SIGNAL("findAllQuYu"),self.dealQu)
        self.modell.start()
        
    def dealQu(self,data):
        if data['stat']:
            #清楚历史数据
            self.quyuIdList = []
            self.tableWidget.setRowCount(0) 
            for i in data['data']:
                self.quyuIdList.append(i['id'])
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
        if str(data['isactive'])=='0':
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
        
        
        
        