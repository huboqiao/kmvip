# --*-- coding:utf-8 --*--
'''
Created on 2014年6月13日

@author: kylin

商品操作类
'''
import hashlib,struct
import time,sys
from lib.db import Mysql

import json
from compiler.ast import TryExcept
reload(sys)
sys.setdefaultencoding( "utf-8" )

class Goods(Mysql):
    def __init__(self):
        Mysql.__init__(self)
         
    #获得所有商品类别
    def getAllClass(self):
        sql ="select * from goodsclass"
        try:
            return self.getAll(sql)
        except:
            return False
    
    #查询某类别下所有商品
    def queryClassGoods(self,data):   
        sql = 'select * from goods where pclass ='+str(data['parentid'])
        try:
            return self.getAll(sql)     
        except:
            return False
        
    def addClass(self,data):
        strs = ''
        keys = 'cdate,'
        for k,v in data.items():
            keys += '`'+k+'`,'
            strs += '"'+str(v)+'",'
        sql = "insert goodsclass(%s) values(UNIX_TIMESTAMP(),%s)"
        sql = sql % (keys[:-1],strs[:-1])
        try:
            self._cursor.execute(sql)
            self._conn.commit()
            return True
        except:
            return False
        
    #修改商品类别
    def editClass(self,cid,muid,data):
        strs = 'mdate =UNIX_TIMESTAMP(),'
        for k,v in data.items():
                strs += '`'+k+'`'+'= "'+str(v)+'",'
        sql = 'UPDATE `goodsclass` SET muid = '+str(muid)+', %s where id ='+str(cid)
        sql = (sql%strs[:-1])
        
        try:
            self._cursor.execute(sql)
            self._conn.commit()
            return True
        except:
            return False
    def queryClassGoods(self,data):
        
        sql = 'select * from goods where pclass ='+str(data['parentid'])
        return self.getAll(sql)
            
    def delClass(self,data):
        '''删除分类
            1、判断分类下是否有商品，如果有的话不能删除
        '''
        classdata = self.queryClassGoods({'parentid':data['cid']})
        if classdata:
            return {'stat':False,'msg':u'该分类下有商品资料，请先清除商品资料数据'}
        #判断是否有子分类
        if self.queryChildClass(data):
            return {'stat':False,'msg':u'该分类下有子分类，请先清除子分类'}
        sql = 'delete from goodsclass where id ='+str(data['cid'])
        try:
            self._cursor.execute(sql)
            self._conn.commit()
            return {'stat':True,'msg':u'删除分类成功'}
        except:
            return {'stat':False,'msg':u'删除分类失败'}
        
    def queryChildClass(self,data):
        sql = 'select * from goodsclass where parentid ='+data['cid']
        return self.getAll(sql)
    
    #为某类别添加商品
    def addGoods(self,data):
        strs = ''
        keys = 'cdate,'
        for k,v in data.items():
            keys += '`'+k+'`,'
            strs += '"'+str(v)+'",'
        sql = "insert into goods(%s) values(UNIX_TIMESTAMP(),%s)"
        try:
            sql = sql % (keys[:-1],strs[:-1])
            self._cursor.execute(sql)
            self._conn.commit()
            return {'stat':True,'msg':u'添加商品成功，是否继续添加？'}
        except:
            return {'stat':False,'msg':u'系统内部错误，请稍后添加'}   
         
    #修改商品信息
    def editGoods(self,data):
        strs = 'mdate =UNIX_TIMESTAMP(),'
        for k,v in data['data'].items():
                strs += '`'+k+'`'+'= "'+str(v)+'",'
        sql = 'UPDATE `goods` SET muid = '+str(data['muid'])+', %s where id ='+str(data['gid'])
        try:
            sql = (sql %strs[:-1])
            self._cursor.execute(sql)
            self._conn.commit()
            return {'stat':True,'msg':u'商品更新成功！'}
        except:
            return {'stat':False,'msg':u'系统内部错误，请稍后操作！'}
         
    def delGoods(self,data):
        #判断该商品资料下是否有入库商品
        sql = 'select * from goodslist where pid = '+str(data['gid'])
        if self.getOne(sql):
            return {'stat':False,'msg':u'该商品资料己经存在商品，无法删除'}
        sql = 'delete from goods where id ='+str(data['gid'])
        try:
            self._cursor.execute(sql)
            self._conn.commit()
            return {'stat':True,'msg':u'商品删除成功！'}
        except:
            return {'stat':False,'msg':u'系统错误，请稍后重试'}