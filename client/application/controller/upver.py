# -*- coding: utf-8 -*-
'''
Created on 2014年10月30日

@author: ivan
'''
from PyQt4 import QtGui
from application.lib.Commethods import *
from application.view.upver import Ui_Dialog
from application.model.downloadModel import Download,VerCheck
from nt import getcwd
import os

class upVerController(ControllerAction,Ui_Dialog):
    def __init__(self,parent=None):
        ControllerAction.__init__(self,parent,title=u'系统更新')
        self.label_2.setText(self.tr(self.cf.get('ver', 'version')))
        self.ver = ''
        self.ver = VerCheck(self.cf,'checkver',self.cf.get('ver','version'))
        self.connect(self.ver, SIGNAL('checkver'),self.checkver)
        self.ver.start()
    
    def checkver(self,data):
        self.ver = data['version']
        self.label_4.setText(self.tr(self.ver))
        if data['flag'] == False:
            self.a = Download(self.cf,'download')
            self.connect(self.a,SIGNAL('download'),self.download)
            self.connect(self.a,SIGNAL('error'),self.error)
            self.a.start()  
        else:
            self.accept()
            self.boxWarning(u'提示', u"您的版本是最新的，无需更新！")
    
    def closeEvent(self,e):
        try:
            self.a.stoped = True
        except:
            pass
    
    def upok(self):
        self.cf.set('ver','version',self.ver)
        self.cf.write(open('config.ini',"w"))
        self.accept()
        self.boxWarning(u'提示', u'更新成功 ，重启程序后生效！')

    def error(self,data):
        self.boxInfo(u'提示', data)
        
    def download(self,datas):
        if datas == None: return
        loaded = float(datas['load'])
        self.progressBar.setProperty("value", loaded)
        if 100 == loaded:
            self.upok()
            self.disconnect(self.a, SIGNAL('download'), self.download)
            QApplication.exit()
            
