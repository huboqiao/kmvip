# -*- coding: utf-8 -*-
'''
Created on 2014-09-26

@author: ivan
'''


from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.QtCore import pyqtSignature
import Image,urllib,os
import ConfigParser


#图片处理
class ImageProcess(QThread):
    def __init__(self,parent=None):
        self.cf = ConfigParser.ConfigParser()
        self.cf.read('config.ini')    
    def downloadImg(self,url,imgname):
        try:
            https = 'http://'+self.cf.get('server', 'ip')+'/'
            content = urllib.urlopen(https+url).read()
            fname = os.getcwd()+'/image/'+imgname
            f = file(fname,"wb")
            f.write(content)
            f.close()
#            print fname
            return fname
        except:
            print u'文件IO错误'
            return False
    #生成缩略图
    def thumbnails(self,imgurl,saveimgurl,imgwidth,imgheight):
        try:
            im = Image.open(imgurl)
            out = im.resize((imgwidth,imgheight),Image.ANTIALIAS) #resize image with high-quality
            out.save(saveimgurl)
        except:
            QMessageBox.information(self,u'提示',u'生成缩略图出错',QMessageBox.Ok)
            
    #将图片转化为图片编码(imgurl:图片路径)
    def generatePictureCoding(self,imgurl):
        try:
            fh = open(imgurl, 'rb')  
            return fh.read() 
        except:
            QMessageBox.information(self,u'提示',u'图片转化成编码出错',QMessageBox.Ok)
            return 
    
    #将图片编码生成图片(imgcoding:图片编码，saveimgurl：保存图片的路径)
    def generatePicture(self,imgcoding,saveimgurl):
            f = open(saveimgurl , "wb" )  
            f.write(imgcoding) 
            f.close()
    
    #显示图片(imageurl:图片路径，imageLabel：图片容积，imageVolume：图片标签，left：左边距离，top：上面距离，imgwidth：显示图片宽度，imgheight：显示图片高度)
    def showImage(self,imageurl,imageLabel,imageVolume,left,top,imgwidth,imgheight):
        try:
            if imageVolume.load(imageurl):
                imageLabel.setGeometry(QRect(left,top, imgwidth, imgheight))
                imageLabel.setPixmap(QPixmap.fromImage(imageVolume))
        except:
            QMessageBox.information(self,u'提示',u'显示图片出错',QMessageBox.Ok)
            
        
        