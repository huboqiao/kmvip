# -*- coding: utf8 -*-
# Author:       LiuXinwu
# Created:      2015/03/09
#
from firefly.server.globalobject import remoteserviceHandle
from app.center.core.user import Users,Merchant,UserGroup
import json,time,os
from app.center.core.stock import Stock

@remoteserviceHandle("gate") 
def queryCustomer(data,_conn):

    stockmodel = Stock()
    
    re = stockmodel.queryCustomer(data)
    if re:
        return json.dumps(({'stat':True, 'data':re},"#end"))
    else:
        return json.dumps(({'stat':False, 'msg':u'没有相关客户记录'},"#end"))
    
    
@remoteserviceHandle("gate") 
def queryStockById(data,_conn):

    stockmodel = Stock()
    
    re = stockmodel.queryStockById(data)
    if re:
        return json.dumps(({'stat':True, 'data':re},"#end"))
    else:
        return json.dumps(({'stat':False, 'msg':u'该客户无库存记录'},"#end"))
    