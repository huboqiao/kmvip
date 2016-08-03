# -*- coding: utf-8 -*-
'''
Created on 2015年2月8日

@author: huaan
'''
from PyQt4 import QtGui
from application.lib.Commethods import *
from application.view.grant import Ui_Dialog
from application.lib.finger import *


QTextCodec.setCodecForTr(QTextCodec.codecForName("utf8")) 
class ControllerAction1(QDialog):
    """
        @param appdata:dict    存放用户数据（用户登陆信息）
    """
    appdata = {}
    def __init__(self,parent=None,title=''):
        QDialog.__init__(self,parent)
        self.setWindowTitle(title)
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

class CheckFingerToAlterPassword(ControllerAction1,Ui_Dialog):
    def __init__(self,parent=None,title=u"指纹验证"):
        ControllerAction1.__init__(self,parent,title)
        self.parent = parent
        self.setupUi(self)
        self.connect(self.pushButton, SIGNAL("clicked()"), self.close)
    
        global ACTIVEX
        ACTIVEX = self
        EventsHanld
        self.finger = FingerClass().getFinger(EventsHanld,self)
        if self.finger:
            self.finger.BeginCapture()
            
    #匹配指纹   
    def checkFinger(self,verTemp):
        # 先拉取说有财务人员
        for finger in self.parent.fingers:
            # 匹配
            if finger != '':
                flag = self.finger.VerFingerFromStr(finger,verTemp,False,False)
                if flag[0]:
                    #授权成功
                    self.close()
                    self.parent.checkPwd({'stat':1, 'finger':finger})
                    return
        self.parent.checkPwd({'stat':-1, 'msg':u'指纹不匹配！'})
        
    
        
