#coding:utf-8
'''
Created on 2015年1月29日

@author: king
'''

from firefly.server.globalobject import remoteserviceHandle
from lib.massage import MassageModel
from app.center.core.shots import Shots
import json
import time
import thread

@remoteserviceHandle("gate")
def getshots(data,_conn):
    goryset = Shots()
    re = goryset.getshots()
    return json.dumps((re,"#end"))

@remoteserviceHandle("gate")
def getshot(data,_conn):
    goryset = Shots()
    re = goryset.getshots()
    return json.dumps(re)


@remoteserviceHandle("gate")
def addshot(data,_conn):
    goryset = Shots()
    re = goryset.addshots(data)
    return json.dumps((re,"#end"))


@remoteserviceHandle("gate")
def edishot(data,_conn):
    goryset = Shots()
    re = goryset.edishots(data)
    return json.dumps((re,"#end"))

@remoteserviceHandle("gate")
def delshot(data,_conn):
    goryset = Shots()
    re = goryset.delshots(data)
    return json.dumps((re,"#end"))

@remoteserviceHandle("gate")
def noteMassage(data,_conn):
    goryset = Shots()
    re = goryset.noteMassage(data)
    return json.dumps(re)

@remoteserviceHandle("gate")
def sendCustomerMsg(data, _conn):
    model = MassageModel()
    failedCount = 0
    for tel in data['tels']:
#         thread.start_new_thread(model.sendCustomMessage, ({'toMobile':tel, 'content':data['content']},))
        re = model.sendCustomMessage({'toMobile':tel, 'content':data['content']})
        if not re['stat']:
            if cmp(re['msg'], u'你提交过来的短信内容必须与报备过的模板格式相匹配') == 0:
                return json.dumps((re, "#end"))
            failedCount += 1
    return json.dumps(({'failedCount':failedCount}, "#end"))
        
