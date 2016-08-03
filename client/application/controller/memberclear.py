# -*- coding: utf-8 -*-
'''
Created on 2015年3月4日
#注销客户
@author: LiuXinwu
'''
from PyQt4 import QtGui
from application.lib.Commethods import *
from application.view.bindingcard import Ui_Dialog
from application.lib.ImageProcess import ImageProcess
from application.model.customermodel import CustomerModel
from application.model.membermanager_model import *
from application.controller.grants import GrantContorller
import application.lib.formatCheck as check


class MemberClearController(ControllerAction,Ui_Dialog):
    def __init__(self,parent=None):
        ControllerAction.__init__(self,parent)
        self.parent = parent
        self.pushButton.setText(self.tr(str("注 销")))
        #显示图片
        self.idcardImage = QImage(self.groupBox_3)            #加载身份证图片
        self.idcardimageLabel=QLabel(self.groupBox_3)         #身份证图像标签     
        self.zhaopian = QImage(self.widget)                   #加载照片图片
        self.zhaopianimageLabel=QLabel(self.widget)           #照片图像标签 
        #初始化值
        self.amount = 0 
        self.actdate = 0
        #实例化model
        self.model = CustomerModel()
        self.model2 = MemberManagerModel()
        #绑定事件
        self.connect(self.lineEdit, SIGNAL("returnPressed()"), self.getMemberData)      #输入身份证验证后获取客户信息
        self.connect(self.pushButton, SIGNAL("clicked()"), self.logout)      #输入身份证验证后获取客户信息
        check.stringFilter(self.lineEdit, "^[1-9]\d{5}[1-9]\d{3}((0\d)|(1[0-2]))(([0|1|2]\d)|3[0-1])\d{3}([0-9]|X)$")
        
    #注销客户  授权  
    def logout(self):
        if self.validate():
            if self.idcard.text():
                #注销前，判断客户此时的状态
                if self.customerStat==3:
                    self.boxWarning(u'提示',u'用户已注销！')
                    return 
                if self.customerStat==2:
                    self.boxInfo(u'提示',u'用户冻结中,不可以注销！')
                    return 
                #客户绑定卡的情况下，注销
                if float(self.amount)<=0.01:
                    if self.boxConfirm(u"提示",u"是否确认注销？", u'确定 ', u'取消'):
                        win= GrantContorller(self)
                        win.exec_()
                else:
                   self.boxInfo(u'提示',u'客户卡内还有余额，请先取现后再注销！') 
        else:
            #客户还未绑定卡的情况下，注销
            if self.boxConfirm("提示", "确定是否注销？"):
                win= GrantContorller(self)
                win.exec_()
            
    #验证身份证
    def validate(self):
        idcard = str(self.lineEdit.text())
        if QRegExp("^[1-9]\d{7}((0\d)|(1[0-2]))(([0|1|2]\d)|3[0-1])\d{3}$").indexIn(idcard)<0 and \
                QRegExp("^[1-9]\d{5}[1-9]\d{3}((0\d)|(1[0-2]))(([0|1|2]\d)|3[0-1])\d{3}([0-9]|X)$").indexIn(idcard)<0:
            self.boxInfo(u'提示',u'请输入正确的身份证号码！')
            return False
        else:
            pass
