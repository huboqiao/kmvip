# -*- coding: utf-8 -*-
'''
Created on 2014年6月11日

@author: chenyong
'''
from PyQt4 import QtGui
from application.lib.Commethods import *
from application.view.interestpayinfo import Ui_Dialog
import time,math
import locale



class InterestPayInfoController(ControllerAction,Ui_Dialog):
    def __init__(self,parent=None):
        ControllerAction.__init__(self,parent)
        self.parent=parent
       
        locale.setlocale(locale.LC_ALL, '') 
        
        self.label.setText(self.parent.dates)
        self.label_3.setText(str(locale.format("%.3f", float(self.parent.conunt_price), 1))+u'元')
        self.label_6.setText(self.tr(str(self.numtoCny(float(self.parent.conunt_price)))))
        self.connect(self.pushButton, SIGNAL("clicked()"),self.submit)             #确认发放
        self.connect(self.pushButton_2, SIGNAL("clicked()"),SLOT('close()'))       #取消
    
    #确认发放    
    def submit(self):
        self.close()
        self.parent.goPay()
        
        
        
    #人民币金额转大写
    def numtoCny(self,change_number):
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


   
    
