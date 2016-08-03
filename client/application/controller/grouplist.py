# -*- coding: utf-8 -*-
'''
Created on 2015年3月2日

@author: LiuXinwu
'''
from PyQt4 import QtGui
from application.lib.Commethods import *
from application.view.grouplist import Ui_Dialog
from application.model.grouplist_model import GroupListModel
from application.controller.groupadd import GroupAddController
from application.controller.groupedit import GroupEditController
from application.controller.groupinfo import GroupInfoController
from application.lib.commodel import getDataThread


class GroupListController(ControllerAction,Ui_Dialog):
    def __init__(self,parent=None):
        ControllerAction.__init__(self,parent)
        self.parent = parent
        self.tableWidget.horizontalHeader().setResizeMode(QHeaderView.Stretch)      #铺满表格
        
        #绑定事件
        self.connect(self.tableWidget, SIGNAL("itemClicked (QTableWidgetItem*)"), self.outSelect)
        self.connect(self.pushButton, SIGNAL("clicked()"),self.groupAdd)        #添加
        self.connect(self.pushButton_3, SIGNAL("clicked()"),self.groupDel)      #删除
        self.connect(self.pushButton_2, SIGNAL("clicked()"),self.groupAlter)    #修改
        self.connect(self.pushButton_4, SIGNAL("clicked()"),self.groupInfo)     #详情
        
        self.startQuery = True
        self.model=GroupListModel()
        self.init()
    
    #查看用户组详情
    def groupInfo(self):
        if self.id:
            win = GroupInfoController(self)
            win.exec_()
        else:
            self.boxWarning(u'提示',u'请选择要查看的用户组')
    
    #点击单元格选中用户组
    def outSelect(self,itme):
        self.id=self.tableWidget.item(itme.row(),0).text()
        self.name=self.tableWidget.item(itme.row(),1).text()
        self.txt=self.tableWidget.item(itme.row(),2).text()
        self.pushButton_2.setEnabled(True)
        self.pushButton_3.setEnabled(True)
        self.pushButton_4.setEnabled(True) 
    
    #修改用户组
    def groupAlter(self):
        if self.id:
            if str(self.id)=='1':
                self.boxWarning(u'提示',u'该用户组不能修改')
            else:
                win = GroupEditController(self)
                win.exec_()
        else:
            self.boxWarning(u'提示',u'请选择要修改的用户组')
    
    
    #删除用户组
    def groupDel(self):
        if self.id :
            if (str(self.id)=='1') or (str(self.id)=='2'):
                self.boxWarning(u'提示',u'该组不能删除')
            else:
                button=QMessageBox.question(self,"Question",  
                                    self.tr("确定要删除用户组："+str(self.name)+"?"),  
                                    QMessageBox.Ok|QMessageBox.Cancel,  
                                    QMessageBox.Ok)  
                if button==QMessageBox.Ok:  
                    json=self.model.deletePower(str(self.id))
                    self.delGroupInfo(json)
        else:
            self.boxWarning(u'提示',u'请选择要删除的用户组！')
            
    #判断删除用户是否成功
    def delGroupInfo(self,data):
        if data['stat'] == 1:
            self.boxInfo(u'提示',data['msg'].decode('utf8'))
            self.init()
        else:
            self.boxWarning(u'提示',data['msg'].decode('utf8')) 
    
    
    #添加用户组
    def groupAdd(self):
        win = GroupAddController(self)
        win.exec_()
        
    #用户列表
    def init(self):
        if not self.startQuery :
            return
        data={'node':'logic','act_fun':'getPow','data':''}
        self.threadmodel = getDataThread(data,0,"getPow")
        self.connect(self.threadmodel,SIGNAL("getPow"),self.getgroup)
        self.threadmodel.start()
        self.startQuery = False
    
    
    def getgroup(self,data):
        data = data
        self.startQuery = True
        self.upPower(data)

        
    #接收服务器返回来的所有用户组和用户组资源权限
    def upPower(self,data):
        self.grouplist_data=data['usergroup']
        self.resource_data=data['resource']
        if self.grouplist_data:
            self.tableWidget.setRowCount(0)
            self.pushButton_2.setEnabled(False) 
            self.pushButton_3.setEnabled(False) 
            self.pushButton_4.setEnabled(False) 
            for i in range(len(self.grouplist_data)):
                    self.updateTable(self.grouplist_data[i])
           
    #更新表格
    def updateTable(self,data):
        counts = int(self.tableWidget.rowCount()) 
        self.tableWidget.setRowCount(counts+1)
        id = QTableWidgetItem(self.tr(str(data['id'])))
        id.setFlags(Qt.ItemIsEnabled)
        id.setTextAlignment(Qt.AlignCenter)
        group_name = QTableWidgetItem(self.tr(str(data['group_name'])))
        group_name.setFlags(Qt.ItemIsEnabled)
        group_name.setTextAlignment(Qt.AlignCenter)
        role_describe = QTableWidgetItem(self.tr(str(data['role_describe'])))
        role_describe.setFlags(Qt.ItemIsEnabled)
        role_describe.setTextAlignment(Qt.AlignCenter)
        self.tableWidget.setItem(counts,0,id)
        self.tableWidget.setItem(counts,1,group_name)
        self.tableWidget.setItem(counts,2,role_describe)
        
    
        