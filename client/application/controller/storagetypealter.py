# -*- coding: utf-8 -*-
'''
Created on 2015年2月9日

@author: LiuXinwu
'''
from PyQt4 import QtGui
from application.lib.Commethods import *
from application.view.storagetypealter import Ui_Dialog
from application.model.storagemodel import StorageModel

class StorageTypeAlterController(ControllerAction,Ui_Dialog):
    def __init__(self,parent=None):
        ControllerAction.__init__(self,parent)
        self.parent = parent
        self.comboBox.addItem(self.tr(str('是')))
        self.comboBox.addItem(self.tr(str('否')))
        #实例化model
        self.model = StorageModel()
        self.initData()
        #绑定事件
        self.connect(self.pushButton_2,SIGNAL("clicked()"),self.cancel)
        self.connect(self.pushButton,SIGNAL("clicked()"),self.alterStorageType)
        
     #验证数据
    def validate(self):
        typeName = str(self.lineEdit.text())
        name = typeName.strip()
        if self.tpname==name:
            pass
        else:
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
    
    #修改仓库类型数据
    def alterStorageType(self):
        if self.validate():
            #获得表单数据
            strName = str(self.lineEdit.text())
            name = strName.strip()
            stat = self.comboBox.currentIndex()
            if stat == 0:
                stat = 1  
            else:
                stat = 0
            re = self.model.updateStorageType({'name':name,'stat':stat,'id':str(self.parent.id)})
            self.boxInfo(u'提示',re['msg'])
            self.cancel()
            self.parent.init()
        else:
            pass
    
    #初始化数据
    def initData(self):
        storageTypeData = self.model.findOneStorageType({'id':str(self.parent.id)})
        st = storageTypeData['data']
        self.lineEdit.setText(self.tr(str(st['name'])))
        self.tpname = str(st['name'])
        zhuangtai = st['stat']
        if zhuangtai==0:#未启动
            self.comboBox.setCurrentIndex(1)
        else:
            self.comboBox.setCurrentIndex(0)
            
            
        
    
    #关闭窗口
    def cancel(self):
        self.close()