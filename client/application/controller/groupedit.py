# -*- coding: utf-8 -*-
'''
Created on 2015年3月2日

@author: LiuXinwu
'''
from PyQt4 import QtGui
from application.lib.Commethods import *
from application.view.group import Ui_Dialog
from application.model.grouplist_model import GroupListModel


class GroupEditController(ControllerAction,Ui_Dialog):
    def __init__(self,parent=None):
        ControllerAction.__init__(self,parent)
        self.parent = parent
        
        self.treeItemIndex = QTreeWidgetItem(self.treeWidget)
        self.treeItemIndex.setText(0,u'全部资源')
        
        self.setWindowTitle(u'修改用户组')
        self.pushButton.setText(u'修改')
        self.connect(self.pushButton, SIGNAL("clicked()"),self.groupEdit)
        self.connect(self.pushButton_2, SIGNAL("clicked()"),self.winClose)
        self.init()
        self.model=GroupListModel()
        
    #初始化数据
    def init(self):
        self.group_name.setText(self.tr(str(self.parent.name)))
        self.lineEdit.setText(self.tr(str(self.parent.txt)))
        for i in range(len(self.parent.grouplist_data)):
            if str(self.parent.id)==str(self.parent.grouplist_data[i]['id']):
                self.role_list=self.parent.grouplist_data[i]['role_list']
        self.resource=self.parent.resource_data
        if self.role_list:
            data=str(self.role_list).split(',')
            for v in data:
                for i in  self.resource:
                    if int(v)==int(i['id']):
                        i['checked']=1
            
            for i in self.resource:
                try:
                    i['checked']
                except:
                    i['checked']=0

        else:
            for i in  self.resource:
                i['checked']=0
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
    
    #修改用户组
    def groupEdit(self):
        group_name=str(self.group_name.text())
        if group_name=='':
            self.boxWarning(u'提示',u'用户组名不能为空')
            return
        for i in range(len(self.parent.grouplist_data)):
            if str(self.parent.grouplist_data[i]['id'])!=str(self.parent.id):
                if group_name==str(self.parent.grouplist_data[i]['group_name']):
                    self.boxWarning(u'提示',u'该用组名已存在')
                    return
        role_describe=str(self.lineEdit.text())
        self.treeCheckValue(self.treeItemIndex,self.treeItemIndex.childCount())
        if self.data:
            data={'id':str(self.parent.id),'group_name':group_name,'role_describe':role_describe,'role_list':str(self.data[:-1])}
        else:
            data={'id':str(self.parent.id),'group_name':group_name,'role_describe':role_describe,'role_list':''}
        json=self.model.editPower(data)
        self.getEditGroupInfo(json)
    
    #接收用户组添加是否成功
    def getEditGroupInfo(self,data):
        if data=='1':
            self.boxInfo(u'提示',u'修改用户组成功！')
            self.parent.init()
            self.close()
        else:
            self.boxWarning(u'提示',u'您没有提交可修改的内容！')
    
    
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
        
        
        