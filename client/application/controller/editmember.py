# -*- coding: utf-8 -*-
'''
Created on 2014年9月27日

@author: huaan
'''
from PyQt4 import QtGui
from application.lib.Commethods import *
from application.view.addMember import Ui_Dialog
from application.controller.opencard import OpenCardContorller
from application.lib.cam import CamClass
from application.controller.camController import CamController
from application.controller.finger import FingerController
from application.lib.ImageProcess import ImageProcess
from application.model.memberModel import MemberModel
from application.lib.commodel import getDataThread
from application.model.storeQuery import StoreQueryModel
import application.lib.formatCheck as check
from application.controller.grants import GrantContorller
import time
import ctypes, linecache, os
from PyQt4.Qt import QLabel, QDateTime, QLineEdit

class EditMemberController(ControllerAction, Ui_Dialog):
    def __init__(self, parent = None, ctype = 0):
        ControllerAction.__init__(self, parent)
        self.parent = parent
        self.memberData = ControllerAction.memberData
        # 激活用户名、名族、身份证号输入框
        self.enableInfoControl()
        # 设置2个字体颜色
        self.setLabelTextColor()
        self.img = ImageProcess()
        # 已输入的银行卡号位数，起始值为 0
        self.bankCardCount = 0
        # 默认客户性别为“男”
        self.comboBox.setCurrentIndex(1)
        self.lineEdit.setFocus(True)
        self.pushButton.hide()
        # 保存用户组所有权限
        self.powers = [] 
        self.storeModel = StoreQueryModel()
        self.memberModel = MemberModel()
                
        self.size = int(self.cf.get('cam', 'smalimagesize')) 
        self.image_photo = ''                                #照片默认为空 
        self.idcard_image_photo = ''                          #身份证图像默认为空
        self.idcard_image_photot = ''                         #身份证反面图像默认为空
        
        self.zhaopian = QImage(self.head)              #加载照片图片
        self.zhaopianLabel = QLabel(self.head)           #照片图像标签
        self.idcardImage = QImage(self.front)    #加载身份证图片
        self.imageLabel2 = QLabel(self.front)      #身份证图像标签
        self.idcardImage_t = QImage(self.back)    #加载身份证反面图片
        self.imageLabel2_t = QLabel(self.back)      #身份证反面图像标签
        
#         self.connect(self.pushButton, SIGNAL("clicked()"), self.idcardInfo)  #读取身份证信息
        self.connect(self.pushButton_2, SIGNAL("clicked()"), self.opencam)  # 拍头像
        self.connect(self.pushButton_3, SIGNAL("clicked()"), self.uploadIdcard) # 上传身份证正面照
        self.connect(self.pushButton_4, SIGNAL("clicked()"), self.uploadIdcardt) # 上传身份证背面照
        self.connect(self.pushButton_5, SIGNAL("clicked()"), self.alterMember) # 
        self.connect(self.pushButton_6, SIGNAL("clicked()"), self.getFinger1)
        self.connect(self.pushButton_7, SIGNAL("clicked()"), self.getFinger2)
        self.connect(self.pushButton_8, SIGNAL("clicked()"), self.getFinger3)
        self.connect(self.lineEdit, SIGNAL("textChanged(QString)"), self.automaticBankUser)
