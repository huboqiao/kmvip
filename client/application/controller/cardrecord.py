# -*- coding: utf-8 -*-
'''
Created on 2014年6月11日

@author: huboqiao
'''
from PyQt4 import QtGui
from application.lib.Commethods import *
from application.view.cardrecord import Ui_Dialog
import time

class CardRecordController(ControllerAction,Ui_Dialog):
    def __init__(self,parent=None):
        ControllerAction.__init__(self,parent)
#         self.setupUi(self)
        self.parent=parent
        self.cardtableWidget.horizontalHeader().setResizeMode(QHeaderView.Stretch)      #铺满表格
        self.Init()
    
    def Init(self):
        for i in range(len(self.parent.cardrecordlist)):
            self.updateTable(self.parent.cardrecordlist[i])
           
    #更新表格
    def updateTable(self,data):
        counts = int(self.cardtableWidget.rowCount()) 
        self.cardtableWidget.setRowCount(counts+1)
        noid = QTableWidgetItem(self.tr(str(data['noid'])))
        noid.setTextAlignment(Qt.AlignCenter|Qt.AlignVCenter)
        cardid = QTableWidgetItem(self.tr(str(data['cardid'])))
        cardid.setTextAlignment(Qt.AlignCenter|Qt.AlignVCenter)
        if str(data['stat'])=='1':
            stat='正常'
        elif str(data['stat'])=='2':
            stat='已注销'
        elif str(data['stat'])=='3':
            stat='已冻结'   
        else:
            stat='未绑定'
        stat = QTableWidgetItem(self.tr(stat))
        stat.setTextAlignment(Qt.AlignCenter|Qt.AlignVCenter)
        timeArray = time.localtime(int(data['bdate']))
        otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        cdate= QTableWidgetItem(self.tr(str(otherStyleTime)))
        cdate.setTextAlignment(Qt.AlignCenter|Qt.AlignVCenter)
        self.cardtableWidget.setItem(counts,0,noid)
        self.cardtableWidget.setItem(counts,1,cardid)
        self.cardtableWidget.setItem(counts,2,cdate)
        self.cardtableWidget.setItem(counts,3,stat)
       
 
    