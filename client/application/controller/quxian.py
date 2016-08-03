# -*- coding: utf-8 -*-
'''
Created on 2014年6月11日

@author: chenyong
'''
from PyQt4 import QtGui
from application.lib.Commethods import *
from application.view.quxian import Ui_Dialog
from application.lib.ImageProcess import ImageProcess
from application.controller.quxianpwd import quXianPwdController
from application.lib.PrintMy import printer
import math,time,decimal,sys
from PyQt4.QtWebKit import *
from PyQt4 import QtNetwork
from application.controller.quxianpassword import QuXianPasswordContorller
import locale
from application.model.quxian_model import QuxianModel
from application.lib.commodel import getDataThread
import application.lib.formatCheck as check
from PyQt4 import QtCore

class QuxianContorller(ControllerAction,Ui_Dialog):
    def __init__(self,parent=None):
        ControllerAction.__init__(self,parent)
        self.parent=parent
        self.webView.hide()
        self.flag = True
        self.remark = ''
        self.idcardImage = QImage(self.groupBox_4)            #加载身份证图片
        self.idcardimageLabel=QLabel(self.groupBox_4)         #身份证图像标签     
        self.zhaopian = QImage(self.widget)                   #加载照片图片
        self.zhaopianimageLabel=QLabel(self.widget)           #照片图像标签 
        self.commandLinkButton_2.hide()                       #隐藏重打印按钮
        locale.setlocale(locale.LC_ALL, '') 
        self.commandLinkButton_3.setText(u'下一步')
        
        self.pwdNum=0       #记录用户输错密码次数
        
        self.connect(self.inputcardid, SIGNAL("returnPressed()"), self.getMemberInfo)      #输入会员卡号验证后获取客户信息
        self.connect(self.commandLinkButton_3, SIGNAL("clicked()"),self.nextWithdrawal)    #验证信息后进行取现下一步操作
        self.connect(self.webView, SIGNAL("loadProgress(int)"),self.init)                   #打印替换内容
        self.connect(self.lineEdit, SIGNAL("textChanged(QString)"), self.formatAmount)
        filename = 'file:///'+os.getcwd()+'/print/print.html'
        self.webView.load(QUrl(filename))
        
        check.stringFilter(self.inputcardid, "[\d\s]+$")
        check.stringFilter(self.lineEdit, "^\+?(\d*\.\d{2})$")
        
    def formatAmount(self, strs):
        print check.autoFormat(self.lineEdit, str(self.lineEdit.text()))
        
    def dis(self):
        self.commandLinkButton_3.setText(u'重打印')
        self.disconnect(self.commandLinkButton_3, SIGNAL("clicked()"),self.nextWithdrawal) 
        self.connect(self.commandLinkButton_3, SIGNAL("clicked()"),self.printquxian)
        
    #获取打印内容
    def init(self,numbers):
        if numbers == 100:
            frame = self.webView.page().mainFrame()
            self.document = frame.documentElement()
        
    #打印    
    def printquxian(self):
        self.printcdate=time.localtime(int(self.creattimes))
        self.printcdate=time.strftime('%Y-%m-%d %H:%M',self.printcdate)
        self.document.evaluateJavaScript(self.tr("document.getElementById('a1').innerHTML = '时间：")+check.separate(self.tr(str(self.printcdate)))+"'")
        self.document.evaluateJavaScript(self.tr("document.getElementById('a21').innerHTML = '时间：")+check.separate(self.tr(str(self.printcdate)))+"'")
        self.document.evaluateJavaScript(self.tr("document.getElementById('a12').innerHTML = '金荣卡号：")+check.separate(self.cardid.text())+"'")   #卡号
        self.document.evaluateJavaScript(self.tr("document.getElementById('a23').innerHTML = '金荣卡号：")+check.separate(self.cardid.text())+"'")   #卡号
        self.document.evaluateJavaScript(self.tr("document.getElementById('a2').innerHTML = '户名：")+check.separate(self.membername.text())+"'")
        self.document.evaluateJavaScript(self.tr("document.getElementById('a22').innerHTML = '户名：")+check.separate(self.membername.text())+"'")   #客户名
        idcard=str(self.idcard.text())
        idcard=idcard[0:10]+'****'+idcard[-4:]
        tel=str(self.tel.text())
        tel=tel[0:3]+'****'+tel[-4:]
        
        quxianMoney=decimal.Decimal(float(self.quxianMoney)).quantize(decimal.Decimal('0.01'))
        if self.quxianMode==0:
            self.document.evaluateJavaScript(self.tr("document.getElementById('a11').innerHTML = '取款方式：现金'")) #支付方式
            self.document.evaluateJavaScript(self.tr("document.getElementById('a24').innerHTML = '取款方式：现金'")) #支付方式
            self.document.evaluateJavaScript(self.tr("document.getElementById('a3').innerHTML = '金额：")+check.separate(self.tr(str(quxianMoney)))+"'") #取款金额
            self.document.evaluateJavaScript(self.tr("document.getElementById('a25').innerHTML = '金额：")+check.separate(self.tr(str(quxianMoney)))+"'") #取款金额
            self.document.evaluateJavaScript(self.tr("document.getElementById('a4').innerHTML = '备注：")+check.separate(self.tr(self.txData['txt']))+"'") #备注
            self.document.evaluateJavaScript(self.tr("document.getElementById('a26').innerHTML = '备注：")+check.separate(self.tr(self.txData['txt']))+"'") #备注
            self.document.evaluateJavaScript(self.tr("document.getElementById('a5').innerHTML = '复  核：'")) #复核
            bigMoney = self.tr(check.numtoCny(float(self.quxianMoney)))
            self.document.evaluateJavaScript(self.tr("document.getElementById('a13').innerHTML = '大写："
                                                     )+check.separate(bigMoney.left(11))+"'") #取款金额大写
            if bigMoney.length() > 11:
                self.document.evaluateJavaScript(self.tr("document.getElementById('a14').innerHTML = '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
                                                         )+check.separate(bigMoney.mid(11, 11))+"'") #取款金额大写
            if bigMoney.length() > 22:
                self.document.evaluateJavaScript(self.tr("document.getElementById('a15').innerHTML = '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
                                                         )+check.separate(bigMoney.mid(22, 11))+"'") #取款金额大写
                self.document.evaluateJavaScript(self.tr("document.getElementById('a16').innerHTML = '经办人："
                                                         )+check.separate(self.tr(str(self.appdata['user']['nice_name'])))+"'")   #经办人
            else:
                self.document.evaluateJavaScript(self.tr("document.getElementById('a15').innerHTML = '经办人："
                                                         )+check.separate(self.tr(str(self.appdata['user']['nice_name'])))+"'")   #经办人
        else:
            self.document.evaluateJavaScript(self.tr("document.getElementById('a11').innerHTML = '取款方式：银行卡'")) #支付方式
            self.document.evaluateJavaScript(self.tr("document.getElementById('a24').innerHTML = '取款方式：银行卡'")) #支付方式
            self.document.evaluateJavaScript(self.tr("document.getElementById('a3').innerHTML = '转入银行：")+check.separate(self.tr(self.txData['bankname']))+"'") #银行名称
            self.document.evaluateJavaScript(self.tr("document.getElementById('a25').innerHTML = '转入银行：")+check.separate(self.tr(self.txData['bankname']))+"'") #银行名称
            self.document.evaluateJavaScript(self.tr("document.getElementById('a14').innerHTML = '转入卡号：")+check.separate(self.tr(self.txData['bankcard']))+"'")         #银行账号
            self.document.evaluateJavaScript(self.tr("document.getElementById('a27').innerHTML = '转入卡号：")+check.separate(self.tr(self.txData['bankcard']))+"'")         #银行账号
            self.document.evaluateJavaScript(self.tr("document.getElementById('a4').innerHTML = '转入户名：")+check.separate(self.tr(self.txData['bankusername']))+"'")  #银行账户开户人
            self.document.evaluateJavaScript(self.tr("document.getElementById('a26').innerHTML = '转入户名：")+check.separate(self.tr(self.txData['bankusername']))+"'")  #银行账户开户人
            self.document.evaluateJavaScript(self.tr("document.getElementById('a5').innerHTML = '金额：")+check.separate(self.tr(str(quxianMoney)))+"'") #取款金额
            self.document.evaluateJavaScript(self.tr("document.getElementById('a28').innerHTML = '金额：")+check.separate(self.tr(str(quxianMoney)))+"'") #取款金额
            self.document.evaluateJavaScript(self.tr("document.getElementById('a6').innerHTML = '备注：")+check.separate(self.tr(self.txData['txt']))+"'") #备注
            self.document.evaluateJavaScript(self.tr("document.getElementById('a29').innerHTML = '备注：")+check.separate(self.tr(self.txData['txt']))+"'") #备注
            self.document.evaluateJavaScript(self.tr("document.getElementById('a7').innerHTML = '复  核：'")) #复核
            bigMoney = self.tr(str(check.numtoCny(float(self.quxianMoney))))
            self.document.evaluateJavaScript(self.tr("document.getElementById('a15').innerHTML = '大写："
                                                     )+check.separate(bigMoney.left(11))+"'") #取款金额大写
            if bigMoney.length() > 11:
                self.document.evaluateJavaScript(self.tr("document.getElementById('a16').innerHTML = '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
                                                         )+check.separate(bigMoney.mid(11, 11))+"'") #取款金额大写
            if bigMoney.length() > 22:
                self.document.evaluateJavaScript(self.tr("document.getElementById('a17').innerHTML = '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
                                                         )+check.separate(bigMoney.mid(22, 11))+"'") #取款金额大写
                self.document.evaluateJavaScript(self.tr("document.getElementById('a18').innerHTML = '经办人："
                                                         )+check.separate(self.tr(str(self.appdata['user']['nice_name'])))+"'")   #经办人
            else:
                self.document.evaluateJavaScript(self.tr("document.getElementById('a17').innerHTML = '经办人："
                                                         )+check.separate(self.tr(str(self.appdata['user']['nice_name'])))+"'")   #经办人
        #开始打印
        self.document.evaluateJavaScript("document.body.removeChild(document.getElementById('backimg'))")
        pname = self.cf.get('print_ini', 'defprint')
        if pname=='':
            self.boxWarning(u'提示',u'请选择打印机')
            return
        p = printer.printing(self.tr(pname))
        '保存打印信息到文件'
        try:
            self.webView.print_(p)
        except:
            self.boxWarning(u'提示', u'打印机未就绪，请检查打印服务是否开启')
            return
        self.boxWarning(u'提示',u'正在打印凭据，打印完成后请关闭此窗口！')
        
        
    #输入会员卡号验证后获取客户信息   
    def getMemberInfo(self):
        if self.flag == False:
            return
        self.emptyMemberInfo()
        cardid=str(self.inputcardid.text()).replace(' ','')
        try:
            int(cardid)
        except:
            self.boxWarning(u'提示',u'金荣卡号只能由数字组成，请确认！')
            self.inputcardid.setFocus()
            return
        if cardid:
            
            data={'node':'logic','act_fun':'getMemberInfo1','data':{'cardid':cardid, 'act':''}}
            self.threadmodel = getDataThread(data,0,"getMemberInfo1")
            self.connect(self.threadmodel,SIGNAL("getMemberInfo1"),self.memberInfo)
            self.flag = False
            self.threadmodel.start()
        else:
            self.boxWarning(u'提示',u'请刷入要取现的会员卡！')
    
    
    #显示客户详细信息
    def memberInfo(self,recvData):
        recvData = recvData
        self.flag = True
        if recvData['stat'] == -1:
            self.boxWarning(u'提示', recvData['msg'].decode('utf8'))
            return
        data = recvData['data']
        self.customerInfos = data
        self.fingers = [data['finger1'], data['finger2'], data['finger3']]
        if str(data['storename'])=='0':
            self.commandLinkButton_2.setText(u'农户取现')
        else:
            self.commandLinkButton_2.setText(u'商户取现')
        self.memberId=data['id']
        self.memberamount=data['amount']
        self.lineEdit.setText(self.tr(str(data['amount'])))
        self.freezen = data['freezen']
        self.commandLinkButton_2.setEnabled(True)
        self.membername.setText(self.tr(str(data['membername'])))
        self.cardid.setText(self.tr(str(data['noid'])))
        self.sex.setCurrentIndex(int(data['sex']))
        self.tel.setText(self.tr(str(data['tel'])))
        self.nation.setText(self.tr(str(data['nation'])))
        self.idcard.setText(self.tr(str(data['idcard'])))
        self.adder.setText(self.tr(str(data['adder'])))
        
        carddate=time.localtime(int(data['carddate']))
        carddate=time.strftime('%Y-%m-%d %H:%M:%S',carddate)
        self.carddate.setText(self.tr(str(carddate)))
        
        self.bankusername.setText(self.tr(str(data['bankusername'])))
        self.bankname.setText(self.tr(str(data['bankname'])))
        self.bankcard.setText(self.tr(str(data['bankcard'])))
        self.bankadder.setText(self.tr(str(data['bankadder'])))
        img=ImageProcess()
