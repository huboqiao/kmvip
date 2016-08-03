# -*- coding: utf-8 -*-
'''
Created on 2015年2月11日

@author: LiuXinwu
'''
from PyQt4 import QtGui
from application.lib.Commethods import *
from application.view.addquyu import Ui_Dialog
from application.model.storagemodel import StorageModel


class AddQuYuController(ControllerAction,Ui_Dialog):
    def __init__(self,parent=None):
        ControllerAction.__init__(self,parent)
        self.parent = parent
        self.model = StorageModel()
        #绑定事件
        self.connect(self.pushButton,SIGNAL('clicked()'),self.addQuYu)
        self.connect(self.pushButton_2,SIGNAL('clicked()'),self.cancel)
    
    #关闭此窗口
    def cancel(self):
        self.close()
    
    #添加区域
    def addQuYu(self):
        #获取用户名
        nameStr = str(self.lineEdit.text())
        name = nameStr.strip()
        if len(name)==0:
            self.boxInfo(u'提示：',u'区域名称不能为空！')
            self.lineEdit.setFocus(True)
            return 
        else:
            #添加区域
            isactive = self.comboBox.currentIndex()
            if isactive  == 0:
                isactive = 1
            else:
                isactive = 0
            re = self.model.insertQuYu({'sid':str(self.parent.id),'name':name,'isactive':str(isactive)})
            self.boxInfo(u'提示：',re['msg'])
            self.parent.init()
            self.close()
            
            