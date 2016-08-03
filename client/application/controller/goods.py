# -*- coding: utf-8 -*-
'''
Created on 2015年2月5日

@author: LiuXinwu
商品资料控制器
操控类别及类别下的商品
'''
from PyQt4 import QtGui
from application.lib.Commethods import *
from application.view.goodsliuliu import Ui_Dialog
from application.controller.goodclass import GoodClassController
from application.controller.goodeditclass import GoodClassEditController
from application.controller.addgoods import  AddGoodsController
from application.controller.editgoods import  EditGoodsController
from application.model.goods_model import GoodsModel
from application.lib.commodel import getDataThread

class GoodsController(ControllerAction,Ui_Dialog):
    def __init__(self,parent=None):
        ControllerAction.__init__(self,parent)
        self.parent=parent
        
        self.startQuery = True
        
        self.treeItemIndex = QTreeWidgetItem(self.treeWidget)
        self.treeItemIndex.setText(0,u'顶级分类')
        self.treeItemIndex.setData(0,1,str(0))
        self.initClass()
        
        
        self.connect(self.treeWidget, SIGNAL('itemClicked(QTreeWidgetItem*, int)'), self.onClick) 
        self.tableWidget.horizontalHeader().setResizeMode(QHeaderView.Stretch)      #铺满表格
        
        
        self.connect(self.pushButton, SIGNAL("clicked()"),self.addGoodsClass)       #添加分类
        self.connect(self.pushButton_6, SIGNAL("clicked()"),self.editGoodsClass)    #修改分类
        self.connect(self.pushButton_3, SIGNAL("clicked()"),self.delGoodsClass)     #删除分类
        self.connect(self.pushButton_2, SIGNAL("clicked()"),self.addGoods)          #添加商品
        self.connect(self.pushButton_4, SIGNAL("clicked()"),self.editGoods)         #修改商品
        self.connect(self.pushButton_5, SIGNAL("clicked()"),self.delGoods)          #删除商品
        self.connect(self.tableWidget, SIGNAL("itemClicked (QTableWidgetItem*)"), self.outSelect)
    
    #添加商品
    def addGoods(self):
        win = AddGoodsController(self)
        win.exec_()
        
    #修改商品
    def editGoods(self):
        if self.id:
            win = EditGoodsController(self)
            win.exec_()
        else:
            self.boxWarning(u'提示',u'请选择要修改的商品！')
    #删除商品
    def delGoods(self):
        if self.id:
            button=QMessageBox.question(self,"Question",  
                                    self.tr("确定要删除商品："+str(self.pname)+"?"),  
                                    QMessageBox.Ok|QMessageBox.Cancel,  
                                    QMessageBox.Ok)  
            if button==QMessageBox.Ok:
                try:
                    re = self.goodsmodel.delGoods({'gid':str(self.id)})
                    self.delGoodsInfo(re)
                    pass
                except:
                    self.boxWarning(u'提示', u'连接服务器超时，请重新登录！')
         
    #删除商品结果
    def delGoodsInfo(self,data):
        if data['stat'] == True:
            self.boxInfo(u'提示',data['msg'])
            try:
                self.queryClassGoods(str(self.ClassParentid))
                            
            except:
                self.boxWarning(u'提示', u'连接服务器超时，请重新登录！')
        else:
            self.boxWarning(u'提示',data['msg'])
     
    def queryClassGoods(self,parentid): 
        if not self.startQuery:
            return    
        data = {'node':'logic','act_fun':'queryClassGoods','data':{'parentid':parentid}}
        self.modell = getDataThread(data,0,"queryClassGoods")
        self.connect(self.modell,SIGNAL("queryClassGoods"),self.updateClassGoods)
        self.modell.start()
        self.startQuery = False  
                
                
    def updateClassGoods(self,re):
        self.startQuery = True  
        if re['stat'] == 1:
            self.classGoodsList(re['data'])
                
                        
    #添加分类
    def addGoodsClass(self):
        self.select_type=0
        win = GoodClassController(self)
        win.exec_()
        
    #修改商品分类
    def editGoodsClass(self):
        try:
            if str(self.ClassParentid)=='0':
                self.boxWarning(u'提示',u'顶级分类不能修改！')
            else:
                win = GoodClassEditController(self)
                win.exec_()
        except:
            self.boxWarning(u'提示',u'请选择要修改的商品分类！')
    
    #删除商品分类
    def delGoodsClass(self):
        try:
            if str(self.ClassParentid)=='0':
                self.boxWarning(u'提示',u'顶级分类不能删除！')
            else:
                button=QMessageBox.question(self,"Question",  
                                    self.tr("确定要删除："+str(self.className)+"分类?"),  
                                    QMessageBox.Ok|QMessageBox.Cancel,  
                                    QMessageBox.Ok)  
                if button==QMessageBox.Ok:
                    try:
                        data={}
                        data['cid'] = self.ClassParentid
                        re = self.goodsmodel.delClass(data)
                        self.delClassInfo(re)
                    except:
                        self.boxWarning(u'提示', u'连接服务器超时，请重新登录！')
        except:
            self.boxWarning(u'提示',u'请选择要删除的商品分类！')
        
    def delClass(self):     
        pass
        
    #删除商品分类的结果
    def delClassInfo(self,data):
        
        
        if data['stat'] == 1:
            self.pushButton_4.setEnabled(False)
            self.pushButton_5.setEnabled(False)
            self.tableWidget.setRowCount(0) 
            self.treeItemIndex.takeChildren()  #删除treeItemIndex下的所有节点
            self.boxInfo(u'提示',data['msg'])
            self.initClass()
        else:
            self.boxWarning(u'提示',data['msg'])
        
    
    
    #向服务器发出获取所有的商品分类
    def initClass(self):
        
        self.goodsmodel = GoodsModel()
        re = self.goodsmodel.getAllClass()
        if re['stat'] ==1:
            self.getGoodsClassAll(re['data'])
                
    #接收服务器返回来的所有商品分类
    def getGoodsClassAll(self,data):
        self.pushButton_3.setEnabled(False)
        self.pushButton_6.setEnabled(False)
        if data:
            self.resource=data
            self.ShowResource()  
            self.treeWidget.expandAll()
            
    #获取蔬菜分类id   
    def onClick(self,item,column):  
        self.pushButton_3.setEnabled(True)
        self.pushButton_6.setEnabled(True)
        
        if str(item.data(0,1).toString())!='0':
            self.Paretid=item.parent().data(0,1).toString()
        self.ClassParentid=str(item.data(0,1).toString())
        self.className=str(item.text(0))
        if str(self.ClassParentid)!='0':
            self.tableWidget.setRowCount(0)
            try:
                self.queryClassGoods(str(self.ClassParentid))
            except Exception,e:
                print 'e=',e
                self.boxWarning(u'提示', u'连接服务器超时，请重新登录！')
                
                
    #商品分类下的商品
    def classGoodsList(self,data):
        self.tableWidget.setRowCount(0)
        self.pushButton_4.setEnabled(False)
        self.pushButton_5.setEnabled(False)
        
        if data:
            for i in range(len(data)):
                self.updateTable(data[i])
                
    #更新表格
    def updateTable(self,data):
        counts = int(self.tableWidget.rowCount()) 
        self.tableWidget.setRowCount(counts+1)
        
        id = QTableWidgetItem(self.tr(str(data['id'])))
        id.setTextAlignment(Qt.AlignCenter|Qt.AlignVCenter)
        id.setFlags(Qt.ItemIsEnabled)
        pname = QTableWidgetItem(self.tr(str(data['pname'])))
        pname.setFlags(Qt.ItemIsEnabled)
        for i in range(len(self.resource)):
            if str(data['pclass'])==str(self.resource[i]['id']):
                pclassname=str(self.resource[i]['name'])
                self.classType=self.resource[i]['v_type']
        self.pclass=data['pclass']
        pclass = QTableWidgetItem(self.tr(str(pclassname)))
        pclass.setTextAlignment(Qt.AlignCenter|Qt.AlignVCenter)
        pclass.setFlags(Qt.ItemIsEnabled)
        unit = QTableWidgetItem(self.tr(str(data['unit'])))
        unit.setTextAlignment(Qt.AlignCenter|Qt.AlignVCenter)
        unit.setFlags(Qt.ItemIsEnabled)
        
        goodssn = QTableWidgetItem(self.tr(str(data['goodssn'])))
        goodssn.setFlags(Qt.ItemIsEnabled)
        self.tableWidget.setItem(counts,0,id)
        self.tableWidget.setItem(counts,1,pname)
        self.tableWidget.setItem(counts,2,pclass)
        self.tableWidget.setItem(counts,3,unit)
        self.tableWidget.setItem(counts,4,goodssn)

    #选择某单元格
    def outSelect(self,itme=None):
        self.pushButton_4.setEnabled(True)
        self.pushButton_5.setEnabled(True)
        self.id=self.tableWidget.item(itme.row(),0).text()
        self.pname=self.tableWidget.item(itme.row(),1).text()
        self.clsname=self.tableWidget.item(itme.row(),2).text()
        self.unit=self.tableWidget.item(itme.row(),3).text()
        self.ssn=self.tableWidget.item(itme.row(),4).text()
            
            
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