#coding:utf-8

from application.lib.Commethods import *
from application.view.tixian import Ui_Dialog

class BangKa(ControllerAction,Ui_Dialog):
    
    def __init__(self,parent = None):
        ControllerAction.__init__(self, parent)
#         layout = QVBoxLayout(self)
#         btn = KButton(u"关闭当前")
#         layout.addWidget(btn)
        self.connect(self.pushButton, SIGNAL("clicked()"),self.closeTab)