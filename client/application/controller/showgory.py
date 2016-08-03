#coding:utf-8
'''
Created on 2015年1月29日

@author: king
'''

from application.lib.Commethods import *
from application.lib.commodel import getDataThread
from application.view.goryset import Ui_Dialog
from application.controller.addgory import Addgory
from application.controller.edigory import Edigory


import time

class Showgory(ControllerAction, Ui_Dialog):
    def __init__(self,data={},parent = None):
        ControllerAction.__init__(self,parent)
        self.tableWidget.isColumnHidden (1)
#         
        self.connect(self.pushButton,SIGNAL("clicked()"),self.sure)
        self.connect(self.pushButton_2,SIGNAL("clicked()"),self.cel)
        self.connect(self.pushButton_4,SIGNAL("clicked()"),self.addgory)
        self.connect(self.pushButton_5,SIGNAL("clicked()"),self.edigory)
        self.connect(self.pushButton_6,SIGNAL("clicked()"),self.delgory)
        self.abc()
        
    def abc(self):
        data = {'node':'logic','act_fun':'getgory','data':""}
        self.dayreportmodel = getDataThread(data,0,"getgory")
        self.connect(self.dayreportmodel,SIGNAL("getgory"),self.toAccept)
        self.dayreportmodel.start()
        
    def toAccept(self,data):
        print data
        if not data["stat"]:
            #提示错误
#             self.infoBox(data["msg"])
            return
        data = data["data"]
        self.tableWidget.setRowCount(len(data))

        for key,value in enumerate(data):
            if value['isactive'] == 1:
                isactive = QTableWidgetItem(u"是")
            else:
                isactive = QTableWidgetItem(u"否")
            name = QTableWidgetItem(value['name'])
            isactive.setData(Qt.UserRole,value)
            self.tableWidget.setItem(key,1,isactive)
            name.setData(Qt.UserRole,value)
            self.tableWidget.setItem(key,0,name)
#             else:
#                 name = QTableWidgetItem(str(value['name']))
#                 isactive = QTableWidgetItem(u"否")
#                 name.setData(Qt.UserRole,value)
#                 isactive.setData(Qt.UserRole,value)
#                 self.tableWidget.setItem(key,0,name)
#                 self.tableWidget.setItem(key,1,isactive)
                
           
        
        
    def addgory(self):
        self.addgory = Addgory()
        if self.addgory.exec_() == QDialog.Accepted:
            self.abc()

    def edigory(self):
        if self.tableWidget.currentItem()==None:
            self.boxWarning(u'提示',u'请选择你要修改的记录')
            return
        self.message = self.getcurrentmessage()
        self.edigoty = Edigory(self.message)
        if self.edigoty.exec_() == QDialog.Accepted:
            self.abc()
    
    def delgory(self):
        if self.tableWidget.currentItem()==None:
            self.boxWarning(u'提示',u'请选择你要删除的记录')
            return
        else:
            data = self.getcurrentmessage()            
            data = {'node':'logic','act_fun':'delgory','data':{"id":data["id"]}}
            self.dayreportmodel = getDataThread(data,0,"delgory")
            self.connect(self.dayreportmodel,SIGNAL("delgory"),self.todel)
            self.dayreportmodel.start()
            
    def todel(self,data):
        if not data["stat"]:
            #提示错误
            self.infoBox(data["msg"])
            return
        self.tableWidget.clear()
        self.abc()        

    #获取当前的那行的信息
    def getcurrentmessage(self):
        currentitem = self.tableWidget.currentItem().data(Qt.UserRole)
        tmplist = currentitem.toPyObject()
        senddata = {}
        for key,value in tmplist.items():
            senddata[str(key)] = str(value)
        return senddata

    def cel(self):
        self.close()
        
    def sure(self):
        self.accept()

        
        
