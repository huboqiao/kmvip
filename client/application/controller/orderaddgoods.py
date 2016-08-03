# -*- coding: utf-8 -*-
'''
Created on 2015年2月6日

@author: LiuXinwu

'''
from PyQt4 import QtGui,QtCore
from application.lib.Commethods import *
from application.view.orderaddgoods import Ui_Dialog
from application.model.orderAddModel import OrderAddModel
from application.lib.commodel import getDataThread

class OrderAddGoodsController(ControllerAction,Ui_Dialog):
    def __init__(self,parent=None):
        
        ControllerAction.__init__(self,parent)
        self.parent=parent
        
        self.treeItemIndex = QTreeWidgetItem(self.treeWidget)
        self.treeItemIndex.setText(0,u'顶级分类')
        self.treeItemIndex.setData(0,1,str(0))
        self.initClass()
                
        self.connect(self.treeWidget, SIGNAL('itemClicked(QTreeWidgetItem*, int)'), self.onClick) 
        self.tableWidget.horizontalHeader().setResizeMode(QHeaderView.Stretch)      #铺满表格
        
        self.connect(self.tableWidget, SIGNAL("itemDoubleClicked (QTableWidgetItem*)"), self.outSelect)
        self.connect(self.pushButton, SIGNAL('clicked()'), self.addEnd)
    
    def addEnd(self):
        self.close()

    #向服务器发出获取所有的商品分类
    def initClass(self):
        
        self.goodsmodel = OrderAddModel()
        re = self.goodsmodel.getAllClass()
        if re['stat'] ==1:
            self.getGoodsClassAll(re['data'])
                
    #接收服务器返回来的所有商品分类
    def getGoodsClassAll(self,data):
        if data:
            self.resource=data
            self.ShowResource()  
            self.treeWidget.expandAll()
            
    #获取蔬菜分类id   
    def onClick(self,item,column):  
        print item 
        if str(item.data(0,1).toString())!='0':
            self.Paretid=item.parent().data(0,1).toString()
        self.ClassParentid=str(item.data(0,1).toString())
        self.className=str(item.text(0))
        if str(self.ClassParentid)!='0':
            try:
                data = {'node':'logic','act_fun':'queryClassGoodss','data':{'parentid':str(self.ClassParentid)}}   
                self.record = getDataThread(data,0,"queryClassGoodss")
                self.connect(self.record,SIGNAL("queryClassGoodss"),self.cardRecord)
                self.record.start() 
                
            except:
                self.boxWarning(u'提示', u'连接服务器超时，请重新登录！')
    def cardRecord(self,data):
        if data['stat'] == 1:
            self.classGoodsList(data['data'])
    #商品分类下的商品
    def classGoodsList(self,data):
        self.tableWidget.setRowCount(0)
        if data:
            for i in range(len(data)):
                self.updateTable(data[i])
                
    #更新表格
    def updateTable(self,data):
        counts = int(self.tableWidget.rowCount()) 
        self.tableWidget.setRowCount(counts+1)
        
        id = QTableWidgetItem(self.tr(str(data['id'])))
        id.setFlags(Qt.ItemIsEnabled)
        pname = QTableWidgetItem(self.tr(str(data['pname'])))
        pname.setFlags(Qt.ItemIsEnabled)
        for i in range(len(self.resource)):
            if str(data['pclass'])==str(self.resource[i]['id']):
                pclassname=str(self.resource[i]['name'])
                self.classType=self.resource[i]['v_type']
        self.pclass=data['pclass']
        pclass = QTableWidgetItem(self.tr(str(pclassname)))
        pclass.setFlags(Qt.ItemIsEnabled)
        unit = QTableWidgetItem(self.tr(str(data['unit'])))
        unit.setFlags(Qt.ItemIsEnabled)
        
        goodssn = QTableWidgetItem(self.tr(str(data['goodssn'])))
        goodssn.setFlags(Qt.ItemIsEnabled)
        self.tableWidget.setItem(counts,0,id)
        self.tableWidget.setItem(counts,1,pname)
        self.tableWidget.setItem(counts,2,pclass)
        self.tableWidget.setItem(counts,3,unit)
        self.tableWidget.setItem(counts,4,goodssn)

    #双击某单元格
    def outSelect(self,item=None):
        self.id=self.tableWidget.item(item.row(),0).text()
#        self.id=unicode(self.tableWidget.item(item.row(),0).text().toUtf8(),'utf-8','ignore')
        self.pname=self.tableWidget.item(item.row(),1).text()
        self.clsname=self.tableWidget.item(item.row(),2).text()
        self.unit=self.tableWidget.item(item.row(),3).text()
#        self.pname=self.tableWidget.item(item.row(),1).text()
#        self.clsname=self.tableWidget.item(item.row(),2).text()
#        self.unit=self.tableWidget.item(item.row(),3).text()
#        self.parent.addAGoods([self.clsname, self.pname, self.unit, self.id])
        self.parent.addAGoods(self.pname, self.unit, self.id)
        
            
    #显示所有资源
    def ShowResource(self):
        for i in range(len(self.resource)):
            if self.resource[i]['v_type']==0:
                if str(self.resource[i]['parentid'])=='0':
                    self.treeItem='treeItem'+str(i)
                    self.treeItem= QTreeWidgetItem(self.treeItemIndex)
                    self.treeItem.setText(0,self.tr(str(self.resource[i]['name'])))
                    self.treeItem.setData(0,1,str(self.resource[i]['id']))
                    self.getChild(self.treeItem,self.resource[i]['id'])
                
    
    def getChild(self,dqtreeItem,id):
        for i in range(len(self.resource)):
            if self.resource[i]['v_type']==0:
                if self.resource[i]['parentid']==id:
                    self.treeItem='treeItem'+str(id)+'_'+str(i)
                    self.treeItem= QTreeWidgetItem(dqtreeItem)
                    self.treeItem.setText(0,self.tr(str(self.resource[i]['name'])))
                    self.treeItem.setData(0,1,str(self.resource[i]['id']))
                    self.getChild(self.treeItem,self.resource[i]['id'])