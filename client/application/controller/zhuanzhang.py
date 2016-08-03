# -*- coding: utf-8 -*-
'''
Created on 2014年6月11日

@author: chenyong
'''
from application.lib.Commethods import *
from application.view.zhuanzhang import Ui_Dialog
from application.controller.zhuanzhangpassword import ZhuanZhangPasswordContorller
from application.lib.ImageProcess import ImageProcess
from application.model.zhuanzhang_model import ZhuanZhangModel
from application.controller.grants import GrantContorller
from application.model.massage import MassageModel
import application.lib.formatCheck as check

class ZhuanzhangContorller(ControllerAction,Ui_Dialog):
    def __init__(self,parent=None):
        ControllerAction.__init__(self,parent)
        self.parent=parent
        self.pwdNum = 0
        self.idcardImage = QImage(self.groupBox_4)            #加载转出人身份证图片
        self.idcardimageLabel=QLabel(self.groupBox_4)         #转出人身份证图像标签     
        self.zhaopian = QImage(self.widget)                   #加载转出人照片图片
        self.zhaopianimageLabel=QLabel(self.widget)           #转出人照片图像标签 
        
        self.idcardImage2 = QImage(self.groupBox_5)            #加载转入人身份证图片
        self.idcardimage2Label=QLabel(self.groupBox_5)         #转入人身份证图像标签     
        self.zhaopian2 = QImage(self.widget_2)                   #加载转入人照片图片
        self.zhaopianimage2Label=QLabel(self.widget_2)           #转入人照片图像标签 
        
        self.connect(self.inputzccardid, SIGNAL("returnPressed()"), self.expensesCard)      #查询支出卡号信息
        self.connect(self.inputzrcardid, SIGNAL("returnPressed()"), self.transferCard)      #查询转入卡号信息
        self.connect(self.commandLinkButton_2, SIGNAL("clicked()"),self.zhuanzhangSbumit)   #确认提交
        self.connect(self.money, SIGNAL("returnPressed()"), self.zhuanzhangSbumit)      #确认提交
        self.gant = False
        
        self.connect(self.webView, SIGNAL("loadProgress(int)"),self.init)   #打印替换内容
        filename = 'file:///'+os.getcwd()+'/print/print.html'
        self.webView.load(QUrl(filename.encode('cp936')))
        check.stringFilter(self.inputzccardid, "[\d\s]+$")
        check.stringFilter(self.inputzrcardid, "[\d\s]+$")
        check.stringFilter(self.money, "^\+?(\d*\.\d{2})$")
        
    #获取打印内容   
    def init(self,numbers):
        if numbers == 100:
            frame = self.webView.page().mainFrame()
            self.document = frame.documentElement()
        
    #查询支出卡号信息  
    def expensesCard(self):
        self.emptyMemberInfo()
        cardid=str(self.inputzccardid.text()) #转出账号
        self.model = ZhuanZhangModel()
        self.zcCardData = self.model.getCardInfo(cardid)
        if self.zcCardData['stat'] == 'True' :
            self.zcid = self.zcCardData['data']['id']
            self.zccard = self.zcCardData['data']['noid']
            self.fingers = [self.zcCardData['data']['finger1'], self.zcCardData['data']['finger2'], self.zcCardData['data']['finger3']]
            self.memberInfo(self.zcCardData['data'])
        else:
            self.boxWarning(u'提示',self.zcCardData['msg'])
            self.inputzccardid.setText("")
            self.inputzccardid.setFocus() 
            
    def pwdOk(self,child):
        child.close()
