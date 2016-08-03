# -*- coding: utf8 -*-
# Author:       kylin
# Created:      2015/2/7



from firefly.server.globalobject import remoteserviceHandle
from app.center.core.rate import Rate
import json,time


@remoteserviceHandle("gate")
def queryRate(data,_conn):
    '''查询利率'''
    model = Rate()
    re = model.queryRate(data)
    
    return json.dumps((re,"#end"))

@remoteserviceHandle("gate")
def updateRate(data,_conn):
    '''更新利率'''
    model = Rate()
    re = model.updateRate(data)
    
    return json.dumps((re,"#end"))
    

@remoteserviceHandle("gate")
def ratesList(data,_conn):
    """利息列表"""
    model = Rate()
    re = model.ratesList(data)
    
    return json.dumps((re,"#end"))

@remoteserviceHandle("gate")
def payRates(data,_conn):
    """利息结算"""
    model = Rate()
    re = model.payRates(data)
    
    return json.dumps((re,"#end"))
    

