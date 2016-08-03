# -*- coding: utf-8 -*-
'''
Created on 2015年3月5日

@author: LiuXinwu
'''
from PyQt4 import QtGui
from application.lib.Commethods import *
from application.view.grant import Ui_Dialog
from application.lib.finger import *
from application.lib.commodel import getDataThread


from PyQt4 import Qt
from PyQt4.QtCore import *
import ConfigParser

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

class GrantContorller(ControllerAction1,Ui_Dialog):
    def __init__(self,parent=None,title=u"指纹验证"):
        ControllerAction1.__init__(self,parent,u"指纹验证")
        self.setupUi(self)
        self.parent = parent
        self.pushButton.hide()
        global ACTIVEX
        ACTIVEX = self
        self.finger = FingerClass().getFinger(EventsHanld,self)
        if self.finger:
            self.finger.BeginCapture()
        
    #匹配指纹   
    def checkFinger(self,verTemp):
        
        self.verTemp = verTemp
        data = {'node':'logic','act_fun':'getRightersFingers','data':''}
        self.dayreportmodel = getDataThread(data,0,"getRightersFingers")
        self.connect(self.dayreportmodel, SIGNAL("getRightersFingers"), self.matching)
        self.dayreportmodel.start()
        
    def matching(self, data):
        
        # 匹配
        if not data['stat']:
            data['data'] = []
        
        for i in data['data']:
            if i['finger'] != '':
                flag = self.finger.VerFingerFromStr(i['finger'],self.verTemp,False,False)
                if flag[0]:
                    #授权成功
                    self.close()
                    self.parent.gart(i['id'])
                    self.accept()
                    return
        self.boxWarning(u'提示',u'你没有授权权限，请按授权指纹！')
