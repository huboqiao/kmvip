# -*- coding: UTF-8 -*-
'''
Created on 2015年1月16日
校验邮箱，身份证号， 手机号码， 电话号码
@author: huaan
'''
import re
import time
import locale
from PyQt4 import QtCore
from PyQt4.QtCore import QRegExp
from PyQt4.QtGui import QRegExpValidator

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

def separate(text):
    result = ''
    for i in text:
        result += '<span>' + i + '</span>'
    return result
        
def checkDate(date):
    a = "((^((1[8-9]\d{2})|([2-9]\d{3}))([-\/\._])(10|12|0?[13578])([-\/\._])(3[01]|[12][0-9]|0?[1-9])$)|(^((1[8-9]\d{2})|([2-9]\d{3}))([-\/\._])(11|0?[469])([-\/\._])(30|[12][0-9]|0?[1-9])$)|(^((1[8-9]\d{2})|([2-9]\d{3}))([-\/\._])(0?2)([-\/\._])(2[0-8]|1[0-9]|0?[1-9])$)|(^([2468][048]00)([-\/\._])(0?2)([-\/\._])(29)$)|(^([3579][26]00)([-\/\._])(0?2)([-\/\._])(29)$)|(^([1][89][0][48])([-\/\._])(0?2)([-\/\._])(29)$)|(^([2-9][0-9][0][48])([-\/\._])(0?2)([-\/\._])(29)$)|(^([1][89][2468][048])([-\/\._])(0?2)([-\/\._])(29)$)|(^([2-9][0-9][2468][048])([-\/\._])(0?2)([-\/\._])(29)$)|(^([1][89][13579][26])([-\/\._])(0?2)([-\/\._])(29)$)|(^([2-9][0-9][13579][26])([-\/\._])(0?2)([-\/\._])(29)$))"
    return re.compile(a).match(str(date))

def stringFilter(control, filters="[\d]+$"):
    regx = QRegExp(filters)
    validator = QRegExpValidator(regx, control)
    control.setValidator(validator)
    
def timeStamp(stamp, showFormat='%Y-%m-%d %H:%M:%S'):
    t= time.localtime(float(stamp))
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

def autoFormat(control, text=''):
    try:
        control.setText(str(locale.format("%.2f", float(text), 1)))
    except:
        return False

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
    if not idCard:
        return False
    idCard = idCard.upper()
    return (re.compile('^[1-9]\d{7}((0\d)|(1[0-2]))(([0|1|2]\d)|3[0-1])\d{3}$').match(str(idCard))
        or re.compile('^[1-9]\d{5}[1-9]\d{3}((0\d)|(1[0-2]))(([0|1|2]\d)|3[0-1])\d{3}([0-9]|X)$').match(str(idCard)))
def checkData(data, mold):
    # 检查待检验数据（data）是否可转为字符串
    try:
        data = str(data)
    except:
        print 'Checking data error, please transfer a string to the function\'s first parameter.'
        return False
    # 检查目标数据格式（mold）是否可转为字符串
    try:
        mold = str(mold).lower()
    except:
        print 'Checking data error, please transfer a string to the function\'s second parameter.'
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
        print 'Checking data error, please transfer correctly string to the function\'s second parameter. \n \
               To check email transfer string \"email\" or \"mail\";\n\
               To check telephone number transfer string \"tel\" or \"telephone\";\n\
               To check mobile phone number stransfer string \"mobile\" or \"mobilephone\";\n\
               To check ID card number stransfer string \"id\" or \"idcard\".\n;\
               The parameter case insensitive'
        return False
    
def check(data, mold):
    # 检查待检验数据（data）是否可转为字符串
    try:
        data = str(data)
    except:
        print 'Checking data error, please transfer a string to the function\'s first parameter.'
        return False
    # 检查目标数据格式（mold）是否可转为字符串
    try:
        mold = str(mold).lower()
    except:
        print 'Checking data error, please transfer a string to the function\'s second parameter.'
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
        print 'Checking data error, please transfer correctly string to the function\'s second parameter. \n \
               To check email transfer string \"email\" or \"mail\";\n\
               To check telephone number transfer string \"tel\" or \"telephone\";\n\
               To check mobile phone number stransfer string \"mobile\" or \"mobilephone\";\n\
               To check ID card number stransfer string \"id\" or \"idcard\".\n;\
               The parameter case insensitive'
        return False
    

#人民币金额转大写
def numtoCny(change_number):
    """
    .转换数字为大写货币格式( format_word.__len__() - 3 + 2位小数 )
    change_number 支持 float, int, long, string
    """
    format_word = ["分", "角", "元",
               "拾","佰","仟","万",
               "拾","佰","仟","亿",
               "拾","佰","仟","万",
               "拾","佰","仟","兆"]

    format_num = ["零","壹","贰","叁","肆","伍","陆","柒","捌","玖"]
    if type( change_number ) == str:
        # - 如果是字符串,先尝试转换成float或int.
        if '.' in change_number:
            try:    change_number = float( change_number )
            except: raise ValueError, '%s   can\'t change'%change_number
        else:
            try:    change_number = int( change_number )
            except: raise ValueError, '%s   can\'t change'%change_number

    if type( change_number ) == float:
        real_numbers = []
        for i in range( len( format_word ) - 3, -3, -1 ):
            if change_number >= 10 ** i or i < 1:
                real_numbers.append( int( round( change_number/( 10**i ), 2)%10 ) )

    elif isinstance( change_number, (int, long) ):
        real_numbers = [ int( i ) for i in str( change_number ) + '00' ]

    else:
        raise ValueError, '%s   can\'t change'%change_number

    zflag = 0                       #标记连续0次数，以删除万字，或适时插入零字
    start = len(real_numbers) - 3
    change_words = []
    for i in range(start, -3, -1):  #使i对应实际位数，负数为角分
        if 0 <> real_numbers[start-i] or len(change_words) == 0:
            if zflag:
                change_words.append(format_num[0])
                zflag = 0
            change_words.append( format_num[ real_numbers[ start - i ] ] )
            change_words.append(format_word[i+2])

        elif 0 == i or (0 == i%4 and zflag < 3):    #控制 万/元
            change_words.append(format_word[i+2])
            zflag = 0
        else:
            zflag += 1

    if change_words[-1] not in ( format_word[0], format_word[1]):
        # - 最后两位非"角,分"则补"整"
        change_words.append("整")

    return ''.join(change_words)