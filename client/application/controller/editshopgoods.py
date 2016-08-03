# -*- coding: utf-8 -*-
'''
Created on 2015年3月18日

@author: kylin
修改商城商品控制器
'''
from PyQt4 import QtGui
from application.lib.Commethods import *
from application.view.shopgoodsalterliu import Ui_Dialog
from application.model.shopgoods_model import GoodsModel
from application.lib.commodel import getDataThread

class EditGoodsController(ControllerAction,Ui_Dialog):
    def __init__(self,parent=None):
        ControllerAction.__init__(self,parent)
        self.parent=parent
        
        self.startQuery = True
        
        self.treeItemIndex = QTreeWidgetItem(self.treeWidget)
        self.treeItemIndex.setText(0,u'商品分类')
        self.init()
        #绑定事件
        self.connect(self.treeWidget, SIGNAL('itemClicked(QTreeWidgetItem*, int)'), self.onClick) 
        self.connect(self.pushButton, SIGNAL("clicked()"),self.editGoods)
        self.connect(self.pushButton_2, SIGNAL("clicked()"),self.winClose)
        #初始化数据
        self.goodsname.setText(self.tr(str(self.parent.pname)))
        self.unit.setText(self.tr(str(self.parent.unit)))
        self.ssn.setText(self.tr(str(self.parent.ssn)))
        self.price.setText(self.tr(str(self.parent.price)))
        self.comboBox_2.setCurrentIndex(self.parent.is_active)
        self.ClassParentid=self.parent.pclass
        
    
    #关闭窗口
    def winClose(self):
        self.close()
    
    #获取商品分类id   
    def onClick(self,item,column):  
        self.ClassParentid=str(item.data(0,1).toString())
        
                
    def getAllParty(self,data):
        self.comboBox.clear()
        self.comboBox.addItem(u"请选择", 0)
        currentIndex = 0
        for i in data:
            if self.parent.pid == i["suppliers_id"]:
                currentIndex = int(i["suppliers_id"])
            self.comboBox.addItem(i['suppliers_name'], i["suppliers_id"])
#         print currentIndex
        self.comboBox.setCurrentIndex(currentIndex)
        
    #提交修改商品
    def editGoods(self):
        name=str(self.goodsname.text())
        unit=str(self.unit.text())
        ssn=str(self.ssn.text()) 
        price = str(self.price.text()).strip()
       
        
        if ssn=="null":
            ssn = ""
        
        if name=='':
            self.boxWarning(u'提示',u'请输入商品名！')
            self.goodsname.setFocus(True)
            return
        if self.ClassParentid=='0':
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
        
        pid = str(self.comboBox.itemData(self.comboBox.currentIndex()).toString())
        is_active = str(self.comboBox_2.currentIndex())
        
        
        if int(pid) <=0:
            self.infoBox(u"请选择供应商")
            self.comboBox.setFocus()
            return
                    
        dataa={'goods_name':name,'cat_id':str(self.ClassParentid),'unit':unit,
               'goods_sn':ssn,"is_active":is_active,"goods_desc":"",
               'goods_price':price,"suppliers_id":pid}
        data={}
        data['data']=dataa
        data['goods_id'] = str(self.parent.id)
#         try:
        print "ddddddddddd"
        re = self.goodsmodel.editGoods(data)
        print re
        self.getClassInfo(re)
#         except:
#             self.boxWarning(u'提示', u'连接服务器超时，请重新登录！')
            
    #接收服务返回添加的状态
    def getClassInfo(self,data):
        if data['stat'] == True:
            self.boxInfo(u'提示',data['msg'])
            try:
                self.msg = data['msg']
                self.queryClassGoods(str(self.ClassParentid))
            except:
                self.boxWarning(u'提示', u'连接服务器超时，请重新登录！！！！')
            self.close()
        else:
            self.boxWarning(u'提示',data['msg'])
            
            
    
    #向服务器发出获取所有的商品分类
    def init(self):
        self.goodsmodel = GoodsModel()
        try:
            re = self.goodsmodel.getAllClass()
            if re['stat'] ==1:
                self.getGoodsClassAll(re['data'])
        except:
            self.boxWarning(u'提示', u'连接服务器超时，请重新登录！！！！！')
        try:
            re = self.goodsmodel.getAllParty()
            if re['stat'] == 1:
                self.getAllParty(re['data'])
        except:
            self.boxWarning(u'提示', u'连接服务器超时，请重新登录！！！！！！')
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
        if data['stat']:
            self.boxInfo(u'提示', data['msg'])
            self.close()
        else:
            self.boxWarning(u'提示',data['msg'])
        
         
    def queryClassGoods(self,parentid):
        if not self.startQuery:
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
            
#         button=QMessageBox.question(self,"Question",  
#                                 self.tr(self.msg),  
#                                 QMessageBox.Ok|QMessageBox.Cancel,  
#                                 QMessageBox.Ok)  
#         if button!=QMessageBox.Ok:
#             self.close()
        else:
            self.goodsname.setText('')
            self.goodsname.setFocus(True)
