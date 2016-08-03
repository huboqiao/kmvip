# --*-- coding:utf-8 --*--
'''
Created on 2015年3月20日

@author: LiuXinwu
操作 ecs_supplier表
'''
import hashlib,struct
import time,sys
from lib.db import Mysql

import json
reload(sys)
sys.setdefaultencoding( "utf-8" )

class Party(Mysql):
    def __init__(self):
        Mysql.__init__(self)
          
    
    #查询供应商是否有提供货物
    def querySupGoods(self,data):
        suppliers_id = int(data['suppliers_id'])
        sql = 'SELECT goods_id FROM ecs_goods WHERE suppliers_id = %s'
        re = self.getAll(sql,suppliers_id)
        return re
    
    #添加
    def addParty(self,data):
        #获得参数
        name = data['name']
        tel = data['tel']
        phone = data['phone']
        email = data['email']
        address = data['address']
        man = data['man']
        desc = data['desc']
        ty = data['ty']
        ctdate = int(time.time())
        sql = 'INSERT INTO ecs_supplier(suppliers_name,tel,mobile,email,address,linkman,ctdate,is_check,suppliers_desc) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        try:
            self.insertOne(sql,(name,tel,phone,email,address,man,ctdate,ty,desc))
            self.end()
            return True
        except:
            return False
        
        
    #修改
    def updateParty(self,datas):
        #获得参数
        id = int(datas['id'])
        data = datas['data']
        name = str(data['name'])
        tel = str(data['tel'])
        phone = str(data['phone'])
        email = str(data['email'])
        address = str(data['address'])
        man = str(data['man'])
        desc = str(data['desc'])
        ty = str(data['ty'])
        mddate = int(time.time())
        sql = 'UPDATE ecs_supplier SET suppliers_name=%s,tel=%s,mobile=%s,email=%s,address=%s,linkman=%s,mddate=%s,is_check=%s,suppliers_desc=%s WHERE suppliers_id = %s'
        try:
            self.update(sql,(name,tel,phone,email,address,man,mddate,ty,desc,id))
            self.end()
            return True
        except:
            return False
        
        
        
        
        
        
        
        