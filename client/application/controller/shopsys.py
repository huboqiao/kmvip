# -*- coding: utf-8 -*-
'''
Created on 2014年6月11日

@author: chenyong
'''
from application.lib.Commethods import *
from application.view.shopsys import Ui_Dialog
from application.lib.finger import *

class ShopSysController(KLockDialog,Ui_Dialog):
    def __init__(self,parent=None):
        KLockDialog.__init__(self,parent)
        self.setupUi(self)
        self.parent = parent
        self.setWindowTitle(u'锁屏')
        self.keylist = []
        self.ok = False
    
        global ACTIVEX
        ACTIVEX = self
        self.finger = FingerClass().getFinger(EventsHanld,self)
        if self.finger:
            self.finger.BeginCapture()
        
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
   
    #匹配指纹   
    def checkFinger(self,verTemp):
        
        flag = self.finger.VerFingerFromStr(ControllerAction.appdata['user']['finger'],verTemp,False,False)
        if flag[0]:
            #解锁成功
            self.ok = True
            self.close()
        else:
            self.infoBox(u'解锁失败！')
            
    
    def close(self):        
        if self.ok:
            QWidget.close(self)
    def reject(self, *args, **kwargs):
        #ALT + F4 调用该方法
        if self.ok:
            return KLockDialog.reject(self, *args, **kwargs)
        else :
            self.infoBox(u'请按指纹解锁！')
            
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:  #如果按下ESC键，不让界面关闭。
            self.infoBox(u'请按指纹解锁！')
        
    
        
