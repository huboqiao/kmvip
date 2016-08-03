#coding:utf-8
'''
Created on 2015年2月1日

@author: kylin

利率设置
'''
from application.lib.Commethods import *
from application.view.rateset import Ui_Dialog
from application.lib.commodel import getDataThread
import application.lib.formatCheck as check

class RateSet(ControllerAction,Ui_Dialog):
    def __init__(self,parent = None):
        ControllerAction.__init__(self, parent)
        
        
        self.queryRate()        
        self.setSIGNAL()
        check.stringFilter(self.lineEdit, "^\+?(\d*\.\d{5})$")

    
    def queryRate(self):    
        data = {'node':'logic','act_fun':'queryRate','data':{}}
        self.ratemodel = getDataThread(data,0,"queryRate")
        self.connect(self.ratemodel,SIGNAL("queryRate"),self.getData)
        self.ratemodel.start()
    
    def getData(self,data):
        data = data
        if not data["stat"]:
            self.oldrate = None
            self.id = 0
            return
        data = data["data"]
        self.id = data["id"]
        self.oldrate = float(data["rates"])
        self.lineEdit.setText(str(data["rates"]))
        self.lineEdit.setFocus(True)
        pass
        
    def setSIGNAL(self):
        self.connect(self.pushButton, SIGNAL("clicked()"),self.submitRateSet)   
        
    def submitRateSet(self):
        try:
            rates = float(str(self.lineEdit.text()).replace(" ",""))
            
        except:
            self.infoBox(u"请输入正确利率值")
            self.lineEdit.setFocus(True)
            return
        
        print self.oldrate
        print rates
        if self.oldrate == rates:
            self.infoBox(u"更新成功")
            self.lineEdit.setFocus()
            return
        
        data = {'node':'logic','act_fun':'updateRate','data':{"rates":str(rates),"id":str(self.id)}}
        self.ratemodel = getDataThread(data,0,"updateRate")
        self.connect(self.ratemodel,SIGNAL("updateRate"),self.updateFinish)
        self.ratemodel.start()
    
    def updateFinish(self,data):
        if data["stat"]:
            self.infoBox(u"更新成功")
            self.lineEdit.setFocus()
            self.queryRate()
        else:
            self.infoBox(data["msg"])
            self.queryRate()
            
    
            