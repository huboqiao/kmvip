# -*- coding: utf-8 -*-
'''
Created on 2014年9月27日

@author: tang
'''
import time
from application.lib.Commethods import *
from application.view.cardpwd import Ui_Dialog
from application.lib.ImageProcess import ImageProcess
from application.controller.adminAllow import AdminAllow
from application.controller.pwdt import PwdtContorller
from application.controller.pwd import PwdContorller
from application.model.cardeditpwd_model import CardEidtPwdModel
import application.lib.formatCheck as check

class CardPwdContorller(ControllerAction,Ui_Dialog):
    def __init__(self,parent=None):
        ControllerAction.__init__(self, parent)
        self.parent=parent
        self.idcardImage = QImage(self.groupBox_4)            #加载身份证图片
        self.idcardimageLabel=QLabel(self.groupBox_4)         #身份证图像标签     
        self.zhaopian = QImage(self.widget)                   #加载照片图片
        self.zhaopianimageLabel=QLabel(self.widget)           #照片图像标签 
        self.model=CardEidtPwdModel()
        
        self.connect(self.inputcardid, SIGNAL("returnPressed()"), self.getMemberInfo)      #输入会员卡号验证后获取客户信息
        self.connect(self.pushButton_2, SIGNAL("clicked()"),self.fingerT)
        self.connect(self.pushButton, SIGNAL("clicked()"),self.fingerTw)
        self.connect(self.pushButton_3, SIGNAL("clicked()"), self.getMemberInfo)
        check.stringFilter(self.inputcardid, "[\d\s]+$")
        
    #输入会员卡号验证后获取客户信息   
    def getMemberInfo(self):
        self.emptyMemberInfo()
        cardid=str(self.inputcardid.text())
        if cardid:
            json=self.model.getCardInfo(cardid)
            if json['stat']==-1:
                self.boxWarning(u'提示',json['msg'])
                self.inputcardid.selectAll()
                return
            
            self.GetCardInfo(json)
            
        else:
            self.boxWarning(u'提示',u'请刷入要更改密码的会员卡卡号！')
    
    def fingerT(self):
        if self.membername.text() != '':
            win=AdminAllow(self)
            win.exec_()      
        else:
            self.boxWarning(u'提示', u'请读取金荣卡号') 
            self.inputcardid.selectAll()
    
    def fingerTw(self):
        if self.membername.text() != '':
            PwdtContorller(self).exec_()
        else:
            self.boxWarning(u'提示', u'请读取金荣卡号')
            self.inputcardid.selectAll()
              
    def gart(self,flag):
        if flag:
            PwdContorller(self).exec_()
    
    def postPwd(self,pwd):
        json=self.model.upCardPwd(str(self.cardid.text()),str(pwd))

        if json:
            self.boxInfo(u'提示',u'密码修改成功！')
            ControllerAction.closeTab(self)
            return
        else:
            self.boxWarning(u'提示',u'密码修改失败！')
    
    #显示客户详细信息
    def memberInfo(self,data):
        data=data['data']
        self.fingers = (data['finger1'], data['finger2'], data['finger3'])
        self.password = data['password']
        self.memberId=data['id']
        self.memberamount=data['amount']
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
        if data['useimg_path']:
            fname = img.downloadImg(data['useimg_path'], 'useimg_path')
            img.showImage(fname,self.zhaopianimageLabel,self.zhaopian,25,20,170,170)
        if data['cardimg_path']:
            fname = img.downloadImg(data['cardimg_path'], 'cardimg_path')
            img.showImage(fname,self.idcardimageLabel,self.idcardImage,25,30,370,170)

    #清空客户详情信息
    def emptyMemberInfo(self):
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
        else:
            self.memberInfo(data)
            
    #修改结果
    def memberPwd(self,data):
        if data:
            self.boxInfo(u'提示',u'修改密码成功！')
            ControllerAction.closeTab(self)
        else:
            self.boxWarning(u'提示',u'修改密码失败！')
        
