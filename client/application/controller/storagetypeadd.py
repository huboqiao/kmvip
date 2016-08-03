# -*- coding: utf-8 -*-
'''
Created on 2015年1月28日

@author: LiuXinwu
添加仓库类型控制器
'''
from PyQt4 import QtGui
from application.lib.Commethods import *
from application.view.storagetypeadd import Ui_Dialog
from application.model.storagemodel import StorageModel

class StorageTypeAddController(ControllerAction,Ui_Dialog):
    def __init__(self,parent=None):
        ControllerAction.__init__(self,parent)
        self.parent = parent
        #初始化界面
        self.comboBox.addItem(self.tr(str('是')))
        self.comboBox.addItem(self.tr(str('否')))
        #实例化model
        self.model = StorageModel()
        #绑定事件
        self.connect(self.pushButton,SIGNAL('clicked()'),self.addType)
        self.connect(self.pushButton_2,SIGNAL('clicked()'),self.cancel)
    
    #关闭窗口
    def cancel(self):
        self.close()
    
    #验证数据
    def validate(self):
        typeName = str(self.lineEdit.text())
        name = typeName.strip()
        if name=='':
            self.boxInfo(u'提示',u'请填写仓库类型名称！')
            self.lineEdit.clear()
            self.lineEdit.setFocus(True)
            return False
        else:
            pass
        
        nameData = self.model.findTypeNames()
        if nameData['stat']:
            for i in nameData['data']:
                if name==i['name']:
                    self.boxWarning(u'警示',u'类型名称已有，请重新输入！')
                    self.lineEdit.clear()
                    self.lineEdit.setFocus(True)
                    return False
                else:
                    pass
        else:
            self.boxInfo(u'提示',nameData['msg'])
            
        return True
    
    #添加仓库类型
    def addType(self):
        if self.validate():
            #获取表单数据
            typeName = str(self.lineEdit.text())
            name = typeName.strip()
            stat = self.comboBox.currentIndex()
            if stat==0:
                stat = 1
            else:
                stat = 0
            re = self.model.insertStorageType({'name':name,'stat':stat})
            self.boxInfo(u'提示',re['msg'])
            #清空数据
            self.lineEdit.clear()
            self.lineEdit.setFocus(True)
            #更新列表
            self.parent.init()
        else:
            pass
        
        
        
        
        
        
        
        
        
        
        
        
        
        