#             按了注销按钮 再按回车键就是BUG了
#             if self.membername.text()=='':
#                 self.boxInfo("提示", u'请先按回车键，获得客户信息！')
        return True
    
    #获得客户基本信息与附加信息
    def getMemberData(self):
        if self.validate():
            idcard = str(self.lineEdit.text())
            customerData = self.model.findOneCustomer({'idcard':str(idcard)})
            if customerData['stat']:
                #清楚上次数据
                self.clearCustomerData()
                self.clearAdditionalData()
                self.fillSpace(customerData['data'])
            else:
                #清楚上次数据
                self.clearCustomerData()
                self.clearAdditionalData()
                self.boxWarning(u'警告',customerData['msg'])
        else:
            self.lineEdit.clear()
            self.lineEdit.setFocus(True)
    
       
    #清楚客户基本信息
    def clearCustomerData(self):
        self.membername.clear()
        self.cardid.clear()
        self.sex.setCurrentIndex(2)
        self.tel.clear()
        self.nation.clear()
        self.idcard.clear()
        self.adder.clear()
        self.carddate.clear()
     
    #清除客户附加信息
    def clearAdditionalData(self):
        self.relativesname.clear()
        self.relativessex.setCurrentIndex(2)
        self.relationship.clear()
        self.relationtem.clear()
        self.lineEdit_12.clear()
        self.lineEdit_13.clear()
        self.lineEdit_14.clear()
        self.lineEdit_15.clear()
        self.records_txt.clear()
        self.records_txt_2.clear()
        self.records_txt_3.clear()
        self.records_txt_4.clear()   
        #清空数据时，图片就用这个
        img=ImageProcess()
        img.showImage(os.getcwd()+'/image/111.png',self.zhaopianimageLabel,self.zhaopian,20,0,170,170)
        img.showImage(os.getcwd()+'/image/222.png',self.idcardimageLabel,self.idcardImage,60,20,360,150)
       
    #填充空格        
    def fillSpace(self,data):
        #获取客户的id，便于修改其状态
        self.user_id=str(data['id'])
        self.customerStat = data['stat']
        #获得客户挂失的时间
        self.actdate = data['actdate']
        #当账户处于冻结中，每次更新账户冻结期限是否已满。
        if self.customerStat==2:
            nowTime = int(time.time())
            if nowTime-self.actdate>=3*24*60*60:#期限已满，设为正常状态
                self.model.updateCustomerStat({'customerId':str(data['id'])})
                self.customerStat = 1           #将当前状态设为正常
        #获取客户余额
        self.amount = data['amount']
        #填充客户基本资料
        self.membername.setText(self.tr(str(data['membername'])))
        self.cardid.setText(self.tr(str('')))
        self.sex.setCurrentIndex(data['sex'])
        self.tel.setText(self.tr(str(data['tel'])))
        self.nation.setText(self.tr(str(data['nation'])))
        self.idcard.setText(self.tr(str(data['idcard'])))
        self.adder.setText(self.tr(str(data['adder'])))
        try:
            cd = time.strftime('%Y-%m-%d',time.localtime(float(data['carddate'])))
            self.carddate.setText(self.tr(str(cd)))
        except:
            cd = time.strftime('%Y/%m/%d',time.localtime(float(data['carddate'])))
            self.carddate.setText(self.tr(str(cd)))
        #填充客户附加信息
        cid = data['id']
        self.id = cid
        additionalCustomerData = self.model.findOneCustomerAdditional({'cid':str(cid)})
        if additionalCustomerData['stat']:
            data2 = additionalCustomerData['data']
            try:
                #显示头像图片
                img = ImageProcess()
                if data2['useimg_path']:
                    fname = img.downloadImg(data2['useimg_path'], 'useimg.png')
                    if fname != False:
                        img.showImage(fname,self.zhaopianimageLabel,self.zhaopian,20,0,170,170)
                #显示身份证图片
                if data2['cardimg_path']:
                    fname = img.downloadImg(data2['cardimg_path'], 'cardimg.png')
                    img.showImage(fname,self.idcardimageLabel,self.idcardImage,60,20,360,150)
            except:
                pass
            
            if data2['relativesname'] == None:
                 self.relativesname.setText(self.tr(str('')))
            else:
                self.relativesname.setText(self.tr(str(data2['relativesname'])))
            self.relativessex.setCurrentIndex(data2['relativessex'])
            if data2['relationship'] == None:
                self.relationship.setText('')
            else:
                self.relationship.setText(self.tr(str(data2['relationship'])))
            if data2['relationtem'] == None:
                self.relationtem.setText('')
            else:
                self.relationtem.setText(self.tr(str(data2['relationtem'])))
            if data2['bankusername']==None:
                self.lineEdit_12.setText(self.tr(str('')))
            else:
                self.lineEdit_12.setText(self.tr(str(data2['bankusername'])))
            if data2['bankname']==None:
                self.lineEdit_13.setText(self.tr(str('')))
            else:
                self.lineEdit_13.setText(self.tr(str(data2['bankname'])))
            if data2['bankcard']==None:
                self.lineEdit_14.setText(self.tr(str('')))
            else:
                self.lineEdit_14.setText(self.tr(str(data2['bankcard'])))
            if data2['bankadder']==None:
                self.lineEdit_15.setText(self.tr(str('')))
            else:
                self.lineEdit_15.setText(self.tr(str(data2['bankadder'])))
        else:
            #清空附加信息表数据
            self.clearAdditionalData()
            
        #查询会员卡号
        uid = data['id']
        cardData = self.model.findCardWithUid({'uid':str(uid)})
        if cardData['stat']:
            data3 = cardData['data']
            if str(data3['noid']).replace(' ', '') == '1000000000':
                self.boxWarning(u'提示', u'公司账号不可注销')
                ControllerAction.closeTab(self)
                return
            self.cardid.setText(self.tr(str(data3['noid'])))
            self.cardStat = data3['stat']
        else:
            self.cardid.setText(self.tr(str('')))
            self.boxWarning(u'警告',cardData['msg'])
            
        #显示此卡近期交易信息
        self.records_txt.clear()
        self.records_txt_2.clear()
        self.records_txt_3.clear()
        self.records_txt_4.clear()
        if self.cardid.text()!='':
            if self.cardStat==1:
                g = self.model.getMemberInfo2({'cardid':str(self.cardid.text()), 'act':''})
                self.memberInfo(g)
            else:
                if self.cardStat==3:
                    self.boxWarning(u'提示',u'用户绑定卡已冻结！')
                    return 
                if self.cardStat==4:
                    self.boxInfo(u'提示',u'用户绑定卡已登记挂失！')
                    return 
                if self.cardStat==2:
                    self.boxInfo(u'提示',u'用户绑定卡已注销！')
                    return 
            
            
    def memberInfo(self,recvData):
        self.flag = True
        if recvData['stat'] == -1:
            #self.boxWarning(u'提示', recvData['msg'].decode('utf8'))
            return
        data = recvData['data']
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
       
       
    def gart(self,data):
       if data: 
           datas = {'cid': str(self.user_id), 'noid':str(self.cardid.text()), 'uid':self.appdata['user']['user_id']}
           json=self.model2.offCustomer(datas)
           if  json:
               self.boxInfo(u'提示',u'注销成功！')
               ControllerAction.closeTab(self)
           else:
               self.boxWarning(u'提示',u'注销失败！')
        