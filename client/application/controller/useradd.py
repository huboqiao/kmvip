# -*- coding: utf-8 -*-
'''
Created on 2015年3月2日

@author: LiuXinwu
'''
from PyQt4 import QtGui
from application.lib.Commethods import *
from application.view.useradd import Ui_Dialog
from PyQt4.Qt import SIGNAL
import hashlib,time,Image
from application.lib.commodel import getDataThread
from application.controller.finger import FingerController
from application.controller.camController import CamController
from application.lib.cam import CamClass
from application.lib.ImageProcess import ImageProcess
from application.model.userlist_model import UserlistModel
from application.model.grouplist_model import GroupListModel
from application.model.memberAdd_model import MemberAddModel
import application.lib.formatCheck as check

class UserAddController(ControllerAction,Ui_Dialog):
    def __init__(self,parent=None):
        ControllerAction.__init__(self,parent,title=u'添加用户')
        self.parent = parent
        
        self.model=UserlistModel()
        self.groupmodel=GroupListModel()
        self.comboBox.setCurrentIndex(0)
        self.init()
        self.connect(self.pushButton_4, SIGNAL("clicked()"),self.addUser)
        self.connect(self.shenfenzheng, SIGNAL("clicked()"),self.idcardImages)
        self.connect(self.shenfenzheng_t, SIGNAL("clicked()"),self.idcardImagest)
        self.connect(self.pushButton_6, SIGNAL("clicked()"),self.opencam)
        self.connect(self.pushButton_5, SIGNAL("clicked()"),self.winClose)
        self.connect(self.pushButton_8, SIGNAL("clicked()"),self.openFinger)
        self.size = int(self.cf.get('cam','smalimagesize'))  
        self.img=ImageProcess()
        self.membermodel = MemberAddModel()
        self.image_photo =''   
        self.idcard_image_photo=''
        self.idcard_image_photot=''
        self.idcardImage = QImage(self.shenfenzhengimage)          #加载身份证图片
        self.imageLabel2=QLabel(self.shenfenzhengimage)            #身份证图像标签 
        self.idcardImage_t = QImage(self.shenfenzhengimage_t)          #加载身份证反面图片
        self.imageLabel2_t=QLabel(self.shenfenzhengimage_t)            #身份证反面图像标签         
        self.t = QImage(self.groupBox)                  #加载照片图片
        self.imageLabel=QLabel(self.groupBox)           #照片图像标签 
        self.fingerdata = ''                            #设置一个变量用来存储指纹    
#         check.stringFilter(self.username, "[\d\s]+$")
        check.stringFilter(self.tel, "^[1][3-8]+\\d{9}$")
        check.stringFilter(self.card, "^[1-9]\d{5}[1-9]\d{3}((0\d)|(1[0-2]))(([0|1|2]\d)|3[0-1])\d{3}([0-9]|X)$")
        
        
    def init(self):
        
        data={'node':'logic','act_fun':'getPow','data':''}
        self.threadmodel = getDataThread(data,0,"getPow")
        self.connect(self.threadmodel,SIGNAL("getPow"),self.upGroup)
        self.threadmodel.start()
        
#         json=self.groupmodel.getPower()
#         self.upGroup(json['usergroup'])
        
    #更新group控件
    def upGroup(self,data):
        if not data['usergroup']:
            self.boxWarning(u'提示', u'没有启用中的用户组，请先添加')
            self.close()
            return
        self.group_data=data['usergroup']
        self.tempd = {}
        for c_type in self.group_data:
            self.group.addItem(c_type['group_name'])
            self.tempd[c_type['group_name']]=c_type['id']
    #取消关闭窗口
    def winClose(self):
        self.close() 
    
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
    
    def opencam(self):
        #检查是否有摄像头
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
        
    def addUser(self):
        username=str(self.username.text())      #用户名
        nickname=str(self.nickname.text())      #真实姓名
        password=str(self.password.text())      #密码 
        password2=str(self.password2.text())    #确认密码
        tel=str(self.tel.text())                #联系电话
        sex=str(self.sex.currentIndex())        #性别（0：女，1：男）
        status=str(0)                           #状态（0：正常，1：停用）
        group=str(self.group.currentText())    #职位
        group=self.tempd[unicode(group)]
        ctime=str(int(time.time()))             #入职日期
        card=str(self.card.text())              #身份证
        finger=self.fingerdata                  #指纹
        hukou=str(self.hukou.text())            #户籍
        adder=str(self.adder.text())            #住宅地址
        useimg=self.image_photo                 #用户图像
        cardimg=self.idcard_image_photo         #身份证图片
        cardimgt=self.idcard_image_photot         #身份证反面图片
        lasttime=str(0)
        birthday=str(self.birthday.text())
        if username=='':
            self.boxWarning(u'提示', u'登录名不能为空！')
            return
        if nickname=='':
            self.boxWarning(u'提示', u'真实姓名不能为空！')
            return
        if password=='':
            self.boxWarning(u'提示', u'密码不能为空！')
            return
        elif password!=password2:
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
            self.boxWarning(u'提示', u'请选择所在组！')
            return
        if card=='':
            self.boxWarning(u'提示', u'身份证不能为空！')
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
#        if useimg=='':
#            self.boxWarning(u'提示', u'请拍照！')
#            return
        if cardimg=='':
            self.boxWarning(u'提示', u'请上传身份证正面图像！')
            return
        if cardimgt=='':
            self.boxWarning(u'提示', u'请上传身份证反面图像！')
            return
       
        pwd=hashlib.md5()
        pwd.update(password)
        pwd.hexdigest()
        data={'righter':self.comboBox.currentIndex(),'card':card,'birthday':birthday,'lasttime':lasttime,'username':username,'nickname':nickname,'password':pwd.hexdigest(),'tel':tel,'sex':sex,'status':status,'group':group,'ctime':ctime,'hukou':hukou,'adder':adder,'useimg':useimg,'cardimg':cardimg,'cardimgt':cardimgt,'finger':self.fingerdata}
        json=self.model.addUser(data)
        if json['stat'] == 1:
            self.boxInfo(u'提示',json['msg'].decode('utf8'))
            self.addUserSuccess()
        else:
            self.boxWarning(u'提示',json['msg'].decode('utf8'))
    
    #打开指纹界面
    def openFinger(self):
        win=FingerController(self)
        win.exec_()
    
    
    #添加员工成功
    def addUserSuccess(self):
        self.parent.userInit()
        self.close()
    
        
        
        
        
        