# -*- coding: utf-8 -*-
'''
Created on 2015年3月18日

@author: kylin
修改商城商品类别控制器
'''
from PyQt4 import QtGui
from application.lib.Commethods import *
from application.view.altershopgoodsclassliu import Ui_Dialog
from application.model.shopgoods_model import GoodsModel

class GoodClassEditController(ControllerAction,Ui_Dialog):
    def __init__(self,parent=None):
        ControllerAction.__init__(self,parent)
        self.parent=parent
        
        self.treeItemIndex = QTreeWidgetItem(self.treeWidget)
        self.treeItemIndex.setText(0,u'顶级分类')
        self.treeItemIndex.setData(0,1,str(0))
        self.init()
        #绑定事件
        self.connect(self.treeWidget, SIGNAL('itemClicked(QTreeWidgetItem*, int)'), self.onClick) 
        self.connect(self.pushButton, SIGNAL("clicked()"),self.editClassSubmit)
        self.connect(self.pushButton_2, SIGNAL("clicked()"),self.winClose)
        self.classname.setText(self.tr(str(self.parent.className)))
        self.ClassParentid=self.parent.Paretid
    
    #关闭窗口
    def winClose(self):
        self.close()
        
    #获取上级分类id   
    def onClick(self,item,column):  
        self.ClassParentid=str(item.data(0,1).toString())
        
    #提交修改分类
    def editClassSubmit(self):
        name=str(self.classname.text())
        if name=='':
            self.boxWarning(u'提示',u'请输入商品分类名！')
            return
        try:
            self.ClassParentid
        except:
            self.boxWarning(u'提示',u'请选择父级商品分类')
            return
        if self.ClassParentid=='':
            self.boxWarning(u'提示',u'请选择父级商品分类')
            return
        dataa={'cat_name':name,'parent_id':str(self.ClassParentid)}
        for i in range(len(self.resource)):
            if str(self.resource[i]['cat_id'])!=str(self.parent.ClassParentid):
                if str(self.resource[i]['cat_name'])==str(name):
                    self.boxWarning(u'提示',u'该商品分类已存在！')
                    return
        if str(self.parent.ClassParentid)==str(self.ClassParentid):
            self.boxWarning(u'提示',u'父级分类不能是自己！')
            return
        try:
            data={}
            data['data'] = dataa
            data['cat_id'] = str(self.parent.ClassParentid)
            re = self.goodsmodel.editClass(data)
            self.getClassInfo(re)
        except:
            self.boxWarning(u'提示', u'连接服务器超时，请重新登录！')
                 
            
    #接收服务返回添加的状态
    def getClassInfo(self,data):
        if data['stat'] == 1:
            self.parent.treeItemIndex.takeChildren()  #删除treeItemIndex下的所有节点
            self.parent.pushButton_4.setEnabled(False)
            self.parent.pushButton_5.setEnabled(False)
            self.parent.tableWidget.setRowCount(0) 
            self.parent.initClass()
            self.boxInfo(u'提示',data['msg'])
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
            self.boxWarning(u'提示', u'连接服务器超时，请重新登录！')
     
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
