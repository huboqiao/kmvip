# --*-- coding:utf-8 --*--
'''
Created on 2015年1月28日

@author: LiuXinwu

仓库
'''
import hashlib
import time,sys
from lib.db import Mysql


reload(sys)
sys.setdefaultencoding( "utf-8" )

class Storage(Mysql):
    def __init__(self):
        Mysql.__init__(self)
    
    #添加号数
    def insertHaoShu(self,data):
        qid = int(data['qid'])
        name = data['name']
        stat = int(data['stat'])
        cdate = time.time()
        sql = 'INSERT INTO storage_hs VALUES(NULL,%s,%s,%s,%s)'
        try:
            self.insertOne(sql,(qid,name,stat,cdate))
            self.end()
            return True
        except:
            return False
            
            
    #删除号数
    def deleteHaoShu(self,data):
        if self.getAll('select id from customer where storagenumber = %s', (data['id'])):
            return {'stat':False, 'msg':u'存在使用该号仓库的客户，不能删除'}
        id = int(data['id'])
        sql = 'DELETE FROM storage_hs WHERE id = %s'
        try:
            self.delete(sql,id)
            self.end()
            return {'stat':False, 'msg':u'删除成功'}
        except:
            return {'stat':False, 'msg':u'删除随便，请稍后再试'}
        
    #查询某区域的所有号数
    def findAllHaoShu(self,data):
        qid = int(data['qid'])
        sql = 'SELECT * FROM storage_hs WHERE qid = %s'
        re = self.getAll(sql,qid)
        return re
        

    #修改区域
    def updateQuYu(self,data):
        id = int(data['id'])
        name = data['name']
        isactive = int(data['isactive'])
        cdate = time.time()
        sql = 'UPDATE storage_qy SET `name`=%s,isactive=%s,cdate=%s where id = %s'
        try:
            self.update(sql,(name,isactive,cdate,id))
            self.end()
            return True
        except:
            return False
        
    
    #删除区域
    def deleteQuYu(self,data):
        id = int(data['id'])
        hs = self.getAll('select id from storage_hs where qid = %s', (data['id']))
        if hs:
            for h in hs:
                if self.getAll('select id from customer where storagenumber = %s', (h['id'])):
                    return {'stat': False, 'msg':u'删除仓库区域失败，存在使用该仓库区域的客户'}
        sql = 'DELETE FROM storage_qy WHERE id = %s'
        sql2 = 'DELETE FROM storage_hs WHERE qid = %s'
        try:
            #先删除本区域的所有号数
            self.delete(sql2,id)
            #再删除本区域信息
            self.delete(sql,id)
            self.end()
            return True
        except:
            return False
        
    #添加区域
    def insertQuYu(self,data):    
        sid = int(data['sid'])
        name = data['name']
        isactive = int(data['isactive'])
        cdate = time.time()
        
        sql = 'INSERT INTO storage_qy VALUES(NULL,%s,%s,%s,%s)'
        try:
            self.insertOne(sql,(sid,name,isactive,cdate))
            self.end()
            return True
        except:
            return False
    
    #查询某仓库的所有区域信息
    def findAllQuYu(self,data):
        sid = int(data['sid'])
        sql = 'SELECT * FROM storage_qy WHERE sid = %s'
        re = self.getAll(sql,sid)
        return re
        
    #根据区域id,查询区域的名称
    def findQuYuName(self,data):
        id = int(data['id'])
        sql = 'SELECT `name` FROM storage_qy WHERE id = %s'
        re = self.getOne(sql,id)
        return re
    
    #查询某区域的号数
    def findOneQuYuHaoShu(self,data):
        qid = int(data['qid'])
        sql = 'SELECT * FROM storage_hs WHERE qid = %s'
        re = self.getAll(sql,qid)
        return re
    
    
    #修改仓库类型
    def updateStorageType(self,data):
        name = data['name']
        stat = data['stat']
        cdate = time.time()
        id = int(data['id'])
        sql = 'UPDATE storagetype SET `name` = %s,stat = %s,cdate = %s WHERE id = %s'
        try:
            self.update(sql,(name,stat,cdate,id))
            self.end()
            return True
        except:
            return False
        
        
    #查询某仓库类型数据
    def findOneStorageType(self,data):
        id = int(data['id'])
        sql = 'SELECT * FROM storagetype WHERE id = %s'
        re = self.getOne(sql,id)
        return re
    
    #查询所有仓库类型名称
    def findTypeNames(self):
        sql = 'select `name` from storagetype'
        re = self.getAll(sql)
        return re
    
    #删除仓库类型
    def deleteStorageType(self,data):
        id = int(data['id'])
        
        if self.getAll('select id from customer where typeid = %s', (data['id'])):
            return {'stat':False, 'msg':u'有客户在使用该仓库区域，不能删除！'}
        sql = 'DELETE FROM storagetype WHERE id = %s'
        try:
            self.delete(sql,id)
            self.end()
            return {'stat':True, 'msg':u'删除成功！'}
        except:
            return {'stat':False, 'msg':u'删除失败，请稍后再试！'}
    
    #添加仓库类型
    def insertStorageType(self,data):    
        name = data['name']
        cdate = int(time.time())
        sql = 'INSERT INTO storagetype VALUES(NULL,%s,%s,%s)'
        try:
            self.insertOne(sql,(name,data['stat'],cdate))
            self.end()
            return True
        except:
            return False
    
    #查询所有仓库类型信息
    def findAllStorageType(self):
        sql = "select * from `storagetype`"
        re = self.getAll(sql)
        return re
    
    #查询所有仓库信息
    def findAllStorage(self):
        sql = "select * from `storage`"
        re = self.getAll(sql)
        return re
    
    #删除仓库
    def deleteStorage(self,data):
        id = int(data['id'])
        try:
            #查询此仓库下的所有区域id
            sql2 = 'SELECT id FROM storage_qy WHERE sid = %s'
            quyuIdsData = self.getAll(sql2,id)
            for i in quyuIdsData:
                hs = self.getAll('select id from storage_hs where qid = %s', (i['id']))
                if hs:
                    for h in hs:
                        if self.getAll('select id from customer where storagenumber = %s',(h['id'])):
                            return {'stat':False, 'msg':u'存在使用该仓库的客户，不能删除该仓库'}
                        #删除号数表
                        sql3 = 'DELETE FROM storage_hs WHERE qid = %s'
                        self.delete(sql3,i['id'])
            
                #删除区域表
                sql4 = 'DELETE FROM storage_qy WHERE sid = %s'
                self.delete(sql4,id)
            
            #删除仓库表中数据
            sql = "delete from `storage` where id = %s"
            re = self.delete(sql,id)
            self.end()
            
            return {'stat':True, 'msg':u'删除成功'}
        except:
            return {'stat':False, 'msg':u'删除失败，请稍后再试'}
        
    #查询所有仓库名称
    def findAllStorageName(self):
        sql = 'select `name` from `storagetype`'
        re = self.getAll(sql)
        return re
    
    #查询某仓库基本信息
    def findOneStorage(self,data):
        id = int(data['id'])
        sql = 'select * from `storage` where id = %s'
        re = self.getOne(sql,id)
        return re
    
    #查询某仓库区域信息
    def findOneStorageQuYu(self,data):
        id = int(data['id'])
        sql = 'select * from storage_qy where sid = %s'
        re = self.getAll(sql,id)
        return re
    
    #查询某仓库号数信息
    def findOneStorageHaoShu(self,data):
        id = int(data['id'])
        sql = 'select * from storage_hs where qid = %s'
        re = self.getAll(sql,id)
        return re
    
    #修改仓库
    def updateStorage(self,data):
        id = int(data['id'])
        name = data['name']
        stat = data['stat']
        cdate = time.time()

        sql = 'UPDATE `storage` SET `name`=%s,stat=%s,cdate=%s WHERE id = %s'
        try:
            self.update(sql,(name,stat,cdate,id))
            self.end()
            return True
        except:
            return False
       
    
    #添加仓库,区域,号数
    def insertStorage(self,data):
        name = data['name']
        stat = int(data['stat'])
        cdate = time.time()

        quyulist = data['quyulist']
        haoshulist = data['haoshulist']
        
        try:
            sql = "insert into `storage` values(null,%s,%s,%s)"
            #插入storagetype表
            self.insertOne(sql,(name,stat,cdate))
            self.end()
            #获得刚插入的仓库id
            sidData = self.getOne('SELECT @@identity')
            sid = int(sidData['@@identity'])
            #插入storage_qy表
            for i in quyulist:
                sql = 'INSERT INTO storage_qy(sid,`name`,cdate) VALUES(%s,%s,%s)'
                self.insertOne(sql,(sid,i,cdate))
                self.end()
                #获得刚插入的仓库区域id
                qidData = self.getOne('SELECT @@identity')
                qid = int(qidData['@@identity'])
                #遍历号数列表
                for j in haoshulist:
                    if j['quyu']==i:
                        #获得这个区域下所有号数
                        sql2 = 'INSERT INTO storage_hs(qid,`name`,cdate) VALUES(%s,%s,%s)'
                        self.insertOne(sql2,(qid,j['haoshu'],cdate))
                        self.end()
                    else:
                        pass
                    
            return True
        except:
            return False
        
        
        
        
        
        
        
        
        
        
