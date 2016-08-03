# --*-- coding:utf-8 --*--
'''
Created on 2014年10月15日

@author: huaan

'''
import hashlib,struct
import time,sys
from lib.db import Mysql

import json
reload(sys)
sys.setdefaultencoding( "utf-8" )

class Order(Mysql):
    def __init__(self):
        Mysql.__init__(self)
         
    
    def orderAdd(self, data):
        '''添加订单'''
        orderInfo = data['orderInfo']
        sql = 'insert into `order`(ordersn, cid, price, cdate, pdate, uid, pstat, ostat) values(%s,%s,%s,%s,UNIX_TIMESTAMP("'+orderInfo['exceptDate'] +'"),%s,%s,%s)'
#        orderInfo = data['orderInfo']
#        exceptTimeArray = time.strptime(orderInfo['exceptDate'], '%Y/%m/%d')
#        exceptTime = int(time.mktime(exceptTimeArray))
        
        temp = [orderInfo['orderSN'],
                orderInfo['supplierID'],
                orderInfo['total'],
                int(time.time()),
                orderInfo['purchaserID'],
                orderInfo['biddingType'],
                orderInfo['orderStatu'],
                ]
        re = self.insertOne(sql, temp)
        if not re:
            return {'stat':False, 'msg':u'添加订单失败！'}
#        self.end()
        sql = '''select id from `order` where ordersn = %s'''
        orderID = self.getOne(sql, str(orderInfo['orderSN']))
#        sql = 'select id from `order` where ordersn = ' + str(orderInfo['orderSN'])
#        orderID = self.getAll()
        sql = '''insert into order_info(orderid, goodsid, price, unit, counts) values(%s,%s,%s,%s,%s)'''
        
        for goods in data['goods']:
            temp = [orderID['id'], 
                    goods['goodsID'], 
                    goods['price'], 
                    goods['unit'], 
                    goods['count']
                    ]
            re = self.insertOne(sql, temp)
            if not re:
                return {'stat':False, 'msg':u'添加订单失败！'}
        self.end()
        return {'stat':True, 'msg':u'添加订单成功！'}
       
    def orderAlter(self, data):
        '''添加订单'''
        orderInfo = data['orderInfo']
        sql = 'update `order` set cid = %s, price = %s, cdate = UNIX_TIMESTAMP("'+orderInfo['startDate'] +'"), pdate = UNIX_TIMESTAMP("'+orderInfo['exceptDate'] +'"), uid = %s, pstat = %s, ostat = %s, cstat = %s, hstat = %s where id = ' + data['orderID']
#        return data['orderID']
#        startTimeArray = time.strptime(orderInfo['startDate'], '%Y/%m/%d')
#        startTime = int(time.mktime(startTimeArray))
#        exceptTimeArray = time.strptime(orderInfo['exceptDate'], '%Y/%m/%d')
#        exceptTime = int(time.mktime(exceptTimeArray))
        
        temp = [orderInfo['supplierID'],
                orderInfo['total'],
                orderInfo['purchaserID'],
                orderInfo['biddingType'],
                orderInfo['orderStatu'],
                orderInfo['supplierAgree'],
                orderInfo['paid']
                ]
        re = self.update(sql, temp)
#        if not re:
#            return {'stat':False, 'msg':u'修改订单失败,无法更新order表！'}
        
        sql = 'delete from order_info where orderid = ' + data['orderID']
        self.delete(sql)
        sql = '''insert into order_info(orderid, goodsid, price, unit, counts) values(%s,%s,%s,%s,%s)'''
        
        for goods in data['goods']:
            temp = [data['orderID'], 
                    goods['goodsID'], 
                    goods['price'], 
                    goods['unit'], 
                    goods['count']
                    ]
            re = self.insertOne(sql, temp)
#            if not re:
#                return {'stat':False, 'msg':u'修改订单失败，无法更新goodsInfo表！'}
        self.end()
        return {'stat':True, 'msg':u'修改订单成功！'}
        
    def getAllValidPurchasers(self):
        '''检索所有有效采购员'''
        sql = 'select id, username, nickname from user where status = 0'
        re = self.getAll(sql)
        return re

    def getAllValidSuppliers(self):
        '''ͨ检索所有有效供应商'''
        sql = 'select id, membername from customer where ugroup = 1 and stat = 1'
        re = self.getAll(sql)
        return re
    
    def getGoodsSN(self, goodsID):
        '''查询商品信息'''
#        sql = 'select g.pname, g.unit, gl.pid, gl.price, gl.counts from goodslist as gl, goods as g where gl.pid = ' + goodsID  
#        'and gl.pid = '
        sql = 'SELECT goodssn from goods where id = ' + goodsID
        re = self.getOne(sql)
        return re
    
    def getGoodsInfo(self, goodsName):
        '''查询商品信息'''
