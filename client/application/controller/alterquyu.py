# -*- coding: utf-8 -*-
'''
Created on 2015年2月11日

@author: LiuXinwu
'''
from PyQt4 import QtGui
from application.lib.Commethods import *
from application.view.alterquyu import Ui_Dialog
from application.model.storagemodel import StorageModel

class AlterQuYuController(ControllerAction,Ui_Dialog):
    def __init__(self,parent=None):
        ControllerAction.__init__(self,parent)
        self.parent = parent
        
        self.comboBox.setCurrentIndex(1)
        self.model = StorageModel()
        self.qid = self.parent.quyuid
        self.initData()
        #绑定事件
        self.connect(self.pushButton,SIGNAL('clicked()'),self.alterQuYu)
        self.connect(self.pushButton_2,SIGNAL('clicked()'),self.cancel)
        
    #初始化数据，填充空框
    def initData(self):
        #查询本区域的所有信息
        quyuname = self.parent.quyuname
        self.lineEdit.setText(self.tr(str(quyuname)))
        strisactive = str(self.parent.quyustatname)
        if cmp(strisactive,'启用') == 0:
            self.comboBox.setCurrentIndex(1)
        else:
            self.comboBox.setCurrentIndex(0)

    #修改区域
    def alterQuYu(self):
        nameStr = str(self.lineEdit.text())
        name = nameStr.strip()
        if len(name)==0:
            self.boxInfo(u'提示：',u'区域名称不能为空！')
            self.lineEdit.setFocus(True)
            return 
        else:
            #修改区域
            isactive = self.comboBox.currentIndex()
            re = self.model.updateQuYu({'id':str(self.qid),'name':name,'isactive':str(isactive)})
            self.boxInfo(u'提示：',re['msg'])
            self.parent.init()
            self.close()
        
        
        
        
        
    #关闭窗口
    def cancel(self):
        self.close()