# -*- coding: utf-8 -*-
'''
Created on 2015年3月3日
发送短信
初始化参数：url
触发信号：sendStatu
返回值{'result':document, # 发送结果XML格式
      'time':t} # 发送时间戳
@author: huaan
'''
import urllib
import time

class SendMassage(object):
    def __init__(self,url):
        self.url = url
        
    def send(self):
        url = self.url.encode('utf-8')
        result = urllib.urlopen(url)
        t = int(time.time())
        lines = result.readlines()
        result.close()
        document = ""
        for line in lines :
            document += line.decode('utf-8')
        return {'result':document, 'time':t}
        
