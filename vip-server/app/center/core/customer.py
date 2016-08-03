# --*-- coding:utf-8 --*--
'''
Created on 2015年1月31日

@author: LiuXinwu

客户资料
'''
import hashlib
import time,sys
from lib.db import Mysql


reload(sys)
sys.setdefaultencoding( "utf-8" )

class Customer(Mysql):
    def __init__(self):
        Mysql.__init__(self)
    
    #查询客户卡的状态(最新的卡)
    def findCustomerCardStat(self,data):
        id = int(data['customerId'])
        sql = 'SELECT stat,noid,password FROM card WHERE uid = %s ORDER BY bdate DESC'
        return self.getOne(sql,id)
        
        
        
    #查询客户状态
    def findCustomerStat(self,data):
        id = int(data['customerId'])
        sql = 'SELECT stat FROM customer WHERE id = %s'
        return self.getOne(sql,id)
        
    
    
    #更新客户状态
    def updateCustomerStat(self,data):
        id = int(data['customerId'])
        
        sql = 'UPDATE  customer SET stat = 1 WHERE id = %s'
        try:
            self.update(sql,(id,id))
            self.end()
            return True
        except:
            return False
        
    #查询客户信息
    def findOneCustomer(self,data):
        idcard = data['idcard']
        sql = "select * from `customer` where idcard = %s"
        re = self.getOne(sql,idcard)
        return re
    
    #查询客户额外信息
    def findOneCustomerAdditional(self,data):
        cid = int(data['cid'])
        sql = "select * from `customerinfo` where cid = %s"
        re = self.getOne(sql,cid)
        return re
    
    #查询客户绑定卡(最近绑定的某张卡)的信息
    def findCardWithUid(self,data):
        uid = int(data['uid'])
        sql = "SELECT * FROM `card` WHERE uid = %s ORDER BY bdate DESC "
        re = self.getOne(sql,uid)
        return re
        
    #查询此金融卡是否存在数据库中
    def findCardExists(self,data):
        cnoid = data['cnoid']
        sql = 'SELECT * FROM card WHERE cardid = %s OR noid = %s'
        re = self.getOne(sql,(cnoid,cnoid))
        return re
        
        
    #为客户绑定此卡
    def bindCardForCustomer(self,data):    
        #更新新卡的状态
        sql = 'UPDATE card SET uid = %s,bdate = %s,`password`= %s,stat=1 WHERE noid = %s OR cardid = %s'
        try:
            #更新客户的资金
            self.update(sql,(data['cid'],time.time(),data['pwd'],data['cnoid'],data['cnoid']))
            self.update('update customer set stat = 1 where id = %s'%int(data['cid']))
            sql = 'insert into statu_changes(id, cid, uid, type, noid, cdate) values(NULL, %s, %s, 0, %s, UNIX_TIMESTAMP())'
            temp = (data['cid'], data['uid'], data['cnoid'])
            self.insertOne(sql, temp)
            self.end()
            return True
        except:
            return False
        
        
    #为客户绑定此卡
    def guashiCardForCustomer(self,data):    
        cnoid = data['cnoid']
        customerId = data['customerId']
        #把卡的状态设为挂失，客户的状态设为冻结
        sql = 'UPDATE card SET stat=4 WHERE noid = %s OR cardid = %s'
        sql2 = 'UPDATE customer SET stat=2 WHERE id = %s'
        try:
            self.update(sql,(cnoid,cnoid))
            self.update(sql,customerId)
            self.end()
            return True
        except:
            return False
    
    #查询客户最近一次交易详情
    def findOneLog(self,data):
        uid = int(data['cid'])
        sql = 'SELECT * FROM `log` WHERE uid = %s ORDER BY cdate DESC'
        re = self.getOne(sql,uid)
        return re
        
        
    #查询挂失和注销用户信息
    def serviceQuery(self,name='',idcard=''):
        wheres = ''
        if name == '':
            wheres += ' 1=1 '
        else:
            wheres += ' `membername` like "%'+name+'%"'
            
        if idcard == '':
            wheres += ' and 1=1 '
        else:
            wheres += ' and idcard like "%'+str(idcard)+'%"'
            
        sql = "select * from customer where %s and (`stat` = 2 or `stat` = 3)"
        return self.getAll(sql % wheres)
        
        
