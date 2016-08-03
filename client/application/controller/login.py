#coding:utf-8
'''
Created on 2015年1月20日

@author: kylin

登陆窗口

'''
from application.lib.Commethods import *
from PyQt4 import QtGui
from application.view.login import Ui_Dialog
from application.model.login_model import LoginModel
from application.lib.commodel import getDataThread
from application.controller.fingerWindow import FingerWindow
import json

class Login(KLoginDialog, Ui_Dialog):
    def __init__(self,parent = None):
        KLoginDialog.__init__(self,parent)
        
        self.setupUi(self)
        self.updateLayout()
         
        self.setSignal()
        self.resizeAble = False
#         self.setCloseAble(widget, self)
    
    def setSignal(self):
        self.connect(self.pushButton, SIGNAL("clicked()"),self.login)
        self.connect(self.pushButton_2, SIGNAL("clicked()"),self.checkFinger)
        
    def updateLayout(self):
        
        self.setColor(QColor.fromRgb(239,235,231))
        
        self.setStyleSheet("QDialog{background:#efebe7;}")
        
        self.verticalLayout.setMargin(0)
        
        pixmap = QPixmap("./img/login_top.png")
        self.label.setPixmap(pixmap)
        
#         pixmap = QPixmap("./img/login_head.png")
#         self.label_2.setPixmap(pixmap)
        
#         self.label_2.setContentsMargins(20, 0, 20, 0)
        
        self.widget_2.setContentsMargins(0, 0, 20, 0)
        
        font = QFont()
        font.setPixelSize(14)
        
        self.label_3.setFont(font)
        self.label_4.setFont(font)
        self.label_3.setStyleSheet("font-family:Microsoft YaHei;")
        self.label_4.setStyleSheet("font-family:Microsoft YaHei;")
        
        self.pushButton = KPushButton()
        
        self.pushButton.loadPixmap("./img/login_btn.png")
        self.pushButton.loadText(u"登　  录")
        self.horizontalLayout_5.addWidget(self.pushButton,0,Qt.AlignLeft)
        
        self.pushButton.setStyleSheet("color:#fff;")
        
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem2)
        
        self.pushButton_2 = KPushButton()
        
        self.pushButton_2.loadPixmap("./img/login_btn.png")
        self.pushButton_2.loadText(u"指纹登录")
        self.horizontalLayout_5.addWidget(self.pushButton_2,0,Qt.AlignRight)
        
        self.pushButton_2.setStyleSheet("color:#fff;")
        
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem3)
        
        self.widget_7.setFixedHeight(30)
        self.widget_7.setStyleSheet("background:#c19753;")
#         self.horizontalLayout_5.removeWidget(self.pushButton)
    
    def login(self):
        self.setWidgetsEnable(False)
        username = str(self.lineEdit.text())
        passwd   = str(self.lineEdit_2.text())
        a = LoginModel()
        data = eval(a.login(username,passwd))
        if data['status'] != 1:
            ControllerAction().boxWarning(u'提示',data['msg'].decode("utf8"))
            self.setWidgetsEnable(True)
        else:
            ControllerAction.appdata['user'] = data
            odata={'user_id':str(data['user_id'])}
            data = {'node':'logic','act_fun':'getcurrentrole','data':odata}
            self.dayreportmodel = getDataThread(data,0,"getrolelist")
            self.connect(self.dayreportmodel,SIGNAL("getrolelist"),self.toAccept)
            self.dayreportmodel.start()
            
    def checkFinger(self):
        # 拉取所有用户指纹
        data = {'node':'logic','act_fun':'getGrantsFinger','data':''}
        self.dayreportmodel = getDataThread(data,0,"getGrantsFinger")
        self.connect(self.dayreportmodel, SIGNAL("getGrantsFinger"), self.matching)
        self.dayreportmodel.start()
        
    def checkPwd(self, data):
        if data['stat'] == 1:
            data = {'node':'logic','act_fun':'getInfosByFinger','data':data['finger']}
            self.dayreportmodel = getDataThread(data,0,"getInfosByFinger")
            self.connect(self.dayreportmodel, SIGNAL("getInfosByFinger"), self.fingerChecked)
            self.dayreportmodel.start()
        else:
            ControllerAction().boxWarning(u'提示', data['msg'])
            
    def fingerChecked(self, data):
        data = json.loads(data)
        ControllerAction.appdata['user'] = data
        odata={'user_id':str(data['user_id'])}
        data = {'node':'logic','act_fun':'getcurrentrole','data':odata}
        self.dayreportmodel = getDataThread(data,0,"getrolelist")
        self.connect(self.dayreportmodel,SIGNAL("getrolelist"),self.toAccept)
        self.dayreportmodel.start()
        
    def matching(self, data):
        self.fingers = []
        if data['stat']:
            for finger in data['data']:
                self.fingers.append(finger['finger'])
        FingerWindow(self, u'指纹登录').exec_()
        
    def toAccept(self,data):
        ControllerAction.appdata['user']['role_list'] = data['data']['role_list']
        ControllerAction.appdata['user']['finger'] = data['data']['finger']
        ControllerAction.app = ControllerAction.appdata
        self.accept()
        
    def setWidgetsEnable(self, statu=True):
        self.lineEdit.setEnabled(statu)
        self.lineEdit_2.setEnabled(statu)
        self.pushButton.setEnabled(statu)
