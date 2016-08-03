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
    dbObject = Mysql()                                            #定义数据库对象全局变量
    userData = data
    '''用户登陆方法'''
    global dbObject, authenticationKey,loginTempList
    #处理用户提交的数据
    if data=='':
        returnStr = "{'status':-1, 'msg':'请输入您的用户名和密码.'}"
        return returnStr
    username = userData['u']
    password = userData['p']
        
    if userData['u']=='' or userData['p']=='':
        returnStr = "{'status':-3, 'msg':'请输入您的用户名和密码.'}"
        return returnStr

     #这里要做参数过滤，因为是Demo所以就不再过滤了
    if dbObject==False:
        returnStr = "{'status':-6, 'msg':'对不起，系统连接丢失，请联系管理员.'}"
        return returnStr

    pwds=hashlib.md5()
    pwds.update(userData['p'])
    returnUserData = dbObject.getOne('select * from user where username="'+str(userData['u'])\
        +'" and password="'+str(pwds.hexdigest())+'"')    
    if returnUserData==False or returnUserData==None:
        returnStr = "{'status':-4, 'msg':'对不起，您的用户名或者密码不正确.'}"
        return returnStr
    #否则返回用户信息 , [0]id, [1]user_name, [2]password
    userkeyStr = str(returnUserData['id'])+returnUserData['username']+authenticationKey
    userkeyStr = hashlib.md5(userkeyStr).hexdigest().upper()
    #查询用户组名
    group = dbObject.getOne('select * from usergroup where id = '+str(returnUserData['group']))
    returnStr = '{"status":1,"userkey":"'+str(userkeyStr)+'","user_id":'+str(returnUserData['id'])+',"user_name":"'+str(returnUserData['username'])+'","nice_name":"'+str(returnUserData['nickname'])+'","group":"'+str(group['group_name'])+'","group_id":"'+str(group['id'])+'","password":"' + str(pwds.hexdigest()) + '"}'
    return returnStr


@remoteserviceHandle("gate")
def getcurrentrole(data,_conn):
    dbObject = Mysql()
    role_list = dbObject.getOne('select a2.role_list,a1.finger from user as a1 left join usergroup as a2 on a1.group=a2.id where a1.id = '+str(data['user_id']))
    return json.dumps(({'data':role_list},"#end"))