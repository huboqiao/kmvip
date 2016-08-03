# -*- coding: utf-8 -*-
'''
Created on 2015年1月28日

@author: LiuXinwu
'''
from PyQt4 import QtGui
from application.lib.Commethods import *
from application.view.userlist import Ui_Dialog
from application.controller.useredit import UserEditController
from application.lib.commodel import getDataThread
from application.model.userlist_model import UserlistModel
from application.controller.useradd import UserAddController


class UserListController(ControllerAction, PrintAction, Ui_Dialog):
    def __init__(self,parent=None):
        ControllerAction.__init__(self,parent)
        PrintAction.__init__(self, self.tableWidget)
        self.setTableFormat()
        self.parent = parent
        self.tableWidget.horizontalHeader().setResizeMode(QHeaderView.Stretch)      #铺满表格
        
        self.model=UserlistModel()
        
        self.startQuery = True
        #绑定事件
        self.connect(self.tableWidget, SIGNAL("itemClicked (QTableWidgetItem*)"), self.outSelect)
        self.connect(self.pushButton, SIGNAL("clicked()"),self.userAdd)
        self.connect(self.pushButton_2, SIGNAL("clicked()"),self.userEdit)
        self.connect(self.pushButton_3, SIGNAL("clicked()"),self.userShop)
        self.connect(self.tableWidget, SIGNAL("cellDoubleClicked(int, int)"), self.userEdit)
        self.userInit()
    
    #注销用户
    def userShop(self):
        if self.id:
            if str(self.id)=='1':
                self.boxWarning(u'提示',u'该用户不能删除！')
                return
            else:
                button=QMessageBox.question(self,u"提示",u"确定要注销登录名为："+self.tr(str(self.user_name))+"?",QMessageBox.Ok|QMessageBox.Cancel,QMessageBox.Ok)  
                if button==QMessageBox.Ok:
                    json=self.model.delUser(str(self.id))

                    self.delUserInfo(json)
        else:
            self.boxWarning(u'提示',u'该用户不能删除！')

    def delUserInfo(self,data):
        if data['stat']==1:
            self.boxInfo(u'提示',u'删除员工成功！')
            self.userInit()
        else:
            self.boxWarning(u'提示',data['stat'].decode('utf8'))
    
    #注销成功更新页面
    def shopUserSuccess(self):
        self.boxInfo(u'提示',u'注销成功成功')
        self.tableWidget.setRowCount(0) 
        self.userinit()
    
    #选择某单元格
    def outSelect(self,itme=None):
        self.id=self.tableWidget.item(itme.row(),0).text()
        self.user_name=self.tableWidget.item(itme.row(),1).text()
        self.pushButton_2.setEnabled(True)
        self.pushButton_3.setEnabled(True)
    
    #修改用户
    def userEdit(self):
        if self.id:
            t=UserEditController(self)
            t.exec_()
        else:
            QMessageBox.warning(self, u'提示',u'请选择要修改的用户',QMessageBox.Ok)
    
    #添加员工    
    def userAdd(self):
        win = UserAddController(self)
        win.exec_()
    
    #初次查询所有员工    
    def userInit(self):
        if not self.startQuery:
            return
        data={'node':'logic','act_fun':'queryUser','data':''}
        self.threadmodel = getDataThread(data,0,"queryUser")
        self.connect(self.threadmodel,SIGNAL("queryUser"),self.getusers)
        self.threadmodel.start()
        self.startQuery = False
            
    def getusers(self,data):
        self.startQuery = True
        if data['stat'] == 1:
            self.userList(data['data']) 
    
    def userList(self,data):
        self.tableWidget.setRowCount(0) 
        if data:
            self.userList_data=data
            self.pushButton_2.setEnabled(False) #修改按钮
            self.pushButton_3.setEnabled(False) #注销按钮
            self.insertTable(data)
        
    def setTableFormat(self):
        #字段格式
        self.table_fmt_list = []
        self.table_fmt_list.append({"alignment":"center","color":"black","format":"general","count":False})
        self.table_fmt_list.append({"alignment":"center","color":"black","format":"general","count":False})
        self.table_fmt_list.append({"alignment":"center","color":"black","format":"general","count":False})
        self.table_fmt_list.append({"alignment":"center","color":"black","format":"general","count":False})
        self.table_fmt_list.append({"alignment":"center","color":"black","format":"enum","count":False,"enum":[u"女",u"男"]})
        self.table_fmt_list.append({"alignment":"center","color":"black","format":"general","count":False})
        self.table_fmt_list.append({"alignment":"center","color":"black","format":"enum","count":False,"enum":[u"无",u"有"]})
        
        #需要汇总的字段
        self.countColumn = [key for key,value in enumerate(self.table_fmt_list) if value['count'] == True]
        
        #表格列匹配数据库字段
        self.columnName = ["id","username","group_name","nickname",'sex','tel','righter']
        
        #初始化汇总字段的值为0
        self.countList = {}
        for i in self.countColumn:
            self.countList[str(i)] = 0
        
        
    def insertTable(self,data):
        self.tableWidget.setRowCount(len(data))
        for i,value in enumerate(data):
            
            for j in range(self.tableWidget.columnCount()):
                
                item = QTableWidgetItem(unicode(str(value[self.columnName[j]])))
                self.formatTableItem(item,self.table_fmt_list[j])
                item.setData(Qt.UserRole,value["id"])
                self.tableWidget.setItem(i,j,item)
                if j in self.countColumn:
                    self.countList[str(j)] += value[self.columnName[j]]
                    
        if len(self.countColumn)>0:
            rowCount = self.tableWidget.rowCount()
            self.tableWidget.setRowCount(rowCount+1)
            self.tableWidget.setItem(rowCount,0,QTableWidgetItem(u"合计：共%s条记录"%len(data)))
            for key,value in self.countList.items():
                item = QTableWidgetItem(str(value))
                self.tableWidget.setItem(rowCount,int(key),item)
                self.formatTableItem(item,self.table_fmt_list[int(key)])