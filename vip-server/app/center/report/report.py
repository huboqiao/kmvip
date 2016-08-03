#coding:utf8
""" 
Author:        

Created:      2014/09/27

Describe：            报表模块

"""
from firefly.server.globalobject import remoteserviceHandle
import json,time,os
from app.center.core.report import Report
from time import sleep



@remoteserviceHandle("gate")
def queryJingbanren(data,_conn):
    ''' 公司资金报表'''
    model = Report()
#     re = model.queryJingbanren()
    re = model.queryCompanyAll(data)
    if re:
        return json.dumps(({'stat':True, 'data':re},"#end"))
    else:
        return json.dumps(({'stat':False, 'msg':u'没有经办人可供查询！'},"#end"))

@remoteserviceHandle("gate")
def queryCompanyZiJinDetail(data,_conn):
    ''' 公司资金报表明细'''
    model = Report()
    re = model.queryCompanyZiJinDetail(data)
    if re:
        return json.dumps(({'stat':True, 'data':re},"#end"))
    else:
        return json.dumps(({'stat':False, 'msg':u'没有经办人可供查询！'},"#end"))
    
@remoteserviceHandle("gate")
def queryCustomerAccount(data,_conn):
    ''' 客户资金报表'''
    model = Report()
    re = model.queryCustomerAccount(data)
    return json.dumps((re,"#end"))

@remoteserviceHandle("gate")
def queryCustomerAccountDetail(data,_conn):
    ''' 客户资金明细报表'''
    model = Report()
    re = model.queryCustomerAccountDetail(data)
    return json.dumps((re,"#end"))

@remoteserviceHandle("gate")
def queryKehuJibenziliao(data,_conn):
    ''' 客户基本资料'''
    model = Report()
    re = model.queryKehuJibenziliao(data)
    return json.dumps((re,"#end"))

@remoteserviceHandle("gate")
def queryGoodsScaleAccount(data,_conn):
    ''' 商品销售管理'''
    
    model = Report()
    re = model.queryGoodsScaleAccount(data)
    return json.dumps((re,"#end"))

@remoteserviceHandle("gate")
def queryGoodsScaleAccountDetail(data,_conn):
    ''' 商品销售明细'''
    
    model = Report()
    re = model.queryGoodsScaleAccountDetail(data)
    return json.dumps((re,"#end"))
    
    
@remoteserviceHandle("gate")
def queryZhuanZhangAccount(data,_conn):
    model = Report()
    re = model.queryZhuanZhangAccount(data)
    return json.dumps((re,"#end"))