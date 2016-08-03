#coding:utf-8
'''
Created on 2015年1月28日

@author: king
'''
from application.lib.Commethods import *
from application.lib.commodel import getDataThread
from application.view.edishot import Ui_Dialog
class Edishot(ControllerAction, Ui_Dialog):
    def __init__(self,data={},parent = None):
        ControllerAction.__init__(self,parent)
        print data
        self.id = data["id"]
        self.lineEdit.setText(unicode(data["username"]))
        self.lineEdit_2.setText(unicode(data["url"]))
        self.lineEdit_3.setText(unicode(data["password"]))
        self.lineEdit_4.setText(unicode(data["content"]))
        self.comboBox.setCurrentIndex(int(data["type"]))
        if data["isactive"] ==0:
            self.comboBox_2.setCurrentIndex(0)
        else:
            self.comboBox_2.setCurrentIndex(1)
        self.connect(self.pushButton,SIGNAL("clicked()"),self.edishot)
        self.connect(self.pushButton_2,SIGNAL("clicked()"),self.cancel)
     
        

    def cancel(self):
        self.reject()
  
    def edishot(self):
        username = self.lineEdit.text()
        url = self.lineEdit_2.text()
        password = self.lineEdit_3.text()
        content = self.lineEdit_4.text()
        type =  self.comboBox.currentIndex()
        isactive = self.comboBox_2.currentIndex()
    
        senddata = {"username":str(username),"url":str(url),"password":str(password),"content":str(content),"type":str(type),"isactive":str(isactive),"id":self.id}
        print senddata["isactive"]
        data = {'node':'logic','act_fun':'edishot','data':senddata}
        self.dayreportmodel = getDataThread(data,0,"edishot")
        self.connect(self.dayreportmodel,SIGNAL("edishot"),self.ok)
        self.dayreportmodel.start()
        
    def ok(self,data):
        if not data["stat"]:
            self.infoBox(data["msg"])
            return
        self.accept()
        
        

        
        