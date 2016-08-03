# -*- coding: utf-8 -*-
'''
Created on 2015年4月8日

@author: huaan
'''
from application.lib.Commethods import *
from application.lib.commodel import getDataThread
from application.view.checkMemberID import Ui_Dialog
import application.lib.formatCheck as check
from application.model.memberModel import MemberModel
from application.controller.editmember import EditMemberController
from application.controller.fingerWindow import FingerWindow
import hashlib, ctypes, linecache

class CheckMemberID(ControllerAction,Ui_Dialog):
    def __init__(self,parent=None):
        ControllerAction.__init__(self,parent)
        self.parent = parent
        self.title = u'密码验证'
        self.memberModel = MemberModel()
        self.connect(self.pushButton_2, SIGNAL("clicked()"), self.checkFinger)
        self.connect(self.pushButton, SIGNAL("clicked()"), self.checkPassword)
        self.connect(self.pushButton_3, SIGNAL("clicked()"), self.idcardInfo)
        self.connect(self.lineEdit, SIGNAL("returnPressed()"), self.checkIDCard)
        self.connect(self.lineEdit_2, SIGNAL("returnPressed()"), self.checkCard)
        self.connect(self.lineEdit_3, SIGNAL("returnPressed()"), self.checkPassword)
        check.stringFilter(self.lineEdit_2, "[\d\s]+$")
        check.stringFilter(self.lineEdit, "^[1-9]\d{5}[1-9]\d{3}((0\d)|(1[0-2]))(([0|1|2]\d)|3[0-1])\d{3}([0-9]|X)$")
    
    def checkFinger(self):
        if not self.checkCard():
            return
        FingerWindow(self).exec_()
        
    def checkPwd(self, stat):
        if not self.checkCard():
            return
        if stat['stat'] != 1:
            self.boxWarning(u'提示', stat['msg'])
            return
        ControllerAction.memberData = self.memberData
        self.accept()
    
    def enableLineEdit(self, enable=True):
        self.lineEdit_2.clear()
        self.lineEdit_3.clear()
        self.lineEdit_2.setEnabled(enable)
        self.lineEdit_3.setEnabled(enable)
        self.pushButton.setEnabled(enable)
        self.pushButton_2.setEnabled(enable)
        
    # 根据身份证查询到客户信息
    def checkIDCard(self, cardId = ''):
        self.enableLineEdit(False)
        if cardId == '':
            cardId = str(self.lineEdit.text()).upper()
            self.lineEdit.setText(self.tr(cardId))
            if not check.checkIdCard(cardId):
                self.boxWarning(u'提示', u'您输入的身份证号不正确，请重新输入！')
                self.lineEdit.setFocus(True)
                return
        data = {'node':'logic','act_fun':'getMemberInfoss','data':{'idCard': cardId}}
        self.thread_2 = getDataThread(data,0,"getMemberInfoss")
        self.connect(self.thread_2, SIGNAL("getMemberInfoss"), self.cardChecked)
        self.thread_2.start()
        
    def cardChecked(self,data):
        if not data['stat']:
            self.boxWarning(u'提示', u'该身份证未注册')
            self.enableLineEdit(False)
            self.lineEdit.setFocus()
            return
        else:
            self.memberData = data['data'][0]
            try: 
                float(self.memberData['card'])
            except:
                self.boxWarning(u'提示', u'该用户没有正常的金荣卡，请先解冻或重新绑卡后再试')
                self.lineEdit.setFocus(True)
                return
            if self.appdata['user']['user_id'] == 1:
                ControllerAction.memberData = self.memberData
                self.accept()
                return
            else:
                self.fingers = (self.memberData['finger1'], self.memberData['finger2'], self.memberData['finger3'])
                
                self.enableLineEdit(True)
                self.lineEdit_2.clear()
                self.lineEdit_3.clear()
                self.lineEdit_2.setFocus()
            
    def checkCard(self):
        if cmp(str(self.lineEdit_2.text()), str(self.memberData['card'])) != 0:
            self.boxWarning(u'提示 ', u'卡号与该身份证正常使用的卡号不匹配，请重新输入')
            self.lineEdit_2.setFocus(True)
            return False
        self.lineEdit_3.setFocus()
        return True
        
    def checkPassword(self):
        if not self.checkCard():
            return
        pwd=hashlib.md5()
        pwd.update(str(self.lineEdit_3.text()))
        if cmp(str(pwd.hexdigest()), self.memberData['password']) != 0:
            self.boxWarning(u'提示', u'您输入的密码不正确，请重新输入！')
            self.lineEdit_3.setFocus(True)
            return
        ControllerAction.memberData = self.memberData
        self.accept()
        
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
                            f.close()
                        except:
                            if not self.boxConfirm(u'提示', u'身份证读取失败，请从新放置身份证','手动输入','重试'):
                                continue
                            else:
                                self.enableInfoControl()
                                return
                        self.readIDCard()
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
    
    #身份证验证可以使用
    def readIDCard(self):
        self.lineEdit.clear()
        try:
            f = open('./dll/wz.txt', 'r') 
        except:
            self.boxWarning(u'提示', u'身份证读取失败！')
            self.lineEdit.setFocus()
            return False
        f.seek(0) 
        i = 1
        for line in f:  
            if i == 6:
                self.lineEdit.setText(unicode(line.rstrip(), 'gbk').strip()) #身份证号
            i = i+1
        f.close()
        try:
            os.remove('./dll/wz.txt')
        except:
            pass
        self.checkIDCard()