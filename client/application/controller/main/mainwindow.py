#coding:utf-8
'''
Created on 2015年1月20日

@author: kylin

主窗口

'''
from application.lib.Commethods import *
from application.controller.main.main_menu import MainMenu
from application.controller.main.main_leftmenu import MainLeftMenu
from application.controller.main.main_bottom import MainBottom
from application.controller.tabdialog import TabDialog
from application.view.mainwindow import Ui_MainWindow
from application.controller.main.maintab import MainTab
from application.controller.main.main_tool import MainTool
from application.lib.servicecontroller import ServiceControl
from application.controller.main_order import MainOrder
from application.controller.upver import upVerController
from application.model.downloadModel import VerCheck
import ConfigParser

class MainWindow(KMainWindow,Ui_MainWindow):
    leftmenu = None
    global tab
    def __init__(self,parent = None):
        KMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.setColor(QColor.fromRgb(225,225,225))
        self.setStyleSheet("QMainWindow::{background:white;}")
        self.tab = KTabWidget()
        self.tab.setTabBar(KTabBar())
        self.tab.setTabsClosable(True)
        self.setCentralWidget(self.tab)
        ControllerAction.setTabWidget(self.tab)
        self.maintab = MainTab(self)
        self.tab.addTab(self.maintab,u"主页面")
        MainWindow.tab = self.tab
        self.connect(self.tab, SIGNAL("tabCloseRequested(int)"),self.closeTab)
        
        widget = KDialog()
        widget.is_move = False
        vlayout = QVBoxLayout()
        vlayout.setMargin(0)
        vlayout.setContentsMargins(0, 0, 0, 0)
        vlayout.setSpacing(0)
        vlayout.addWidget(MainMenu(self))
        widget.setLayout(vlayout)
        
        dock = KDockWidget()
        dock.setWidget(widget)
        dock.setAllowedAreas(Qt.TopDockWidgetArea)
        self.addDockWidget(Qt.TopDockWidgetArea, dock)
        
        dock2 = KDockWidget()
        leftmenu = MainLeftMenu(self)
        dock2.setWidget(leftmenu)
        dock2.setAllowedAreas(Qt.LeftDockWidgetArea)
        self.addDockWidget(Qt.LeftDockWidgetArea, dock2)
        self.connect(leftmenu, SIGNAL("btnClicked"), self.maintab.updateList)
        
        dock3 = KDockWidget()
        dock3.setWidget(MainBottom(self))
        dock3.setAllowedAreas(Qt.BottomDockWidgetArea)
        self.addDockWidget(Qt.BottomDockWidgetArea, dock3)
        
        self.setContentsMargins(0, 0, 0, 0)
        self.statusBar().hide()
        self.menuBar().hide()
        self.setStyleSheet("QMainWindow::separator{background: rgb(200, 200, 200);width: 0px;height: 0px;}");
        ControllerAction.tab = self.tab
        
        self.cf = ConfigParser.ConfigParser()
        self.cf.read('config.ini')
        self.ver = VerCheck(self.cf,'checkver',self.cf.get('ver','version'))
        self.connect(self.ver, SIGNAL('checkver'),self.checkver)
        self.ver.start()
    
    def checkver(self,data):
        ver = data['version']
        if data['flag'] == False:
            button = QMessageBox.question(self, u'提示', u'检测到新版本:%s，是否现在更新？'%ver, u'现在更新', u'以后更新')
            if button == 0:
                upVerController().exec_()
                
    def openPrint(self):
          
        #管理window服务
        serviceController = ServiceControl()
        #打印服务是否关闭
        if serviceController.isStop("Spooler"):
            #开启打印服务
            if not serviceController.start("Spooler"):
                print "开启服务失败"
                return


    def openTab(self, obj, string):
        for i in range(ControllerAction.tab.count()):
            if str(ControllerAction.tab.tabText(i)) == string:
                ControllerAction.tab.setCurrentIndex(i)
                break
        else:
            obj.setMargin(0)
            ControllerAction.tab.addTab(obj, string)
            nowTabId = ControllerAction.tab.count()-1
            obj.tabid = nowTabId
            ControllerAction.tab.setCurrentIndex(nowTabId)

    def closeTab(self,i):
        if i == 0:
            self.maintab.updateList(0)
            return
        self.tab.removeTab(i)
        
