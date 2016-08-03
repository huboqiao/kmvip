# -*- coding: utf-8 -*-
'''
Created on 2015年3月2日

@author: LiuXinwu
'''
from PyQt4 import QtGui
from application.lib.Commethods import *
from application.lib.commodel import getDataThread
from application.view.useradd import Ui_Dialog
import hashlib,time,Image
import application.lib.formatCheck as check
from application.controller.camController import CamController
from application.lib.cam import CamClass
from application.controller.finger import FingerController
from application.lib.ImageProcess import ImageProcess
from application.model.grouplist_model import GroupListModel
from application.model.userlist_model import UserlistModel
from application.model.membermanager_model import MemberManagerModel
import application.lib.formatCheck as check

class UserEditController(ControllerAction,Ui_Dialog):
    def __init__(self,parent=None):
        ControllerAction.__init__(self,parent,title=u'修改用户')
        self.parent=parent
        self.pushButton_4.setText(self.tr(str("修改")))
        
        
        self.size = int(self.cf.get('cam','smalimagesize'))  
        self.idcardImage = QImage(self.shenfenzhengimage)           #加载身份证图片
        self.imageLabel2=QLabel(self.shenfenzhengimage)              #身份证图像标签     
        self.idcardImage_t = QImage(self.shenfenzhengimage_t)           #加载身份证图片
        self.imageLabel2_t=QLabel(self.shenfenzhengimage_t)              #身份证图像标签     
        self.t = QImage(self.groupBox)                  #加载照片图片
        self.imageLabel=QLabel(self.groupBox)           #照片图像标签 
        self.img=ImageProcess()
        self.groupmodel=GroupListModel()
        self.model=UserlistModel()
        self.fingerdata = ''                            #设置一个变量用来存储指纹       
        self.init1()
        self.membermodel=MemberManagerModel()
        
        self.connect(self.pushButton_4, SIGNAL("clicked()"),self.editUser)
        self.connect(self.shenfenzheng, SIGNAL("clicked()"),self.idcardImages)
        self.connect(self.shenfenzheng_t, SIGNAL("clicked()"),self.idcardImagest)
        self.connect(self.pushButton_6, SIGNAL("clicked()"),self.opencam)
        self.connect(self.pushButton_5, SIGNAL("clicked()"),self.winClose)
        self.connect(self.pushButton_8, SIGNAL("clicked()"),self.openFinger)
#         check.stringFilter(self.username, "[\d\s]+$")
        check.stringFilter(self.tel, "^[1][3-8]+\\d{9}$")
        check.stringFilter(self.card, "^[1-9]\d{5}[1-9]\d{3}((0\d)|(1[0-2]))(([0|1|2]\d)|3[0-1])\d{3}([0-9]|X)$")
        
    def init1(self):
        
        data={'node':'logic','act_fun':'getPow','data':''}
        self.threadmodel = getDataThread(data,0,"getPow")
        self.connect(self.threadmodel,SIGNAL("getPow"),self.fillGroup)
        self.threadmodel.start()
        
