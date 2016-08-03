# -*- coding: utf8 -*-
# Author:       LiuXinwu
# Created:      2015/2/27
#说明：客户管理模块
#
from firefly.server.globalobject import remoteserviceHandle
import json,time
from app.center.core.party import Party
import hashlib,struct
import sys
from lib.db import Mysql
from compiler.ast import TryExcept
reload(sys)
sys.setdefaultencoding( "utf-8" )


@remoteserviceHandle("gate")
def getparty(data,_conn):
    if data!='':
        sql = 'select * from ecs_supplier where suppliers_name like "%'+data+'%"'
    else: 
        sql = 'select * from ecs_supplier'
    try:
        conn=Mysql()
        return json.dumps(({'stat':1,'data':conn.getAll(sql) },"#end"))    
    except:
        return json.dumps(({'stat':-1,'data':''},"#end"))

@remoteserviceHandle("gate")
def upparty(datas,_conn):
    data=datas['data']
    id=datas['id']
    strs = ''
    for k,v in data.items():
            strs += '`'+k+'`'+'= "'+str(v)+'",'
    sql = 'UPDATE `ecs_supplier` SET %s where id ='+id
    sql = (sql%strs[:-1])
    try:
        conn=Mysql()
        conn._cursor.execute(sql)
        conn._conn.commit()
        return json.dumps({'stat':1,'msg':u'更新成功！'})
    except:
        return json.dumps({'stat':-1,'msg':u'更新失败！'})


@remoteserviceHandle("gate")
def querySupGoods(data,_conn):
    partyModel = Party()
    re = partyModel.querySupGoods(data)
    if re:
        return json.dumps({'stat':True,'msg':u'供应商有提供货物，不能删除'})
    else:
        return json.dumps({'stat':False,'msg':u'供应商没有提供货物！'})
    


@remoteserviceHandle("gate")
def updateParty(data,_conn):
    partyModel = Party()
    re = partyModel.updateParty(data)
    if re:
        return json.dumps({'stat':True,'msg':u'更改成功！'})
    else:
        return json.dumps({'stat':False,'msg':u'更改失败'})
    
@remoteserviceHandle("gate")
def addParty(data,_conn):
    partyModel = Party()
    re = partyModel.addParty(data)
    if re:
        return json.dumps({'stat':True,'msg':u'添加成功！'})
    else:
        return json.dumps({'stat':False,'msg':u'添加失败'})



@remoteserviceHandle("gate")
def deleteparty(datas,_conn):
    sql='delete from ecs_supplier where suppliers_id='+datas
    try:
        conn=Mysql()
        conn._cursor.execute(sql)
        conn._conn.commit()
        return json.dumps({'stat':1,'msg':''})
    except:
        return json.dumps({'stat':-1,'msg':''})


@remoteserviceHandle("gate")
def addparty(data,_conn):
    strs = ''
    keys = 'cdate,'
    for k,v in data.items():
        keys += '`'+k+'`,'
        strs += '"'+str(v)+'",'
    sql = "insert party(%s) values(UNIX_TIMESTAMP(),%s)"
    sql = sql % (keys[:-1],strs[:-1])
    try:
        conn=Mysql()
        conn._cursor.execute(sql)
        conn._conn.commit()
        return json.dumps({'stat':1,'msg':''})
    except:
        return json.dumps({'stat':-1,'msg':''})
    
    
