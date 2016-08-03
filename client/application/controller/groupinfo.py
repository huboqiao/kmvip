# -*- coding: utf-8 -*-
'''
Created on 2015年3月2日

@author: LiuXinwu
'''
from PyQt4 import QtGui
from application.lib.Commethods import *
from application.view.group import Ui_Dialog
from application.model.grouplist_model import GroupListModel

class GroupInfoController(ControllerAction,Ui_Dialog):
    def __init__(self,parent=None):
        ControllerAction.__init__(self,parent)
        self.parent=parent
        
        self.treeItemIndex = QTreeWidgetItem(self.treeWidget)
        self.treeItemIndex.setText(0,u'全部资源')
        
        self.setWindowTitle(u'查看用户组')
        self.pushButton.hide()
        self.connect(self.pushButton_2, SIGNAL("clicked()"),self.winClose)
        self.model = GroupListModel()
        self.init()
        
    #初始化数据
    def init(self):
        self.group_name.setText(self.tr(str(self.parent.name)))
        self.lineEdit.setText(self.tr(str(self.parent.txt)))
        for i in range(len(self.parent.grouplist_data)):
            if str(self.parent.id)==str(self.parent.grouplist_data[i]['id']):
                self.role_list=self.parent.grouplist_data[i]['role_list']
        #获取数据
        json=self.model.getPower(str(self.parent.name))
        self.resource = json['resource']
          
        if self.role_list:
            data=str(self.role_list).split(',')
            for v in data:
                for i in  range(len(self.resource)):
                    if int(v)==int(self.resource[i]['id']):
                        self.resource[i]['checked']=1
            
            for i in range(len(self.resource)):
                try:
                    self.resource[i]['checked']
                except:
                    self.resource[i]['checked']=0

        else:
            for i in  range(len(self.resource)):
                self.resource[i]['checked']=0
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
                if self.resource[i]['checked']==0:
                    self.treeItem.setCheckState(0,Qt.Unchecked)
                else:
                    self.treeItem.setCheckState(0,Qt.Checked)
                self.getChild(self.treeItem,self.resource[i]['id'])
                
    
    def getChild(self,dqtreeItem,id):
        for i in range(len(self.resource)):
            if self.resource[i]['parent_id']==id:
                self.treeItem='treeItem'+str(id)+'_'+str(i)
                self.treeItem= QTreeWidgetItem(dqtreeItem)
                self.treeItem.setText(0,self.tr(str(self.resource[i]['re_name'])))
                self.treeItem.setData(0,1,str(self.resource[i]['id']))
                if self.resource[i]['checked']==0:
                    self.treeItem.setCheckState(0,Qt.Unchecked)
                else:
                    self.treeItem.setCheckState(0,Qt.Checked)
                self.getChild(self.treeItem,self.resource[i]['id'])
    
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
        
    
    #关闭窗口
    def winClose(self):
        self.close()
        