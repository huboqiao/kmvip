# -*- coding: utf8 -*-
# Author:       huaan
# Created:      2015/04/10
#说明：缴费管理模块
from firefly.server.globalobject import remoteserviceHandle
from app.center.core.payment import Payment
import json
# 检索缴费项目
@remoteserviceHandle("gate")
def payNow(data,_conn):
    model = Payment()
    re = model.payNow(data)
    return json.dumps((re, "#end"))

# 检索缴费项目
@remoteserviceHandle("gate")
def queryPayTypes(data,_conn):
    model = Payment()
    re = model.queryPayTypes(data)
    return json.dumps((re, "#end"))

# 检索数据（缴费项目和缴费记录）
@remoteserviceHandle("gate")
def queryData(data,_conn):
    model = Payment()
    re = model.queryPaymentRecord(data['data'])
    re = {'record':re}
    if data['isQueryType']:
        payTypes = model.queryPayTypes({'typeStat':1})
        re['payTypes'] = payTypes
    return json.dumps((re, "#end"))
# 添加缴费项目
@remoteserviceHandle("gate")
def addPayType(data,_conn):
    model = Payment()
    re = model.addPayType(data)
    return json.dumps((re, "#end"))
# 生成待缴费单
@remoteserviceHandle("gate")
def addPayment(data,_conn):
    model = Payment()
    re = model.addPayment(data)
    return json.dumps((re, "#end"))
# 修改待缴费单
@remoteserviceHandle("gate")
def alterPayment(data,_conn):
    model = Payment()
    re = model.alterPayment(data)
    return json.dumps((re, "#end"))
# 修改缴费项目
@remoteserviceHandle("gate")
def alterPayType(data,_conn):
    model = Payment()
    re = model.alterPayType(data)
    return json.dumps((re, "#end"))

# 删除缴费项目
@remoteserviceHandle("gate")
def deletePayType(data,_conn):
    model = Payment()
    re = model.deletePayType(data)
    return json.dumps((re, "#end"))

# 删除待缴费记录
@remoteserviceHandle("gate")
def deletePayments(data,_conn):
    model = Payment()
    re = model.deletePayments(data)
    return json.dumps((re, "#end"))

