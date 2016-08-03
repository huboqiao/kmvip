# -*- coding: utf-8 -*-
'''
Created on 2014年9月26日

@author: kylin
'''
from application.lib.Commethods import *
from application.view.setting import Ui_Dialog
from application.lib.PrintMy import printer
from application.lib.cam import CamClass
import application.lib.formatCheck as check


class SettingController(ControllerAction,Ui_Dialog):
    def __init__(self,parent=None):
        ControllerAction.__init__(self,parent)
        self.connect(self.pushButton,SIGNAL("clicked()"),self.btnUp)
        self.connect(self.pushButton_2,SIGNAL("clicked()"),self.winClose)
        self.printList = printer.printerList()
        self.upSetting()
        check.stringFilter(self.lineEdit, "((?:(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))\.){3}(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d))))")
        check.stringFilter(self.lineEdit_2, "[\d\s]+$")
        check.stringFilter(self.lineEdit_3, "[\d\s]+$")
        check.stringFilter(self.lineEdit_4, "[\d\s]+$")
#         check.stringFilter(self.doubleSpinBox_2, "^\+?(\d*\.\d{2})$")
#         check.stringFilter(self.doubleSpinBox, "^\+?(\d*\.\d{2})$")
        
    def winClose(self):
        ControllerAction.closeTab(self)
    
    def btnUp(self):
        if self.comboBox.currentText() == self.tr('请选择'):
            self.boxWarning(u'提示', u'请选择默认打印机')
            self.comboBox.setFocus()
        else:
            self.cf.set('print_ini', 'defprint', self.comboBox.currentText())
            self.cf.set('server', 'ip', self.lineEdit.text())
            self.cf.set('server', 'port', self.lineEdit_2.text())
            self.cf.set('cam', 'speed', self.doubleSpinBox_2.text())
            self.cf.set('cam', 'quality',int(float(self.doubleSpinBox.text())))
            self.cf.set('cam', 'userimagesize', self.lineEdit_3.text())
            self.cf.set('cam', 'cardimagesize', self.lineEdit_4.text())
            self.cf.set('cam', 'camint', str(self.comboBox_2.currentIndex()))
            self.cf.write(open('config.ini',"w"))
            self.boxInfo(u'提示',u'设置成功！')
            ControllerAction.closeTab(self)
        
    def upSetting(self):
        j = 1
        for i in self.printList:
            self.comboBox.addItem("")
            self.comboBox.setItemText(j, self.tr(str(i)))
            j += 1
        print self.cf.get('print_ini','defprint')
        self.comboBox.setCurrentIndex(int(self.comboBox.findText(self.tr(self.cf.get('print_ini','defprint'))))) 
        self.lineEdit.setText(self.cf.get('server','ip'))
        self.lineEdit_2.setText(self.cf.get('server','port'))
        self.doubleSpinBox.setProperty("value", str(self.cf.get('cam','quality')))
        self.doubleSpinBox_2.setProperty("value", float(self.cf.get('cam','speed')))
        self.lineEdit_3.setText(str(self.cf.get('cam','userimagesize')))
        self.lineEdit_4.setText(str(self.cf.get('cam','cardimagesize')))
        for i in range(0, 10):
            try:
                if i != 0:
                    if str(CamClass().getCam(i).getDisplayName()) == str(self.comboBox_2.currentItemName()):
                        break
                self.comboBox_2.addItem(self.tr(CamClass().getCam(i).getDisplayName()))
                i += 1
            except:
                if i == 0:
                    self.boxWarning(u'提示', u'未找到可用的成像设备，请检查设备驱动\n是否正常或添加成像设备并安装正确的驱动程序')
                break
        try:
            self.comboBox_2.setCurrentIndex(int(self.cf.get('cam','camint')))
        except:
            pass
        