#coding:utf8
'''
Created on 2014年9月27日

@author: huaan
设置利率
'''

from PyQt4.QtCore import QThread
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from application.lib.commodel import Socket_model,Connection_Stock
import json
class MemberModel(Socket_model):
    def __init__(self):
        Socket_model.__init__(self)
        self.conn = Connection_Stock().getConnection()
        
    # 根据用户名模糊查询用户信息
    def queryMembername(self, name):
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'queryMembername','data':name}),0) )
        r = self.conn.recv(self.recvBuff)
        r = self.resolveRecvdata(r)
        return json.loads(r)
    
    # 检索客户类型
    def queryMemberGroup(self, condition):
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'queryMemberGroup','data':condition}),0) )
        r = self.conn.recv(self.recvBuff)
        r = self.resolveRecvdata(r)
        return json.loads(r)
    # 发送图片
    def sendImg(self,imgbyte):
        self.conn.sendall(self.sendData(imgbyte,1) )
        r = self.conn.recv(self.recvBuff)
        r = self.resolveRecvdata(r)  
        return json.loads(r)
    # 添加客户
    def addMember(self,data,dataInfo,uid):
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'addMember','data':{'data':data,'dataInfo':dataInfo,'addUser':uid}}),0) )
        r = self.conn.recv(self.recvBuff)
        r = self.resolveRecvdata(r)
        return json.loads(r)
    # 添加客户
    def alterMember(self,data,dataInfo,uid):
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'alterMember','data':{'data':data,'dataInfo':dataInfo,'addUser':uid}}),0) )
        r = self.conn.recv(self.recvBuff)
        r = self.resolveRecvdata(r)
        return json.loads(r)
    # 查询身份证号是否已注册
    def checkIDcard(self, ID):
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'checkIdCard','data':ID}),0) )
        r = self.conn.recv(self.recvBuff)
        r = self.resolveRecvdata(r)
        return json.loads(r)
    # 根据客户组id检索权限
    def queryPower(self, groupId):
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'queryPower','data':groupId}),0) )
        r = self.conn.recv(self.recvBuff)
        r = self.resolveRecvdata(r)
        return json.loads(r)
                
    # 根据身份证号获取用户信息
    def getMemberInfos(self, condition):
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'getMemberInfos','data':condition}),0) )
        r = self.conn.recv(self.recvBuff)
        r = self.resolveRecvdata(r)
        return json.loads(r)
    # 获取用户组
    def getGroups(self, condition):
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'getGroups','data':condition}),0) )
        r = self.conn.recv(self.recvBuff)
        r = self.resolveRecvdata(r)
        return json.loads(r)
    # 获取用户组
    def getGroupPowers(self, powerIDs):
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'getGroupPowers','data':powerIDs}),0) )
        r = self.conn.recv(self.recvBuff)
        r = self.resolveRecvdata(r)
        return json.loads(r)
    