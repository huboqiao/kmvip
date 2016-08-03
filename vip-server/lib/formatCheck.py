# -*- coding: UTF-8 -*-
'''
Created on 2015年1月16日
校验邮箱，身份证号， 手机号码， 电话号码
@author: huaan
'''
import re
import time

def timeStamp(stamp, showFormat='%Y-%m-%d %H:%M:%S'):
    t= time.localtime(stamp)
    t = time.strftime(showFormat, t)
    return t
# 银行卡号每4位添加空格   
def autoSpace(bankCardCount, control, text=''):
    if text == '':
        text = str(control.text())
    charCount = len(str(text))
    if charCount < bankCardCount:
        return charCount
    bankCardCount = charCount
    text = str(text).strip()
    lenght = len(text)
    if lenght == 4 or (lenght - 4) % 5 == 0:
        text = text + ' '
    if lenght != 0 and lenght % 5 == 0:
        text = text[:-1] + ' ' + text[-1]
    control.setText(text)
    return bankCardCount

def autoKFormat(count, control, text='', separator=','):
    if str(text) == '':
        text = str(control.text()).replace(' ', '')
    if str(text).find('.') != -1:
        return str(text).find('.') + 1
    charCount = len(str(text))
    if charCount < count:
        return charCount
    count = charCount
    text = str(text).strip()
    lenght = len(text)
    if text[-1] == ',':
        lenght += 1
    if lenght == 3 or (lenght - 3) % 4 == 0:
        text = text + separator
    if lenght != 0 and lenght % 4 == 0:
        text = text[:-1] + separator + text[-1]
    control.setText(text)
    return count

# 校验邮箱
def checkEmail(email):
    return re.compile('[^\._-][\w\.-]+@(?:[A-Za-z0-9]+\.)+[A-Za-z]+$').match(str(email))
# 校验固定电话号码（必须带区号）
def checkTelephone(tel):
    return re.compile('^0\d{2,3}\d{7,8}$').match(str(tel))       
# 校验手机号码
def checkMobilePhone(mobilePhone):
    return re.compile('^[1][3-8]+\\d{9}$').match(str(mobilePhone))
# 校验身份证号
def checkIdCard(idCard):
    return (re.compile('^[1-9]\d{7}((0\d)|(1[0-2]))(([0|1|2]\d)|3[0-1])\d{3}$').match(str(idCard))
            or re.compile('^[1-9]\d{5}[1-9]\d{3}((0\d)|(1[0-2]))(([0|1|2]\d)|3[0-1])\d{3}([0-9]|X)$').match(str(idCard)))
            
def checkData(data, mold):
    # 检查待检验数据（data）是否可转为字符串
    try:
        data = str(data)
    except:
        return False
    # 检查目标数据格式（mold）是否可转为字符串
    try:
        mold = str(mold).lower()
    except:
        return False
        
    # 校验邮箱
    if mold == 'email' or mold == 'mail':
        return re.compile('[^\._-][\w\.-]+@(?:[A-Za-z0-9]+\.)+[A-Za-z]+$').match(data)
    # 校验固话号码
    elif mold == 'tel' or mold == 'telephone':
        return re.compile('^0\d{2,3}\d{7,8}$').match(data) 
    # 校验手机号码
    elif mold == 'mobile' or mold == 'mobilephone':
        return re.compile('^[1][3-8]+\\d{9}$').match(data)
    # 校验身份证号码
    elif mold == 'id' or mold == 'idcard':
        return (re.compile('^[1-9]\d{7}((0\d)|(1[0-2]))(([0|1|2]\d)|3[0-1])\d{3}$').match(data)
            or re.compile('^[1-9]\d{5}[1-9]\d{3}((0\d)|(1[0-2]))(([0|1|2]\d)|3[0-1])\d{3}([0-9]|X)$').match(data))
    # 检验其他数据不支持
    else:
        return False
    
def check(data, mold):
    # 检查待检验数据（data）是否可转为字符串
    try:
        data = str(data)
    except:
        return False
    # 检查目标数据格式（mold）是否可转为字符串
    try:
        mold = str(mold).lower()
    except:
        return False
        
    # 校验邮箱
    if mold == 'email' or mold == 'mail':
        return re.compile('[^\._-][\w\.-]+@(?:[A-Za-z0-9]+\.)+[A-Za-z]+$').match(data)
    # 校验数字
    elif mold == 'int' or mold == 'number':
        return re.compile('^[0-9]*$').match(data.replace(' ', ''))
    # 校验小数
    elif mold == 'float':
        try:
            return float(data.replace(' ', '').replace(',', ''))
        except:
            return False
    # 添加千分符
    elif mold == 'kformat':
        if float(data.replace(' ', '').replace(',', '')):
            try:
                return format(float(data),',f')[:-4]
            except:
                return False
    # 校验固话号码
    elif mold == 'tel' or mold == 'telephone':
        return re.compile('^0\d{2,3}\d{7,8}$').match(data) 
    # 校验手机号码
    elif mold == 'mobile' or mold == 'mobilephone':
        return re.compile('^[1][3-8]+\\d{9}$').match(data)
    # 校验身份证号码
    elif mold == 'id' or mold == 'idcard':
        return (re.compile('^[1-9]\d{7}((0\d)|(1[0-2]))(([0|1|2]\d)|3[0-1])\d{3}$').match(data)
            or re.compile('^[1-9]\d{5}[1-9]\d{3}((0\d)|(1[0-2]))(([0|1|2]\d)|3[0-1])\d{3}([0-9]|X)$').match(data))
    # 检验其他数据不支持
    else:
        return False