#         self.connect(self.lineEdit_3, SIGNAL("returnPressed()"), self.getMemberInfo)
        self.connect(self.lineEdit_8, SIGNAL("textChanged(QString)"), self.autoSpace)
        self.connect(self.front, SIGNAL("doubleClicked()"), self.uploadIdcard)
        self.connect(self.back, SIGNAL("doubleClicked()"), self.uploadIdcardt)
        self.connect(self.dateEdit, SIGNAL("editingFinished()"), self.checkExpdate)
        self.connect(self.comboBox_2, SIGNAL("currentIndexChanged(int)"), self.queryStore)
        self.connect(self.comboBox_3, SIGNAL("currentIndexChanged(int)"), self.queryAllRegionByStoreId)
        self.connect(self.comboBox_4, SIGNAL("currentIndexChanged(int)"), self.queryAllSerialNumberByRegionId)
        # 检索基本信息（客户组，用户组权限，  仓库类型， 仓库， 仓库区域， 仓库号数）
        self.fillGroup(self.memberModel.getGroups(1))
        self.fillMemberInfo(self.memberData)
        check.stringFilter(self.lineEdit_8, "[\d\s]+$")
        check.stringFilter(self.lineEdit_4, "^[1][3-8]+\\d{9}$")
        check.stringFilter(self.lineEdit_12, "^[1][3-8]+\\d{9}$")
        check.stringFilter(self.lineEdit_3, "^[1-9]\d{5}[1-9]\d{3}((0\d)|(1[0-2]))(([0|1|2]\d)|3[0-1])\d{3}([0-9]|X)$")
        
    # 判断身份证有效期时候超过当前日期   
    def checkExpdate(self):
        localDate = datetime.date.today().isoformat().replace('-','')
        date = str(self.dateEdit.text()).replace('/', '')  
        if date < localDate:
            self.warning(self.label_26, u'已过期', False)
            self.dateEdit.setFocus()
            return
        self.warning(self.label_26)
        
    # 清空用户信息
    def clearInfos(self):
        for control in self.findChildren(QLineEdit):
            control.clear()

    # 根据身份证号获取用户信息    
    def getMemberInfo(self):
        data = {'idCard': str(self.lineEdit_3.text())}
        if not check.checkIdCard(data['idCard']):
            self.clearInfos()
            self.boxWarning(u'提示', u'请输入完整的身份证号码')
            self.lineEdit_3.setFocus()
            return
        data = {'node':'logic','act_fun':'getMemberInfoss','data':data}
        self.thread_2 = getDataThread(data,0,"getMemberInfoss")
        self.connect(self.thread_2, SIGNAL("getMemberInfoss"), self.fillMemberInfo)
        self.thread_2.start()
    # 填充客户信息
    def fillMemberInfo(self, data):
        customerInfo = data
        self.id = customerInfo['id']
        try:
            cardDate = check.timeStamp(customerInfo['actdate'], '%Y/%m/%d')
            if customerInfo['stat'] == 2:
                self.boxWarning(u'提示', u'该用户已于%s被冻结'%cardDate)
                self.lineEdit_3.setFocus()
                return
            elif customerInfo == 3:
                self.boxWarning(u'提示', u'该用户已于%s注销'%cardDate)
                self.lineEdit_3.setFocus()
                return
        except:
            pass
        cardDate = check.timeStamp(customerInfo['carddate'], '%Y/%m/%d')
        self.dateEdit.setDate(QDate().fromString(cardDate, "yyyy/MM/dd"))
        self.comboBox.setCurrentIndex(int(customerInfo['sex']))
        self.comboBox_7.setCurrentIndex(int(customerInfo['relativessex']))
        try:
            self.comboBox_2.setCurrentIndex(self.groupIDs.index(int(customerInfo['ugroup'])))
        except:
            self.boxWarning(u'提示', u'该用户所属用户类型不存在，请修改其用户类型！')
        self.oldName = customerInfo['membername']
        self.lineEdit.setText(self.tr(customerInfo['membername']))
        self.lineEdit_2.setText(self.tr(customerInfo['nation']))
        self.lineEdit_3.setText(self.tr(customerInfo['idcard']))
        self.lineEdit_4.setText(self.tr(customerInfo['tel']))
        self.lineEdit_5.setText(self.tr(customerInfo['adder']))
        self.lineEdit_6.setText(self.tr(customerInfo['bankusername']))
        self.lineEdit_7.setText(self.tr(customerInfo['bankname']))
        self.lineEdit_8.setText(self.tr(customerInfo['bankcard']))
        self.lineEdit_9.setText(self.tr(customerInfo['relativesname']))
        self.lineEdit_11.setText(self.tr(customerInfo['relationship']))
        self.lineEdit_12.setText(self.tr(customerInfo['relationtem']))
        self.fin1 = customerInfo['finger1']
        self.fin2 = customerInfo['finger2']
        self.fin3 = customerInfo['finger3']
        if self.fin1 == '' or self.fin1 == 'null':
            self.label_11.setText(self.tr(u'未采集'))
            self.label_11.setPalette(self.red)
        else:
            self.label_11.setText(self.tr(u'已存在'))
            self.label_11.setPalette(self.green)
        if self.fin2 == '' or self.fin2 == 'null':
            self.label_13.setText(self.tr(u'未采集'))
            self.label_13.setPalette(self.red)
        else:
            self.label_13.setText(self.tr(u'已存在'))
            self.label_13.setPalette(self.green)
        if self.fin3 == '' or self.fin3 == 'null':
            self.label_15.setText(self.tr(u'未采集'))
            self.label_15.setPalette(self.red)
        else:
            self.label_15.setText(self.tr(u'已存在'))
            self.label_15.setPalette(self.green)
        #下载头像
        self.image_photo = str(customerInfo['useimg_path'])
        head = self.img.downloadImg(self.image_photo,'tx.png')
        #更新图像
        try:
            if customerInfo['useimg_path']: 
                #缩略
                self.img.thumbnails(head, head, 150, 150)
                #显示
                self.zhaopian.load(head)
                self.zhaopianLabel.setGeometry(QRect(0, 0, 150, 150))
                self.zhaopianLabel.setPixmap(QPixmap.fromImage(self.zhaopian)) 
                self.image_photo = customerInfo['useimg_path']                          #头像
        except:
            pass
        
        #下载身份证正面照 
        self.idcard_image_photo = str(customerInfo['cardimg_path'])
        front = self.img.downloadImg(self.idcard_image_photo,'kh_idcard.png')
        #更新图像
        try:
            if customerInfo['cardimg_path']: 
                #缩略
                self.img.thumbnails(front, front, 238, 150)
                #显示
                self.idcardImage.load(front)
                self.imageLabel2.setGeometry(QRect(0, 0, 238, 150))
                self.imageLabel2.setPixmap(QPixmap.fromImage(self.idcardImage)) 
                self.idcard_image_photo = customerInfo['cardimg_path']                          #头像
        except:
            pass
        
        #下载身份证背面照
        self.idcard_image_photot = str(customerInfo['cardimgt_path'])
        back = self.img.downloadImg(self.idcard_image_photot,'kh_idcardt.png')
        #更新图像
        try:
            if customerInfo['cardimgt_path']: 
                #缩略
                self.img.thumbnails(back, back, 238, 150)
                #显示
                self.idcardImage_t.load(back)
                self.imageLabel2_t.setGeometry(QRect(0, 0, 238, 150))
                self.imageLabel2_t.setPixmap(QPixmap.fromImage(self.idcardImage_t)) 
                self.idcard_image_photot = customerInfo['cardimgt_path']                          #头像
        except:
            pass
        
        try:
            if customerInfo['storagenumber'] and self.groups[self.comboBox_2.currentIndex()]['isstorage'] == 1:
                self.comboBox_3.setCurrentIndex(self.storeIDs.index(customerInfo['store']))
                self.comboBox_4.setCurrentIndex(self.regionIDs.index(customerInfo['region']))
                self.comboBox_5.setCurrentIndex(self.serialNumberIDs.index(customerInfo['storagenumber']))
                try:
                    self.comboBox_6.setCurrentIndex(self.storeTypeIDs.index(customerInfo['typeid']))
                except:
                    pass
        except:
            pass
    # 填充客户类别
    def fillGroup(self, data):
        storeTypes = self.storeModel.queryStoreType()
        self.fillStoreType(storeTypes)
        if data['stat']:
            self.groups = data['data']
            self.groupIDs = []
            for group in data['data']:
                self.comboBox_2.addItem(group['name'])
                self.groupIDs.append(group['id'])
        else:
            self.boxWarning(u'提示', data['msg'])
            self.reject()
            return
            
    # 根据客户类型，有仓库则检索仓库   
    def queryStore(self, index=0):
        self.comboBox_3.clear()
        self.comboBox_4.clear()
        self.comboBox_5.clear()
        if int(self.groups[index]['isstorage']) == 1:
            stores = self.storeModel.queryStore()
            self.storeInfo(stores)
        # 检索客户类型说具有的权限
        
        powers = self.groups[self.comboBox_2.currentIndex()]['typelist']
        if not powers:
            self.fillPower({'stat':False})
            return
        self.fillPower(self.memberModel.getGroupPowers({'list':powers}))
        return
