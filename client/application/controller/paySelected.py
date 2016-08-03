# -*- coding: utf-8 -*-
'''
Created on 2015年4月10日

@author: huaan
'''
from PyQt4 import QtGui
from application.lib.Commethods import *
from application.view.paySelected import Ui_Dialog
from application.lib.commodel import getDataThread
from win32api import GetSystemMetrics
import locale

class PaySelected(ControllerAction, Ui_Dialog):
    def __init__(self, parent=None):
        ControllerAction.__init__(self, parent)
        self.title = u'批量缴费'
        self.parent = parent
        txt = u'%s 缴纳  %s 合计人民币 %s 元。'%(self.parent.toPayRecord[0]['membername'],
                                        '、'.join(list(set(self.parent.selectedRecordPaytype))),
                                        locale.format("%.2f", float(self.parent.selectedRecordCount), 1))
        self.label.setText(self.tr(txt))
        size = self.geometry()
        width = GetSystemMetrics(0)
        height = GetSystemMetrics(1)
        self.move((width - size.width()) / 2, (height - size.height()) / 2) # 重置窗口位置
        self.connect(self.pushButton_2, SIGNAL("clicked()"), self.close)
        self.connect(self.pushButton, SIGNAL("clicked()"), self.paySelected)
        
    def paySelected(self):
        if self.radioButton.isChecked():
            self.parent.payAct = 1
        elif self.radioButton_2.isChecked():
            self.parent.payAct = 2
        else:
            self.parent.payAct = 3
        self.accept()