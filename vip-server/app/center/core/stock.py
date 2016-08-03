# --*-- coding:utf-8 --*--
'''
Created on 2015年3月9日

@author: LiuXinwu

仓库
'''
import hashlib
import time,sys
from lib.db import Mysql


reload(sys)
sys.setdefaultencoding( "utf-8" )

class Stock(Mysql):
    def __init__(self):
        Mysql.__init__(self)
    
    
    def queryCustomer(self,where):
        if(where['membername']):
            where = " a1.membername like '%"+where['membername']+"%' "
        else:
            where = " 1 = 1"
        sql = "SELECT a1.id,a1.membername,a2.cardid \
                FROM customer AS a1 \
                LEFT JOIN card AS a2 ON a1.id = a2.uid \
                WHERE "+where
                
        return self.getAll(sql)
    
    def queryStockById(self,where):
        sql = "SELECT a2.goods_id,SUM(a2.goods_numbers) as goods_numbers,a3.pname ,a3.unit \
                FROM `order` AS a1 \
                INNER JOIN `stock_into` AS a4 on a1.id = a4.oid \
                INNER JOIN `stock` AS a2 on a4.id = a2.sid \
                INNER JOIN `goods` AS a3 on a2.goods_id = a3.id \
                WHERE a1.cid = "+where['uid']+" \
                GROUP BY goods_id "
        return self.getAll(sql)