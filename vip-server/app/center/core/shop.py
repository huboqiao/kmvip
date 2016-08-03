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
import random 
reload(sys)
sys.setdefaultencoding( "utf-8" )

class Shop(Mysql):
    def __init__(self):
        Mysql.__init__(self)
         
    #获得所有商品类别
    def getAllShopClass(self):
        sql ="select * from ecs_category"
        try:
            return self.getAll(sql)
        except:
            return False
    
    #查询某类别下所有商品
    def queryShopClassGoods(self,data):   
        sql = 'select g.*,p.suppliers_name,c.cat_name from ecs_goods as g \
                left join ecs_category as c on c.cat_id = g.cat_id \
                left join ecs_supplier as p on g.suppliers_id = p.suppliers_id \
                where g.cat_id ='+str(data['cat_id'])
        try:
            return self.getAll(sql)     
        except:
            return False
        
    def addShopClass(self,data):
        strs = ''
        keys = ''
        for k,v in data.items():
            keys += '`'+k+'`,'
            strs += '"'+str(v)+'",'
        sql = "insert ecs_category(%s) values(%s)"
        sql = sql % (keys[:-1],strs[:-1])
        try:
            self._cursor.execute(sql)
            self._conn.commit()
            return True
        except:
            return False
        
    #修改商品类别
    def editShopClass(self,cat_id,data):
        strs = ''
        for k,v in data.items():
                strs += '`'+k+'`'+'= "'+str(v)+'",'
        sql = 'UPDATE `ecs_category` SET %s where cat_id ='+str(cat_id)
        sql = (sql%strs[:-1])
        
        try:
            self._cursor.execute(sql)
            self._conn.commit()
            return True
        except:
            return False
    def queryShopClassGoods(self,data):
        
        sql = 'select g.*,p.suppliers_name,c.cat_name from ecs_goods as g \
                left join ecs_category as c on c.cat_id = g.cat_id \
                left join ecs_supplier as p on g.suppliers_id = p.suppliers_id \
                where g.cat_id ='+str(data['cat_id'])
        return self.getAll(sql)
    
    def getAllParty(self):
        sql = 'select p.suppliers_name,p.suppliers_id  from ecs_supplier as p '
        return self.getAll(sql)
            
    def delShopClass(self,data):
        '''删除分类
            1、判断分类下是否有商品，如果有的话不能删除
        '''
        classdata = self.queryShopClassGoods({'cat_id':data['cat_id']})
        if classdata:
            return {'stat':False,'msg':u'该分类下有商品资料，请先清除商品资料数据'}
        #判断是否有子分类
        if self.queryChildClass(data):
            return {'stat':False,'msg':u'该分类下有子分类，请先清除子分类'}
        sql = 'delete from ecs_category where cat_id ='+str(data['cat_id'])
        try:
            self._cursor.execute(sql)
            self._conn.commit()
            return {'stat':True,'msg':u'删除分类成功'}
        except:
            return {'stat':False,'msg':u'删除分类失败'}
        
    def queryChildClass(self,data):
        sql = 'select * from ecs_category where parent_id ='+data['cat_id']
        return self.getAll(sql)
    
    #为某类别添加商品
    def addShopGoods(self,data):
        strs = ''
        keys = '`add_time`,'
        for k,v in data.items():
            keys += '`'+k+'`,'
            strs += '"'+str(v)+'",'
        sql = "insert into ecs_goods(%s) values(UNIX_TIMESTAMP(),%s)"
        try:
            sql = sql % (keys[:-1],strs[:-1])
            self._cursor.execute(sql)
            self._conn.commit()
            return {'stat':True,'msg':u'添加商品成功，是否继续添加？'}
        except:
            return {'stat':False,'msg':u'系统内部错误，请稍后添加'}   
         
    #修改商品信息
    def editShopGoods(self,data):
        strs = 'last_update =UNIX_TIMESTAMP(),'
        for k,v in data['data'].items():
                strs += '`'+k+'`'+'= "'+str(v)+'",'
        sql = 'UPDATE `ecs_goods` SET %s where goods_id ='+str(data['goods_id'])
#         try:
        sql = (sql %strs[:-1])
        self._cursor.execute(sql)
        self._conn.commit()
        return {'stat':True,'msg':u'商品更新成功！'}
