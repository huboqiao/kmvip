# -*- coding: utf-8 -*-
'''
Created on 2014年6月11日

@author: chenyong
'''
from application.lib.Commethods import *
import application.lib.formatCheck as check
from application.view.congZhi import Ui_Dialog
from application.model.congZhi_model import ChongZhiModel
from application.model.massage import MassageModel
from application.controller.grants import GrantContorller
import application.lib.formatCheck as check

class rechargeMoneyController(ControllerAction,Ui_Dialog):
    def __init__(self,parent=None):
        ControllerAction.__init__(self,parent)
        self.parent=parent
        self.title = u'充值'
        self.bankCardCount = 0
        self.moneyCount = 0
        check.stringFilter(self.money, "^\+?(\d*\.\d{2})$")
        check.stringFilter(self.lineEdit_4, "^[A-Za-z0-9]+$")
        
        self.label_6.setText(str(locale.format("%.2f", float(self.parent.memberamount), 1))+u'元')
        self.label_10.setText(self.tr(check.numtoCny(float(self.parent.memberamount))))
        self.connect(self.pushButton, SIGNAL('clicked()'),self.submitRecharge)
        self.connect(self.money,SIGNAL("textChanged(QString)"),self.checkMoney)  #验证输入金额
        self.connect(self.money,SIGNAL("editingFinished()"),self.autoFormat)  #验证输入金额
        self.connect(self.comboBox,SIGNAL("activated(int)"),self.showBank)
        self.comboBox.setCurrentIndex(1)
        
        #如果是银行卡转账填写转账卡的信息
#         self.showOrHideBankInfo('hide')
        self.model = ChongZhiModel()
        
    def showOrHideBankInfo(self, hide='hide'):
        if hide == 'hide':
            self.lineEdit_4.hide()
            self.label_13.hide()
        elif hide == 'show':
            self.lineEdit_4.show()
            self.label_13.show()
        else:
            self.boxWarning(u'提示', u'传入参数错误')
    
    def showBank(self,text):
        if text==1:
            self.showOrHideBankInfo('show')
        else:
            self.showOrHideBankInfo('hide')
    #验证充值金额并转成大写显示在界面
    def checkMoney(self, text=''):
        money=str(self.money.text()).replace(',', '')
        if money:
            try:
                self.label_7.setText(self.tr(check.numtoCny(float(money))))
            except:
                self.label_7.setText('')
        else:
            self.label_7.setText('')
            
    def autoFormat(self):
        money=str(self.money.text()).replace(',', '')
        check.autoFormat(self.money, money)
   
    #提交充值
    def submitRecharge(self):
        self.rechargeMode=self.comboBox.currentIndex()   #充值方式
        self.rechargeMoney=str(self.money.text()).replace(',', '').replace(' ', '')           #充值金额
        self.rechargeTxt=self.txt.toPlainText()               #备注
        try:
            if self.rechargeMoney=='':
                self.boxWarning(u'提示',u'请输入充值金额')
                return
            self.rechargeMoney = float(self.rechargeMoney)
        except:
            self.boxWarning(u'提示',u'请输入正确的充值金额！')
            self.money.setFocus()
            return 
        
        self.bankname=''       #开户行
        self.bankcard=''       #银行账户号
        self.bankusername=''   #开户人
        self.bankadder=''      #开户地址
        if str(self.rechargeMode)=='1':
            self.bankno=str(self.lineEdit_4.text())              #转账流水号
            if self.bankno=='':
                self.boxWarning(u'提示',u'请输入转账流水号！')
                return
#             adminAllowed = GrantContorller(self)
#             adminAllowed.exec_()
            self.gart(True)
        else:
            self.bankno=''         #转账流水号
            self.gart(True)

    def gart(self, allowed):
        if not allowed:
            self.boxWarning(u'提示', u'主管指纹不匹配')
            return
        amount = str(self.rechargeMoney)
        self.label_6.setText(str(locale.format("%.2f", float(self.parent.memberamount), 1))+u'元')
        if self.boxConfirm(u"提示",u"确定要提交充值   %s 元？"%locale.format('%.2f', float(amount), 1),u'确定', u'取消'):
            data={'uid':str(self.appdata['user']['user_id']),
                  'cardid':str(self.parent.cardid.text()),
                  'ctype':str(self.rechargeMode),
                  'amount':amount,
                  'txt':str(self.rechargeTxt),
                  'bankname':self.bankname,
                  'bankcard':self.bankcard,
                  'bankusername':self.bankusername,
                  'bankadder':'-',
                  'bankno':self.bankno,
                  'customerID':self.parent.memberId,
                  'toMobile':self.parent.customerInfos['tel'],
                  'customerName':self.parent.customerInfos['membername'],
                  'balance':float(self.parent.memberamount) + float(amount)}  
            self.parent.remark = data['txt']  
            #try:
            recvData = self.model.inRecharge(data)
            print 'recvData', recvData
            if recvData['stat']:
                '''
                # 转入方短信
                self.msgData = {
                           'customerID':self.parent.memberId, 
                           'oparetion':u'现金充值',
                           'toMobile':self.parent.customerInfos['tel'],
                           'content':{'customerName':self.parent.customerInfos['membername'],
                                      'cardID':str(data['cardid']),
                                      'time':recvData['times'], 
                                      'amount':str(data['amount']),
                                      'balance':float(self.parent.memberamount) + float(data['amount'])
                                      }  # 短信内容参数
                           }
                if recvData['ctype'] == 1:
                    self.msgData['oparetion'] = u'从银行卡充值'
                #验校发送短息的文本是否有效
                a = MassageModel()
                a.checkMessageText(self.msgData)
                '''
                self.rechargeOK(recvData)
            else:
                self.rechargeError(recvData['msg'].decode('utf8'))
            #except:
                #self.boxWarning(u'提示', u'连接服务器超时，请重新登录！')
    #充值失败提示
    def rechargeError(self,data):
        self.boxWarning(u'提示',data)
    #充值成功
    def rechargeOK(self,data):
        self.parent.creattimes=data['times']              #充值时间
        self.noid=data
#         self.parent.commandLinkButton_2.hide()   
#         self.parent.commandLinkButton_3.show()
        self.parent.commandLinkButton_2.setText(u'重打印')
        self.parent.dis()
#         self.connect(self.parent.commandLinkButton_2, SIGNAL("clicked()"),self.parent.printchongzhi)
        self.parent.inputcardid.setEnabled(False)
        self.parent.rechargeMode=self.rechargeMode       #充值方式
        self.parent.rechargeMoney= self.rechargeMoney    #充值金额
        self.parent.bankname=self.bankname               #开户行
        self.parent.bankcard=self.bankcard               #银行账户号
        self.parent.bankusername=self.bankusername       #开户人
        self.parent.bankno=self.bankno       #流水号
        self.parent.remark=self.rechargeTxt       #备注
        
        ControllerAction.closeTab(self)
        #打印小票
        if not self.boxConfirm(u'提示', u'充值成功！按确定后打印凭条。', u'确定', u'不打印'):
            self.close()
            return
        self.parent.printchongzhi()
        self.close()
  
            
            

            
        
     
            

          
        
            
            
        