#        sql = 'select g.pname, g.unit, gl.pid, gl.price, gl.counts from goodslist as gl, goods as g where gl.pid = ' + goodsID  
#        'and gl.pid = '
        sql = 'SELECT a.id, a.pname,  FROM goods AS a INNER JOIN goodslist AS b ON a.id = b.pid WHERE a.id = ' + goodsName
        re = self.getOne(sql)
        return re
    
    #查询订单列表
    def getOrderList(self):
        sql = "select * from `order`"
        re = self.getAll(sql)
        return re
    
    #查询uid的名字
    def getUsername(self,id):
        sql = 'select nickname from user where id = ' + id
        re = self.getOne(sql)
        return re
    
    #删除订单
    def deleteOrder(self,id):
        sql = 'delete from `order` where id = '+ id 
        try:
            self._cursor.execute(sql)
            #顺便删除order_info表内容
            self.deleteOrderInfo(id)
            self._conn.commit()
            return {'stat':True,'msg':u'删除订单成功'}
        except:
            return {'stat':False,'msg':u'删除订单失败'}
        
    #删除订单info
    def deleteOrderInfo(self,id):
        sql = 'delete from order_info where orderid = '+ id
        self._cursor.execute(sql)
        self._conn.commit()
       
    #查询某个订单详情
    def queryOrderDetail(self,id):
        sql = 'select * from `order` a,order_info b where a.id = '+id+ ' AND '+ 'b.orderid = '+id
        #sql = 'select * from `order` a,order_info b,goods c where a.id ='+id+' AND '+'b.orderid ='+id+' AND c.id = (select goodsid from order_info where orderid ='+id+')'
        re = self.getAll(sql)
        return re

    
    #查询供应商名称
    def queryApplyName(self,id):
        sql = 'select membername from customer where id = '+ id
        re = self.getOne(sql)
        return re
        
    #查询商品表与订单info表的相关信息    
    def queryGoodsAndOrderinfo(self,id):
        sql = 'select * from goods a,order_info b where a.id = b.goodsid and b.orderid = '+ id
        re = self.getAll(sql)
        return re
        
    #查询订单详情及商品
    def getOrderInfo(self, orderID):
        sql = 'select * from `order` where id = ' + orderID
        info = self.getOne(sql)
        sql = 'select * from order_info where orderid = ' + orderID
        goods = self.getAll(sql)
        return goods
        return {'info':info, 'goods':goods}
      
      
    #查询订单表中某一订单的详情   
    def getOneOrder(self,id):
        sql = 'select * from `order` where id = '+id
        re = self.getOne(sql)
        return re
    
    #查询某一订单的所有商品总共价钱
    def querySumZongjia(self,id):
        sql = 'select sum(order_info.counts*order_info.price) as amount from order_info where orderid = '+id                  
        re = self.getOne(sql)
        return re
    
    
    #根据条件，筛选orderlist
    def filterOrderList(self,data):
        #从参数中取值
        uid = data['uid']
        ostat = data['ostat']
        pstat = data['pstat']
        #判断参数值是否合法,列举所有情况
        #0个参数为空
        if uid!='' and ostat!='' and pstat!='':
           sql = 'select * from `order` where uid='+uid+' and ostat='+ostat+' and pstat='+pstat
            
        #一个参数为空
        if uid=='' and ostat!='' and pstat!='':
           sql = 'select * from `order` where ostat='+ostat+' and pstat='+pstat
        if uid!='' and ostat=='' and pstat!='':
           sql = 'select * from `order` where uid='+uid+' and pstat='+pstat
        if uid!='' and ostat!='' and pstat=='':
           sql = 'select * from `order` where uid='+uid+' and ostat='+ostat

        #两个参数为空
        if uid=='' and ostat=='' and pstat!='':
           sql = 'select * from `order` where pstat='+pstat
        if uid=='' and ostat!='' and pstat=='':
           sql = 'select * from `order` where ostat='+ostat
        if uid!='' and ostat=='' and pstat=='':
           sql = 'select * from `order` where uid='+uid
        
        #三个参数为空
        if uid=='' and ostat=='' and pstat=='':
           sql = 'select * from `order`' 
        re = self.getAll(sql)
        return re
    
    
    #查询用户表里的所有用户真实姓名
    def queryNickname(self):
        sql = 'select id,nickname from user'
        re = self.getAll(sql)
        return re
    
    def getOrdersID(self,orderSN):
        sql = 'select ordersn from `order` where ordersn = "' + orderSN + '"'
        re = self.getAll(sql)
        return re
        