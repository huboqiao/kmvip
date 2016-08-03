# -*- coding: utf-8 -*-
'''
Created on 2015年2月12日

@author: LiuXinwu
'''
from PyQt4 import QtGui
from application.lib.Commethods import *
from application.view.addhaoshu import Ui_Dialog
from application.model.storagemodel import StorageModel

class AddHaoShuController(ControllerAction,Ui_Dialog):
    def __init__(self,parent=None):
        ControllerAction.__init__(self,parent)
        self.parent = parent
        self.qid = self.parent.quyuId
        self.model = StorageModel()
        #绑定事件
        self.connect(self.pushButton,SIGNAL('clicked()'),self.addHaoShu)
        self.connect(self.pushButton_2,SIGNAL('clicked()'),self.cancel)
    
    #关闭此窗口
    def cancel(self):
        self.close()
    
    #添加号数
    def addHaoShu(self):
        #获取用户名
        nameStr = str(self.lineEdit.text())
        name = nameStr.strip()
        if len(name)==0:
            self.boxInfo(u'提示：',u'号数不能为空！')
            self.lineEdit.setFocus(True)
            return 
        else:
            #添加号数
            stat = self.comboBox.currentIndex()
            if stat == 0:
                stat = 1
            else:
                stat = 0 
            re = self.model.insertHaoShu({'qid':str(self.qid),'name':name,'stat':str(stat)})
            self.boxInfo(u'提示：',re['msg'])
            self.parent.initData()
            self.close()
            