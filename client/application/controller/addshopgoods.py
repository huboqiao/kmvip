# -*- coding: utf-8 -*-
'''
Created on 2015年3月18日

@author: kylin
添加类的商城商品控制器
'''
from PyQt4 import QtGui
from application.lib.Commethods import *
from application.view.shopgoodsaddliu import Ui_Dialog
from application.model.shopgoods_model import GoodsModel
from application.lib.commodel import getDataThread
# from distutils.tests.setuptools_build_ext import if_dl

class AddGoodsController(ControllerAction,Ui_Dialog):
    def __init__(self,parent=None):
        ControllerAction.__init__(self,parent)
        self.parent=parent
        #查询标志
        self.startQuery = True
        #初始化treeWidget里数据
        self.treeItemIndex = QTreeWidgetItem(self.treeWidget)
        self.treeItemIndex.setText(0,u'商品分类')
        self.init()
        #绑定事件
        self.connect(self.treeWidget, SIGNAL('itemClicked(QTreeWidgetItem*, int)'), self.onClick) 
        self.connect(self.pushButton, SIGNAL("clicked()"),self.addGoods)
        self.connect(self.pushButton_2, SIGNAL("clicked()"),self.winClose)
       
    
    #关闭窗口
    def winClose(self):
        self.close()
    
    
    #获取商品分类id   
    def onClick(self,item,column):  
        self.ClassParentid=str(item.data(0,1).toString())
        self.parent.ClassParentid=self.ClassParentid
        
        
    #提交添加商品
    def addGoods(self):
        name=str(self.goodsname.text())
        unit=str(self.unit.text())
        ssn=str(self.ssn.text())
        price = str(self.price.text()).strip()
       
        if name=='':
            self.boxWarning(u'提示',u'请输入商品名！')
            self.goodsname.setFocus()
            return
        try:
            self.ClassParentid
        except:
            self.boxWarning(u'提示',u'请选择商品分类')
            return
        if self.ClassParentid=='':
            self.boxWarning(u'提示',u'请选择商品分类')
            return
        try:
            float(price)
        except:
            self.infoBox(u"请输入正确价格")
            self.price.setFocus()
            return
        if float(price) <= 0:
            self.infoBox(u"请输入正确价格")
            self.price.setFocus()
            return
        try:
            pid = str(self.comboBox.itemData(self.comboBox.currentIndex()).toString())
            
            if int(pid) <=0:
                self.infoBox(u"请选择供应商")
                self.comboBox.setFocus()
                return
        except:
            
            self.infoBox(u"请选择供应商")
            self.comboBox.setFocus()
            return
                    
        is_active = str(self.comboBox_2.currentIndex())
    
    
        data={'goods_name':name,'cat_id':str(self.ClassParentid),
              'unit':unit,'goods_sn':ssn,
              'goods_price':price,'suppliers_id':pid,
              'is_active':is_active,"goods_desc" : ""
              }
        print data
        try:
            re = self.goodsmodel.addGoods(data)       
            self.getGoodsInfo(re)
        except:
            self.boxWarning(u'提示', u'连接服务器超时，请重新登录！')
            
    #向服务器发出获取所有的商品分类及供应商
    def init(self):
    
        self.goodsmodel = GoodsModel()
        try:
            re = self.goodsmodel.getAllClass()
            if re['stat'] == 1:
                self.getGoodsClassAll(re['data'])
        except:
            self.boxWarning(u'提示', u'连接服务器超时，请重新登录！')
        try:
            re = self.goodsmodel.getAllParty()
            if re['stat'] == 1:
                self.getAllParty(re['data'])
        except:
            self.boxWarning(u'提示', u'连接服务器超时，请重新登录！')
            
    def getAllParty(self,data):
        self.comboBox.clear()
        self.comboBox.addItem(u"请选择", 0)
        for i in data:
            self.comboBox.addItem(i['suppliers_name'], i["suppliers_id"])
    #接收服务器返回来的所有商品分类
    def getGoodsClassAll(self,data):
        if data:
            self.resource=data
            self.ShowResource()  
            self.treeWidget.expandAll()
            
    #显示所有资源
    def ShowResource(self):
        for i in range(len(self.resource)):
            if str(self.resource[i]['parent_id'])=='0':
                self.treeItem='treeItem'+str(i)
                self.treeItem= QTreeWidgetItem(self.treeItemIndex)
                self.treeItem.setText(0,self.tr(str(self.resource[i]['cat_name'])))
                self.treeItem.setData(0,1,str(self.resource[i]['cat_id']))
                self.getChild(self.treeItem,self.resource[i]['cat_id'])
                
    
    def getChild(self,dqtreeItem,id):
        for i in range(len(self.resource)):
            if self.resource[i]['parent_id']==id:
                self.treeItem='treeItem'+str(id)+'_'+str(i)
                self.treeItem= QTreeWidgetItem(dqtreeItem)
                self.treeItem.setText(0,self.tr(str(self.resource[i]['cat_name'])))
                self.treeItem.setData(0,1,str(self.resource[i]['cat_id']))
                self.getChild(self.treeItem,self.resource[i]['cat_id'])
                
    def getGoodsInfo(self,data):
        if data['stat'] == 1:
            try:
                self.msg = data['msg']
                self.queryClassGoods(str(self.ClassParentid))
            except:
                self.boxWarning(u'提示', u'连接服务器超时，请重新登录！')
            
        else:
            self.boxWarning(u'提示',data['msg'])
            
         
    def queryClassGoods(self,parentid):
        
        if not self.startQuery :
            return
        
        data = {'node':'logic','act_fun':'queryShopClassGoods','data':{'cat_id':parentid}}
        self.modell = getDataThread(data,0,"queryShopClassGoods")
        self.connect(self.modell,SIGNAL("queryShopClassGoods"),self.updateClassGoods)
        self.modell.start()
        self.startQuery = False
        
        
    def updateClassGoods(self,re):
        self.startQuery = True
        if re['stat'] == 1:
            self.parent.classGoodsList(re['data'])
            
        button=QMessageBox.question(self,"Question",  
                                self.tr(self.msg),  
                                QMessageBox.Ok|QMessageBox.Cancel,  
                                QMessageBox.Ok)  
        if button!=QMessageBox.Ok:
            self.close()
        else:
            self.goodsname.setText('')
            self.price.setText('')
            self.unit.setText('')
            self.ssn.setText('')
            self.goodsname.setFocus(True)
            self.comboBox.setCurrentIndex(0)
            self.comboBox_2.setCurrentIndex(0)