# -*- coding: utf8 -*-
# Author:       ivan
# Created:      2014/09/27
#说明：用户管理模块
#
from firefly.server.globalobject import remoteserviceHandle
from app.center.core.user import Users,Merchant,UserGroup
from app.center.core.card import Card
import json,time


@remoteserviceHandle("gate")
def alterMyPassword(data,_conn):
    '根据指纹获取用户信息'
    model = Users()
    re = model.alterMyPassword(data)
    return json.dumps(re)

@remoteserviceHandle("gate")
def getInfosByFinger(finger,_conn):
    '根据指纹获取用户信息'
    model = Users()
    re = model.getInfosByFinger(finger)
    return json.dumps((re, "#end"))
@remoteserviceHandle("gate")
def getGrantsFinger(groupId,_conn):
    '''获用户及管理员信息'''
    userModel = Users()
    re = userModel.getGrantsFinger(groupId)
    return json.dumps((re, "#end"))
@remoteserviceHandle("gate")
def getRightersFingers(data,_conn):
    '''获用户及管理员信息'''
    userModel = Users()
    re = userModel.getRightersFingers()
    return json.dumps((re, "#end"))
    
@remoteserviceHandle("gate")
def getUserAndAdmin(uid,_conn):
    '''获用户及管理员信息'''
    userModel = Users()
    usergroup = UserGroup()
    re = userModel.queryUserAndAdmin(uid)
    power = usergroup.queryResource()
    re['resource'] = power
    return json.dumps((re,"#end"))

@remoteserviceHandle("gate")
def memberAdd(datas,_conn):
    '''添加会员卡'''
    merchant = Merchant()            
    data = datas['data']
    datainfo = datas['data_info']
    uid = datas['uid']
    '''新加会员卡用户'''
    re = merchant.addMerchant(data,datainfo,uid)
    return json.dumps(re)

@remoteserviceHandle("gate")
def queryMerchant(datas,_conn):
    '''查询客户'''
    merchant = Merchant()            
#    re = merchant.queryAllMerchant(datas)
    re = merchant.queryMerchant(datas)
    ''''''
    store = Store()
    return json.dumps((re,"#end"))
    for i in re:
        storename = store.queryStoreName(i['storename'])
        i['storename'] = storename['name']
    return json.dumps((re,"#end"))

@remoteserviceHandle("gate")
def queryUser(data,_conn):
    '''获取所有的员工用户信息'''
    userModel = Users()
    uid = data
    re = userModel.queryUser(uid)
    return json.dumps((re,"#end"))

@remoteserviceHandle("gate")
def idcardQueryMerchant(data,_conn):
    '''通过身份证查询客户资料'''
    merchant = Merchant()            
    cardModel = Card()
    ctpy = data['flag']
    idcard = data['idcard']
    #第一步查询对应身份证的客户信息，包括基本资料、开户信息、安全问答、绑定卡及状态
    usedata =merchant.queryMerchant(idcard,'sel')

    #第二步查询该客户最近30天的用卡记录
    if usedata:
        carddata = cardModel.queryCardRecord(usedata['cardid'])
        data = {'userdata':usedata,'cardrecord':carddata}
        return json.dumps({'stat':1,'userdata':usedata,'cardrecord':carddata})
    else:
        #如果没有找到用户有卡那么就查询客户基本资料不需要查卡
        if ctpy == 'False':
            usedata =merchant.queryMerchant(idcard,'sel','changecard')
            if usedata :
                if usedata['actdate'] != None:
                    usedata['actdate'] = (int(time.time())-int(usedata['actdate']))/(3600*24)
                return json.dumps({'stat':1,'userdata':usedata})
            else:
                return json.dumps({'stat':-1,'msg':'该身份证不存在!'})
        else:
            return json.dumps({'stat':-1,'msg':'没有查到相关记录'})

@remoteserviceHandle("gate")
def getPow2(data,_conn):
    '''获取用户组权限资源'''
    usergroup = UserGroup()
    udate = usergroup.qeuryGroup(data)
    resource = usergroup.queryResource()
    return json.dumps({'usergroup':udate,'resource':resource})

@remoteserviceHandle("gate")
def getPow(data,_conn):
    '''获取用户组权限资源'''
    usergroup = UserGroup()
    udate = usergroup.qeuryGroup(data)
    resource = usergroup.queryResource()
    return json.dumps(({'usergroup':udate,'resource':resource},"#end"))

@remoteserviceHandle("gate")
def delGroup(groupid,_conn):
    '''删除用户组'''
    usergroup = UserGroup()
    re = usergroup.delGroup(groupid)
    return json.dumps(re)

@remoteserviceHandle("gate")
def addGroup(data,_conn):
    '''添加用户组'''
    usergroup = UserGroup()
    name = data['group_name']
    role_list = data['role_list']
    txt = data['txt']
    re = usergroup.addGroup(name, role_list, txt)
    return json.dumps(re)

@remoteserviceHandle("gate")
def editGroup(data,_conn):
    '''修改用户组'''
    usergroup = UserGroup()
    re = usergroup.modifyGroup(data)
    return json.dumps(re)

@remoteserviceHandle("gate")
def addUser(data,_conn):
    '''添加员工'''
    userModel = Users()
    
    re = userModel.addUser(data)
    return json.dumps(re)

@remoteserviceHandle("gate")
def modifyUser(datas,_conn):
    '''修改用户'''
    userModel = Users()
    
    data = datas['data']
    datainfo = datas['datainfo']
    re = userModel.modifyUser(data,datainfo)
    return json.dumps(re)

@remoteserviceHandle("gate")
def delUser(uid,_conn):
    '''删除员工'''
    userModel = Users()
    re = userModel.delUser(uid)
    return json.dumps(re)

@remoteserviceHandle("gate")
def querySuppliers(data,_conn):
    MerchantModel = Merchant()
    re = MerchantModel.querySuppliers(data)
    
    if re:
        return json.dumps(({'state':True, 'data':re},"#end"))
    else:
        return json.dumps(({'state':False, 'msg':u'未找到符合条件的供应商信息。'},"#end"))
    
    
@remoteserviceHandle("gate") 
def findSuppliers(data,_conn):
    merchantModel = Merchant()
    re = merchantModel.findSuppliers(data)
    if re:
        return json.dumps(({'state':True, 'data':re},"#end"))
    else:
        return json.dumps(({'state':False, 'msg':u'未找到符合条件的供应商信息。'},"#end"))
