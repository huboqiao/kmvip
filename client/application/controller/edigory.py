#coding:utf-8
'''
Created on 2015年1月28日

@author: king
'''
from application.lib.Commethods import *
from application.lib.commodel import getDataThread
from application.view.edigroy import Ui_Dialog
import time

class Edigory(ControllerAction, Ui_Dialog):
    def __init__(self,data={},parent = None):
        ControllerAction.__init__(self,parent)

        self.connect(self.pushButton,SIGNAL("clicked()"),self.edigory)
        self.connect(self.pushButton_2,SIGNAL("clicked()"),self.cancel)
        self.id = data["id"]
        self.lineEdit.setText(unicode(data["name"]))
        self.comboBox.setCurrentIndex(int(data["isactive"]))
     
        

    def cancel(self):
        self.close()
  
    def edigory(self):
        name = self.lineEdit.text()
        isactive = self.comboBox.currentIndex()
        cdate = self.gettime()
        
        
        senddata = {"name":str(name),"isactive":str(isactive),"cdate":str(cdate),"id":str(self.id)}
        data = {'node':'logic','act_fun':'edigory','data':senddata}
        self.dayreportmodel = getDataThread(data,0,"edigory")
        self.connect(self.dayreportmodel,SIGNAL("edigory"),self.ok)
        self.dayreportmodel.start()
        
    def ok(self,data):
        if not data["stat"]:
            #提示错误
            self.infoBox(data["msg"])
            return
        self.accept()
        
        

    def gettime(self):
        a = int(time.time())
        return a
    
        
        
        