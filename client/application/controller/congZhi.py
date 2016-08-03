# -*- coding: utf-8 -*-
'''
Created on 2014年6月11日

@author: chenyong
'''
from PyQt4 import QtGui
from application.lib.Commethods import *
from application.view.quxian import Ui_Dialog
from application.lib.ImageProcess import ImageProcess
from application.controller.rechargemoney import rechargeMoneyController
from application.lib.PrintMy import printer
from application.model.congZhi_model import ChongZhiModel
from PyQt4.QtWebKit import *
from PyQt4 import QtNetwork
import math

import time,math,decimal
import locale
from application.lib.formatCheck import check
import application.lib.formatCheck as checkBig
class CongZhiContorller(ControllerAction,Ui_Dialog):
    def __init__(self,parent=None):
        ControllerAction.__init__(self,parent)
        self.parent=parent
        self.lineEdit.hide()
        self.label_4.hide()
        self.groupBox_5.hide() # 隐藏交易记录
        self.commandLinkButton_3.hide()  #隐藏重打印按钮
        self.bankno = ''
        self.remark = ''
        locale.setlocale(locale.LC_ALL, '') 
        self.idcardImage = QImage(self.groupBox_4)            #加载身份证图片
        self.idcardimageLabel=QLabel(self.groupBox_4)         #身份证图像标签     
        self.zhaopian = QImage(self.widget)                   #加载照片图片
        self.zhaopianimageLabel=QLabel(self.widget)           #照片图像标签 
        
        self.setWindowTitle(u"会员卡充值")
        self.commandLinkButton_2.setGeometry(QRect(520,7, 121,41))
        self.commandLinkButton_2.setText(u'充值')

        self.commandLinkButton_3.setGeometry(QRect(520,7, 121,41))
        
        checkBig.stringFilter(self.inputcardid, "[\d\s]+$")
        self.connect(self.inputcardid, SIGNAL("returnPressed()"), self.getMemberInfo)      #输入会员卡号验证后获取客户信息
