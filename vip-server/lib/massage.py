# -*- coding: utf8 -*-
'''
Created on 2014年10月8日

@author: huaan
'''

from lib.sendMassage import SendMassage
from xml.dom.minidom import parseString
import lib.formatCheck as check
import json, sys
from PyQt4.QtGui import QMessageBox,QApplication
from PyQt4.QtCore import QObject
from app.center.core.shots import Shots

class MassageModel():
        
    def getshots(self, data):
        shots = Shots()
        return shots.getshots()
    
    def noteMassage(self, data):
        # 记录该短信到msglist
        shots = Shots()
        return shots.noteMassage(data)
    
    def sendCustomMessage(self, data):# 接收短信模板数据， 发送短信
        msg = self.getshots('')
        # 判断短信模板完整性
        if not msg['stat']:
            return{'stat':False, 'msg': u'没有可用的短信模板，请在【基本资料维护》短信设置】中添加并启用'}
        msg = msg['data'][0]
        if str(msg['isactive']) != '0':
            return {'stat':False, 'msg': u'当前短信模板未启用，请在【基本资料维护》短信设置】中 启用' }
        if msg['username'] == '':
            return{'stat':False, 'msg': u'您未设置短信平台账号，请在【基本资料维护》短信设置】中 设置'}
        if msg['password'] == '':
            return{'stat':False, 'msg': u'您未设置短信平台密码，请在【基本资料维护》短信设置】中 设置'}
        if msg['url'] == '':
            return{'stat':False, 'msg': u'您未设置短信平台url，请在【基本资料维护》短信设置】中 设置'}
        if str(msg['type']) != '0':
            return{'stat':False, 'msg': u'请在【基本资料维护》短信设置】中 设置提交方式为“get”'}
        
        # 匹配短信模板
        param = (msg['username'], msg['password'], data['toMobile'], data['content'])
        url = msg['url'] + '&account=%s&password=%s&mobile=%s&content=%s'%param
        result = SendMassage(url).send()
        # 根据发送情况插入表
        dom =parseString(result['result'])
        statuDescription = dom.getElementsByTagName("msg").pop().firstChild.data
        code = dom.getElementsByTagName("code").pop().firstChild.data
        data['statu'] = statuDescription
        data['time'] = result['time']
        data['oparetion'] = u'自定义短信'
        data['customerID'] = 0
        
        self.noteMassage(data)
        if cmp(data['statu'], u'提交成功') == 0:
            return {'stat':True}
        else:
            return {'stat':False, 'msg':data['statu']}

    def checkMessageText(self,data):
        # 检查短信相关参数完整性 
        try:
            if not data['customerID']:
                return{'stat':False, 'msg': u'请传入接收短信的客户ID。'}
        except:
            return{'stat':False, 'msg': u'请传入接收短信的客户ID。'}
        # 校验接收短信手机号
        try:
            if not check.checkMobilePhone(data['toMobile']):
                return{'stat':False, 'msg': u'请传入正确的手机号。'}
        except:
            return{'stat':False, 'msg': u'请传入正确的手机号。'}
        
        try:
            if not data['content']['customerName']:
                return{'stat':False, 'msg': u'请传入接收短信的客户名称。'}
        except:
            return{'stat':False, 'msg': u'请传入接收短信的客户名称。'}
        
        try:
            if not data['content']['cardID']:
                return{'stat':False, 'msg': u'请传入接收短信的客户金荣卡号。'}
        except:
            return{'stat':False, 'msg': u'请传入接收短信的客户金荣卡号。'}
        # 时间转换为中文字符串
        try:
            self.t = check.timeStamp(int(data['content']['time']), '%Y/%m/%d %H:%M:%S')
        except:
            return{'stat':False, 'msg': u'请传入操作时间（时间戳）。'}
        # 操作类型编号转换为汉字
        try:
            if not data['oparetion']:
                return{'stat':False, 'msg': u'请传入操作。'}
        except:
            return{'stat':False, 'msg': u'请传入操作。'}
        try:
            float(data['content']['amount'])
        except:
            return{'stat':False, 'msg': u'请传入金额。'}
        try:
            float(data['content']['balance'])
        except:
            return{'stat':False, 'msg': u'请传入账户余额。'}
        contentData = (data['content']['customerName'],
                       data['content']['cardID'],
                       self.t,
                       data['oparetion'],
                       data['content']['amount'],
                       data['content']['balance'])
        
        # 接收短信模板数据， 发送短信
        msg = self.getshots('')
        # 判断短信模板完整性
        if not msg['stat']:
            return{'stat':False, 'msg': u'没有可用的短信模板，请在【基本资料维护》短信设置】中添加并启用'}
        msg = msg['data'][0]
        if str(msg['isactive']) != '0':
            return {'stat':False, 'msg': u'当前短信模板未启用，请在【基本资料维护》短信设置】中 启用' }
        if msg['username'] == '':
            return{'stat':False, 'msg': u'您未设置短信平台账号，请在【基本资料维护》短信设置】中 设置'}
        if msg['password'] == '':
            return{'stat':False, 'msg': u'您未设置短信平台密码，请在【基本资料维护》短信设置】中 设置'}
        if msg['url'] == '':
            return{'stat':False, 'msg': u'您未设置短信平台url，请在【基本资料维护》短信设置】中 设置'}
        if str(msg['type']) != '0':
            return{'stat':False, 'msg': u'请在【基本资料维护》短信设置】中 设置提交方式为“get”'}
        count = msg['content'].count('%s')
        if count != 6:
            return{'stat':False, 'msg': u'短信模板中“%s”字符的个数不是6个，请在【基本资料维护》短信设置】中修改模板。'}
        
        # 匹配短信内容参数
        self.content = msg['content']%contentData
        # 匹配短信模板
        param = (msg['username'], msg['password'], data['toMobile'], self.content)
        url = msg['url'] + '&account=%s&password=%s&mobile=%s&content=%s'%param
        result = SendMassage(url).send()
        # 根据发送情况插入表
        dom =parseString(result['result'])
        statuDescription = dom.getElementsByTagName("msg").pop().firstChild.data
        data['content'] = self.content
        data['statu'] = statuDescription
        data['time'] = result['time']
        
        self.noteMassage(data)
        return {'stat':True}