#         GrantContorller(self).exec_()
        self.grant = GrantContorller(self)
        self.grant.show()
    
    #查询转入卡号信息
    def transferCard(self):
           
        self.emptyMemberInfoTo()
        zr_card=str(self.inputzrcardid.text()) #转入账号
        if zr_card:
            if zr_card == self.inputzccardid.text():
                
                self.boxWarning(u'提示',u'同一张卡不可以转账')
                
                self.inputzrcardid.setText("") 
                self.inputzrcardid.setFocus() 
                return
            
            try:
                self.model = ZhuanZhangModel()
                data = self.model.getCardInfo(zr_card)
                if data['stat'] == 'True':
                    self.zrCardData = data['data']
                    self.zrid = data['data']['id']
                    self.zrcard = data['data']['noid'] 
                    self.memberInfoTo(data['data'])
                else:
                    self.boxWarning(u'提示',data['msg'])
                    self.inputzrcardid.setText("") 
                    self.inputzrcardid.setFocus() 
            except:
                self.boxWarning(u'提示',u'连接服务器超时，请重新登录！')
        else:
            self.boxWarning(u'提示',u'请刷入转入会员卡')
            self.inputzrcardid.setFocus() 
    #会员信息详情
    def GetCardInfo(self,data,act):
        if act=='transferCard':
            if type(data)==type({}):
                self.memberInfoTo(data)
                self.money.setFocus()
            else:
                self.boxWarning(u'提示',u'该转入会员卡号:'+data)
                self.inputzrcardid.setText('')
                self.inputzrcardid.setFocus()
            
        else:
            if type(data)==type({}):
                self.memberInfo(data)
                self.inputzrcardid.setFocus()
            else:
                self.boxWarning(u'提示',u'该转账会员卡号:'+data)
                self.inputzccardid.setText('')
                self.inputzccardid.setFocus()
    #显示转出人客户详细信息
    def memberInfo(self,data):
        self.expensesId=data['id']
        self.memberamount=data['amount']
        self.membername.setText(self.tr(str(data['membername'])))
        self.cardid.setText(self.tr(str(data['noid'])))
        self.sex.setCurrentIndex(int(data['sex']))
        self.tel.setText(self.tr(str(data['tel'])))
        self.nation.setText(self.tr(str(data['nation'])))
        self.idcard.setText(self.tr(str(data['idcard'])))
        self.adder.setText(self.tr(str(data['adder'])))
        self.amount.setText(self.tr(str(data['amount'])))
        self.lineEdit.setText(self.tr(str(data['freezen'])))
                    
        img=ImageProcess()
        if data['useimg_path']:
            fname = img.downloadImg(data['useimg_path'], 'useimg')
            img.showImage(fname,self.zhaopianimageLabel,self.zhaopian,0,0,170,170)
        if data['cardimg_path']:
            fname = img.downloadImg(data['cardimg_path'], 'cardimg')
            img.showImage(fname,self.idcardimageLabel,self.idcardImage,10,15,330,170)
    
    #清空转出人客户详情信息
    def emptyMemberInfo(self):
        self.membername.setText('')
        self.cardid.setText('')
        self.sex.setCurrentIndex(2)
        self.tel.setText('')
        self.nation.setText('')
        self.idcard.setText('')
        self.adder.setText('')
        self.amount.setText('')
        img=ImageProcess()
        img.showImage(os.getcwd()+'/image/111.png',self.zhaopianimageLabel,self.zhaopian,0,0,170,170)
        img.showImage(os.getcwd()+'/image/222.png',self.idcardimageLabel,self.idcardImage,10,15,330,170)
      
    #显示转入人客户详细信息
    def memberInfoTo(self,data):
        self.transferId=data['id']
        self.membername_2.setText(self.tr(str(data['membername'])))
        self.cardid_2.setText(self.tr(str(data['noid'])))
        self.sex_2.setCurrentIndex(int(data['sex']))
        self.tel_2.setText(self.tr(str(data['tel'])))
        self.nation_2.setText(self.tr(str(data['nation'])))
        self.idcard_2.setText(self.tr(str(data['idcard'])))
        self.adder_2.setText(self.tr(str(data['adder'])))
        self.amount_2.setText(self.tr(str(data['amount'])))
        self.lineEdit_2.setText(self.tr(str(data['freezen'])))
        
        img=ImageProcess()
        
        if data['useimg_path']:
            fname = img.downloadImg(data['useimg_path'], 'useimg2')
            img.showImage(fname,self.zhaopianimage2Label,self.zhaopian2,0,0,170,170)
        if data['cardimg_path']:
            fname = img.downloadImg(data['cardimg_path'], 'cardimg2')
            img.showImage(fname,self.idcardimage2Label,self.idcardImage2,10,15,330,170)
    #清空转入人客户详情信息
    def emptyMemberInfoTo(self):
        self.membername_2.setText('')
        self.cardid_2.setText('')
        self.sex_2.setCurrentIndex(2)
        self.tel_2.setText('')
        self.nation_2.setText('')
        self.idcard_2.setText('')
        self.adder_2.setText('')
        self.amount_2.setText('')
        img=ImageProcess()
        img.showImage(os.getcwd()+'/image/111.png',self.zhaopianimage2Label,self.zhaopian2,0,0,170,170)
        img.showImage(os.getcwd()+'/image/222.png',self.idcardimage2Label,self.idcardImage2,10,15,330,170)
    #确认转账
    def zhuanzhangSbumit(self):
        if self.cardid.text()=='':
            self.boxWarning(u'提示',u'转出会员卡不能为空！')
            return
        if self.cardid_2.text()=='':
            self.boxWarning(u'提示',u'转入会员卡不能为空！')
            return 
        if str(self.cardid.text())==str(self.cardid_2.text()):
            self.boxWarning(u'提示',u'转出卡号和转入会员卡不能相同！')
            return 
        else:
            self.zzMoney=self.money.text().replace(',','')
            if self.zzMoney=='':
                self.boxWarning(u'提示',u'转账金额不能为空！')
                self.money.setFocus()
                return
            else:
                try:
                    self.money.setText(str(locale.format("%.2f", float(str(self.zzMoney).replace(',', '')), 1)))
                except Exception as e:
                    print 'error:', e
                    self.boxWarning(u'提示',u'请输入正确的转账金额！')
                    self.money.setText('')
                    self.money.setFocus()
                    return
                if float(self.amount.text().replace(',','')) < float(self.zzMoney):
                    self.boxWarning(u'提示',u'转出卡余额不足')
                    return
                if float(self.zzMoney)<0.01:
                    self.boxWarning(u'提示',u'请输入正确的转账金额')
                    return
                check.autoFormat(self.money, self.zzMoney)
                
                self.ShowtransMemPwd()

    def gart(self,data):
        
        self.zdata ={'zccard':self.zccard,
                     'zrcard':self.zrcard,
                     'money':str(self.money.text()).replace(',',''),
                     'zcid':self.zcid,
                     'zrid':self.zrid,
                     'zctel':self.zcCardData['data']['tel'],
                     'zrtel':self.zrCardData['tel'],
                     'zcname':self.zcCardData['data']['membername'],
                     'zrname':self.zrCardData['membername'],
                     'zcbalance':float(self.zcCardData['data']['amount']) - float(self.zzMoney),
                     'zrbalance':float(self.zrCardData['amount']) + float(self.zzMoney),
                     'uid':self.appdata['user']['user_id']}
        data = self.model.transferMoney(self.zdata)
        self.boxWarning(u'提示',data['msg'])
        if not data['stat']:
            return
        self.ztime = data['time']
        self.printzhuanzhang()
        '''
        # 转出方短信
        self.msgData = {
                   'customerID':self.zcCardData['data']['id'],
                   'oparetion':u'转出',
                   'toMobile':self.zcCardData['data']['tel'],
                   'content':{'customerName':self.zcCardData['data']['membername'],
                              'cardID':str(self.zccard),
                              'time':data['time'],
                              'amount':str(self.zzMoney),
                              'balance':float(self.zcCardData['data']['amount']) - float(self.zzMoney)
                              }  # 短信内容参数
                   }
        #验校发送短息的文本是否有效
        MassageModel().checkMessageText(self.msgData)
        # 转入方短信
        self.msgData = {
                   'customerID':self.zrCardData['id'], 
                   'oparetion':u'转入',
                   'toMobile':self.zrCardData['tel'],
                   'content':{'customerName':self.zrCardData['membername'],
                              'cardID':str(self.zrcard),
                              'time':data['time'], 
                              'amount':str(self.zzMoney),
                              'balance':float(self.zrCardData['amount']) + float(self.zzMoney)
                              }  # 短信内容参数
                   }
        #验校发送短息的文本是否有效
        MassageModel().checkMessageText(self.msgData)
        '''
        if data['stat']:
            self.inputzccardid.setEnabled(False)
            self.inputzrcardid.setEnabled(False)
            self.money.setEnabled(False)
            self.commandLinkButton_2.setText(self.tr(u'重打印'))
            self.disconnect(self.commandLinkButton_2, SIGNAL('clicked()'), self.zhuanzhangSbumit)
            self.connect(self.commandLinkButton_2, SIGNAL("clicked()"),self.printzhuanzhang)   #确认提交
        
    #转账信息核对正确后输入转出卡号的密码
    def ShowtransMemPwd(self):
