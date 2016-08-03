# -*- coding: utf-8 -*-
'''
Created on 2015年1月28日

@author: LiuXinwu
'''
from PyQt4 import QtGui
from application.lib.Commethods import *
from application.view.advancedQuery import Ui_Dialog
import application.lib.formatCheck as check


class AdvancedQueryController(ControllerAction,Ui_Dialog):
    def __init__(self,parent=None,title=""):
        ControllerAction.__init__(self,parent,title)
        self.parent = parent
        check.stringFilter(self.lineEdit_2, "[\d\s]+$")
        check.stringFilter(self.lineEdit_7, "[\d\s]+$")
        check.stringFilter(self.lineEdit_4, "^[1][3-8]+\\d{9}$")
        check.stringFilter(self.lineEdit_3, "^[1-9]\d{5}[1-9]\d{3}((0\d)|(1[0-2]))(([0|1|2]\d)|3[0-1])\d{3}([0-9]|X)$")
        
        self.connect(self.lineEdit, SIGNAL("returnPressed()"), self.advancedQuery)
        self.connect(self.lineEdit_2, SIGNAL("returnPressed()"), self.advancedQuery)
        self.connect(self.lineEdit_3, SIGNAL("returnPressed()"), self.advancedQuery)
        self.connect(self.lineEdit_4, SIGNAL("returnPressed()"), self.advancedQuery)
        self.connect(self.lineEdit_5, SIGNAL("returnPressed()"), self.advancedQuery)
        self.connect(self.lineEdit_6, SIGNAL("returnPressed()"), self.advancedQuery)
        self.connect(self.lineEdit_7, SIGNAL("returnPressed()"), self.advancedQuery)
        self.connect(self.lineEdit_8, SIGNAL("returnPressed()"), self.advancedQuery)
        self.connect(self.pushButton, SIGNAL('clicked()'), self.advancedQuery)  # 查询
        self.connect(self.pushButton_2, SIGNAL('clicked()'), self.close)  # 关闭高级查询
        
    # 高级查询
    def advancedQuery(self):
        self.parent.emptyMemberInfo()
        self.parent.queryData['name'] = str(self.lineEdit.text())
        self.parent.queryData['card'] = str(self.lineEdit_2.text())
        self.parent.queryData['idCard'] = str(self.lineEdit_3.text())
        self.parent.queryData['tel'] = str(self.lineEdit_4.text())
        self.parent.queryData['storage'] = str(self.lineEdit_5.text())
        self.parent.queryData['storageRegion'] = str(self.lineEdit_6.text())
        self.parent.queryData['storageNumber'] = str(self.lineEdit_7.text())
        self.parent.queryData['storageType'] = str(self.lineEdit_8.text())
        self.parent.queryNow()
        
        