# -*- coding: utf8 -*-
# Author:       huaan
# Created:      2015/01/29
#说明：华安自定义仓库管理模型
#
from firefly.server.globalobject import remoteserviceHandle
from lib.db import Mysql
import json
import hashlib
import time
import sys

reload(sys)
sys.setdefaultencoding( "utf-8" )

class HaStorage(Mysql):
    def __init__(self):
        Mysql.__init__(self)
    # 检索仓库
    def queryAllStore(self):
        sql = "select * from storage where stat = 1"
        return self.getAll(sql)
    
    # 根据仓库ID检索区域
    def queryAllRegionByStoreId(self, storeId):
        try:
            sql = "select * from storage_qy where isactive = 1 and sid = %s"%int(storeId)
            return self.getAll(sql)
        except:
            return False
         
    # 根据区域ID检索号数
    def queryAllSerialNumberByRegionId(self, regionId):
        try:
            sql = "select * from storage_hs where stat = 1 and qid = %s"%int(regionId)
            return self.getAll(sql)
        except:
            return False    
             
    # 检索仓库类别
    def queryStoreType(self):
        try:
            sql = "select * from storagetype where stat = 1"
            return self.getAll(sql)
        except:
            return False
        
# 检索仓库
@remoteserviceHandle("gate")
def queryStoreName2(data,_conn):
    re = HaStorage().queryAllStore()
    if not re:
        return json.dumps({'stat':False,'msg':u'无记录'})
    else:
        return json.dumps({'stat':True,'data':re})
 # 根据仓库ID检索区域
@remoteserviceHandle("gate")
def queryAllRegionByStoreId(storeId,_conn):
    re = HaStorage().queryAllRegionByStoreId(storeId)
    if not re:
        return json.dumps({'stat':False,'msg':u'无记录'})
    else:
        return json.dumps({'stat':True,'data':re})
# 根据区域ID检索号数
@remoteserviceHandle("gate")
def queryAllSerialNumberByRegionId(regionId,_conn):
    re = HaStorage().queryAllSerialNumberByRegionId(regionId)
    if not re:
        return json.dumps({'stat':False,'msg':u'无记录'})
    else:
        return json.dumps({'stat':True,'data':re})
    
# 检索仓库类别
@remoteserviceHandle("gate")
def queryStoreType(data,_conn):
    re = HaStorage().queryStoreType()
    if not re:
        return json.dumps({'stat':False,'msg':u'无记录'})
    else:
        return json.dumps({'stat':True,'data':re})
    
