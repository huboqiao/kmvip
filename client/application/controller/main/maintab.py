#coding:utf-8
'''
Created on 2015骞�鏈�0鏃�

@author: kylin

涓籘ab

'''
from application.lib.Commethods import *
from application.view.maintab import Ui_Dialog
from application.controller.main_order import MainOrder
from application.lib.commodel import getDataThread
from application.lib.power import PowerAct
from application.controller.checkMemberID import CheckMemberID
from application.controller.main.main_leftmenu import MainLeftMenu
from application.controller.shopsys import ShopSysController
from application.controller.upver import upVerController


class MainTab(ControllerAction):
    def __init__(self,parent = None):
        ControllerAction.__init__(self, parent)
        self.btnList = []
        self.parent = parent
        
        pid = 0
        self.a = getDataThread({'node':'logic','act_fun':'getUserAndAdmin','data':self.appdata['user']['user_name']},pid,'updateStaturBar')
        self.connect(self.a, SIGNAL('updateStaturBar'),self.updateStaturBar)
        self.a.start()  
        
        MainOrder.addMainTab(self)
        self.updateList(0)
       
    def clearList(self):
        self.parent.tab.setCurrentIndex(0)
        for i in self.btnList:
#             i.setParent(None)
            self.gridLayout.removeWidget(i)
            i.deleteLater()
             
        self.btnList = []
        self.update()
        
    def updateList(self,ids):
        self.clearList()
        btnList = MainOrder.order(ids)
        try:
            self.parent.tab.setTabText(0, self.tr(MainLeftMenu.names[ids]))
        except:
            pass
        for key,i in enumerate(btnList):
            btn = KPushButton()
            btn.title = i['title']
            btn.loadPixmap(i['img'])
            btn.window = i['window']
            self.gridLayout.addWidget(btn,key//3,key%3,1,1)
            self.btnList.append(btn)
            self.connect(btn,SIGNAL("clicked()"),self.openTab)

    def keyPressEvent(self,event):
        if event.key() == Qt.Key_Escape:
            return
        return QDialog.keyPressEvent(self,event)
            
    def openTab(self):
        #鍦ㄨ繖閲屽仛鏉冮檺鍒ゆ柇
        print self.sender().title
        if MainTab.pow.matching(self.sender().title):
            if cmp(self.sender().title.decode('utf8'), u'修改客户资料') == 0:
                if not CheckMemberID().exec_():
                    return
            if cmp(self.sender().title.decode('utf-8'), u'锁屏') == 0:
                ShopSysController(self).exec_()
                return
            if cmp(self.sender().title.decode('utf-8'), u'系统更新') == 0:
                upVerController(self).exec_()
                return
            self.parent.openTab(self.sender().window(),self.sender().title)
        else:
            self.infoBox(u'您没有权限使用该功能！')
            
    def updateStaturBar(self,data):
        self.appdata['user_data_info']=data
        MainTab.pow = PowerAct(self.appdata['user']['role_list'],self.appdata['user_data_info']['resource'])
