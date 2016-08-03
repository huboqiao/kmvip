#coding:utf-8
'''
Created on 2015年1月27日

@author: king

登陆窗口

'''
from application.lib.Commethods import *
from application.view.systemsetting import Ui_Dialog
from application.lib.commodel import getDataThread
from application.controller.addcustomer import Addcustomer
from application.controller.edicoumster import Edicustomer

class Systemseting(ControllerAction, Ui_Dialog):
    def __init__(self,parent = None):
        ControllerAction.__init__(self,parent)
        self.tableWidget.isColumnHidden (1)
        self.tableWidget.setEditTriggers(QAbstractItemView.AnyKeyPressed)
        self.abc()
        self.connect(self.pushButton,SIGNAL("clicked()"),self.addcustomer)
        self.connect(self.pushButton_2,SIGNAL("clicked()"),self.edicustomer)
        self.connect(self.pushButton_3,SIGNAL("clicked()"),self.delcustomer)
    #获取所有的用户列表
    def abc(self):
        data = {'node':'logic','act_fun':'getcumster','data':""}
        self.dayreportmodel = getDataThread(data,0,"getcumster")
        self.connect(self.dayreportmodel,SIGNAL("getcumster"),self.toAccept)
        self.dayreportmodel.start()

    def toAccept(self,data):
        if not data["stat"]:
            #提示错误
            self.infoBox(data["msg"])
            return
        data = data["data"]
        self.tableWidget.setRowCount(len(data))

        for key,value in enumerate(data):
            if value['isactive'] == 1:
                isactive = QTableWidgetItem(u"是")
                name = QTableWidgetItem(value['name'])
                name.setData(Qt.UserRole,value)
                name.setTextAlignment(Qt.AlignCenter)
                isactive.setData(Qt.UserRole,value)
                isactive.setTextAlignment(Qt.AlignCenter)
                self.tableWidget.setItem(key,0,name)
                self.tableWidget.setItem(key,1,isactive)
            else:
                isactive = QTableWidgetItem(u"否")
                isactive.setTextAlignment(Qt.AlignCenter)
                name = QTableWidgetItem(value['name'])
                name.setData(Qt.UserRole,value)
                name.setTextAlignment(Qt.AlignCenter)
                isactive.setData(Qt.UserRole,value)
                self.tableWidget.setItem(key,0,name)
                self.tableWidget.setItem(key,1,isactive)
           
            
    def addcustomer(self):
        self.addcumster = Addcustomer()
        if self.addcumster.exec_() == QDialog.Accepted:
            print "添加成功,更新UI"
            self.abc()

    def edicustomer(self):
        if self.tableWidget.currentItem()==None:
            self.boxWarning(u'提示',u'请选择你要修改的记录')
            return
        else:
           
            self.person = self.getcurrentmessage()
            self.edicustomer = Edicustomer(self.person)
            if self.edicustomer.exec_() == QDialog.Accepted:
                self.abc()

    def delcustomer(self):
        if self.tableWidget.currentItem()==None:
            self.boxWarning(u'提示',u'没有你所要删除的记录')
            return
        else:
            data = self.getcurrentmessage()
            self.boxWarning(u'提示',u'是否确定删除')
            data = {'node':'logic','act_fun':'delCustomer','data':{"id":data["id"]}}
            self.dayreportmodel = getDataThread(data,0,"delCustomer")
            self.connect(self.dayreportmodel,SIGNAL("delCustomer"),self.todel)
            self.dayreportmodel.start()
                  
            
    def todel(self,data):
        if not data["stat"]:
            #提示错误
            self.infoBox(data["msg"])
            return
        #更新ui
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

     



        
