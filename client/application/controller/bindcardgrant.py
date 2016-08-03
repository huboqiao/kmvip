# -*- coding: utf-8 -*-
'''
Created on 2015年3月19日

@author: LiuXinwu
'''
from PyQt4 import QtGui
from application.lib.Commethods import *
from application.view.grant import Ui_Dialog
from application.lib.finger import *
from application.model.guashi_model import GuashiModel

class BindCardGrantController(ControllerAction,Ui_Dialog):
    def __init__(self,parent=None,title=u"主管授权指纹验证"):
        ControllerAction.__init__(self,parent,title)
        self.parent=parent
        
        self.model=GuashiModel()
        global ACTIVEX
        ACTIVEX = self
        self.finger = FingerClass().getFinger(EventsHanld,self)
        if self.finger:
            self.finger.BeginCapture()
    
    #匹配指纹   
    def checkFinger(self,verTemp):
        cardid=str(self.parent.cardid.text())
        for i in self.appdata['user_data_info']['admin']:
            if i['finger'] != '':
                flag = self.finger.VerFingerFromStr(i['finger'],verTemp,False,False)
                if flag[0]:
                    #授权成功
                    self.boxInfo(u'提示',u'授权成功')
                   # json=self.model.lossCard(cardid)
#                     if  json['stat'] == 1:
                    self.bindSuccess()
                    return
#                     else:
#                         self.boxWarning(u'提示',json['msg'].decode('utf8'))
#                         return
        self.boxWarning(u'提示',u'你没有授权权限，请按授权指纹！')
        
    #绑定成功
    def bindSuccess(self):
        self.close()
        self.parent.figerBindCard()
        
    
        
