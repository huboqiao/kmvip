# -*- coding: utf-8 -*-
'''
Created on 2014-06-12

@author: chenyong
'''

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.QtCore import pyqtSignature
from application.view.cam import Ui_dialog
from application.lib.cam import AutoCam
from application.lib.ImageProcess import ImageProcess
import Image
# from PIL import Image
import time
import os 
import sys,logging,logging.config
import ConfigParser

# logging.config.fileConfig("log.conf")
QTextCodec.setCodecForTr(QTextCodec.codecForName("utf8"))  

class CamController(QDialog, Ui_dialog):
    def __init__(self, data=None):
        QDialog.__init__(self, data)
        self.setupUi(self)
        self.parent = data
        try:
            self.connect(self.pushButton, SIGNAL("clicked()"), self.paipai)
            # 初始化图形
            self.path = os.getcwd() + '/image/photo.png'
            logging.info(str(self.parent)+','+str(self.parent.cam))
            self.parent.cam.saveSnapshot(self.path, timestamp=3, boldfont=1, quality=75)
            self.Qimage = QLabel(self.frame) 
            self.image = QImage()
            self.autoCam()
    
            self.test = AutoCam(self)
            self.connect(self.test, SIGNAL('autoCam'), self.autoCam)
            self.test.start()
            
            cf = ConfigParser.ConfigParser()
            cf.read('config.ini')
            self.quality = int(cf.get('cam', 'quality'))
            self.timestamp = int(cf.get('cam', 'timestamp'))
            self.boldfont = int(cf.get('cam', 'boldfont'))
            self.size = int(cf.get('cam', 'smalimagesize'))
            self.isVisible()
        except Exception as e :
            self.slotInformation(e)
    
    
    # 初始化摄像头设备错误提示
    def slotInformation(self,strs):  
        logging.info(strs)
        #QMessageBox.information(self, self.tr("提示"),
                                #self.tr(strs), self.tr("确定"))
                                #self.tr("初始化摄像头设备失败，请检查摄像头设备！"), self.tr("确定"))  
    def paipai(self):
            self.parent.cam.saveSnapshot(os.getcwd() + '/image/s2.png', timestamp=self.timestamp, boldfont=self.boldfont, quality=self.quality)
            self.autoCam()
            img = ImageProcess()
            img.thumbnails(os.getcwd() + '/image/s2.png', os.getcwd() + '/image/s3.png', 170, 170)
            self.parent.showimage()
            self.close()

    # 修复关闭时候的异常
    @pyqtSlot()
    def closeEvent(self, eve):
        print 12333
        self.close()        
            
        
    def autoCam(self):
        try:
            if self.image.load(os.getcwd() + '/image/photo.png'):
                self.Qimage.setPixmap(QPixmap.fromImage(self.image))  
                self.resize(500, 400) 
        except:
            pass 
    

