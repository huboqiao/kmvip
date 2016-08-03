# -*- coding: utf-8 -*-
'''
Created on 2015年1月28日

@author: LiuXinwu
'''
from PyQt4 import QtGui
from PyQt4 import QtCore
from application.lib.Commethods import *
from application.view.storageadd import Ui_Dialog
from application.model.storagemodel import StorageModel

class AddStorageController(ControllerAction,Ui_Dialog):
    def __init__(self,parent=None):
        ControllerAction.__init__(self,parent)
        self.parent = parent
        #设置号数不可编辑
        self.lineEdit_3.setEnabled(False)
        self.listWidget_2.setEnabled(False)
        self.pushButton_2.setEnabled(False)
        #初始化数据
        self.model = StorageModel()
        self.quyulist = []
        self.haoshulist = []
        #绑定事件
        self.connect(self.pushButton_4,SIGNAL('clicked()'),self.cancel)
        self.connect(self.pushButton_3,SIGNAL('clicked()'),self.tijiao)
        self.connect(self.pushButton_2,SIGNAL('clicked()'),self.addhaoshu)
        self.connect(self.pushButton,SIGNAL('clicked()'),self.addquyu)
        
        self.connect(self.listWidget,SIGNAL('currentTextChanged (const QString&)'),self.doTest)
        
    def doTest(self,item):
        #设置号数可以编写
        self.lineEdit_3.setEnabled(True)
        self.listWidget_2.setEnabled(True)
        self.pushButton_2.setEnabled(True)
        #删除上次区域的所有号数
        self.lineEdit_3.clear()
        self.listWidget_2.clear()
       
        
    #添加区域数
    def addquyu(self):
        quyu = str(self.lineEdit_2.text())
        if len(quyu.strip())==0:
            self.lineEdit_2.clear()
            self.lineEdit_2.setFocus(True)
        else:
            self.listWidget.addItem(self.tr(str(quyu.strip())))#添加到listWidget里
            self.lineEdit_2.clear()
            self.lineEdit_2.setFocus(True)
    
    #为某区域添加号数
    def addhaoshu(self):
        #获得当前的区域数
        quyuItem = self.listWidget.item(self.listWidget.currentRow())
        quyu = str(quyuItem.text())
        #添加号数
        haoshu = str(self.lineEdit_3.text())
        if len(haoshu.strip())==0:
            self.lineEdit_3.clear()
            self.lineEdit_3.setFocus(True)
        else:
            self.listWidget_2.addItem(self.tr(str(haoshu.strip())))
            self.haoshulist.append({'quyu':quyu,'haoshu':str(haoshu.strip())})
            self.lineEdit_3.clear()
            self.lineEdit_3.setFocus(True)
        
    def validate(self):
        #获取表单数据
        name = str(self.lineEdit.text())
        if(len(name.replace(' ', ''))==0):
            self.lineEdit.setFocus(True)
            self.boxInfo(u'提示',u'请输入仓库名称！')
            return False
        else:
            pass
        
        #获取所有仓库名称，与之匹配
        nameData = self.model.findAllStorageName()
        if nameData['stat']:
            for i in nameData['data']:
                if i['name']==name:
                    self.boxInfo(u'提示',u'名称已被占用，请重新输入！')
                    self.lineEdit.clear()
                    self.lineEdit.setFocus(True)
                    return False
        else:
            pass
        
        #区域listWidget不能为空
        quyucount = int(str(self.listWidget.count()))
        if quyucount==0:
            self.lineEdit_2.setFocus(True)
            self.boxInfo(u'提示',u'区域不能为空！')
            return False
        else:
            pass
        
        #号数listWidget不能为空
        haoshucount = int(str(self.listWidget_2.count()))
        if haoshucount==0:
            self.lineEdit_3.setFocus(True)
            self.boxInfo(u'提示',u'请选择区域并添加号数！')
            return False
        else:
            pass
        
        return True
    
    
    def tijiao(self):
        if self.validate():
            #获取仓库基本数据
            name = str(self.lineEdit.text())
            stat = str(self.comboBox.currentIndex())
            if stat=='0':
                stat='1'
            else:
                stat='0'
            #获取区域列表值
            for i in range(self.listWidget.count()):
                self.quyulist.append(str(self.listWidget.item(i).text()))
                
            re = self.model.insertStorage({'name':name,'stat':stat,'quyulist':self.quyulist,'haoshulist':self.haoshulist})
            self.boxInfo(u'提示',re['msg'])
            self.parent.init()
            self.close()
        else:
             pass   
         
         
         
    def cancel(self):
        self.close()
        

    
 