#         except:
#             return {'stat':False,'msg':u'系统内部错误，请稍后操作！'}
#          
    def delShopGoods(self,data):
        #判断该商品资料下是否有入库商品
        sql = 'select * from `shop_stock_in_info` where goods_id = '+str(data['gid'])
        if self.getOne(sql):
            return {'stat':False,'msg':u'该商品有入库记录，无法删除'}
        sql = 'delete from `ecs_goods` where goods_id ='+str(data['gid'])
        try:
            self._cursor.execute(sql)
            self._conn.commit()
            return {'stat':True,'msg':u'商品删除成功！'}
        except:
            return {'stat':False,'msg':u'系统错误，请稍后重试'}
        
    def getShopGoodsData(self, goodsID):
        '''查询商品信息'''
#        sql = 'select g.pname, g.unit, gl.pid, gl.price, gl.counts from goodslist as gl, goods as g where gl.pid = ' + goodsID  
#        'and gl.pid = '
        sql = 'SELECT g.*,ifnull(p.suppliers_name,"") as suppliers_name from ecs_goods as g \
            left join ecs_supplier as p on g.suppliers_id = p.suppliers_id \
        where goods_id = ' + goodsID
        re = self.getOne(sql)
        return re
    
    def shoporderAdd(self,data):
        if False:
            return {"stat":False,"msg":u"testing"}
#         try:
        cid = data["info"]["cid"]
        stock_on = str(int(time.time()))+str(random.randint(100,999))
        sql = "insert into shop_stock_in(cdate,cid,stock_on) values(%s,%s,%s) " % ('UNIX_TIMESTAMP()',str(cid),stock_on)
        orderId  = self.insertOne(sql,())
        countList = []
        for i in data["goods"]:
            sql = "update ecs_goods set goods_number = goods_number+%s \
                    where goods_id = %s\
            " % (str(i["count"]),str(i["goods_id"]))
            self._cursor.execute(sql)
            countList.append("(%s,%s,%s)" % (str(orderId),str(i["goods_id"]),str(i["count"])))
        sql = "insert into shop_stock_in_info(`sid`,`goods_id`,`goods_numbers`) values %s "
        countList = ",".join(countList) 
        sql = sql % countList 
        self._cursor.execute(sql)
        self._conn.commit()
        return {"stat":True,"msg":u"入库成功"}
