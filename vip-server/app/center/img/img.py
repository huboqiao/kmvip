# -*- coding: utf8 -*-
# Author:       ivan
# Created:      2014/09/27
#说明：图处保存模块
#
from firefly.server.globalobject import remoteserviceHandle
import json,time,os

jsoncofing = json.load(open('config.json', 'r')).get('imgpath')  
imgpath = jsoncofing['path']

@remoteserviceHandle("gate")
def saveImage(imgbyte,_conn):
    '''将客户端传来的图像二进制流保存到指定文件夹'''
    data = imgbyte
    name = str(int(time.time()))+'.png'
    filename = imgpath+name
    resultimgpath = '/img/'+name
    s = open(filename,'wb')
    s.write(data)
    s.close()
    return json.dumps({'stat':1,'msg':'上传成功','path':resultimgpath})
