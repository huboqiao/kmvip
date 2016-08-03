# -*- coding: utf8 -*-
# Author:       LiuXinwu
# Created:      2015/1/31
#说明：关于客户资料的查询
#
from firefly.server.globalobject import remoteserviceHandle
from app.center.core.customer import Customer
import json


@remoteserviceHandle("gate")
def updateCustomerStat(data,_conn):
    customerModel = Customer()
    re = customerModel.updateCustomerStat(data)
    if re:
        return json.dumps({'stat':True,'msg':u'客户状态更改成功！'})
    else:
        return json.dumps({'stat':False,'msg':u'客户状态更改失败'})

@remoteserviceHandle("gate")
def findCustomerStat(data,_conn):
    customerModel = Customer()
    re = customerModel.findCustomerStat(data)
    return json.dumps({'stat':True,'data':re})

@remoteserviceHandle("gate")
def findCustomerCardStat(data,_conn):
    customerModel = Customer()
    re = customerModel.findCustomerCardStat(data)
    if re:
        return json.dumps({'stat':True,'data':re})
    else:
        return json.dumps({'stat':False,'msg':u'该客户没有绑定卡'})
    
@remoteserviceHandle("gate")
def findOneCustomer(data,_conn):
    customerModel = Customer()
    re = customerModel.findOneCustomer(data)
    if re:
        return json.dumps({'stat':True,'data':re})
    else:
        return json.dumps({'stat':False,'msg':u'不存在此身份证的客户'})

@remoteserviceHandle("gate")
def findOneCustomerAdditional(data,_conn):
    customerModel = Customer()
    re = customerModel.findOneCustomerAdditional(data)
    if re:
        return json.dumps({'stat':True,'data':re})
    else:
        return json.dumps({'stat':False,'msg':u'此客户没有填写附加信息！'})
    
    
@remoteserviceHandle("gate")   
def findCardWithUid(data,_conn):
    customerModel = Customer()
    re = customerModel.findCardWithUid(data)
    if re:
        return json.dumps({'stat':True,'data':re})
    else:
        return json.dumps({'stat':False,'msg':u'此客户没有绑定卡！'})
    
@remoteserviceHandle("gate") 
def findCardExists(data,_conn):
    customerModel = Customer()
    re = customerModel.findCardExists(data)
    if re:
        return json.dumps({'stat':True,'data':re})
    else:
        return json.dumps({'stat':False,'msg':u'请先添加此金融卡！'})

@remoteserviceHandle("gate")
def bindCardForCustomer(data,_conn):
    customerModel = Customer()
    re = customerModel.bindCardForCustomer(data)
    if re:
        return json.dumps({'stat':True,'msg':u'绑定成功！'})
    else:
        return json.dumps({'stat':False,'msg':u'绑定失败！'})   
    
@remoteserviceHandle("gate")
def guashiCardForCustomer(data,_conn):
    customerModel = Customer()
    re = customerModel.guashiCardForCustomer(data)
    if re:
        return json.dumps({'stat':True,'msg':u'挂失成功！'})
    else:
        return json.dumps({'stat':False,'msg':u'挂失失败！'})
    
@remoteserviceHandle("gate")
def findOneLog(data,_conn):
    customerModel = Customer()
    re = customerModel.findOneLog(data)
    if re:
        return json.dumps({'stat':True,'data':re})
    else:
        return json.dumps({'stat':False,'msg':u'此客户还未曾交易过！'})
    
#业务查询
@remoteserviceHandle("gate")
def queryService(datas,_conn):
    name=datas['name']
    idcard=datas['idcard']
    merchant = Customer()
    re = merchant.serviceQuery(name, idcard)
    return json.dumps((re,"#end"))
    