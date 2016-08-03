# -*- coding: utf-8 -*-
'''
Created on 2015年4月9日

@author: huaan
'''
from PyQt4 import QtGui,QtCore
from application.lib.Commethods import *
from application.view.quxianpwd import Ui_Dialog
from application.controller.bank import BankController
from application.controller.grants import GrantContorller
from application.model.quxian_model import QuxianModel
from application.model.massage import MassageModel
import application.lib.formatCheck as check
import  time
import locale
from PyQt4.QtCore import QRegExp
_fromUtf8 = QtCore.QString.fromUtf8

class quXianPwdController(ControllerAction,Ui_Dialog):
    def __init__(self,parent=None,amount=0):
        ControllerAction.__init__(self,parent)
        self.parent=parent
        locale.setlocale(locale.LC_ALL, '') 
        self.label_6.setText(str(locale.format("%.2f", float(self.parent.memberamount), 1))+u'元')
        self.label_10.setText(self.tr(check.numtoCny(float(self.parent.memberamount))))
        self.showBank(0)
        self.bankCardCount = 0
        # 设置银行卡号只能输入数字和空格
        check.stringFilter(self.lineEdit_3, "[\d\s]+$")
#         check.stringFilter(self.qxBankNoidInput, "^[A-Za-z0-9]+$")
        check.stringFilter(self.money, "^[(\d*(,\d{3})*.(\d+)?)]+$")
        
        self.connect(self.pushButton,SIGNAL("clicked()"),self.checkQuXian)        #提交
        self.connect(self.money, SIGNAL("textChanged(QString)"), self.bigMoney)
        self.connect(self.money,SIGNAL("editingFinished()"),self.checkMoney)  #验证输入金额
        self.connect(self.lineEdit_3,SIGNAL("textChanged(QString)"),self.autoSpace)
        self.connect(self.comboBox,SIGNAL("currentIndexChanged(int)"),self.showBank)
        self.model = QuxianModel()
        
    def bigMoney(self, m):
        money=m.replace(',', '')
        if money:
            try:
                float(money)
                if float(money) <= 0:
                    self.boxWarning(u'提示',u'你输入的提现金额有误，请重新输入!')
                    return
            except:
                self.boxWarning(u'提示',u'你输入的提现金额有误，请重新输入!')
                return
            
            if float(self.parent.memberamount) < float(money):
                self.label_7.setText(self.tr(u'卡中余额不足!'))
                self.label_7.setStyleSheet(_fromUtf8("color:red\n" ""))
                return
            self.label_7.setText(self.tr(check.numtoCny(float(money))))
            self.label_7.setStyleSheet(_fromUtf8("color:black\n" ""))
        else:
            self.label_7.setText('')
        
        
    def autoSpace(self):
        self.bankCardCount = check.autoSpace(self.bankCardCount, self.lineEdit_3)
        
    # 银行卡取现显示银行卡相关信息    
    def showBank(self,index):
        if index == 1:
#             self.qxBankNoidLabel.show()
#             self.qxBankNoidInput.show()
            self.label_13.show()
            self.label_14.show()
            self.label_15.show()
            self.lineEdit.show()
            self.lineEdit_2.show()
            self.lineEdit_3.show()
            return
        self.qxBankNoidLabel.hide()
        self.qxBankNoidInput.hide()
        self.label_13.hide()
        self.label_14.hide()
        self.label_15.hide()
        self.lineEdit.hide()
        self.lineEdit_2.hide()
        self.lineEdit_3.hide()
    #验证取现金额并转成大写显示在界面
    def checkMoney(self):
        money=self.money.text().replace(',', '')
        if money:
            try:
                float(money)
                if float(money) <= 0:
                    self.boxWarning(u'提示',u'你输入的提现金额有误，请重新输入!')
                    return
            except:
                self.boxWarning(u'提示',u'你输入的提现金额有误，请重新输入!')
                return
            
            if float(self.parent.memberamount) < float(money):
                self.label_7.setText(self.tr(u'卡中余额不足!'))
                self.label_7.setStyleSheet(_fromUtf8("color:red\n" ""))
                return
            check.autoFormat(self.money, money)
            self.label_7.setText(self.tr(check.numtoCny(float(money))))
            self.label_7.setStyleSheet(_fromUtf8("color:black\n" ""))
        else:
            self.label_7.setText('')
    #验证密码，提现
    def checkQuXian(self):
        self.quxianMode=self.comboBox.currentIndex() #提现方式
        self.quxianMoney=str(self.money.text()).replace(',', '')           #提现金额
        quxianTxt=self.txt.toPlainText()             #备注
        try:
            if self.quxianMoney=='':
                self.boxWarning(u'提示',u'请输入提现金额')
                return
            float(self.quxianMoney)
        except:
            self.boxWarning(u'提示',u'请输入正确的提现金额！')
            self.money.setFocus()
            return
        if float(self.parent.memberamount) < float(self.quxianMoney):
            self.boxWarning(u'提示',u'卡中余额不足！')
            return
        
        if str(self.quxianMode)=='1':