#         json=self.groupmodel.getPower()
        
    def fillGroup(self, data):
        self.upGroup(data['usergroup'])
        
    #打开指纹界面
    def openFinger(self):
        win=FingerController(self)
        win.exec_()
                
    #初始化用户
    def init(self):
        user_data=self.parent.userList_data
        for i in range(len(user_data)):
            if str(user_data[i]['id'])==str(self.parent.id):
                user_info=user_data[i]
                self.username.setText(self.tr(str(user_info['username'])))
                self.nickname.setText(self.tr(str(user_info['nickname'])))
                self.tel.setText(self.tr(str(user_info['tel'])))
                self.sex.setCurrentIndex(int(user_info['sex']))
                 
                self.tempd = {}
                for c_type in self.group_data:
                    self.group.addItem(c_type['group_name'])
                    self.tempd[c_type['group_name']]=c_type['id']
                     
                    if c_type['id'] == user_info['group']:
                        self.card_name = c_type['group_name']
                         
                self.group.setCurrentIndex(self.group.findText(self.card_name))
                self.hukou.setText(self.tr(str(user_info['hukou'])))
                self.adder.setText(self.tr(str(user_info['adder'])))
                self.card.setText(self.tr(str(user_info['card'])))
                self.comboBox.setCurrentIndex(user_info['righter'])
                try:
                    cardDate = check.timeStamp(user_info['birthday'], '%Y-%m-%d')
                    self.birthday.setDate(QDate().fromString(cardDate, "yyyy-MM-dd"))
                except:
                    cardDate = check.timeStamp(user_info['birthday'], '%Y/%m/%d')
                    self.birthday.setDate(QDate().fromString(cardDate, "yyyy/MM/dd"))
                    
                self.userid=self.parent.id
                self.fingerdata=user_info['finger']
                if user_info['cardimg_path']:
                    fname = self.img.downloadImg(user_info['cardimg_path'], 'cardimg')
                    try:
                        self.img.showImage(fname,self.imageLabel2,self.idcardImage,5,10,330,170)
                    except:
                        pass
                self.idcard_image_photo =user_info['cardimg_path']
                
                if user_info['useimg_path']:
                    fname = self.img.downloadImg(user_info['useimg_path'], 'useimg')
                    try:
                        self.img.showImage(fname,self.imageLabel,self.t,20,20,170,170)
                    except:
                        pass
                self.image_photo =user_info['useimg_path']
                
                if user_info['cardimgt_path']:
                    fname = self.img.downloadImg(user_info['cardimgt_path'], 'cardimgt')
                    try:
                        self.img.showImage(fname,self.imageLabel2_t,self.idcardImage_t,5,10,330,170)
                    except:
                        pass
                self.idcard_image_photot =user_info['cardimgt_path']
                  
    #更新group控件
    def upGroup(self,group_data):
        self.group_data=group_data
        self.init()
    #取消关闭窗口
    def winClose(self):
        self.close() 
     
    #修改用户
    def editUser(self):
        username=str(self.username.text())      #用户名
        nickname=str(self.nickname.text())      #真实姓名
        password=str(self.password.text())      #密码 
        password2=str(self.password2.text())    #确认密码
        tel=str(self.tel.text())                #联系电话
        sex=str(self.sex.currentIndex())        #性别（0：女，1：男）
        card=str(self.card.text())              #身份证
        group=str(self.group.currentText())
        group=self.tempd[unicode(group)]        #职位
        finger=self.fingerdata                  #指纹
        hukou=str(self.hukou.text())            #户籍
        adder=str(self.adder.text())            #住宅地址
        useimg=self.image_photo                 #用户图像
        cardimg=self.idcard_image_photo         #身份证图片
        cardimgt=self.idcard_image_photot       #身份证反面图片
        try:
            birthday=int(time.mktime(time.strptime(str(self.birthday.text()),'%Y/%m/%d')))
        except:
            birthday=int(time.mktime(time.strptime(str(self.birthday.text()),'%Y-%m-%d')))
            
        if username=='':
            self.boxWarning(u'提示', u'登录名不能为空！')
            return
        if nickname=='':
            self.boxWarning(u'提示', u'真实姓名不能为空！')
            return
        if password!='':
            if password!=password2:
                self.boxWarning(u'提示', u'两次输入的密码不一致！')
                return
        if tel=='':
            self.boxWarning(u'提示', u'联系电话不能为空！')
            return
        else:
            if QRegExp("1\d{10}|((0(\d{3}|\d{2}))-)?\d{7,8}(-\d*)?").indexIn(tel)<0:
                self.boxWarning(u'提示',u'请输入正确的电话')
                self.tel.setFocus()
                return
        if group=='0':
            group=str(1)
            # self.boxWarning(u'提示', u'请选择所在组！')
            # return
        if card=="":
            self.boxWarning(u'提示', u'请输入身份证号！')
            return
        else:
            if QRegExp("^[1-9]\d{7}((0\d)|(1[0-2]))(([0|1|2]\d)|3[0-1])\d{3}$").indexIn(card)<0 and \
                QRegExp("^[1-9]\d{5}[1-9]\d{3}((0\d)|(1[0-2]))(([0|1|2]\d)|3[0-1])\d{3}([0-9]|X)$").indexIn(card)<0 :
                self.boxWarning(u'提示', u'请输入正确的身份证号！')
                self.card.setFocus()
                return
        if finger=='':
            self.boxWarning(u'提示', u'请按指纹登记指纹！')
            return
        if cardimg=='':
            self.boxWarning(u'提示', u'请上传身份证正面图像！')
            return
        if cardimgt=='':
            self.boxWarning(u'提示', u'请上传身份证反面图像！')
            return
        #第一个用户不能修改所在组
        if str(self.userid)=='1':
            if str(group)!='1':
                self.boxWarning(u'提示', u'该用户不能修改其所在组！')
                return
        pwd=hashlib.md5()
        pwd.update(password)
        pwd.hexdigest()
        data_info={'card':card,'adder':adder,'birthday':birthday,'hukou':hukou,'useimg_path':useimg,'cardimg_path':cardimg,'cardimgt_path':cardimgt}
        if password=='':
            data={'userid':str(self.userid),'username':username,'nickname':nickname,'tel':tel,'sex':sex,'group':group,'finger':self.fingerdata, 'righter': self.comboBox.currentIndex()}
        else:
            data={'userid':str(self.userid),'username':username,'nickname':nickname,'tel':tel,'sex':sex,'group':group,'password':pwd.hexdigest(),'finger':self.fingerdata, 'righter': self.comboBox.currentIndex()}
