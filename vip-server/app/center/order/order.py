# -*- coding: utf8 -*-
# Author:       huaan
# Created:      2014/10/15

from firefly.server.globalobject import remoteserviceHandle
from app.center.core.order import Order
import json,time

@remoteserviceHandle("gate")
def orderAdd(data,_conn):
    '''添加订单'''
    model = Order()
    re = model.orderAdd(data)
    
    return json.dumps(re)

@remoteserviceHandle("gate")
def orderAlter(data,_conn):
    '''添加订单'''
    model = Order()
    re = model.orderAlter(data)
    
    return json.dumps(re)
    
@remoteserviceHandle("gate")
def queryPurchasers(data,_conn):
    '''检索采购员'''
    model = Order()
    re = model.getAllValidPurchasers()
    if re:
        return json.dumps({'stat':True, 'data':re})
    else:
        return json.dumps({'stat':False, 'msg':u'没有有效的采购员，请先添加采购员！'})

@remoteserviceHandle("gate")
def querySupplier(data,_conn):
    '''检索供应商'''
    model = Order()
    re = model.getAllValidSuppliers()
    if re:
        return json.dumps({'stat':True, 'data':re})
    else:
        return json.dumps({'stat':False, 'msg':u'没有有效的供应商，请先添加供应商！'})
    
@remoteserviceHandle("gate")
def getGoodsSN(goodsID,_conn):
    '''查询商品'''
    
    model = Order()
    re = model.getGoodsSN(goodsID)
    if re:
        return json.dumps({'stat':True, 'data':re})
    else:
        return json.dumps({'stat':False, 'msg':u'获取商品条形码失败！'})
    
@remoteserviceHandle("gate")
def getOrderList(data,_conn):
    '''查询订单列表'''
    model = Order()
    re = model.getOrderList()
    if re:
        return json.dumps(({'stat':True, 'data':re},"#end"))
    else:
        return json.dumps(({'stat':False, 'msg':u'获取订单列表失败！'},"#end")) 
    
    
@remoteserviceHandle("gate")
def getOrderUsername(data,_conn):
    '''查询订单列表中uid字段的用户真名'''
    model = Order()
    re = model.getUsername(data)
    if re!='':
        return json.dumps({'stat':True, 'data':re})
    else:
        return json.dumps({'stat':False, 'msg':u'没有对应的用户！'}) 
    
    
@remoteserviceHandle("gate")
def deleteOrder(data,_conn):
    '''删除订单'''
    model = Order()
    re = model.deleteOrder(data)
    return json.dumps(re) 


@remoteserviceHandle("gate")
def queryOrderDetail(data,_conn):
    '''查询某个订单与订单info里所有内容'''
    model = Order()
    re = model.queryOrderDetail(data)
    if re:
        return json.dumps(({'stat':True, 'data':re},"#end"))
    else:
        return json.dumps(({'stat':False, 'msg':u'无订单详情可供查询！'},"#end"))

@remoteserviceHandle("gate")
def queryApplyName(data,_conn):
    '''查询某个订单与订单info里所有内容'''
    model = Order()
    re = model.queryApplyName(data)
    if re:
        return json.dumps({'stat':True, 'data':re})
    else:
        return json.dumps({'stat':False, 'msg':u'没有供应商与之对应！'})
    
  
@remoteserviceHandle("gate")
def queryGoodsAndOrderinfo(data,_conn):
    '''查询某个订单与订单info里所有内容'''
    model = Order()
    re = model.queryGoodsAndOrderinfo(data)
    if re:
        return json.dumps({'stat':True, 'data':re})
    else:
        return json.dumps({'stat':False, 'msg':u'无订单详情可供查询！'})  
 
@remoteserviceHandle("gate")
def getOrderInfo(orderID,_conn):
    '''查询某个订单与订单info里所有内容'''
    model = Order()
    re = model.getOrderInfo(orderID)
    if re:
        return json.dumps({'stat':True, 'data':re})
    else:
        return json.dumps({'stat':False, 'msg':u'没有该订单的数据！'})     

@remoteserviceHandle("gate")
def getOneOrder(data,_conn):
    '''查询订单表中某一订单详情'''
    model = Order()
    re = model.getOneOrder(data)
    if re:
        return json.dumps({'stat':True, 'data':re})
    else:
        return json.dumps({'stat':False, 'msg':u'没有这个订单详情！'})

@remoteserviceHandle("gate")
def querySumZongjia(data,_conn):
    '''求出某一订单下所有商品所需的总价'''
    model = Order()
    re = model.querySumZongjia(data)
    if re:
        return json.dumps({'stat':True, 'data':re})
    else:
        return json.dumps({'stat':False, 'msg':u'没购买这种商品！'})
    
    
@remoteserviceHandle("gate")
def filterOrderList(data,_conn):
    '''查询符合条件的order'''

    model = Order()
    re = model.filterOrderList(data)
    if re:
        return json.dumps(({'stat':True, 'test':'test','data':re},"#end"))
    else:
        return json.dumps(({'stat':False,'test':'test', 'msg':u'没有符合这种查询条件的订单！'},"#end"))    


@remoteserviceHandle("gate")
def queryNickname(data,_conn):
    '''查询用户表中所有用户真实姓名及id'''
    model = Order()
    re = model.queryNickname()
    if re:
        return json.dumps({'stat':True, 'data':re})
    else:
        return json.dumps({'stat':False, 'msg':u'未添加用户！'})

@remoteserviceHandle("gate")
def getOrdersID(data,_conn):
    '''查询用户表中所有用户真实姓名及id'''
    model = Order()
    re = model.getOrdersID(data['orderSN'])
    if re != False:
        return json.dumps({'orderExists':True})
    else:
        return json.dumps({'orderExists':False})
    