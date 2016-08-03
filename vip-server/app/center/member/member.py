#coding:utf8
'''
Created on 2015年1月29日
客户资料管理模块
@author: huaan
'''
from firefly.server.globalobject import remoteserviceHandle
from app.center.core.member import Users,Member,UserGroup
from app.center.core.card import Card
import json,time

# 根据用户姓名模糊查询客户信息
@remoteserviceHandle("gate")
def queryMembername(name, _conn):
    member = Member()
    re = member.queryMembername(name)
    return json.dumps(re)

#根据身份证号获取用户信息
@remoteserviceHandle("gate")
def getMemberInfos(idCard,_conn):
    member = Member()
    re = member.getMemberInfos(idCard)
    return json.dumps(re)   


#根据身份证号获取用户信息
@remoteserviceHandle("gate")
def getMemberInfosss(data,_conn):
    member = Member()
    re = member.getMemberInfoss(data)
    return json.dumps(re) 

#根据身份证号获取用户信息
@remoteserviceHandle("gate")
def getMemberInfoss(data,_conn):
    member = Member()
    re = member.getMemberInfoss(data)
    return json.dumps((re, "#end"))
#根据身份证号获取用户信息
@remoteserviceHandle("gate")
def getMemberBaseInfo(data,_conn):
    member = Member()
    re = member.getMemberBaseInfo(data)
    return json.dumps((re, "#end"))
#检索客户类型
@remoteserviceHandle("gate")
def queryMemberGroup(condition,_conn):
    member = Member()
    re = member.queryMemberGroup(condition)   
    return json.dumps(re)

# 添加客户
@remoteserviceHandle("gate")
def addMember(data,_conn):
    member = Member()
    re = member.addMember(data)   
    return json.dumps(re)

# 修改客户资料
@remoteserviceHandle("gate")
def alterMember(data,_conn):
    member = Member()
    re = member.alterMember(data)   
    return json.dumps(re)

#检索客户类型
@remoteserviceHandle("gate")
def checkIdCard(idCard,_conn):
    member = Member()
    re = member.checkIdCard(idCard)   
    return json.dumps(re)

#修改客户资料
@remoteserviceHandle("gate")
def updateMember(datas,_conn):
    data=datas['data']
    datainfo=datas['data_info']
    member = Member()
    re = member.modifyMember(data, datainfo)   
    return json.dumps(re)

#注销客户
@remoteserviceHandle("gate")
def offCustomer(data,_conn):
    member = Member()
    re = member.offMember(data)   
    return json.dumps(re)

#业务查询
@remoteserviceHandle("gate")
def queryService22(data,_conn):
    member = Member()
    re = member.serviceQuery(data)
    return json.dumps((re,"#end"))
    
#修改金荣卡密码
@remoteserviceHandle("gate")
def updateCardPwd(datas,_conn):
    pwd=datas['pwd']
    cardid=datas['cardid']
    card = Card()
    re = card.modifyCardPasswd(cardid, pwd)    
    return json.dumps(re)
    
    