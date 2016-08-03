# -*- coding: utf8 -*-
# Author:       LiuXinwu
# Created:      2015/1/28
#说明：仓库管理模型
#
from firefly.server.globalobject import remoteserviceHandle
from app.center.core.storage import Storage
import json


@remoteserviceHandle("gate")
def findAllStorage(data,_conn):
    storemodel = Storage()
    re = storemodel.findAllStorage()
    if not re:
        return json.dumps(({'stat':-1,'msg':'无记录'},"#end"))
    else:
        return json.dumps(({'stat':1,'data':re},"#end"))

@remoteserviceHandle("gate")
def deleteStorage(data,_conn):
    storemodel = Storage()
    re = storemodel.deleteStorage(data)
    return json.dumps(re)
    
@remoteserviceHandle("gate")
def findAllStorageName(data,_conn):
    storemodel = Storage()
    re = storemodel.findAllStorageName()
    if re:
        return json.dumps({'stat':True,'data':re})
    else:
        return json.dumps({'stat':False,'msg':u'没有仓库名称信息！'})

@remoteserviceHandle("gate")
def insertStorage(data,_conn):
    storemodel = Storage()
    re = storemodel.insertStorage(data)
    if re:
        return json.dumps({'stat':True,'msg':u'仓库插入成功！'})
    else:
        return json.dumps({'stat':False,'msg':u'仓库插入失败！'})

@remoteserviceHandle("gate")
def updateStorage(data,_conn):
    storemodel = Storage()
    re = storemodel.updateStorage(data)
    if re:
        return json.dumps({'stat':True,'msg':u'仓库修改成功！'})
    else:
        return json.dumps({'stat':False,'msg':u'仓库修改失败！'})
    
@remoteserviceHandle("gate")
def findOneStorage(data,_conn):
    storemodel = Storage()
    re = storemodel.findOneStorage(data)
    return json.dumps({'data':re})

@remoteserviceHandle("gate")
def findOneStorageQuYu(data,_conn):
    storemodel = Storage()
    re = storemodel.findOneStorageQuYu(data)
    return json.dumps({'data':re})

@remoteserviceHandle("gate")
def findOneStorageHaoShu(data,_conn):
    storemodel = Storage()
    re = storemodel.findOneStorageHaoShu(data)
    return json.dumps({'data':re})

@remoteserviceHandle("gate")
def findTypeNames(data,_conn):
    storemodel = Storage()
    re = storemodel.findTypeNames()
    if re:
        return json.dumps({'stat':True,'data':re})
    else:
        return json.dumps({'stat':False,'msg':u'请添加仓库类型数据！'})
    
    
@remoteserviceHandle("gate")
def insertStorageType(data,_conn):
    storemodel = Storage()
    re = storemodel.insertStorageType(data)
    if re:
        return json.dumps({'stat':True,'msg':u'添加仓库类型成功！'})
    else:
        return json.dumps({'stat':False,'msg':u'添加仓库类型失败！'})
    
@remoteserviceHandle("gate")
def findAllStorageType(data,_conn):
    storemodel = Storage()
    re = storemodel.findAllStorageType()
    if re:
        return json.dumps(({'stat':True,'data':re},"#end"))
    else:
        return json.dumps(({'stat':False,'msg':u'无数据，请添加仓库类型！'},"#end"))
    
    
@remoteserviceHandle("gate")
def deleteStorageType(data,_conn):
    storemodel = Storage()
    re = storemodel.deleteStorageType(data)
    return json.dumps(re)

@remoteserviceHandle("gate")    
def findOneStorageType(data,_conn):
    storemodel = Storage()
    re = storemodel.findOneStorageType(data)
    return json.dumps({'stat':True,'data':re})

@remoteserviceHandle("gate") 
def updateStorageType(data,_conn):
    storemodel = Storage()
    re = storemodel.updateStorageType(data)
    if re:
        return json.dumps({'stat':True,'msg':u'修改仓库类型成功！'})
    else:
        return json.dumps({'stat':False,'msg':u'修改仓库类型失败！'})
    
@remoteserviceHandle("gate")   
def findOneQuYuHaoShu(data,_conn):
    storemodel = Storage()
    re = storemodel.findOneQuYuHaoShu(data)
    if re:
        return json.dumps({'stat':True,'data':re})
    else:
        return json.dumps({'stat':False,'msg':u'此区域无号数！'})
    
    
@remoteserviceHandle("gate") 
def findQuYuName(data,_conn):
    storemodel = Storage()
    re = storemodel.findQuYuName(data)
    return json.dumps({'stat':True,'data':re})


@remoteserviceHandle("gate")
def findAllQuYu(data,_conn):
    storemodel = Storage()
    re = storemodel.findAllQuYu(data)
    if re:
        return json.dumps(({'stat':True,'data':re},"#end"))
    else:
        return json.dumps(({'stat':False,'msg':u'无数据，请添加仓库区域！'},"#end"))

@remoteserviceHandle("gate")
def insertQuYu(data,_conn):
    storemodel = Storage()
    re = storemodel.insertQuYu(data)
    if re:
        return json.dumps({'stat':True,'msg':u'添加区域成功！'})
    else:
        return json.dumps({'stat':False,'msg':u'添加区域失败！'})

@remoteserviceHandle("gate")  
def deleteQuYu(data,_conn):
    storemodel = Storage()
    re = storemodel.deleteQuYu(data)
    return json.dumps(re)
    
@remoteserviceHandle("gate")   
def updateQuYu(data,_conn):
    storemodel = Storage()
    re = storemodel.updateQuYu(data)
    if re:
        return json.dumps({'stat':True,'msg':u'修改区域成功！'})
    else:
        return json.dumps({'stat':False,'msg':u'修改区域失败！'})
   
@remoteserviceHandle("gate") 
def findAllHaoShu(data,_conn):
    storemodel = Storage()
    re = storemodel.findAllHaoShu(data)
    if re:
        return json.dumps(({'stat':True,'data':re},"#end"))
    else:
        return json.dumps(({'stat':False,'msg':u'无数据，请添加此区域的号数！'},"#end"))
    
@remoteserviceHandle("gate") 
def deleteHaoShu(data,_conn):
    storemodel = Storage()
    re = storemodel.deleteHaoShu(data)
    return json.dumps(re)
   
@remoteserviceHandle("gate") 
def insertHaoShu(data,_conn):
    storemodel = Storage()
    re = storemodel.insertHaoShu(data)
    if re:
        return json.dumps({'stat':True,'msg':u'添加号数成功！'})
    else:
        return json.dumps({'stat':False,'msg':u'添加号数失败！'})
    
    