#             if str(self.qxBankNoidInput.text())=='':
#                 self.boxWarning(u'提示',u'请输入银行卡提现流水号！')
#                 return
            if str(self.lineEdit.text())=='':
                self.boxWarning(u'提示',u'请输入银行名称！')
                return
            if str(self.lineEdit_2.text())=='':
                self.boxWarning(u'提示',u'请输入银行卡持卡人姓名！')
                return
            if str(self.lineEdit_3.text())=='':
                self.boxWarning(u'提示',u'请输入银行卡账号！')
                return
            if not self.boxConfirm(u'提示', u'请确认取款金额、银行卡信息，按“确定”取现', u'确定', u'取消'):
                return
            self.bankNo='-'
#             self.bankNo=str(self.qxBankNoidInput.text())
            self.bankName = str(self.lineEdit.text()).strip()
            self.bankUsername = str(self.lineEdit_2.text()).strip()
            self.bankCard = str(self.lineEdit_3.text()).strip()
            
            self.win = GrantContorller(self)
            self.win.show()
            self.close()
        else:
            if not self.boxConfirm(u'提示', u'请确认取款金额，按“确定”取现', u'确定', u'取消'):
                return
            self.bankNo=''
            self.bankName=''
            self.bankUsername=''
            self.bankCard=''
            self.data={'uid'   : str(self.appdata['user']['user_id']),
                       'cardid': str(self.parent.cardid.text()),
                       'ctype' : str(self.quxianMode),
                       'amount': str(self.quxianMoney),
                       'txt'   : str(quxianTxt),
                       'bankno': self.bankNo,
                       'bankname':self.bankName,
                       'bankusername':self.bankUsername,
                       'bankcard':self.bankCard,
                       'customerID':self.parent.memberId,
                       'toMobile':self.parent.customerInfos['tel'],
                       'customerName':self.parent.customerInfos['membername'],
                       'balance':float(self.parent.memberamount) - float(str(self.quxianMoney))}
            recvData = self.model.quxian(self.data)
            if recvData['stat']:
                '''
                # 短信
                self.msgData = {
                           'customerID':self.parent.memberId, 
                           'oparetion':u'现金提现',
                           'toMobile':self.parent.customerInfos['tel'],
                           'content':{'customerName':self.parent.customerInfos['membername'],
                                      'cardID':str(self.data['cardid']),
                                      'time':recvData['times'], 
                                      'amount':str(self.data['amount']),
                                      'balance':float(self.parent.memberamount) - float(self.data['amount'])
                                      }  # 短信内容参数
                           }
                if recvData['ctype'] == 1:
                    self.msgData['oparetion'] = u'银行卡提现'
                #验校发送短息的文本是否有效
                a = MassageModel()
                a.checkMessageText(self.msgData)
                '''
                self.txOK(recvData)
                self.close()
            else:
                self.txError(recvData['msg'].decode("utf8"))
                
    #提现失败提示
    def txError(self,data):
        self.boxWarning(u'提示',data)
    
    #提现成功
    def txOK(self,data):
        self.parent.dis()
        self.parent.inputcardid.setEnabled(False)
        self.parent.quxianMode=self.quxianMode             #提现方式
        self.parent.quxianMoney=self.quxianMoney           #提现金额
        self.parent.creattimes=data['times']              #提现时间
        self.parent.txData = self.data
        self.close()
        if self.boxConfirm(u'提示',u'提现成功，是否打印凭条？',u'是', u'否'):
        #打印
            self.parent.printquxian()

    def gart(self,data):
        quxianTxt=self.txt.toPlainText()             #备注
        self.data={'uid':str(self.appdata['user']['user_id']),
                   'cardid':str(self.parent.cardid.text()),
                   'ctype':str(self.quxianMode),
                   'amount':str(self.quxianMoney),
                   'txt':str(quxianTxt),
                   'bankno':self.bankNo,
                   'bankname':self.bankName,
                   'bankusername':self.bankUsername,
                   'bankcard':self.bankCard}
        recvData = self.model.quxian(self.data)
        if recvData['stat'] == True:
            self.txOK(recvData)
            self.close()
        else:
            self.txError(recvData['data']['msg'].decode("utf8"))