#         AdvancedQueryController(self,u"高级查询").show()
        ZhuanZhangPasswordContorller(self).exec_()
    #转账是否成功
    def transferInfo(self,data):
        if data['stat']:
            self.boxInfo(u'提示',data['msg'])
            self.commandLinkButton_2.setEnabled(False)
        else:
            self.boxWarning(u'提示',data['msg'])
            if data['msg']=='用户密码输入错误！':
                ZhuanZhangPasswordContorller(self).exec_()
            else:
                self.commandLinkButton_2.setEnabled(True)
                self.money.setEnabled(True)
                self.inputzccardid.setEnabled(True)
                self.inputzrcardid.setEnabled(True)

    #打印    
    def printzhuanzhang(self):
        self.printcdate=time.localtime(int(self.ztime))
        self.printcdate=time.strftime('%Y-%m-%d %H:%M',self.printcdate)
        self.document.evaluateJavaScript(self.tr("document.getElementById('a1').innerHTML = '时间：")+check.separate(self.tr(str(self.printcdate)))+"'") 
        self.document.evaluateJavaScript(self.tr("document.getElementById('a21').innerHTML = '时间：")+check.separate(self.tr(str(self.printcdate)))+"'") 
        self.document.evaluateJavaScript(self.tr("document.getElementById('a12').innerHTML = '金荣卡号：")+check.separate(self.cardid.text())+"'")   #转出卡号
        self.document.evaluateJavaScript(self.tr("document.getElementById('a23').innerHTML = '金荣卡号：")+check.separate(self.cardid.text())+"'")   #转出卡号
        self.document.evaluateJavaScript(self.tr("document.getElementById('a13').innerHTML = '转入卡号：")+check.separate(self.cardid_2.text())+"'")   #转入卡号
        self.document.evaluateJavaScript(self.tr("document.getElementById('a25').innerHTML = '转入卡号：")+check.separate(self.cardid_2.text())+"'")   #转入卡号
        self.document.evaluateJavaScript(self.tr("document.getElementById('a2').innerHTML = '户名：")+check.separate(self.membername.text())+"'")   #客户名
        self.document.evaluateJavaScript(self.tr("document.getElementById('a22').innerHTML = '户名：")+check.separate(self.membername.text())+"'")   #客户名
        self.document.evaluateJavaScript(self.tr("document.getElementById('a3').innerHTML = '转入户名：")+check.separate(self.membername_2.text())+"'")   #转入客户名
        self.document.evaluateJavaScript(self.tr("document.getElementById('a24').innerHTML = '转入户名：")+check.separate(self.membername_2.text())+"'")   #转入客户名
        self.document.evaluateJavaScript(self.tr("document.getElementById('a5').innerHTML = '备注：'"))  #备注
        self.document.evaluateJavaScript(self.tr("document.getElementById('a27').innerHTML = '备注：'"))   #备注
        self.document.evaluateJavaScript(self.tr("document.getElementById('a6').innerHTML = '复核：'")) #复核
        bigMoney = self.tr(check.numtoCny(float(self.zdata['money'])))
        zmoney=locale.format("%.2f",float(self.zdata['money']), 1)
        self.document.evaluateJavaScript(self.tr("document.getElementById('a4').innerHTML = '金额：")+check.separate(self.tr(self.zdata['money']))+"'") #充值金额
        self.document.evaluateJavaScript(self.tr("document.getElementById('a26').innerHTML = '金额：")+check.separate(self.tr(self.zdata['money']))+"'") #充值金额
        
        self.document.evaluateJavaScript(self.tr("document.getElementById('a14').innerHTML = '大写："
                                                 )+check.separate(bigMoney.left(11))+"'") #取款金额大写
        if bigMoney.length() > 11:
            self.document.evaluateJavaScript(self.tr("document.getElementById('a15').innerHTML = '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
                                                     )+check.separate(bigMoney.mid(11, 11))+"'") #取款金额大写
        if bigMoney.length() > 22:
            self.document.evaluateJavaScript(self.tr("document.getElementById('a16').innerHTML = '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
                                                     )+check.separate(bigMoney.mid(22, 11))+"'") #取款金额大写
            self.document.evaluateJavaScript(self.tr("document.getElementById('a17').innerHTML = '经办人："
                                                     )+check.separate(self.tr(str(self.appdata['user']['nice_name'])))+"'")   #经办人
        else:
            self.document.evaluateJavaScript(self.tr("document.getElementById('a16').innerHTML = '经办人："
                                                         )+check.separate(self.tr(str(self.appdata['user']['nice_name'])))+"'")   #经办人
        self.document.evaluateJavaScript(self.tr("document.getElementById('a11').innerHTML = '转账方式：转账'")) #支付方式
             
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