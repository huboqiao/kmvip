# -*- coding: utf8 -*-
# Author:       LiuXinwu
# Created:      2015/2/6
#说明：商品模块
#
from firefly.server.globalobject import remoteserviceHandle
import json,time,os
from app.center.core.goods import Goods

jsoncofing = json.load(open('config.json', 'r')).get('imgpath')  
imgpath = jsoncofing['path']

    
@remoteserviceHandle("gate")
def getAllClass(data,_conn):
    goodsmodel = Goods()
    re = goodsmodel.getAllClass()
    if not re:
        return json.dumps({'stat':-1,'msg':'无记录'})
    else:
        return json.dumps({'stat':1,'data':re})
    
@remoteserviceHandle("gate")
def queryClassGoods(data,_conn):
    goodsmodel = Goods()
    re = goodsmodel.queryClassGoods(data)
    if not re:
        return json.dumps(({'stat':-1,'msg':'无记录'},"#end"))
    else:
        return json.dumps(({'stat':1,'data':re},"#end"))

@remoteserviceHandle("gate")
def queryClassGoodss(data,_conn):
    goodsmodel = Goods()
    re = goodsmodel.queryClassGoods(data)
    if not re:
        return json.dumps(({'stat':-1,'msg':'无记录'},"#end"))
    else:
        return json.dumps(({'stat':1,'data':re},"#end"))

@remoteserviceHandle("gate")
def addClass(data,_conn):
    goodsmodel = Goods()
    re = goodsmodel.addClass(data)
    if not re:
        return json.dumps({'stat':-1,'msg':'系统内部错误，请稍后添加'})
    else:
        return json.dumps({'stat':1,'msg':'添加商品分类成功，是否继续添加？'})
    
@remoteserviceHandle("gate")
def editClass(data,_conn):
    goodsmodel = Goods()
    re = goodsmodel.editClass(data['cid'],data['muid'],data['data'])
    if not re:
        return json.dumps({'stat':-1,'msg':'系统内部错误，请稍后修改'})
    else:
        return json.dumps({'stat':1,'msg':'修改商品分类成功！'})    
    
@remoteserviceHandle("gate")
def delClass(data,_conn):
    goodsmodel = Goods()
    re = goodsmodel.delClass(data)
    return json.dumps(re)

@remoteserviceHandle("gate")
def addGoods(data,_conn):
    goodsmodel = Goods()
    re = goodsmodel.addGoods(data)
    return json.dumps(re)

@remoteserviceHandle("gate")
def editGoods(data,_conn):
    goodsmodel = Goods()
    re = goodsmodel.editGoods(data)
    return json.dumps(re)

@remoteserviceHandle("gate")
def delGoods(data,_conn):
    goodsmodel = Goods()
    re = goodsmodel.delGoods(data)
    return json.dumps(re)