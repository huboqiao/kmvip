# -*- coding: utf-8 -*-
'''
Created on 2014-06-12

@author: ivan
'''


from VideoCapture import Device

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.QtCore import pyqtSignature
from application.view.cam import Ui_dialog
import time,os,Image,ConfigParser,logging,logging.config

# logging.config.fileConfig("log.conf")

class AutoCam(QThread):
    def __init__(self,data):
        try: 
            super(AutoCam,self).__init__()
            self.T = False
            self.mutex = QMutex()        
            self.data = data
            cf = ConfigParser.ConfigParser()
            cf.read('config.ini')
            self.speed = float(cf.get('cam','speed'))
            self.quality = int(cf.get('cam','quality'))
            self.timestamp = int(cf.get('cam','timestamp'))
            self.boldfont = int(cf.get('cam','boldfont'))
            self.size = int(cf.get('cam','smalimagesize'))
            self.camint = int(cf.get('cam','camint'))
        except:
            pass
        
    
    def run(self):
        try:
            with QMutexLocker(self.mutex):
                self.T = False        
            while True:
                if self.T:
                    return      
                time.sleep(self.speed)
                
                if self.data.isVisible() == False:
                    return      
                try:
                    self.data.parent.cam.saveSnapshot(self.data.path, timestamp=self.timestamp,boldfont=self.boldfont, quality=self.quality)
                except:
                    pass
                self.emit(SIGNAL("autoCam"),self.data.path,False)
        except:
            pass
            
    def stop(self):
        with QMutexLocker(self.mutex):
            self.T = True       
            
class CamClass( object ):
    instance = None
    def __init__(self):
        pass
    @staticmethod
    def getCam(camint=0):
        global ACTIVEX
        
        if(CamClass.instance == None):
            try:
                cam = Device(devnum=camint, showVideoWindow=0)
                CamClass.instance = cam
            except Exception as e:
                CamClass.instance = None
        return CamClass.instance

 
 