# -*- coding: utf-8 -*-
'''
Created on 2015年3月2日

@author: LiuXinwu
'''
from PyQt4 import QtGui
from application.lib.Commethods import *
from application.view.group import Ui_Dialog
from application.model.grouplist_model import GroupListModel

class GroupAddController(ControllerAction,Ui_Dialog):
    def __init__(self,parent=None):
        ControllerAction.__init__(self,parent)
        self.parent = parent
        
        self.treeItemIndex = QTreeWidgetItem(self.treeWidget)
        self.treeItemIndex.setText(0,u'全部资源')
        
        self.connect(self.pushButton, SIGNAL("clicked()"),self.add)
        self.connect(self.pushButton_2, SIGNAL("clicked()"),self.winClose)
        
        self.model=GroupListModel()
        self.init()
    
    #关闭窗口
    def winClose(self):
        self.close()
    
    #初始化数据
    def init(self):
        self.resource=self.parent.resource_data
        self.ShowResource()
        self.treeWidget.expandAll()
    
    #显示所有资源
    def ShowResource(self):
        for i in range(len(self.resource)):
            if str(self.resource[i]['parent_id'])=='0':
                self.treeItem='treeItem'+str(i)
                self.treeItem= QTreeWidgetItem(self.treeItemIndex)
                self.treeItem.setText(0,self.tr(str(self.resource[i]['re_name'])))
                self.treeItem.setData(0,1,str(self.resource[i]['id']))
                self.treeItem.setCheckState(0,Qt.Unchecked)
                self.getChild(self.treeItem,self.resource[i]['id'])
    
    def getChild(self,dqtreeItem,id):
        for i in range(len(self.resource)):
            if self.resource[i]['parent_id']==id:
                self.treeItem='treeItem'+str(id)+'_'+str(i)
                self.treeItem= QTreeWidgetItem(dqtreeItem)
                self.treeItem.setText(0,self.tr(str(self.resource[i]['re_name'])))
                self.treeItem.setData(0,1,str(self.resource[i]['id']))
                self.treeItem.setCheckState(0,Qt.Unchecked)
                self.getChild(self.treeItem,self.resource[i]['id'])
                
    #添加
    def add(self):
        group_name=str(self.group_name.text())
        if group_name=='':
            self.boxWarning(u'提示',u'用户组名不能为空')
            return
        role_describe=str(self.lineEdit.text())
        self.treeCheckValue(self.treeItemIndex,self.treeItemIndex.childCount())
        if self.data:
            data={'group_name':group_name,'txt':role_describe,'role_list':str(self.data[:-1])}
        else:
            data={'group_name':group_name,'txt':role_describe,'role_list':''}
        json=self.model.groupAdd(data)
        print json
        self.getAddGroupInfo(json)
    
    #接收用户组添加是否成功
    def getAddGroupInfo(self,data):
        
        if data['stat']:
            self.boxInfo(u'提示',data['msg'])
            self.parent.init()
            self.close()
        else:
            self.boxWarning(u'提示',data['msg'])
    
    
    #获取树形目录所有复选框选中的值(trObj:获取树形对象，Count:树形对象下所有选项)
    def treeCheckValue(self,trObj,Count):
        self.data=''
        for i in range(Count):
            if Qt.Checked==trObj.child(i).checkState(0):
                self.data+=str(trObj.child(i).data(0,1).toString())+','
            if trObj.child(i).childCount()>0:
                self.childCheckValue(trObj.child(i),trObj.child(i).childCount())
                 
                         
    def childCheckValue(self,data,data2):
         
        for i in range(data2):
            if Qt.Checked==data.child(i).checkState(0):
                self.data+=str(data.child(i).data(0,1).toString())+','
                 
            if data.child(i).childCount()>0:
                self.childCheckValue(data.child(i),data.child(i).childCount())