#         self.connect(self.inputcardid, SIGNAL("editingFinished()"), self.getMemberInfo)      #输入会员卡号验证后获取客户信息
        self.connect(self.commandLinkButton_2, SIGNAL("clicked()"),self.memberRecharge)    #验证信息后进行充值下一步操作
        self.connect(self.commandLinkButton_3, SIGNAL("clicked()"),self.printchongzhi)    #重打印
        
        self.connect(self.webView, SIGNAL("loadProgress(int)"),self.init)   #打印替换内容
        filename = 'file:///'+os.getcwd()+'/print/print.html'
        self.webView.load(QUrl(filename.encode('cp936')))
        self.model = ChongZhiModel()
    
    def dis(self):
        self.disconnect(self.commandLinkButton_2, SIGNAL('clicked()'), self.memberRecharge)
        self.connect(self.commandLinkButton_2, SIGNAL("clicked()"),self.printchongzhi)
    
    #获取打印内容   
    def init(self,numbers):
        if numbers == 100:
            frame = self.webView.page().mainFrame()
            self.document = frame.documentElement()
        
    #打印    
    def printchongzhi(self):
        self.printcdate=time.localtime(int(self.creattimes))
        self.printcdate=time.strftime('%Y-%m-%d %H:%M',self.printcdate)
        rechargeMoney=locale.format("%.2f",float(self.rechargeMoney), 1)
        self.document.evaluateJavaScript(self.tr("document.getElementById('a1').innerHTML = '时间：")+checkBig.separate(self.tr(str(self.printcdate)))+"'") 
        self.document.evaluateJavaScript(self.tr("document.getElementById('a21').innerHTML = '时间：")+checkBig.separate(self.tr(str(self.printcdate)))+"'") 
        self.document.evaluateJavaScript(self.tr("document.getElementById('a12').innerHTML = '金荣卡号：")+checkBig.separate(self.inputcardid.text())+"'")   #卡号
        self.document.evaluateJavaScript(self.tr("document.getElementById('a23').innerHTML = '金荣卡号：")+checkBig.separate(self.inputcardid.text())+"'")   #卡号
        self.document.evaluateJavaScript(self.tr("document.getElementById('a2').innerHTML = '户名：")+checkBig.separate(self.membername.text())+"'")   #客户名
        self.document.evaluateJavaScript(self.tr("document.getElementById('a22').innerHTML = '户名：")+checkBig.separate(self.membername.text())+"'")   #客户名
        self.document.evaluateJavaScript(self.tr("document.getElementById('a3').innerHTML = '金额：")+checkBig.separate(self.tr(str(rechargeMoney)))+"'") #充值金额
        self.document.evaluateJavaScript(self.tr("document.getElementById('a25').innerHTML = '金额：")+checkBig.separate(self.tr(str(rechargeMoney)))+"'") #充值金额
        bigMoney = self.tr(checkBig.numtoCny(float(self.rechargeMoney)))
        self.document.evaluateJavaScript(self.tr("document.getElementById('a13').innerHTML = '大写："
                                                 )+checkBig.separate(bigMoney.left(11))+"'") #取款金额大写
        if bigMoney.length() > 11:
            self.document.evaluateJavaScript(self.tr("document.getElementById('a14').innerHTML = '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
                                                     )+checkBig.separate(bigMoney.mid(11, 11))+"'") #取款金额大写
        if bigMoney.length() > 22:
            self.document.evaluateJavaScript(self.tr("document.getElementById('a15').innerHTML = '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
                                                     )+checkBig.separate(bigMoney.mid(22, 11))+"'") #取款金额大写
        if self.rechargeMode==0:
            self.document.evaluateJavaScript(self.tr("document.getElementById('a11').innerHTML = '充值方式：现金'")) #支付方式
            self.document.evaluateJavaScript(self.tr("document.getElementById('a24').innerHTML = '充值方式：现金'")) #支付方式
            self.document.evaluateJavaScript(self.tr("document.getElementById('a4').innerHTML = '备注：")+checkBig.separate(self.tr(str(self.remark)))+"'")   #备注
            self.document.evaluateJavaScript(self.tr("document.getElementById('a5').innerHTML = '复核：'")) #支付方式
            self.document.evaluateJavaScript(self.tr("document.getElementById('a26').innerHTML = '备注：")+checkBig.separate(self.tr(str(self.remark)))+"'")   #备注
            if bigMoney.length() > 22:
                self.document.evaluateJavaScript(self.tr("document.getElementById('a16').innerHTML = '经办人："
                                                         )+checkBig.separate(self.tr(str(self.appdata['user']['nice_name'])))+"'")   #经办人
            else:
                self.document.evaluateJavaScript(self.tr("document.getElementById('a15').innerHTML = '经办人："
                                                         )+checkBig.separate(self.tr(str(self.appdata['user']['nice_name'])))+"'")   #经办人
                
        else:
            self.document.evaluateJavaScript(self.tr("document.getElementById('a11').innerHTML = '充值方式：银行卡'")) #支付方式
            self.document.evaluateJavaScript(self.tr("document.getElementById('a24').innerHTML = '充值方式：银行卡'")) #支付方式
            self.document.evaluateJavaScript(self.tr("document.getElementById('a4').innerHTML = '流水号：")+checkBig.separate(self.tr(str(self.bankno)))+"'")  #流水号
            self.document.evaluateJavaScript(self.tr("document.getElementById('a26').innerHTML = '流水号：")+checkBig.separate(self.tr(str(self.bankno)))+"'")  #流水号
            self.document.evaluateJavaScript(self.tr("document.getElementById('a5').innerHTML = '备注：")+checkBig.separate(self.tr(str(self.remark)))+"'")   #备注
            self.document.evaluateJavaScript(self.tr("document.getElementById('a6').innerHTML = '复核：'")) #支付方式
            self.document.evaluateJavaScript(self.tr("document.getElementById('a27').innerHTML = '备注：")+checkBig.separate(self.tr(str(self.remark)))+"'")   #备注
            self.document.evaluateJavaScript(self.tr("document.getElementById('a16').innerHTML = '经办人："
                                                         )+checkBig.separate(self.tr(str(self.appdata['user']['nice_name'])))+"'")   #经办人
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
        self.emptyMemberInfo()
        cardid = str(self.inputcardid.text()).replace(' ','')
        try:
            int(cardid)
        except:
            self.boxWarning(u'提示',u'金荣卡号只能由数字组成，请确认！')
            self.inputcardid.setFocus()
            return
        if cardid:
            data = self.model.getCardInfo(cardid)
            self.GetCardInfo(data)
        else:
            self.boxWarning(u'提示',u'请刷入要取现的会员卡！')
    
    #显示客户详细信息
    def memberInfo(self,data):
        if data['stat'] == 'True':
            data = data['data']
        else:
            self.boxWarning(u'提示', data['msg'])
            return
#         if data['storename'] == 0:
#             self.commandLinkButton_2.setText(u'农户充值')
#         else:
#             self.commandLinkButton_2.setText(u'商户充值')
        self.customerInfos = data
        self.memberId=data['id']
        self.memberamount=data['amount']
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

        if data['cardimg_path']:
            fname = img.downloadImg(data['cardimg_path'], 'cardimg.png')
            img.showImage(fname,self.idcardimageLabel,self.idcardImage,25,20,370,170)
        if data['useimg_path']:
            fname = img.downloadImg(data['useimg_path'], 'useimg.png')
            img.showImage(fname,self.zhaopianimageLabel,self.zhaopian,10,0,170,170)
            
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
    
    #接收会员卡查询返回来的客户信息详情
    def GetCardInfo(self,data):
        if type(data)!=type({}):
            self.boxWarning(u'提示',self.tr('该会员卡'+str(data)))
            self.inputcardid.setText('')
        else:
            self.memberInfo(data)
            
    #核对信息后进行充值
    def memberRecharge(self):
        #
        if self.cardid.text():
            rechargeMoneyController(self).exec_()
        else:
            self.boxWarning(u'提示',u'请输入会员卡号！')
     