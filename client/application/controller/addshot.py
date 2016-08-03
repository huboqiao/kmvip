#coding:utf-8
'''
Created on 2015年1月29日

@author: king
'''
from application.lib.Commethods import *
from application.lib.commodel import getDataThread
from application.view.addshot import Ui_Dialog

class Addshot(ControllerAction, Ui_Dialog):
    def __init__(self,data={},parent = None):
        ControllerAction.__init__(self,parent)
        self.connect(self.pushButton,SIGNAL("clicked()"),self.addshot)
        self.connect(self.pushButton_2,SIGNAL("clicked()"),self.cel)
        
    def cel(self):
        self.reject()

    def addshot(self):
        username = self.lineEdit.text()
        url = self.lineEdit_2.text()
        password = self.lineEdit_3.text()
        content = self.lineEdit_4.text()
        type =  self.comboBox.currentIndex()
        isactive = self.comboBox_2.currentIndex()
        data = {"username":str(username),"url":str(url),"password":str(password),"content":str(content),"type":str(type),"isactive":str(isactive)}
        data = {'node':'logic','act_fun':'addshot','data':data}
        self.dayreportmodel = getDataThread(data,0,"addshot")
        self.connect(self.dayreportmodel,SIGNAL("addshot"),self.ok)
        self.dayreportmodel.start()
        
         
    def ok(self,data):
        print data
        if not data["stat"]:
            self.infoBox(data["msg"])
            return
        self.accept()


    
         

         
         