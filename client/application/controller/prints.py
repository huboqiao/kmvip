# -*- coding: utf-8 -*-
'''
Created on 2014年6月11日

@author: chenyong
'''
from application.lib.Commethods import *
from application.view.prints import Ui_Dialog
from application.lib.PrintMy import printer
import time,os
from PyQt4.QtWebKit import *
from PyQt4 import QtNetwork



class PrintContorller(ControllerAction,Ui_Dialog):
    def __init__(self,parent=None):
        ControllerAction.__init__(self,parent)
        self.setupUi(self)
        self.parent=parent
        self.connect(self.webView, SIGNAL("loadProgress(int)"),self.init)
        self.connect(self.pushButton, SIGNAL("clicked()"),self.printchongzhi)
        filename = 'file:///'+os.getcwd()+'/print/model.html'
        self.webView.load(QUrl(filename))
        
    def init(self,numbers):
        if numbers == 100:
            frame = self.webView.page().mainFrame()
            self.document = frame.documentElement()
            self.printcdate=time.localtime(int(time.time()))
            self.printcdate=time.strftime('%Y-%m-%d %H:%M:%S',self.printcdate)
            self.document.evaluateJavaScript("document.getElementById('cdate').innerHTML = '"+self.tr(str(self.printcdate))+"'")        
           
        
    #打印    
    def printchongzhi(self):
        
        self.document.evaluateJavaScript("document.getElementById('cardid').innerHTML = '"+self.tr(str(self.parent.cardid.text()))+"'")   #卡号
        self.document.evaluateJavaScript("document.getElementById('name').innerHTML = '"+self.tr(str(self.parent.membername.text()))+"'")   #客户名
        self.document.evaluateJavaScript("document.getElementById('money').innerHTML = '"+self.tr(str(float(self.parent.rechargeMoney)))+"'") #充值金额
        self.document.evaluateJavaScript("document.getElementById('upmomey').innerHTML = '"+self.tr(str(self.parent.numtoCny(float(self.parent.rechargeMoney))))+u'整'"'") #取款金额大写
        self.document.evaluateJavaScript("document.getElementById('popname').innerHTML = '"+self.tr(str(self.appdata['user_data_info']['user']['nickname']))+"'")   #经办人
        if self.parent.rechargeMode==0:
            self.document.evaluateJavaScript("document.getElementById('fangshi').innerHTML = '"+self.tr('现金')+"'") #支付方式
            self.document.evaluateJavaScript("document.getElementById('bankname').innerHTML = ''") #银行名称
            self.document.evaluateJavaScript("document.getElementById('bankid').innerHTML = ''")   #银行账号
            self.document.evaluateJavaScript("document.getElementById('bankuser').innerHTML = ''")  #银行账户开户名
        else:
            self.document.evaluateJavaScript("document.getElementById('fangshi').innerHTML = '"+self.tr('银行卡')+"'") #支付方式
            self.document.evaluateJavaScript("document.getElementById('bankname').innerHTML = '"+self.tr(str(self.parent.bankname.text()))+"'") #银行名称
            self.document.evaluateJavaScript("document.getElementById('bankid').innerHTML = '"+self.tr(str(self.parent.bankcard.text()))+"'")         #银行账号
            self.document.evaluateJavaScript("document.getElementById('bankuser').innerHTML = '"+self.tr(str(self.parent.bankusername.text()))+"'")  #银行账户开户人
             
        #开始打印
        self.document.evaluateJavaScript("document.body.removeChild(document.getElementById('bkimg'))")
        pname = self.cf.get('print_ini', 'defprint')
        p = printer.printing(pname)
        if not p:
            self.boxWarning(u'提示  ', u'打印失败，未找到可用的打印机！')
            return
        self.webView.print_(p)
    
    
        
        
       
        
     