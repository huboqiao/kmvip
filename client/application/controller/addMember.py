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
import linecache
import time
import datetime
import ctypes, linecache, os
from PyQt4.Qt import QLabel

class AddMemberController(ControllerAction, Ui_Dialog):
    def __init__(self, parent = None, ctype = 0):
        ControllerAction.__init__(self, parent)
        self.parent = parent
        try:
            os.remove(os.getcwd() + "/dll/wz.txt")
        except:
            pass
        
        self.setLabelTextColor()
        self.img = ImageProcess()
        self.bankCardCount = 0
        self.comboBox.setCurrentIndex(1)
        self.lineEdit.setFocus(True)
        self.charCount = 0
        self.powers = []
        self.storeModel = StoreQueryModel()
        self.memberModel = MemberModel()
        self.fin1 = ''
        self.fin2 = ''
        self.fin3 = ''
                
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
        
        self.connect(self.pushButton, SIGNAL("clicked()"), self.idcardInfo)  #读取身份证信息
        self.connect(self.pushButton_2, SIGNAL("clicked()"), self.opencam)  # 拍头像
        self.connect(self.pushButton_3, SIGNAL("clicked()"), self.uploadIdcard) # 上传身份证正面照
        self.connect(self.pushButton_4, SIGNAL("clicked()"), self.uploadIdcardt) # 上传身份证背面照
        self.connect(self.pushButton_5, SIGNAL("clicked()"), self.addMember)
        self.connect(self.pushButton_6, SIGNAL("clicked()"), self.getFinger1)
        self.connect(self.pushButton_7, SIGNAL("clicked()"), self.getFinger2)
        self.connect(self.pushButton_8, SIGNAL("clicked()"), self.getFinger3)
        self.connect(self.lineEdit, SIGNAL("textChanged(QString)"), self.automaticBankUser)
        self.connect(self.lineEdit_3, SIGNAL("editingFinished()"), self.checkIdCard)
        self.connect(self.lineEdit_3, SIGNAL("returnPressed()"), self.checkIdCard)
        self.connect(self.lineEdit_8, SIGNAL("textChanged(QString)"), self.autoSpace)
        self.connect(self.front, SIGNAL("doubleClicked()"), self.uploadIdcard)
        self.connect(self.back, SIGNAL("doubleClicked()"), self.uploadIdcardt)
        self.connect(self.dateEdit, SIGNAL("editingFinished()"), self.checkExpdate)
        self.connect(self.comboBox_2, SIGNAL("currentIndexChanged(int)"), self.queryStore)
        self.connect(self.comboBox_3, SIGNAL("currentIndexChanged(int)"), self.queryAllRegionByStoreId)
        self.connect(self.comboBox_4, SIGNAL("currentIndexChanged(int)"), self.queryAllSerialNumberByRegionId)
        
        data = {'node':'logic','act_fun':'getcumster','data':1}
        self.dayreportmodel = getDataThread(data,0,"getcumster")
        self.connect(self.dayreportmodel, SIGNAL("getcumster"), self.fillGroup)
        self.dayreportmodel.start()
        check.stringFilter(self.lineEdit_8, "[\d\s]+$")
        check.stringFilter(self.lineEdit_4, "^[1][3-8]+\\d{9}$")
        check.stringFilter(self.lineEdit_12, "^[1][3-8]+\\d{9}$")
        check.stringFilter(self.lineEdit_3, "^[1-9]\d{5}[1-9]\d{3}((0\d)|(1[0-2]))(([0|1|2]\d)|3[0-1])\d{3}([0-9]|X)$")
        
    def warning(self, control, warnings='', true=True):
        control.setText(self.tr(warnings))
        if true:
            control.setPalette(self.green)
        else:
            control.setPalette(self.red)
        
    # 判断身份证有效期时候超过当前日期   
    def checkExpdate(self):
        localDate = datetime.date.today().isoformat().replace('-','')
        date = str(self.dateEdit.text()).replace('/', '')  
        if date < localDate:
            self.warning(self.label_26, u'已过期', False)
            self.dateEdit.setFocus()
            return False
        self.warning(self.label_26)
        return True
            
    # 填充客户类别
    def fillGroup(self, data):
        data = data
        storeTypes = self.storeModel.queryStoreType()
        self.fillStoreType(storeTypes)
        if data['stat']:
            self.groups = data['data']
            for group in self.groups:
                self.comboBox_2.addItem(group['name'])
        else:
            self.boxWarning(u'提示', data['msg'])
            ControllerAction.closeTab(self)
            
    # 根据客户类型，有仓库则检索仓库   
    def queryStore(self, index=0):
        self.comboBox_3.clear()
        self.comboBox_4.clear()
        self.comboBox_5.clear()
        if self.groups[index]['isstorage'] == 1:
            stores = self.storeModel.queryStore()
            self.storeInfo(stores)
        # 检索客户类型说具有的权限
        powers = self.groups[self.comboBox_2.currentIndex()]['typelist']
        if not powers:
            self.fillPower({'stat':False})
            return
        data = {'node':'logic','act_fun':'getonegory','data':{'list':powers}}
        self.myThread = getDataThread(data,0,"getcumster")
        self.connect(self.myThread,SIGNAL("getcumster"),self.fillPower)
        self.myThread.start()
            
    # 填充仓库类型
    def fillStoreType(self, storeTypes):
        if storeTypes['stat']:
            self.storeTypes = storeTypes['data']
            for storeType in self.storeTypes:
                self.comboBox_6.addItem(self.tr(storeType['name']))
        else:
            self.boxWarning(u'提示', u'请添加仓库类型！')
            
    #仓位信息
    def storeInfo(self, stores):
        if stores['stat']:
            self.stores = stores['data']
            for store in self.stores:
                self.comboBox_3.addItem(self.tr(str(store['name'])))
        else:
            self.boxWarning(u'提示', u'未添加仓库，请添加')
    # 填充权限    
    def fillPower(self, powers):
        powers = powers
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
        storeId = self.stores[index]['id']
        regions = self.storeModel.queryAllRegionByStoreId(storeId)
        if regions['stat']:
            self.regions = regions['data']
            for region in self.regions:
                self.comboBox_4.addItem(self.tr(region['name']))
        
    # 根据区域id检索号数
    def queryAllSerialNumberByRegionId(self, index):
        self.comboBox_5.clear()
        regionId = self.regions[index]['id']
        serialNumbers = self.storeModel.queryAllSerialNumberByRegionId(regionId)
        if serialNumbers['stat']:
            self.serialNumbers = serialNumbers['data']
            for serialNumber in self.serialNumbers:
                self.comboBox_5.addItem(self.tr(serialNumber['name']))
                   
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
        
    def enableInfoControl(self):
        self.lineEdit.setReadOnly(False)    # 姓名
        self.lineEdit_2.setReadOnly(False)  # 名族
        self.lineEdit_3.setReadOnly(False)  # 身份证号
        self.lineEdit.setFocus()
    
    def clearBasicInfos(self):
        self.lineEdit.clear()    # 姓名
        self.lineEdit_2.clear()  # 名族
        self.lineEdit_3.clear()  # 身份证号
    
    # 读取身份证信息
    def idcardInfo(self):
        # 先清除基本信息数据
        self.clearBasicInfos()
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
                path_cd = os.getcwd()
                if cvr_auth == 1:
                    cvr_read_idcard = dll.CVR_Read_Content(4)
                    if cvr_read_idcard == 1:
                        #读身份证成功
                        try:
                            f = open(path_cd+'/dll/wz.txt', 'r')
                            carddata = f.readlines()
                            cardid = carddata[5].strip('\n')
                            f.close()
                        except:
                            if not self.boxConfirm(u'提示', u'身份证读取失败，请从新放置身份证','手动输入','重试'):
                                continue
                            else:
                                self.enableInfoControl()
                                return
                        self.idcardOK()
                        if not self.checkIdCard(cardid):
                            return
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
    def checkIdCard(self, cardId = ''):
        if cardId == '':
            cardId = str(self.lineEdit_3.text()).strip('\n')
            if not check.checkIdCard(cardId):
                self.warning(self.label_17, u'格式错误', False)
                return False
        data = self.memberModel.checkIDcard(cardId)
        self.lineEdit_3.setText(cardId)
        if data:
            #身份证已经注册, 清空基本信息
            self.warning(self.label_17, u'已注册', False)
            return False
        
        else:
            #身份证可以使用
            self.warning(self.label_17, u'可用')
            return True
    
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
            elif i == 8:
                idcard_overdue = unicode(line.rstrip(), 'gbk')
                idcard_overdue = idcard_overdue[11:]
                idcard_overdue = int(time.mktime(time.strptime(idcard_overdue, '%Y.%m.%d')))
                carddate = time.ctime(idcard_overdue)
                carddate = time.strptime(carddate, '%a %b %d %H:%M:%S %Y')
                date = QDate(int(time.strftime('%Y', carddate)), 
                             int(time.strftime('%m', carddate)), 
                             int(time.strftime('%d', carddate)))
                t = QTime(int(time.strftime('%H', carddate)), 
                          int(time.strftime('%M', carddate)), 
                          int(time.strftime('%S', carddate)))
                self.dateEdit.setDateTime(QDateTime(date, t))
                
            i = i+1
        f.close()
        self.checkIdCard()
        self.checkExpdate()
  
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
                           10, 25, 150, 150) #显示照片
        self.image_photo = self.img.generatePictureCoding(os.getcwd()+'/image/s3.png') #将照片转换成字符
        data = self.memberModel.sendImg(self.image_photo)
        if data['stat'] == '-1':
            self.boxWarning(u'msg', u'upload img is error')
        else:
            self.image_photo = data['path']
    #添加客户信息并绑定卡
    def addMember(self):
        data = {'name':str(self.lineEdit.text()).strip(), 
                'sex':str(self.comboBox.currentIndex()), 
                'nation':str(self.lineEdit_2.text()).strip(), 
                'mobile':str(self.lineEdit_4.text()).strip(), 
                'idCard':str(self.lineEdit_3.text()).strip(), 
                'cardDate':int(time.mktime(time.strptime(str(self.dateEdit.text()), '%Y/%m/%d'))), 
                'addUser':self.appdata['user']['user_id'],
                'address':str(self.lineEdit_5.text()).strip(), 
                'memberGroup':str(self.groups[self.comboBox_2.currentIndex()]['id']),
                'storeNumber':'',
                'storeType':''}
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
        if str(data['name']).replace(' ', '') == u'金荣':
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
            self.label_17.setText(self.tr(u'格式错误'))
            self.label_17.setPalette(self.red)
            self.lineEdit_2.setFocus(True)
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
        if not self.checkIdCard():
            self.boxWarning(u'提示', u'身份证不可用')
            self.lineEdit_3.setFocus()
            return
        if not self.checkExpdate():
            self.boxWarning(u'提示', u'身份证已过期')
            self.dateEdit.setFocus()
            return
        if not self.boxConfirm(u'提醒', u'请确认用户信息，按  “确定” 提交， “取消”取消提交！'):
            return
        try:
            self.recvData = self.memberModel.addMember(data, dataInfo, self.appdata['user']['user_id'])
        except:
            self.boxWarning(u'提示', u'连接服务器超时，请重新登录！')
        if self.recvData['stat'] == True:
            self.setPasswordNow(self.recvData['data'])
        else:
            self.boxWarning(u'提示', self.recvData['msg'].decode('utf8'))
            
    def setPasswordNow(self, data): 
        self.user_id = data
        OpenCardContorller(self).exec_()
