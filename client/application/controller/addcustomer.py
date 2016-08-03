#coding:utf-8
'''
Created on 2015年1月28日

@author: king
'''
from application.lib.Commethods import *
from application.lib.commodel import getDataThread
from application.view.addcustomer import Ui_Dialog
from application.controller.showgory import Showgory
import time

class Addcustomer(ControllerAction, Ui_Dialog):
    def __init__(self,data={},parent = None):
        ControllerAction.__init__(self,parent)
        self.comboBox.setCurrentIndex(1)
        self.connect(self.pushButton,SIGNAL("clicked()"),self.showgory)
        self.connect(self.pushButton_2,SIGNAL("clicked()"),self.addcustomer)
        self.connect(self.pushButton_3,SIGNAL("clicked()"),self.cel)
        self.showsomegory()
    def cel(self):
        self.reject()
         
    def showgory(self):
        print "showgory"
        self.getgory =  Showgory()
        if self.getgory.exec_() == QDialog.Accepted:
            self.widget.update()
            self.showsomegory()
         
    def addcustomer(self):
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
        data = {"name":name,"isactive":isactive,"isstorage":isstorage,"cdate":cdate,"typelist":changetypelist}
        data = {'node':'logic','act_fun':'addcustomer','data':data}
        self.dayreportmodel = getDataThread(data,0,"addcustomer")
        self.connect(self.dayreportmodel,SIGNAL("addcustomer"),self.ok)
        self.dayreportmodel.start()
        
         
    def ok(self,data):
        if not data["stat"]:
            self.infoBox(data["msg"])
            return
        self.accept()

        
    def gettime(self):
        a = int(time.time())
        return a
     
    def showsomegory(self):
        data = {'node':'logic','act_fun':'getsomegory','data':None}
        self.dayreportmodel = getDataThread(data,0,"getsomegory")
        self.connect(self.dayreportmodel,SIGNAL("getsomegory"),self.toshow)
        self.dayreportmodel.start()
         
    def toshow(self,data):
        
        gridlayout = self.groupBox.layout()
        if gridlayout == None:
        
            gridlayout = QGridLayout(self.groupBox)
        
        for i in self.findChildren(KCheckBox):
            gridlayout.removeWidget(i)
            i.deleteLater()
        
        if not data["stat"]:
            return
        data = data['data']
        #遍历元组，列表
#         self.groupBox.setParent(None)
   
#         self.groupBox.update()     
            
        
        print data
        for key,value in enumerate(data):
            i = key / 4
            j = key % 4
            checkbox = KCheckBox(unicode(value["name"]),value["id"])
            gridlayout.addWidget(checkbox,i,j)
#         self.groupBox.setLayout(gridlayout)   

#         self.groupBox.update()     
         
         
         
         
         