# -*- coding: utf-8 -*-
'''
Created on 2015年2月6日

@author: LiuXinwu
修改商品控制器
'''
from PyQt4 import QtGui
from application.lib.Commethods import *
from application.view.goodsalterliu import Ui_Dialog
from application.model.goods_model import GoodsModel
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
        self.ClassParentid=self.parent.pclass
        
    
    #关闭窗口
    def winClose(self):
        self.close()
    
    #获取商品分类id   
    def onClick(self,item,column):  
        self.ClassParentid=str(item.data(0,1).toString())
        
        
    #提交修改商品
    def editGoods(self):
        name=str(self.goodsname.text())
        unit=str(self.unit.text())
        ssn=str(self.ssn.text())
        
        if ssn=="null":
            ssn = ""
        
        if name=='':
            self.boxWarning(u'提示',u'请输入商品名！')
            self.goodsname.setFocus(True)
            return
        if self.ClassParentid=='0':
            self.boxWarning(u'提示',u'请选择商品分类')
            return
        dataa={'pname':name,'pclass':str(self.ClassParentid),'unit':unit,'goodssn':ssn}
        data={}
        data['data']=dataa
        data['gid'] = str(self.parent.id)
        data['muid'] = str(self.appdata['user']['user_id'])
        try:
            re = self.goodsmodel.editGoods(data)
            self.getClassInfo(re)
        except:
            self.boxWarning(u'提示', u'连接服务器超时，请重新登录！')
            
    #接收服务返回添加的状态
    def getClassInfo(self,data):
        if data['stat'] == True:
            self.boxInfo(u'提示',data['msg'])
            try:
                self.msg = data['msg']
                self.queryClassGoods(str(self.ClassParentid))
            except:
                self.boxWarning(u'提示', u'连接服务器超时，请重新登录！')
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
            if str(self.resource[i]['v_type'])=='0':
                if str(self.resource[i]['parentid'])=='0':
                    self.treeItem='treeItem'+str(i)
                    self.treeItem= QTreeWidgetItem(self.treeItemIndex)
                    self.treeItem.setText(0,self.tr(str(self.resource[i]['name'])))
                    self.treeItem.setData(0,1,str(self.resource[i]['id']))
                    self.getChild(self.treeItem,self.resource[i]['id'])
                
    
    def getChild(self,dqtreeItem,id):
        for i in range(len(self.resource)):
            if str(self.resource[i]['v_type'])=='0':
                if self.resource[i]['parentid']==id:
                    self.treeItem='treeItem'+str(id)+'_'+str(i)
                    self.treeItem= QTreeWidgetItem(dqtreeItem)
                    self.treeItem.setText(0,self.tr(str(self.resource[i]['name'])))
                    self.treeItem.setData(0,1,str(self.resource[i]['id']))
                    self.getChild(self.treeItem,self.resource[i]['id'])
                
    def getGoodsInfo(self,data):
        if data['stat']:
            self.boxInfo(u'提示', data['msg'])
            self.close()
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