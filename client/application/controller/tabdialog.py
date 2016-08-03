#coding:utf-8

from application.lib.Commethods import *

from application.view.tabdialog import Ui_Dialog

class TabDialog(ControllerAction,Ui_Dialog):
    def __init__(self,parent = None):
        ControllerAction.__init__(self, parent)
        