#        try:
#            self.appdata['perspective'].callRemote('modifyUser',self,data,data_info)
#        except:
#            self.boxWarning(u'提示', u'连接服务器超时，请重新登录！')
        json=self.model.modifyUser(data,data_info)
        if json['stat'] == 1:
            self.boxInfo(u'提示',json['msg'].decode('utf8'))
            self.editUserSuccess()
        else:
            self.boxWarning(u'提示',json['msg'].decode('utf8'))
    
    #修改员工成功
    def editUserSuccess(self):
        self.parent.userInit()
        self.close()
        
    def opencam(self):
        cf = ConfigParser.ConfigParser()
        cf.read('config.ini')
        camint = int(cf.get('cam','camint'))
        self.cam = CamClass().getCam(camint)
        try:
            self.cam.getDisplayName()
        except:
            if camint != 0:
                try:
                    self.cam = CamClass().getCam(0)
                    self.cam.getDisplayName()
                except:
                    self.boxWarning(u'提示', u'未找到可用的成像设备，请检查设备驱动\n是否正常或添加成像设备并安装正确的驱动程序')
                    return
                    
                    
        win = CamController(self)
        win.exec_()
    
    #显示照片
    def showimage(self):
        self.img.showImage(os.getcwd()+'/image/s3.png',self.imageLabel,self.t,20,20,170,170) #显示照片
        self.image_photo =self.img.generatePictureCoding(os.getcwd()+'/image/s3.png') #将照片转换成字符
        data = self.membermodel.sendImg(self.image_photo)
        if data['stat'] == '-1':
            self.boxWarning(u'msg', data['msg'])
        else:
            self.image_photo = data['path']  


    #身份证图像
    def idcardImages(self):
        txt=str(QFileDialog.getOpenFileName(self,"Open file dialog","/",self.tr("Image Files(*.png *.jpg *.bmp)")))
        if txt:
            self.img.thumbnails(txt.encode('cp936'),os.getcwd()+'/image/s4.png',330,170) #生成身份证缩略图
            self.img.showImage(os.getcwd()+'/image/s4.png',self.imageLabel2,self.idcardImage,5,10,330,170) #显示身份证图片
            self.idcard_image_photo =self.img.generatePictureCoding(os.getcwd()+'/image/s4.png') #将身份证图片转换成字符
            data = self.membermodel.sendImg(self.idcard_image_photo)
            if data['stat'] == '-1':
                self.boxWarning(u'msg', data['msg'])
            else:
                self.idcard_image_photo = data['path']  
            
    #身份证反面图像
    def idcardImagest(self):
        txt=str(QFileDialog.getOpenFileName(self,"Open file dialog","/",self.tr("Image Files(*.png *.jpg *.bmp)")))
        if txt:
            self.img.thumbnails(txt.encode('cp936'),os.getcwd()+'/image/s4t.png',330,170) #生成身份证缩略图
            self.img.showImage(os.getcwd()+'/image/s4t.png',self.imageLabel2_t,self.idcardImage_t,5,10,330,170) #显示身份证图片
            self.idcard_image_photot =self.img.generatePictureCoding(os.getcwd()+'/image/s4t.png') #将身份证图片转换成字符
            data = self.membermodel.sendImg(self.idcard_image_photot)
            if data['stat'] == '-1':
                self.boxWarning(u'msg', data['msg'])
            else:
                self.idcard_image_photot = data['path']  
