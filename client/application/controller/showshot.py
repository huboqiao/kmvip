#coding:utf-8
'''
Created on 2015年1月29日

@author: king
'''
from application.lib.Commethods import *
from application.lib.commodel import getDataThread
from application.view.showshot import Ui_Dialog



class Showshot(ControllerAction, Ui_Dialog):
    def __init__(self,data={},parent = None):
        ControllerAction.__init__(self,parent)

        self.connect(self.pushButton,SIGNAL("clicked()"),self.addshot)
        self.abc()
        self.dataId = 0
     
    def abc(self):
        data = {'node':'logic','act_fun':'getshots','data':""}
        self.dayreportmodel = getDataThread(data,0,"getshots")
        self.connect(self.dayreportmodel,SIGNAL("getshots"),self.toAccept)
        self.dayreportmodel.start()
        
        
    def toAccept(self,data):
        data = data
        if not data["stat"]:
            return
        self.data = data["data"]
        print self.data
        for data in self.data:
            self.dataId = data["id"]
            self.lineEdit.setText(unicode(data["url"]))
            self.lineEdit_2.setText(unicode(data["username"]))
            self.lineEdit_3.setText(unicode(data["password"]))
            self.textEdit.setText(unicode(data["content"])) 
            self.comboBox.setCurrentIndex(int(data["type"]))
            self.comboBox_2.setCurrentIndex(int(data["isactive"]))
                
                
                
    def addshot(self):
        url = self.lineEdit.text()
        username = self.lineEdit_2.text()
        password = self.lineEdit_3.text()
        content = self.textEdit.toPlainText()
        print content
        type = self.comboBox.currentIndex()
        isactive = self.comboBox_2.currentIndex()
        data = {"id":str(self.dataId),"url":str(url),"username":str(username),"password":str(password),"content":str(content),"type":str(type),"isactive":str(isactive)}
        data = {'node':'logic','act_fun':'addshot','data':data}
        self.dayreportmodel = getDataThread(data,0,"addshot")
        self.connect(self.dayreportmodel,SIGNAL("addshot"),self.finsh)
        self.dayreportmodel.start()
        
        
    def finsh(self,data):
        data = data 
        if data["stat"]:
            self.infoBox(data["msg"])
            

        
        
        
        
        
#
#                 