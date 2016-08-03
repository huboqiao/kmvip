#coding:utf-8
'''
Created on 2015年1月29日

@author: King
'''

from firefly.server.globalobject import remoteserviceHandle

from app.center.core.system import System
import json,time
#删除用户组
@remoteserviceHandle("gate")
def delCustomer(data,_conn):
    goryset = System()
    re = goryset.delCustomer(data)
    return json.dumps((re,"#end"))

#获取用户组
@remoteserviceHandle("gate")
def getcumster(data,_conn):
    goryset = System()
    re = goryset.getcumster(data)
    return json.dumps((re,"#end"))

#获取用户组
@remoteserviceHandle("gate")
def getGroups(data,_conn):
    goryset = System()
    re = goryset.getcumster(data)
    return json.dumps(re)

#获取已经启动的用户组
@remoteserviceHandle("gate")
def getonecumstomer(data,_conn):
    goryset = System()
    re = goryset.getonecumstomer(data)
    return json.dumps((re,"#end"))

#添加权限
@remoteserviceHandle("gate")
def addgory(data,_conn):
    goryset = System()
    re = goryset.addGoryset(data)
    return json.dumps((re,"#end"))


#修改权限
@remoteserviceHandle("gate")
def edigory(data,_conn):
    goryset = System()
    re = goryset.edigory(data)
    return json.dumps((re,"#end"))

#删除权限
@remoteserviceHandle("gate")
def delgory(data,_conn):
    goryset = System()
    re = goryset.delgory(data)
    return json.dumps((re,"#end"))

#获取权限
@remoteserviceHandle("gate")
def getgory(data,_conn):
    goryset = System()
    re = goryset.getgory()
    return json.dumps((re,"#end"))

#获取已经启动的权限
@remoteserviceHandle("gate")
def getsomegory(data,_conn):
    goryset = System()
    re = goryset.getsomegory()
    return json.dumps((re,"#end"))

#获取一个用户组的已经启动的权限
@remoteserviceHandle("gate")
def getonegory(data,_conn):
    goryset = System()
    re = goryset.getonegory(data)
    return json.dumps((re,"#end"))
#获取一个用户组的已经启动的权限
@remoteserviceHandle("gate")
def getGroupPowers(data,_conn):
    goryset = System()
    re = goryset.getonegory(data)
    return json.dumps(re)

#添加用户组
@remoteserviceHandle("gate")
def addcustomer(data,_conn):
    goryset = System()
    re = goryset.addcustomer(data)
    return json.dumps((re,"#end"))
#更新用户组
@remoteserviceHandle("gate")
def updatecustomer(data,_conn):
    goryset = System()
    re = goryset.updatecustomer(data)
    return json.dumps((re,"#end"))