# -*- coding: utf-8 -*-

'''
Created on 2013年12月20日

@author: admin
'''

import win32com.client,win32gui
import ConfigParser


class FingerClass( object ):
    instance = None
    finger = None    
    def __init__(self):
        pass
    
    @staticmethod
    def getFinger(EventsHanld,data):
        global ACTIVEX
        ACTIVEX = data
        if(FingerClass.instance == None):
            cf = ConfigParser.ConfigParser()
            cf.read('config.ini')
            classid = '{'+cf.get('finger','classid')+'}'
            finger = win32com.client.DispatchWithEvents("ZKFPEngXControl.ZKFPEngX", EventsHanld)
            initFinger = finger.InitEngine()
            finger.EnrollCount = cf.get('finger','EnrollCount')
            if initFinger == 0 :
                print u'指纹初始化成功'
                pass
            elif initFinger == 1:
                print '指纹驱动加载失败'
                return
            elif initFinger == 2:
                print '没有连接指纹设备'
                return
            elif initFinger == 3:
                print '指定的指纹设备不存在'
                return
            
            FingerClass.instance = finger
        return FingerClass.instance



class EventsHanld:
    def __init__(self):
        
        global ACTIVEX
        print ACTIVEX.windowTitle()
    #指纹采集
    def OnEnroll(self,ActionResult,ATemplate):
        if ActionResult:
            self.EncodeTemplate1(ATemplate)
            ACTIVEX.obj.fingerdata = self.EncodeTemplate1(ATemplate)
            self.CancelEnroll()
            ACTIVEX.close()
        else:
            self.reEnroll()
        
    #显示指纹图像
    def OnImageReceived(self,AImage):
        #print 1
        #ACTIVEX.label_2.setText(str(self.EnrollIndex)) 
        title = str(ACTIVEX.windowTitle())
        if title == '指纹录入':
            ACTIVEX.label_2.setText(str(self.EnrollIndex)) 
            self.PrintImageAt(win32gui.GetDC(win32gui.FindWindow(None,u'指纹录入')), 10, 10, 260, 290)
        elif title == '锁屏':
            self.PrintImageAt(win32gui.GetDC(win32gui.FindWindow(None,u'锁屏')), 0, 0, 270, 200)
        elif title=='指纹验证':
            self.PrintImageAt(win32gui.GetDC(win32gui.FindWindow(None,u'指纹验证')), 0, 0, 270, 200)
            
    def reEnroll(self):
        ACTIVEX.pushButton.setEnabled(True)
        ACTIVEX.label.setVisible(True)
        self.CancelEnroll()
        ACTIVEX.label_2.setText(str('')) 
        
    #匹配指纹
    def OnCapture(self,ActionResult,ATemplate):
        ACTIVEX.checkFinger(self.EncodeTemplate1(ATemplate))
            

                    
