#coding:utf-8
'''
Created on 2015年1月20日

@author: kylin

主页底部

'''
from application.lib.Commethods import *
from application.view.main_bottom import Ui_Dialog
from application.lib.time_thread import TimeThread
import time

class MainBottom(ControllerAction,Ui_Dialog):
    def __init__(self,parent):
        ControllerAction.__init__(self, parent)
        self.setStyleSheet("background:#e2e0d9;")
        self.horizontalLayout.setContentsMargins(10, 10, 10, 10)
        self.label_4.setText(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
        self.timeThread = TimeThread()
        self.connect(self.timeThread,SIGNAL("pudateTime"),self.updateTime)
        self.timeThread.start()
        self.label_6.setText(unicode(ControllerAction.appdata['user']["nice_name"]))
        v = self.cf.get('ver', 'version')
        self.label.setText(self.tr(u'系统版本：' + v))
        
    def updateTime(self,data):
        self.label_4.setText(data)
                