#coding:utf8

from firefly.server.globalobject import remoteserviceHandle
from firefly.server.globalobject import GlobalObject
from datetime import *
import json,sys,os,time, hashlib                                        #载入一些基础的模块
main_root = os.path.dirname(os.path.dirname(__file__))
sys.path.append(main_root)                                                
from  lib.db import Mysql
sysConfig = json.load(open('config.json', 'r'))
authenticationKey = sysConfig.get("other")
authenticationKey = authenticationKey['authenticationKey']                #载入随机串


def callbackSingleClientData(_conn, callbackstr):                        
    GlobalObject().netfactory.pushObject(0, callbackstr,[_conn.transport.sessionno])

@remoteserviceHandle("gate")
def login(data,_conn):
    '''用户登陆方法'''
    dbObject = Mysql()                                            #定义数据库对象全局变量
    global dbObject, authenticationKey,loginTempList
    #处理用户提交的数据
    data = str(data)
    if data=='':
        returnStr = "{'status':-1, 'msg':'请输入您的用户名和密码.'}"
        #return callbackSingleClientData(_conn, returnStr)
        return returnStr
        
    try:
        userData = eval(data)
    except Exception, e:
        returnStr = "{'status':-5, 'msg':'数据格式不正确, 错误代码:-5.'}"
        #return callbackSingleClientData(_conn, returnStr)
        return returnStr
    try:
        username = userData['u']
        password = userData['p']
    except Exception, e:
        returnStr = "{'status':-2, 'msg':'系统内部错误, 错误代码:-2.'}"
        #return callbackSingleClientData(_conn, returnStr)
        return returnStr
        
    if userData['u']=='' or userData['p']=='':
        returnStr = "{'status':-3, 'msg':'请输入您的用户名和密码.'}"
        #return callbackSingleClientData(_conn, returnStr)
        return returnStr

     #这里要做参数过滤，因为是Demo所以就不再过滤了
    if dbObject==False:
        returnStr = "{'status':-6, 'msg':'对不起，系统连接丢失，请联系管理员.'}"
        #return callbackSingleClientData(_conn, returnStr)                #连接数据库失败
        return returnStr

    pwds=hashlib.md5()
    pwds.update(userData['p'])
    returnUserData = dbObject.getOne('select * from user where username="'+str(userData['u'])\
        +'" and password="'+str(pwds.hexdigest())+'"')    
    if returnUserData==False or returnUserData==None:
        returnStr = "{'status':-4, 'msg':'对不起，您的用户名或者密码不正确.'}"
        #return callbackSingleClientData(_conn, returnStr)
        return returnStr
    #否则返回用户信息 , [0]id, [1]user_name, [2]password
    userkeyStr = str(returnUserData['id'])+returnUserData['username']+authenticationKey
    userkeyStr = hashlib.md5(userkeyStr).hexdigest().upper()
    returnStr = '{"status":1,"userkey":"'+str(userkeyStr)+'","user_id":'+str(returnUserData['id'])+',"user_name":"'+str(returnUserData['username'])+'"}'
    #callbackSingleClientData(_conn, returnStr) 
    return returnStr
