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

class AdminAllow(ControllerAction1,Ui_Dialog):
    def __init__(self,parent=None,title=u"主管授权指纹验证"):
        ControllerAction1.__init__(self,parent,title)
        self.parent = parent
        self.setupUi(self)
#         self.setWindowTitle(title)
        self.pushButton.hide()
        global ACTIVEX
        ACTIVEX = self
        self.finger = FingerClass().getFinger(EventsHanld,self)
        if self.finger:
            self.finger.BeginCapture()
        
    #匹配指纹   
    def checkFinger(self,verTemp):
        
        self.verTemp = verTemp
        # 先拉取说有财务人员
        data = {'node':'logic','act_fun':'getGrantsFinger','data':1}
        self.dayreportmodel = getDataThread(data,0,"getGrantsFinger")
        self.connect(self.dayreportmodel, SIGNAL("getGrantsFinger"), self.matching)
        self.dayreportmodel.start()
        
    def matching(self, fingers):
        
        # 匹配
        if not fingers['stat']:
            self.boxWarning(u'提示', u'获取财务人员指纹失败！')
            return
        for i in fingers['data']:
            if i != '':
                flag = self.finger.VerFingerFromStr(i['finger'],self.verTemp,False,False)
                if flag[0]:
                    #授权成功
                    self.close()
                    self.parent.gart(True)
                    return
        self.boxWarning(u'提示',u'你没有授权权限，请按授权指纹！')

        
    
        
