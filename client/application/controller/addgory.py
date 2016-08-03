#coding:utf-8
'''
Created on 2015年1月28日

@author: king
'''
from application.lib.Commethods import *
from application.lib.commodel import getDataThread
from application.view.addgory import Ui_Dialog
import time

class Addgory(ControllerAction, Ui_Dialog):
    def __init__(self,data={},parent = None):
        ControllerAction.__init__(self,parent)
        
        self.connect(self.pushButton,SIGNAL("clicked()"),self.addgory)
        self.connect(self.pushButton_2,SIGNAL("clicked()"),self.cancel)


    def cancel(self):
        self.close()
  
    def addgory(self):
        name = self.lineEdit.text()
        isactive = self.comboBox.currentIndex()
        cdate = self.gettime()
        data  = {"name":str(name),"isactive":str(isactive),"cdate":str(cdate)}
        print data        
        data = {'node':'logic','act_fun':'addgory','data':data}
        self.dayreportmodel = getDataThread(data,0,"addgory")
        self.connect(self.dayreportmodel,SIGNAL("addgory"),self.add)
        self.dayreportmodel.start()
        
    def add(self,data):
        if not data["stat"]:
            #提示错误
            self.infoBox(data["msg"])
            return
        self.accept()
        
        

    def gettime(self):
        a = int(time.time())
        return a
    
        
        
        