#        try:
        try:
            if data['useimg_path']:
                fname = img.downloadImg(data['useimg_path'], 'useimg')
                img.showImage(fname,self.zhaopianimageLabel,self.zhaopian,10,0,170,170)
            if data['cardimg_path']:
                fname = img.downloadImg(data['cardimg_path'], 'cardimg')
                img.showImage(fname,self.idcardimageLabel,self.idcardImage,25,20,370,170)
        except:
            pass
        if data['cardData'] != False:
            cardrecord=data['cardData']
            records_txt=u'充值记录<br/>'
            try:
                if cardrecord['cz']:
                    for i in range(len(cardrecord['cz'])):
                        cdate=time.localtime(int(cardrecord['cz'][i]['cdate']))
                        cdate=time.strftime('%Y-%m-%d %H:%M:%S',cdate)
                        if str(cardrecord['cz'][i]['ctype'])=='0':
                            records_txt+=str(cdate)+'  卡号:'+str(cardrecord['cz'][i]['cardid'])+',现金充值  '+str(locale.format("%.2f", float(cardrecord['cz'][i]['amount']), 1))+'元<br/>'
                        else:
                            records_txt+=str(cdate)+'  卡号:'+str(cardrecord['cz'][i]['cardid'])+',POS刷卡充值  '+str(locale.format("%.2f", float(cardrecord['cz'][i]['amount']), 1))+'元<br/>'
                else:
                    records_txt = ''
            except:
                records_txt = ''
            records_txt1=u'取现记录<br/>'
            try:
                if cardrecord['tx']:
                    for i in range(len(cardrecord['tx'])):
                        cdate=time.localtime(int(cardrecord['tx'][i]['cdate']))
                        cdate=time.strftime('%Y-%m-%d %H:%M:%S',cdate)
                        if str(cardrecord['tx'][i]['ctype'])=='0':
                            records_txt1+=str(cdate)+'  卡号:'+str(cardrecord['tx'][i]['cardid'])+',提现，现金提现 '+str(locale.format("%.2f", float(cardrecord['tx'][i]['amount']), 1))+'元<br/>'
                        else:
                            records_txt1+=str(cdate)+'  卡号:'+str(cardrecord['tx'][i]['cardid'])+',提现，银行卡转账  '+str(locale.format("%.2f", float(cardrecord['tx'][i]['amount']), 1))+'元<br/>'
                else:
                    records_txt1 = ''
            except:
                records_txt1 = ''
            records_txt2=u'转出记录<br/>'
            try:
                if cardrecord['zz']:
                    for i in range(len(cardrecord['zz'])):
                        cdate=time.localtime(int(cardrecord['zz'][i]['cdate']))
                        cdate=time.strftime('%Y-%m-%d %H:%M:%S',cdate)
                        records_txt2+=str(cdate)+'  卡号:'+str(cardrecord['zz'][i]['paycard'])+',转出'+str(locale.format("%.2f", float(cardrecord['zz'][i]['amount']), 1))+'元<br/>'
                else:
                    records_txt2 = ''
            except:
                records_txt2 = ''
            records_txt3=u'转入记录<br/>'
            try:
                if cardrecord['in']:
                    for i in range(len(cardrecord['in'])):
                        cdate=time.localtime(int(cardrecord['in'][i]['cdate']))
                        cdate=time.strftime('%Y-%m-%d %H:%M:%S',cdate)
                        records_txt3+=str(cdate)+'  卡号:'+str(cardrecord['in'][i]['paycard'])+',转入'+str(locale.format("%.2f", float(cardrecord['in'][i]['amount']), 1))+'元<br/>'
                else:
                    records_txt3 = ''
            except:
                records_txt3 = ''
                
            self.records_txt.setHtml(self.tr(str(records_txt)))
            self.records_txt_2.setHtml(self.tr(str(records_txt1)))
            self.records_txt_3.setHtml(self.tr(str(records_txt2)))
            self.records_txt_4.setHtml(self.tr(str(records_txt3)))
            self.lineEdit.setFocus()
    
    #清空客户详情信息
    def emptyMemberInfo(self):
        self.commandLinkButton_2.setEnabled(False)
        self.membername.setText('')
        self.cardid.setText('')
        self.sex.setCurrentIndex(2)
        self.tel.setText('')
        self.nation.setText('')
        self.idcard.setText('')
        self.adder.setText('')
        self.carddate.setText('')
        self.bankusername.setText('')
        self.bankname.setText('')
        self.bankcard.setText('')
        self.bankadder.setText('')
        img=ImageProcess()
        img.showImage(os.getcwd()+'/image/111.png',self.zhaopianimageLabel,self.zhaopian,10,0,170,170)
        img.showImage(os.getcwd()+'/image/222.png',self.idcardimageLabel,self.idcardImage,25,20,370,170)
        self.records_txt.setHtml(u'充值记录<br/>')
        self.records_txt_2.setHtml(u'取现记录<br/>')
        self.records_txt_3.setHtml(u'转出记录<br/>')
        self.records_txt_4.setHtml(u'转入记录<br/>')
    
    #接收会员卡查询返回来的客户信息详情
    def GetCardInfo(self,data):
        if type(data)!=type({}):
            self.boxWarning(u'提示',self.tr('该会员卡'+str(data)))
            self.inputcardid.setText('')
        else:
            self.memberInfo(data)
            
    #提现输入提现金额和密码   
    def nextWithdrawal(self):
        if self.cardid.text():
            try:
                if float(str(self.lineEdit.text())) == 0:
                    self.boxWarning(u'提示', u'可用余额为0，不能提现！')
                    return
            except:
                pass
            win=QuXianPasswordContorller(self)
            win.exec_()
        else:
            self.boxWarning(u'提示', u'请先输入金荣卡号后回车获取客户信息')
    
    #验证密码成功
    def pwdOk(self):
        self.txData = ''
        quXianPwdController(self, self.lineEdit.text()).exec_() 
