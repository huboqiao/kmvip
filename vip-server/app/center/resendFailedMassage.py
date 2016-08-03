# -*- coding: utf8 -*-
# Author:       kylin
# Created:      20141/10/14
#说明：每日利息统计线程
#
import threading  
import time  
import urllib
from app.center.core.shots import Shots
from xml.dom.minidom import parseString

class Resend(threading.Thread): 
    def __init__(self):  
        threading.Thread.__init__(self)  
   
    def run(self): 
        while True:
            time.sleep(3600)
            try:
                msg = Shots().getshots()
                # 判断短信模板完整性
                if not msg['stat']:
                    continue
                msg = msg['data'][0]
                if str(msg['isactive']) != '0':
                    continue
                if msg['username'] == '':
                    continue
                if msg['password'] == '':
                    continue
                if msg['url'] == '':
                    continue
                if str(msg['type']) != '0':
                    continue
                failedMassages = Shots().getFailedMassages()
                if not failedMassages:
                    continue
            except:
                continue
            try:
                for failedMassage in failedMassages:
                    try:
                        data = (msg['username'], msg['password'], failedMassage['mtel'], failedMassage['content'])
                        url = msg['url'] + '&account=%s&password=%s&mobile=%s&content=%s'%data
                        url = url.encode('utf-8')
                        sendTime = int(time.time())
                        result = urllib.urlopen(url)
                        lines = result.readlines()
                        result.close()
                        document = ""
                        for line in lines :
                            document += line.decode('utf-8')
                        # 解析返回结果
                        dom =parseString(document)
                        statuDescription = dom.getElementsByTagName("msg").pop().firstChild.data
                        # 更新该短信的发送状态和时间
                        data = (statuDescription,sendTime,failedMassage['id'])
                        Shots().updateMassageRecord(data)
                    except:
                        continue
            except:
                continue
                    
    def stop(self):  
        pass