#         except:
#             return {"stat":False,"msg":u"服务器错误"}
    def queryShopOrderAccount(self,data):
             
        order_sn = data["order_sn"]
        customer = data["customer"]
        order_status = data["order_status"]
        pay_status = data["pay_status"]
        start = data["start"]
        end = data["end"]
        where = []
        if  order_sn !="":
            where.append ( " o.order_sn like '%"+order_sn+"%' ") 
        if customer !="":
            where.append ( " ct.membername like '%"+customer+"%' ")
        where.append(" o.add_time >= UNIX_TIMESTAMP('" + start +"')")
        where.append(" o.add_time <= UNIX_TIMESTAMP('" + end+"')")
        if (int(pay_status)>0):
            where.append(" o.pay_status = " + str((int(pay_status)-1)))
        if (int(order_status)>0):
            where.append(" o.order_status = " + str((int(order_status)-1)))
        if (len(where) >0):
            where = " where "+" and ".join(where)
        else :
            where = ""
        sql = "select o.id,o.order_sn,o.add_time,o.pay_time,o.order_status,o.pay_status,ct.membername \
                from `ecs_order_info` as o \
                left join `card` as c on c.noid = o.noid \
                left join `customer` as ct on ct.id = c.uid "+where
                
                
        re =  self.getAll(sql)
        if re:
            for i,data in enumerate(re):
                if(data["pay_status"] == 1):
                    sql = "select sum(og.goods_number*og.goods_price) as amount \
                            from ecs_order_goods as og \
                            where og.order_id = "+str(data["id"])+" \
                            group by og.order_id "
                    dt = self.getOne(sql)
                    if dt:
                        re[i]["amount"] = dt["amount"]
                        re[i]["payamount"] = dt["amount"]
                    else:
                        
                        re[i]["amount"] = 0
                        re[i]["payamount"] = 0
                else:
                    sql = "select sum(og.goods_number*g.goods_price) as amount \
                            from ecs_order_goods as og \
                            left join ecs_goods as g on g.goods_id = og.goods_id \
                            where og.order_id = "+str(data["id"])+" \
                            group by og.order_id "
                    dt = self.getOne(sql)
                    if dt:
                        re[i]["amount"] = dt["amount"]
                        re[i]["payamount"] = 0
                    else:
                        
                        re[i]["amount"] = 0
                        re[i]["payamount"] = 0
            return {'stat':True,'data':re}
        else:
            return {'stat':False,'msg':'没有给定时期的订单记录！'}
        return re
        
    def queryShopOrderAccountDetail(self,data):
        order_id = data["order_id"]
        sql = "select o.*,ct.membername,ct.tel,ct.adder \
                from ecs_order_info as o \
                left join card as c on o.noid = c.noid \
                left join customer as ct on c.uid = ct.id \
                where o.id = "+str(order_id)
                
        re = self.getOne(sql)
        if re:
            if(re["pay_status"] == 1):
                sql = "select o.order_sn,g.goods_name,g.goods_sn,cy.cat_name,og.goods_price,\
                        og.goods_number,(og.goods_price*og.goods_number) as amount,\
                        (og.goods_price*og.goods_number) as payamount \
                         from ecs_order_goods as og \
                         left join ecs_goods as g on g.goods_id = og.goods_id \
                         left join ecs_category as cy on cy.cat_id = g.cat_id \
                         left join ecs_order_info as o on o.id = og.order_id \
                         where og.order_id = "+str(re["id"])
            else:
                 sql = "select o.order_sn,g.goods_name,g.goods_sn,cy.cat_name,g.goods_price,\
                        og.goods_number,(g.goods_price*og.goods_number) as amount,\
                        0 as payamount \
                         from ecs_order_goods as og \
                         left join ecs_goods as g on g.goods_id = og.goods_id \
                         left join ecs_category as cy on cy.cat_id = g.cat_id \
                         left join ecs_order_info as o on o.id = og.order_id \
                         where og.order_id = "+str(re["id"])
            
            
            re["goods"] = self.getAll(sql)
            return {'stat':True,'data':re}
        else:
            return {'stat':False,'msg':'没有给定时期的订单记录！'}
        return re
    
    def queryGoodsStockinList(self,data):
        editor = data["editor"]
        start = data["start"]
        end = data["end"]
        where = []
        if  editor !="":
            where.append ( " u.nickname like '%"+editor+"%' ") 
        where.append(" s.cdate >= UNIX_TIMESTAMP('" + start +"')")
        where.append(" s.cdate <= UNIX_TIMESTAMP('" + end+"')")
        if (len(where) >0):
            where = " where "+" and ".join(where)
        else :
            where = ""
        sql = "select s.id,s.stock_on,s.cdate,u.nickname as editor \
                from `shop_stock_in` as s \
                left join `user` as u on u.id = s.cid "+where+" order by s.cdate desc "
                
        re = self.getAll(sql)
        if re:
            return {'stat':True,'data':re}
        else:
            return {'stat':False,'msg':'没有给定时期的入库记录！'}
        return re
    
  
    def queryGoodsStockinInfo(self,data):
        sid = data["sid"]
        where = []
        where.append(" s.id ="+str(sid))
        if (len(where) >0):
            where = " where "+" and ".join(where)
        else :
            where = ""
        sql = "select g.goods_name,g.goods_sn,cy.cat_name,sp.suppliers_name,sg.goods_numbers,s.cdate,u.nickname as editor \
                from `shop_stock_in_info` as sg \
                left join `ecs_goods` as g on g.goods_id = sg.goods_id \
                left join `ecs_category` as cy on cy.cat_id = g.cat_id \
                left join `ecs_supplier` as sp on sp.suppliers_id = g.suppliers_id \
                left join `shop_stock_in` as s on s.id = sg.sid \
                left join `user` as u on u.id = s.cid "+where
                
        re = self.getAll(sql)
        if re:
            return {'stat':True,'data':re}
        else:
            return {'stat':False,'msg':'没有给定时期的入库记录！'}
        return re
  