#coding:utf-8
'''
Created on 2015年1月28日

@author: king
'''
from application.lib.Commethods import *
from application.lib.commodel import getDataThread
from application.view.edicustomer import Ui_Dialog
from application.controller.showgory import Showgory

import time

class Edicustomer(ControllerAction, Ui_Dialog):
    def __init__(self,data={},parent = None):
        ControllerAction.__init__(self,parent)
        self.gorysys = data["typelist"]
        self.id = data["id"]
        self.lineEdit.setText(unicode(data["name"]))
        self.comboBox.setCurrentIndex(int(data["isactive"]))
        self.comboBox_2.setCurrentIndex(int(data["isstorage"]))
        self.connect(self.pushButton_2,SIGNAL("clicked()"),self.AA)
        self.connect(self.pushButton_3,SIGNAL("clicked()"),self.cel)
        self.connect(self.pushButton,SIGNAL("clicked()"),self.showgory)


        self.getallgory()
#    获取所有用户的所有权限

    def getallgory(self):
        data = {'node':'logic','act_fun':'getsomegory','data':None}
        self.dayreportmodel = getDataThread(data,0,"getsomegory")
        self.connect(self.dayreportmodel,SIGNAL("getsomegory"),self.sendmessage)
        self.dayreportmodel.start()
        
    def sendmessage(self,data):
#         print data
#         print self.gorysys
#         
        gridlayout = self.groupBox.layout()
        if gridlayout == None:       
            gridlayout = QGridLayout(self.groupBox)
            
        for i in self.findChildren(KCheckBox):
            gridlayout.removeWidget(i)
            i.deleteLater()
        
        if not data["stat"]:
#             self.infoBox(data["msg"])
            return
        self.person = []
        if self.gorysys:
            self.person = [int(i) for i in self.gorysys.split(",")]

        data = data['data']
        for key,value in enumerate(data):
            i = key / 4
            j = key % 4
            checkbox = KCheckBox(unicode(value["name"]),value["id"])
            if not self.person ==0:
                if value["id"] in self.person:
                    checkbox.setCheckState(Qt.Checked)
            gridlayout.addWidget(checkbox,i,j)


    def AA(self):
        name = str(self.lineEdit.text()).strip()
        if name =="":
            self.infoBox(u"客户类型不能为空")
            self.lineEdit.setFocus()
            return
        isactive = self.comboBox.currentIndex()
        isstorage = self.comboBox_2.currentIndex()
        cdate = self.gettime()
        changetypelist = []
        for i in self.groupBox.findChildren(KCheckBox):
            if i.checkState():
                changetypelist.append(str(i.getId()))

        changetypelist = ','.join(changetypelist)
        print changetypelist
        data = {"name":str(name),"isactive":isactive,"isstorage":isstorage,"cdate":cdate,"typelist":str(changetypelist),"id":str(self.id)}
        data = {'node':'logic','act_fun':'updatecustomer','data':data}
        self.dayreportmodel = getDataThread(data,0,"updatecustomer")
        self.connect(self.dayreportmodel,SIGNAL("updatecustomer"),self.updateok)
        self.dayreportmodel.start()
        
    def showgory(self):
        self.getgory = Showgory()
        if self.getgory.exec_() == QDialog.Accepted:
            self.widget.update()
            self.getallgory()
        
        
        
    def updateok(self,data):
        if not data["stat"]:
            self.infoBox(data["msg"])
            return
        self.accept()
        
    def cel(self):
        self.close()
       
    
    
    def gettime(self):
        return int(time.time())


        
        
        

        
    
        