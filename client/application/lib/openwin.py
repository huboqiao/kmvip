# -*- coding:utf8 -*-
'''
Created on 2013-7-8

@author: ivan
'''
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import os
class Openwin:
    def __init__(self,workspace):
        self.workspace = workspace
        pass
    
    def openWin(self,win):
        t = self.showWin(win)
        icon = QIcon()
        icon.addPixmap(QPixmap("image/logo.ico"), QIcon.Normal, QIcon.Off)
        t.setWindowIcon(icon)
        
        #重新置顶
        if not t.isTopLevel():
            t.hide()
            t.show()
            
    def showWin(self,win):
        check = self.checkWin(win)
        if check[0] == True:
            self.workspace.workspace.addWindow(check[1])
        return check[1]
    
    def checkWin(self,obj):
        for win in self.workspace.workspace.windowList():
            
            if win.windowTitle() == obj.windowTitle():
                #self.workspace.workspace.setActiveWindow(obj)
                return (False,win)
        return (True,obj)
        
    