#         data = {'node':'logic','act_fun':'getonegory','data':{'list':powers}}
#         self.myThread = getDataThread(data,0,"getcumster")
#         self.connect(self.myThread,SIGNAL("getcumster"),self.fillPower)
# #         try:
#         self.myThread.start()
#         except:
#             self.boxWarning(u'提示', u'连接服务器超时，请检查网络是否畅通！')
            
    # 填充仓库类型
    def fillStoreType(self, storeTypes):
        self.storeTypeIDs = []
        if storeTypes['stat']:
            self.storeTypes = storeTypes['data']
            for storeType in self.storeTypes:
                self.comboBox_6.addItem(self.tr(storeType['name']))
                self.storeTypeIDs.append(storeType['id'])
        else:
            self.boxWarning(u'提示', u'请添加仓库类型！')
            
    #仓位信息
    def storeInfo(self, stores):
        self.comboBox_3.clear()
        self.storeIDs = []
        if stores['stat']:
            self.stores = stores['data']
            for store in self.stores:
                self.comboBox_3.addItem(self.tr(str(store['name'])))
                self.storeIDs.append(store['id'])
        else:
            self.boxWarning(u'提示', u'未添加仓库，请添加')
    # 填充权限    
    def fillPower(self, powers):
        for power in self.powers:
            self.gridLayout.removeWidget(power)
            power.deleteLater()
        self.powers = []
        if powers['stat']:
            i = 0
            while i < len(powers['data']):
                label = QLabel(self.tr(str(i + 1) + u'、' + powers['data'][i]['name']))
                self.powers.append(label)
                self.gridLayout.addWidget(label, 1 + i / 5, i % 5, 1, 1)
                i += 1
 
    # 根据区域id检索区域
    def queryAllRegionByStoreId(self, index):
        self.comboBox_4.clear()
        self.comboBox_5.clear()
        self.regionIDs = []
        storeId = self.stores[index]['id']
        regions = self.storeModel.queryAllRegionByStoreId(storeId)
        if regions['stat']:
            self.regions = regions['data']
            for region in self.regions:
                self.comboBox_4.addItem(self.tr(region['name']))
                self.regionIDs.append(region['id'])
        
    # 根据区域id检索号数
    def queryAllSerialNumberByRegionId(self, index):
        self.comboBox_5.clear()
        self.serialNumberIDs = []
        regionId = self.regions[index]['id']
        serialNumbers = self.storeModel.queryAllSerialNumberByRegionId(regionId)
        if serialNumbers['stat']:
            self.serialNumbers = serialNumbers['data']
            for serialNumber in self.serialNumbers:
                self.comboBox_5.addItem(self.tr(serialNumber['name']))
                self.serialNumberIDs.append(serialNumber['id'])
                   
    # 设置标签字体颜色    
    def setLabelTextColor(self):
        self.red = QPalette()
        self.red.setColor(QPalette().WindowText, Qt.red)
        self.green = QPalette()
        self.green.setColor(QPalette().WindowText, Qt.green)
        
    # 采集指纹1
    def getFinger1(self):
        self.fingerdata = ''
        self.fin1 = ''
        self.label_11.setText(self.tr(u'未采集'))
        self.label_11.setPalette(self.red)
        try:
            win = FingerController(self)
            win.exec_()
            if self.fingerdata == '':
                self.boxWarning(u'提示', u'您未成功录入指纹 1 !')
                return
        except:
            if not self.boxWarning(u'提示', u'您未成功录入指纹 1 ！'):
                return
        self.fin1 = self.fingerdata
        self.label_11.setText(self.tr(u'已采集'))
        self.label_11.setPalette(self.green)
    # 采集指纹2
    def getFinger2(self):
        self.fingerdata = ''
        self.fin2 = ''
        self.label_13.setText(self.tr(u'未采集'))
        self.label_13.setPalette(self.red)
        try:
            win = FingerController(self)
            win.exec_()
            if self.fingerdata == '':
                self.boxWarning(u'提示', u'您未成功录入指纹 2 !')
                return
        except:
            if not self.boxWarning(u'提示', u'您未成功录入指纹 2 ！'):
                return
        self.fin2 = self.fingerdata
        self.label_13.setText(self.tr(u'已采集'))
        self.label_13.setPalette(self.green) 
    # 采集指纹3
    def getFinger3(self):
        self.fingerdata = ''
        self.fin3 = ''
        self.label_15.setText(self.tr(u'未采集'))
        self.label_15.setPalette(self.red)
        try:
            win = FingerController(self)
            win.exec_()
            if self.fingerdata == '':
                self.boxWarning(u'提示', u'您未成功录入指纹 3 !')
                return
        except:
            if not self.boxWarning(u'提示', u'您未成功录入指纹 3 ！'):
                return
        self.fin3 = self.fingerdata
        self.label_15.setText(self.tr(u'已采集'))
        self.label_15.setPalette(self.green)
            
    # 银行卡号每4位添加空格   
    def autoSpace(self, text):
        self.bankCardCount = check.autoSpace(self.bankCardCount, self.lineEdit_8, text)
        
    # 输入客户姓名自动将名称填充到银行开户名        
    def automaticBankUser(self):
        self.lineEdit_6.setText(self.tr(str(self.lineEdit.text())))
    
    # 激活身份信息数区    
    def enableInfoControl(self):
        self.lineEdit.setReadOnly(False)    # 姓名
        self.lineEdit_2.setReadOnly(False)  # 名族
        self.lineEdit_3.setReadOnly(False)  # 身份证号
        self.lineEdit.setFocus()
        
    # 读取身份证信息
    def idcardInfo(self):
        # 先清除基本信息数据
        self.lineEdit.clear()    # 姓名
        self.lineEdit_2.clear()  # 名族
        self.lineEdit_3.clear()  # 身份证号
        while 1:
            try:
                dll = ctypes.windll.LoadLibrary(os.getcwd()+"/dll/termb.dll")
            except:
                if not self.boxConfirm(u'提示', u'缺少termb.dll文件','手动输入','重试'):
                    continue
                else:
                    self.enableInfoControl()
                    return
            
            cvr_init = dll.CVR_InitComm(1001) 
            if cvr_init == 1:
                cvr_auth = dll.CVR_Authenticate () 
                if cvr_auth == 1:
                    cvr_read_idcard = dll.CVR_Read_Content(4)
                    if cvr_read_idcard == 1:
                        #读身份证成功
                        try:
                            f = open('./dll/wz.txt', 'r')
                        except:
                            if not self.boxConfirm(u'提示', u'身份证读取失败，请从新放置身份证','手动输入','重试'):
                                continue
                            else:
                                self.enableInfoControl()
                                return
                        self.checkIdCard(unicode(linecache.getline('./dll/wz.txt', 6).rstrip(), 'gbk'))
                        f.close()
                        dll.CVR_CloseComm()
                        break
                    else:
                        dll.CVR_CloseComm()
                        if not self.boxConfirm(u'提示', u'读取身份证信息失败，请确保身份证未销磁','手动输入','重试'):
                            continue
                        else:
                            self.enableInfoControl()
                            return
                else:
                    if not self.boxConfirm(u'提示', u'身份证阅读失败！请重新将身份证放到身份证阅读机的阅读区后点击“重试”','手动输入','重试'):
                        continue
                    else:
                        self.enableInfoControl()
                        return
                    dll.CVR_CloseComm()
                    
            else:
                if not self.boxConfirm(u'提示', u'身份证阅读机初始化失败, 请检查身份证阅读机是否连接成功','手动输入','重试'):
                    continue
                else:
                    self.enableInfoControl()
                    return

    #根据身份证查询到客户信息
    def checkIdCard(self, cardId):
        data = self.memberModel.checkIDcard({'ID':cardId})
        self.getCheckIdCard(data)
    
    #服务器返回身份证是否已注册信息
    def getCheckIdCard(self, data):
        if data:
            #身份证已经注册, 清空基本信息
            self.boxWarning(u'提示', u'该身份证已经被注册！')
            self.lineEdit_3.setFocus()

        else:
            #身份证可以使用
            self.idcardOK()
    
    #身份证验证可以使用
    def idcardOK(self):
        try:
            f = open('./dll/wz.txt', 'r') 
        except:
            self.boxWarning(u'提示', u'身份证读取失败！')
            self.lineEdit.setFocus()
            return
        f.seek(0) 
        i = 1
        for line in f:  
            if i == 1:
                self.lineEdit.setText(unicode(line.rstrip(), 'gbk'))
            elif i == 2:
                sex = unicode(line.rstrip(), 'gbk')
                if sex == '男':
                    self.comboBox.setCurrentIndex(1) #性别
                else:
                    self.comboBox.setCurrentIndex(0) #性别
            elif i == 3:
                self.lineEdit_2.setText(unicode(line.rstrip(), 'gbk')) #名族
            elif i == 5:
                self.lineEdit_5.setText(unicode(line.rstrip(), 'gbk'))  #地址
            elif i == 6:
                self.lineEdit_3.setText(unicode(line.rstrip(), 'gbk')) #身份证号
                pass
            elif i == 8:
                idcard_overdue = unicode(line.rstrip(), 'gbk')
                idcard_overdue = idcard_overdue[11:]
                idcard_overdue = int(time.mktime(time.strptime(idcard_overdue, '%Y.%m.%d')))
                carddate = time.ctime(idcard_overdue)
                carddate = time.strptime(carddate, '%a %b %d %H:%M:%S %Y')
                self.dateEdit.setDateTime(QDateTime(
                                          QDate(int(time.strftime('%Y', carddate)), 
                                                int(time.strftime('%m', carddate)), 
                                                int(time.strftime('%d', carddate))), 
                                          QTime(int(time.strftime('%H', carddate)), 
                                                int(time.strftime('%M', carddate)), 
                                                int(time.strftime('%S', carddate)))))
            i = i+1
        f.close()
        self.lineEdit_4.setFocus()
  
    #身份证正面图像
    def uploadIdcard(self):
        cardImage = str(QFileDialog.getOpenFileName(self, "Open file dialog", "/", self.tr("Image Files(*.png *.jpg *.bmp)"))) 
        if cardImage:
            self.img.thumbnails(cardImage.encode('cp936'), os.getcwd()+'/image/kh_idcard.png', 
                                238, 150) #生成身份证缩略图
            self.img.showImage(os.getcwd()+'/image/kh_idcard.png', self.imageLabel2, self.idcardImage,
                                0, 0, 238, 150) #显示身份证图片
            self.idcard_image_photo = self.img.generatePictureCoding(os.getcwd()+'/image/kh_idcard.png') #将身份证图片转换成字符
            
            data = self.memberModel.sendImg(self.idcard_image_photo)
            if data['stat'] == '-1':
                self.boxWarning(u'msg', data['msg'])
            else:
                self.idcard_image_photo = data['path']
    #身份证反面图像
    def uploadIdcardt(self):
        cardimaget = str(QFileDialog.getOpenFileName(self, 
                                                     "Open file dialog", 
                                                     "/", 
                                                     self.tr("Image Files(*.png *.jpg *.bmp)"))) 
        if cardimaget:
            self.img.thumbnails(cardimaget.encode('cp936'), 
                                os.getcwd()+'/image/kh_idcardt.png', 
                                238, 150) #生成身份证缩略图
            self.img.showImage(os.getcwd()+'/image/kh_idcardt.png', 
                               self.imageLabel2_t, 
                               self.idcardImage_t, 
                               0, 0, 238, 150) #显示身份证图片
            self.idcard_image_photot = self.img.generatePictureCoding(os.getcwd()+'/image/kh_idcardt.png') #将身份证图片转换成字符
            data = self.memberModel.sendImg(self.idcard_image_photot)
            if data['stat'] == '-1':
                self.boxWarning(u'msg', u' upload img is error')
            else:
                self.idcard_image_photot = data['path']     
        
    #拍照 
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
     
    #初始化摄像头设备错误提示
    def slotInformation(self, mssage):  
        self.statusBar().showMessage(mssage)
     
    #显示照片
    def showimage(self):
        self.img.showImage(os.getcwd()+'/image/s3.png', self.zhaopianLabel, self.zhaopian, 
                           0, 0, 150, 150) #显示照片
        self.image_photo = self.img.generatePictureCoding(os.getcwd()+'/image/s3.png') #将照片转换成字符
        data = self.memberModel.sendImg(self.image_photo)
        if data['stat'] == '-1':
            self.boxWarning(u'msg', u'upload img is error')
        else:
            self.image_photo = data['path']
    #添加客户信息并绑定卡
    def alterMember(self):
        try:
            self.id
        except:
            self.boxWarning(u'提示', u'请输入要修改的用户身份证号码后回车查询用户资料')
            self.lineEdit_3.setFocus()
            return
        data = {'name':str(self.lineEdit.text()).strip(), 
                'sex':str(self.comboBox.currentIndex()), 
                'nation':str(self.lineEdit_2.text()).strip(), 
                'mobile':str(self.lineEdit_4.text()).strip(), 
                'idCard':str(self.lineEdit_3.text()).strip(), 
                'cardDate':int(time.mktime(time.strptime(str(self.dateEdit.text()), '%Y/%m/%d'))), 
                'addUser':self.appdata['user']['user_id'],
                'address':str(self.lineEdit_5.text()).strip(), 
                'memberGroup':str(self.groups[self.comboBox_2.currentIndex()]['id']),
                'id':self.id}
        self.data = data
        if self.groups[self.comboBox_2.currentIndex()]['isstorage'] == 1:
            try:
                data['storeNumber'] = self.serialNumbers[self.comboBox_5.currentIndex()]['id']
                data['storeType'] = self.storeTypes[self.comboBox_6.currentIndex()]['id']
            except:
                pass
        if data['name'] == '':
            self.boxWarning(u'提示', u'请输入客户名！')
            self.lineEdit.setFocus()
            return
        if str(data['name']).replace(' ', '') == u'金荣' and str(self.oldName) != u'金荣':
            self.boxWarning(u'提示', u'您输入的名称是公司账户所用名称，请输入其他名称！')
            self.lineEdit.setFocus()
            return
        if data['nation'] == '':
            self.boxWarning(u'提示', u'请输入名族！')
            self.lineEdit_2.setFocus()
            return
        
        if not check.check(data['mobile'], 'mobile'):
            self.boxWarning(u'提示', u'请输入正确的手机号码！')
            self.lineEdit_4.setFocus()
            return
        
        if not check.check(data['idCard'], 'idcard'):
            self.boxWarning(u'提示', u'请输入正确的身份证号！')
            self.lineEdit_3.setFocus()
            return
        dataInfo = { 'bankAccount':str(self.lineEdit_8.text()).strip(), 
                     'bankName':str(self.lineEdit_7.text()).strip(), 
                     'accountOwner':str(self.lineEdit_6.text()).strip(), 
                     'head':self.image_photo, 
                     'front':self.idcard_image_photo, 
                     'back':self.idcard_image_photot, 
                     'relative':str(self.lineEdit_9.text()).strip(), 
                     'relativeSex':str(self.comboBox_7.currentIndex()), 
                     'relationShip':str(self.lineEdit_11.text()).strip(), 
                     'relationMobile':str(self.lineEdit_12.text()).strip(), 
                     'finger1':self.fin1, 
                     'finger2':self.fin2,
                     'finger3':self.fin3}
        
        self.dataInfo = dataInfo
        
        if dataInfo['front'] == '':
            self.boxWarning(u'提示', u'请上传身份证正面图像！')
            return
        if dataInfo['back'] == '':
            self.boxWarning(u'提示', u'请上传身份证反面图像！')
            return
        if dataInfo['head'] == '':
            self.boxWarning(u'提示', u'请上传头像！')
            return
            
        if dataInfo['bankAccount'] != '': 
            if not check.check(dataInfo['bankAccount'], 'number'):
                self.boxWarning(u'提示', u'请输入正确的银行卡号！')
                self.lineEdit_8.setFocus()
                return
            if dataInfo['bankName'] == '':
                self.boxWarning(u'提示', u'请输入银行卡开户行！')
                self.lineEdit_7.setFocus()
                return
            if dataInfo['accountOwner'] == '':
                self.boxWarning(u'提示', u'请输入银行卡开户人名！')
                self.lineEdit_6.setFocus()
                return
        if dataInfo['relative'] != '':
            if not check.check(dataInfo['relationMobile'], 'mobile'):
                self.boxWarning(u'提示', u'请输入正确的亲属手机号')
                self.lineEdit_12.setFocus()
                return
            
        if not self.boxConfirm(u'提醒', u'请确认用户信息，按  “确定” 提交， “取消”取消提交！'):
            return
        # 费管理员修改用户
        if self.appdata['user']['user_id'] != 1:
            win= GrantContorller(self)
            win.exec_()
        else:
            self.gart(True)
            
        
    def gart(self, data):
        if not data:
            return
        try:
            self.recvData = self.memberModel.alterMember(self.data, self.dataInfo, self.appdata['user']['user_id'])
        except:
            self.boxWarning(u'提示', u'连接服务器超时，请重新登录！')
        self.boxWarning(u'提示', self.recvData['msg'].decode('utf8'))
        print self.recvData
        if self.recvData['stat'] == True:
            ControllerAction.closeTab(self)
