# -*- coding: utf-8 -*-
'''
Created on 2014年6月11日

@author: chenyong
'''
from PyQt4 import QtGui
from application.view.finger import Ui_Dialog
from application.lib.finger import *

from PyQt4 import Qt
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import ConfigParser

QTextCodec.setCodecForTr(QTextCodec.codecForName("utf8")) 
class ControllerAction1(QDialog):
    """
        @param appdata:dict    存放用户数据（用户登陆信息）
    """
    def __init__(self,parent=None):
        QDialog.__init__(self,parent)
        self.cf = ConfigParser.ConfigParser()
        self.cf.read('config.ini')
    '''
                    警告弹窗
        @param title: 弹窗标题
        @param msg  : 显示内容  
    '''
    def boxWarning(self,title,msg):
        QMessageBox.warning(self, title,msg,QMessageBox.Ok)
    '''
                 提示弹窗
        @param title: 弹窗标题
        @param msg  : 显示内容  
    '''
    def boxInfo(self,title,msg):
        QMessageBox.information(self, title,msg,QMessageBox.Ok)
        
class FingerController(ControllerAction1,Ui_Dialog):
    def __init__(self,parent=None):
        ControllerAction1.__init__(self,parent)
        self.setupUi(self)
        self.obj = parent
        
        global ACTIVEX
        
        ACTIVEX = self
        self.finger = FingerClass().getFinger(EventsHanld,self)
        if self.finger:
            self.finger.BeginEnroll()
        
        fingerdata = ''
