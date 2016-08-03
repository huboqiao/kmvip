# -*- coding: utf8 -*-
# Author:       LiuXinwu
# Created:      2015/2/6
#说明：商品模块
#
from firefly.server.globalobject import remoteserviceHandle
import json,time,os
from app.center.core.shop import Shop

jsoncofing = json.load(open('config.json', 'r')).get('imgpath')  
imgpath = jsoncofing['path']

    
@remoteserviceHandle("gate")
def getAllShopClass(data,_conn):
    goodsmodel = Shop()
    re = goodsmodel.getAllShopClass()
    if not re:
        return json.dumps({'stat':-1,'msg':'无记录'})
    else:
        return json.dumps({'stat':1,'data':re})
    
@remoteserviceHandle("gate")
def queryShopClassGoods(data,_conn):
    goodsmodel = Shop()
    re = goodsmodel.queryShopClassGoods(data)
    if not re:
        return json.dumps(({'stat':-1,'msg':'无记录'},"#end"))
    else:
        return json.dumps(({'stat':1,'data':re},"#end"))

@remoteserviceHandle("gate")
def getAllParty(data,_conn):
    goodsmodel = Shop()
    re = goodsmodel.getAllParty()
    if not re:
        return json.dumps({'stat':-1,'msg':'无记录'})
    else:
        return json.dumps({'stat':1,'data':re})

@remoteserviceHandle("gate")
def queryShopClassGoodss(data,_conn):
    goodsmodel = Shop()
    re = goodsmodel.queryShopClassGoods(data)
    if not re:
        return json.dumps(({'stat':-1,'msg':'无记录'},"#end"))
    else:
        return json.dumps(({'stat':1,'data':re},"#end"))

@remoteserviceHandle("gate")
def addShopClass(data,_conn):
    goodsmodel = Shop()
    re = goodsmodel.addShopClass(data)
    if not re:
        return json.dumps({'stat':-1,'msg':'系统内部错误，请稍后添加'})
    else:
        return json.dumps({'stat':1,'msg':'添加商品分类成功，是否继续添加？'})
    
@remoteserviceHandle("gate")
def editShopClass(data,_conn):
    goodsmodel = Shop()
    re = goodsmodel.editShopClass(data['cat_id'],data['data'])
    if not re:
        return json.dumps({'stat':-1,'msg':'系统内部错误，请稍后修改'})
    else:
        return json.dumps({'stat':1,'msg':'修改商品分类成功！'})    
    
@remoteserviceHandle("gate")
def delShopClass(data,_conn):
    goodsmodel = Shop()
    re = goodsmodel.delShopClass(data)
    return json.dumps(re)

@remoteserviceHandle("gate")
def addShopGoods(data,_conn):
    goodsmodel = Shop()
    re = goodsmodel.addShopGoods(data)
    return json.dumps(re)

@remoteserviceHandle("gate")
def editShopGoods(data,_conn):
    goodsmodel = Shop()
    re = goodsmodel.editShopGoods(data)
    return json.dumps(re)


@remoteserviceHandle("gate")
def delShopGoods(data,_conn):
    goodsmodel = Shop()
    re = goodsmodel.delShopGoods(data)
    return json.dumps(re)

@remoteserviceHandle("gate")
def getShopGoodsData(data,_conn):
    goodsmodel = Shop()
    re = goodsmodel.getShopGoodsData(data)
    return json.dumps(re)

@remoteserviceHandle("gate")
def shoporderAdd(data,_conn):
    goodsmodel = Shop()
    re = goodsmodel.shoporderAdd(data)
    return json.dumps(re)
    
@remoteserviceHandle("gate")
def queryShopOrderAccount(data,_conn):
    goodsmodel = Shop()
    re = goodsmodel.queryShopOrderAccount(data)
    return json.dumps((re,"#end"))
    
@remoteserviceHandle("gate")
def queryShopOrderAccountDetail(data,_conn):
    goodsmodel = Shop()
    re = goodsmodel.queryShopOrderAccountDetail(data)
    return json.dumps((re,"#end"))
    
@remoteserviceHandle("gate")
def queryGoodsStockinList(data,_conn):
    goodsmodel = Shop()
    re = goodsmodel.queryGoodsStockinList(data)
    return json.dumps((re,"#end"))
    
    
@remoteserviceHandle("gate")
def queryGoodsStockinInfo(data,_conn):
    goodsmodel = Shop()
    re = goodsmodel.queryGoodsStockinInfo(data)
    return json.dumps((re,"#end"))

    