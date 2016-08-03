#coding:utf8
'''
Created on 2014年9月24日

@author: ivan
'''

from firefly.server.globalobject import netserviceHandle,GlobalObject
#from app.center.autorate import Timer
from app.center.resendFailedMassage import Resend
from app.center.activeFrozenAmount import ActiveFrozenAmount

# 开启每日利息统计线程
#t = Timer()
#t.start()

#resend = Resend()
#resend.start() 

# active = ActiveFrozenAmount()
# active.start()

def doConnectionLost(conn):
    '''当连接断开时调用的方法,这里要判断是否登陆'''
    pass

#GlobalObject().netfactory.doConnectionMade = doConnectionMade           #将自定义的登陆后执行的方法绑定到框架, (补充说明：这里就是所谓的重构方法)
GlobalObject().netfactory.doConnectionLost = doConnectionLost           #将自定义的下线后执行的方法绑定到框架

@netserviceHandle
def Forwarding_0(_conn,data):
    '''消息转发，将客户端发送的消息请求转发给gateserver分配处理
    '''
    dd = GlobalObject().remote['gate'].callRemote("forwarding",data,_conn)
    return dd


@netserviceHandle
def Forwarding_1(_conn,data):
    '''消息转发，将客户端发送的消息请求转发给gateserver分配处理
    '''
    dd = GlobalObject().remote['gate'].callRemote("saveImage",data,_conn)
    return dd

@netserviceHandle
def login_3(_conn,data):
    '''登陆服务'''
    dd = GlobalObject().remote['gate'].callRemote("login",data,_conn)
    return dd
