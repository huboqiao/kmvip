# --*-- coding:utf-8 --*--
'''
Created on 2015年2月1日

@author: kylin

报表操作类
'''
import hashlib,struct
import time,sys
from lib.db import Mysql

import json
reload(sys)
sys.setdefaultencoding( "utf-8" )

class Report(Mysql):
    
    def queryCompanyAll(self,data):
        ''' 公司资金报表'''
        
        start = data["start"]
        end = data["end"]
        uid = data["uid"]
        leftJoinWhere = ""
        selectWhere = ''
        timeWhere = " WHERE cdate <= UNIX_TIMESTAMP('%s 23:59:59') AND cdate >= UNIX_TIMESTAMP('%s 00:00:00') " % (end,start) 
        if int(uid)>0:
            leftJoinWhere = " AND uid = %s " % uid
            selectWhere = "WHERE a1.id = %s " % uid
        
        sql = """SELECT result.*,IFNULL(result.czall-result.txall,0)  AS jyall FROM (
                 SELECT a1.id,a1.nickname, IFNULL(a2.amount,0) AS txall ,IFNULL(a3.amount,0)  AS czall 
                FROM `user` AS a1
                LEFT JOIN 
                    (SELECT uid,SUM(amount) AS amount FROM cardtx  
                    %s %s
                    GROUP BY uid 
                    )AS a2 
                ON a1.id = a2.uid
                LEFT JOIN 
                    (SELECT uid,SUM(amount) AS amount FROM cardcz 
                    %s %s
                    GROUP BY uid
                    )AS a3 ON a1.id = a3.uid
                %s
                )
                AS result
            """
        re = self.getAll(sql % (timeWhere,leftJoinWhere,timeWhere,leftJoinWhere,selectWhere))
        return re
    
    def queryCompanyZiJinDetail(self,data):
        ''' 公司资金报表明细'''
        start = data["start"]
        end = data["end"]
        uid = int(data["uid"])
        type = int(data["type"])
        
        uidWhere = "WHERE a2.uid = %s " % uid 
        timeWhere = " AND a2.cdate >= UNIX_TIMESTAMP('%s') AND a2.cdate < UNIX_TIMESTAMP('%s') + 86400 "%(start, end) 
        typeWhere = ""
        order = "ORDER BY cdate desc"
        sqlCz = """
        SELECT IFNULL(a4.membername,"") as membername,a2.cardid,a2.ctype+1 AS `type`,a2.amount,a1.nickname,a2.cdate FROM `user` AS a1 
        LEFT JOIN cardcz AS a2 ON a1.id = a2.uid 
        LEFT JOIN card AS a3 ON a2.cardid = a3.noid
        LEFT JOIN customer AS a4 ON a3.uid = a4.id
         %s
         %s
         %s
        """
        sqlTx = """
        SELECT IFNULL(a4.membername,"") as membername,a2.cardid,a2.ctype+3 AS `type`,a2.amount,a1.nickname,a2.cdate FROM `user` AS a1 
        LEFT JOIN cardtx AS a2 ON a1.id = a2.uid 
        LEFT JOIN card AS a3 ON a2.cardid = a3.noid
        LEFT JOIN customer AS a4 ON a3.uid = a4.id
         %s        
         %s
         %s
        """
        if type == 0:
            sqlCz = sqlCz % (uidWhere,timeWhere,typeWhere) 
            sqlTx = sqlTx % (uidWhere,timeWhere,typeWhere) 
            sql = sqlCz+" UNION ALL  "+sqlTx
        if type == 1:
            typeWhere = " AND a2.ctype = 0 "
            sql = sqlCz % (uidWhere,timeWhere,typeWhere) 
        if type == 2:
            typeWhere = " AND a2.ctype = 1 "
            sql = sqlCz % (uidWhere,timeWhere,typeWhere)  
        if type == 3:
            typeWhere = " AND a2.ctype = 0 "
            sql = sqlTx % (uidWhere,timeWhere,typeWhere)  
        if type == 4:
            typeWhere = " AND a2.ctype = 1 "
            sql = sqlTx % (uidWhere,timeWhere,typeWhere)    
        sql += order
        
        re = self.getAll(sql)
        return re

    
    def fourSql(self,date):
        CzSql = ' SELECT cz.cardid,SUM(cz.amount) AS `in`, 0 AS `out` \
                FROM cardcz AS cz \
                ' + date + '\
                GROUP BY cz.cardid '
                
        TxSql = ' SELECT tx.cardid,0 AS `in`, SUM(tx.amount) AS `out` \
                FROM cardtx AS tx \
                ' + date + '\
                GROUP BY tx.cardid '
                
        InSql = ' SELECT a3.incomecard AS cardid,SUM(a3.amount) AS `in`,0 AS `out` \
                FROM cardzz AS a3 \
                ' + date + '\
                GROUP BY a3.incomecard '
                
        OutSql = ' SELECT a4.paycard AS cardid, 0 AS `in`,SUM(a4.amount) AS `out` \
                FROM cardzz AS a4 \
                ' + date + '\
                GROUP BY a4.paycard '
        return (CzSql,TxSql,InSql,OutSql)
    
    def queryCustomerAccount(self,data):
        ''' 客户资金报表'''
        '''查询所有会员卡账务变更信息'''
        wheres = ''
        if data['noid'] != '':
            wheres += ' and a.noid like "%' + data['noid'] + '%" '
        if data['name'] != '':
            wheres += ' and b.membername like "%' + data['name'] + '%" '

        date = " where cdate < UNIX_TIMESTAMP('" + data['start'] +"')"
        
        fourSql = self.fourSql(date)   
        CzSql = fourSql[0]
        TxSql = fourSql[1]
        InSql = fourSql[2]
        OutSql = fourSql[3]
                
        
        TableC = CzSql+" UNION ALL "+TxSql+" UNION ALL "+InSql+" UNION ALL "+OutSql

            
        sql = 'SELECT b.id, a.cardid, a.noid, IFNULL((SUM(c.in)-SUM(c.out)),0) AS `amount` \
                FROM customer AS b \
                LEFT JOIN card AS a \
                ON  a.uid = b.id \
                LEFT JOIN ( '+TableC+' ) AS c \
                ON a.noid = c.cardid \
                WHERE a.uid IS NOT NULL \
                 ' + wheres + '\
                GROUP BY b.id'
                #GROUP BY a.cardid'
        #期初
        re1 = self.getAll(sql)
        
        date = " where cdate < UNIX_TIMESTAMP('" + data['end'] +"')"
        
        fourSql = self.fourSql(date)   
        CzSql = fourSql[0]
        TxSql = fourSql[1]
        InSql = fourSql[2]
        OutSql = fourSql[3]
                
                
        TableC = CzSql+" UNION ALL "+TxSql+" UNION ALL "+InSql+" UNION ALL "+OutSql
        #期末
        sql = 'SELECT b.id, a.cardid, a.noid, IFNULL((SUM(c.in)-SUM(c.out)),0) AS `amount` \
                FROM customer AS b \
                LEFT JOIN card AS a \
                ON  a.uid = b.id \
                LEFT JOIN ( '+TableC+' ) AS c \
                ON a.noid = c.cardid \
                WHERE a.uid IS NOT NULL \
                 ' + wheres + '\
                GROUP BY b.id'
                #GROUP BY a.cardid'     
        re2 = self.getAll(sql)  
        
        
        having = ""
        date = " where cdate >= UNIX_TIMESTAMP('" + data['start'] +"')"
        if data['start'] != data['end']:
            date += " and cdate < UNIX_TIMESTAMP('" + data['end'] +"')"
            
    
        
                
        fourSql = self.fourSql(date)   
        CzSql = fourSql[0]
        TxSql = fourSql[1]
        InSql = fourSql[2]
        OutSql = fourSql[3]        
                
                
        ctype = data["ctype"]
        if ctype == "0" :
            TableC = CzSql+" UNION ALL "+TxSql+" UNION ALL "+InSql+" UNION ALL "+OutSql
        elif ctype == "1" :
            TableC = CzSql
        elif ctype == "2" :
            TableC = TxSql
        elif ctype == "3" :
            TableC = InSql
        elif ctype == "4" :
            TableC = OutSql
            
        
#             having = """
#              having UNIX_TIMESTAMP('%s') < UNIX_TIMESTAMP('%s') 
#             """ % (data['start'],data['end'])
        sql = 'SELECT b.id, a.cardid,a.noid,IFNULL(b.membername,"") AS `name`, IFNULL(SUM(c.in),0) AS `in`,IFNULL(SUM(c.out),0) AS `out` \
                FROM customer AS b \
                LEFT JOIN card AS a \
                ON  a.uid = b.id \
                LEFT JOIN ( '+TableC+' ) AS c \
                ON a.noid = c.cardid \
                WHERE a.uid IS NOT NULL \
                 ' + wheres + '\
                GROUP BY b.id'
                #GROUP BY a.cardid'
                #GROUP BY a.cardid '+ having
                
        re = self.getAll(sql)
        if re:
            for i in range(0, len(re)):
                re[i]['in'] = float(re[i]['in'])
                re[i]['out'] = float(re[i]['out'])
                re[i]['startAmount'] = str(float(re1[i]['amount']))
                re[i]['endAmount'] = str(float(re2[i]['amount']))
#                 re[i]['endAmount'] = str(float(re[i]["in"])+float(re1[i]['amount'])-float(re[i]["out"]))
                
            return {'stat':True,'data':re}
        else:
            return {'stat':False,'msg':u'没有给定时期的客户用卡记录！'}
        
    def queryCustomerAccountDetail(self,data):
        start = data["start"]
        end = data["end"]
        beizhu = data["beizhu"]
        ctype = data["ctype"]
        uid = data["uid"]
        noid = data["noid"]
#        
        if int(noid) == 0 :
            noidwhere = ""
        else:
            noidwhere = " AND noid = %s " % (noid)
        # 查询该客户所有用卡记录
        sql = """select noid from card as a  where a.uid = %s %s""" % (uid,noidwhere)
        re = self.getAll(sql)
            
        if True:
            noidlist = [i['noid'] for i in re]
            cardidwhere = ",".join(noidlist)
        else:
            return {"stat":False,"msg":u"该用户无绑定卡"}
        try:
            smoney = float(data["smoney"])
        except:
            smoney = ""
            
        try:
            bmoney = float(data["bmoney"])
        except:
            bmoney = ""
        timeWhere = " WHERE a3.cdate >= UNIX_TIMESTAMP('" + start + "') AND a3.cdate <= UNIX_TIMESTAMP('" + end +"') "
        beizhuWhere = ""
        moneyWhere = ""
        if beizhu !="":
            beizhuWhere = " AND a3.txt like '%%%s%%' " % beizhu
        cardWhere = "AND cardid in (%s)   " % cardidwhere
        if smoney != "":
            moneyWhere +=" AND a3.amount >= %s " % smoney
        if bmoney !="":
            moneyWhere +=" AND a3.amount <= %s " % bmoney
        
        sqlYe = '\
                    select IFNULL((SUM(y.in)-SUM(y.out)),0) AS `ye` FROM ( \
                        SELECT IFNULL(cz.cdate,0) as cdate,SUM(cz.amount) AS `in`, 0 AS `out` \
                        FROM cardcz AS cz \
                        WHERE cz.cardid = %s \
                        AND cz.cdate <= %s  \
                        UNION ALL  \
                        SELECT IFNULL(tx.cdate,0) as cdate,0 AS `in`, SUM(tx.amount) AS `out` \
                        FROM cardtx AS tx \
                        WHERE tx.cardid = %s \
                        AND tx.cdate <= %s  \
                        UNION ALL  \
                        SELECT IFNULL(a3.cdate,0) as cdate,SUM(a3.amount) AS `in`,0 AS `out` \
                        FROM cardzz AS a3 \
                        WHERE a3.incomecard = %s \
                        AND a3.cdate <= %s  \
                        UNION ALL  \
                        SELECT IFNULL(a4.cdate,0) as cdate,0 AS `in`,SUM(a4.amount) AS `out` \
                        FROM cardzz AS a4 \
                        WHERE a4.paycard = %s \
                        AND a4.cdate <= %s  \
                        ) AS `y` '

        selectCz = """
        SELECT a3.bankname, a3.bankusername, a3.bankno, a3.bankcard, a3.balance, u.nickname, a3.cardid, a3.ctype,u.username, amount AS `in`,0 AS `out`,a3.cdate,IFNULL(txt,"") AS txt,"" AS othercard,"" AS othername
             FROM cardcz AS a3
             LEFT JOIN `user` AS u ON u.id = a3.uid 
                   %s   
                   AND cardid in( %s )
                   %s
                   %s
        """ % (timeWhere,cardidwhere,beizhuWhere,moneyWhere)
        
        selectTx = """
        SELECT a3.bankname, a3.bankusername, a3.bankno, a3.bankcard, a3.balance, u.nickname,a3.cardid, a3.ctype+2 AS ctype, u.username, 0 AS `in`, amount AS `out`,a3.cdate,IFNULL(txt,"") AS txt,"" AS othercard,"" AS othername
             FROM cardtx AS a3   
             LEFT JOIN `user` AS u ON u.id = a3.uid 
                    %s
                   AND cardid in( %s )
                    %s
                    %s
        
        """ % (timeWhere,cardidwhere,beizhuWhere,moneyWhere)
        selectZO = """
         SELECT '' AS bankname, '' AS bankusername, '' AS bankno, '' AS bankcard, a3.payeebalance AS balance, u.nickname,  a3.paycard AS cardid,a3.ctype+4 AS ctype,u.username,a3.amount AS `in`,0 AS `out`,a3.cdate,IFNULL(txt,"") AS txt,card.noid AS othercard ,IFNULL(d.membername,"") AS othername
             FROM cardzz AS a3    
             LEFT JOIN `user` AS u ON u.id = a3.uid  
               LEFT JOIN card ON card.noid = a3.incomecard 
           LEFT JOIN customer AS d ON d.id = card.uid        
                  %s
                   AND a3.paycard in( %s )
                   %s
                   %s
        """ % (timeWhere,cardidwhere,beizhuWhere,moneyWhere)
        selectZI = """
         SELECT '' AS bankname, '' AS bankusername, '' AS bankno, '' AS bankcard, a3.paybalance AS balance, u.nickname, a3.incomecard AS cardid,a3.ctype+4 AS ctype,u.username, 0 AS `in`,a3.amount AS `out`,a3.cdate,IFNULL(txt,"") AS txt,card.noid AS othercard,IFNULL(d.membername,"") AS othername
             FROM cardzz AS a3 
             LEFT JOIN `user` AS u ON u.id = a3.uid 
               LEFT JOIN card ON card.noid = a3.paycard 
           LEFT JOIN customer AS d ON d.id = card.uid
                   %s
                   AND a3.incomecard in( %s )
                   %s
                   %s
        """ % (timeWhere,cardidwhere,beizhuWhere,moneyWhere)
#   
        if int(ctype) == 0:
          sql = """
                SELECT c.* FROM (
                    %s UNION ALL  %s UNION ALL  %s UNION ALL  %s
                           ) AS  c order by c.cdate desc   
                """ % (selectCz,selectTx,selectZI,selectZO)
        if int(ctype) == 1:
          sql = """
                SELECT c.* FROM (
                    %s 
                           ) AS c order by c.cdate desc 
                """ % selectCz
        if int(ctype) == 2: 
            sql = """
                SELECT c.* FROM (
                    %s 
                           ) AS c order by c.cdate desc 
                """ % selectTx
        
        if int(ctype) == 3: 
            sql = """
                SELECT c.* FROM (
                    %s 
                           ) AS c order by c.cdate desc 
                """ % selectZI
    
        if int(ctype) == 4: 
            sql = """
                SELECT c.* FROM (
                    %s 
                           ) AS c order by c.cdate desc 
                """ % selectZO
        re =  self.getAll(sql)
        if re:
#             for key,value in enumerate(re):
#                 yy =  self.getOne(sqlYe % (value["cardid"],value["cdate"],value["cardid"],value["cdate"],value["cardid"],value["cdate"],value["cardid"],value["cdate"]))
#                 re[key]["ye"] = yy["ye"]
            return {'stat':True,'data':re}
        else:
            return {'stat':False,'msg':u'没有给定时期的客户用卡记录！'}
    
    def queryKehuJibenziliao(self,data):
        uid = data["uid"]
        sql = """
        select a.noid,b.amount,IFNULL(b.membername,"") as membername,tel,a.stat as cardStat,
            bankname,bankcard,idcard from customer as b
            left join card as a on a.uid = b.id
            left join customerinfo as c on b.id = c.cid
            where b.id = %s order by a.stat
        """ % uid
        re =  self.getAll(sql)
        if re:
                    return {'stat':True,'data':re}
        else:
            return {'stat':False,'msg':u'没有给定时期的客户用卡记录！'}
        return re
    
    def queryGoodsScaleAccountDetail(self,data):
         
        goodsname = data["goodsname"]
        supplier = data["supplier"]
        customer = data["customer"]
        goodstype = data["goodstype"]
        start = data["start"]
        end = data["end"]
        where = []
        if goodsname !="":
            where.append ( " g.goods_name='"+goodsname+"' ") 
        if supplier !="":
            where.append ( " s.suppliers_name like '%"+supplier+"%' ") 
        if customer !="":
            where.append ( " ct.membername like '%"+customer+"%' ")
        if  goodstype !="":
            where.append ( " cy.cat_name like '%"+goodstype+"%' ")
        where.append(" o.add_time >= UNIX_TIMESTAMP('" + start +"')")
        where.append(" o.add_time <= UNIX_TIMESTAMP('" + end+"')")
        where.append(" o.pay_status = 1 ")
        if (len(where) >0):
            where = " where "+" and ".join(where)
        else :
            where = ""
        sql = "select g.goods_name,s.suppliers_name,o.order_sn,o.pay_time,og.goods_price,IFNULL(og.goods_number,0) AS goods_number,IFNULL((og.goods_number * og.goods_price) ,0.00) as amount,IFNULL(ct.membername,'') as membername,cy.cat_name \
                from `ecs_order_goods` as og \
                left join `ecs_goods` as g on g.goods_id = og.goods_id \
                left join `ecs_supplier` as s on s.suppliers_id = g.suppliers_id \
                left join `ecs_category` as cy on cy.cat_id = g.cat_id \
                left join `ecs_order_info` as o on o.id = og.order_id \
                left join `card` as c on c.noid = o.noid \
                left join `customer` as ct on ct.id = c.uid "+where
                
        re =  self.getAll(sql)
        if re:
                    return {'stat':True,'data':re}
        else:
            return {'stat':False,'msg':u'没有给定时期的销售明细！'}
        return re
            
        
    
    def queryGoodsScaleAccount(self,data):
        
        goodsname = data["goodsname"]
        supplier = data["supplier"]
        customer = data["customer"]
        goodstype = data["goodstype"]
        start = data["start"]
        end = data["end"]
        where = []
        if goodsname !="":
            where.append ( " g.goods_name='"+goodsname+"' ") 
        if supplier !="":
            where.append ( " s.suppliers_name like '%"+supplier+"%' ") 
        if customer !="":
            where.append ( " ct.membername like '%"+customer+"%' ")
        if  goodstype !="":
            where.append ( " cy.cat_name like '%"+goodstype+"%' ")
        where.append(" o.add_time >= UNIX_TIMESTAMP('" + start +"')")
        where.append(" o.add_time <= UNIX_TIMESTAMP('" + end+"')")
        where.append(" o.pay_status = 1 ")
        if (len(where) >0):
            where = " where "+" and ".join(where)
        else :
            where = ""
        sql = "select g.goods_name,s.suppliers_name,IFNULL(og.goods_number,0) AS goods_number,IFNULL((og.goods_number * og.goods_price) ,0.00) as amount,IFNULL(ct.membername,'') as membername,cy.cat_name \
                from `ecs_goods` as g \
                left join `ecs_supplier` as s on s.suppliers_id = g.suppliers_id \
                left join `ecs_category` as cy on cy.cat_id = g.cat_id \
                left join `ecs_order_goods` as og on g.goods_id = og.goods_id \
                left join `ecs_order_info` as o on o.id = og.order_id \
                left join `card` as c on c.noid = o.noid \
                left join `customer` as ct on ct.id = c.uid "+where
                
        re =  self.getAll(sql)
        if re:
                    return {'stat':True,'data':re}
        else:
            return {'stat':False,'msg':u'没有给定时期的销售记录！'}
        return re
            
              
    def queryZhuanZhangAccount(self,data):
        
        start = str(data["start"])
        end = str(data["end"])
        where = " where zz.cdate >= UNIX_TIMESTAMP('" + start +"') and zz.cdate < (UNIX_TIMESTAMP('" + end + "') + 86400) "
        if data['noid'].strip() != '':
            where += " and c.noid like '%" + data['noid'] + "%' "
        if data['name'].strip() != '':
            where += " and ct.membername like '%" + data['name'] + "%' "
        where += " order by cdate desc"
            
        if data['type'] == 0:
            sql = " select ct.membername as payname,c.noid as paycard,c.uid,\
                    ctt.membername as incomename,cc.noid as incomecard,\
                    zz.amount,zz.cdate,zz.ctype,paybalance,payeebalance,\
                    IFNULL(zz.txt,'') AS txt \
                    from cardzz as zz \
                    left join `card` as c on zz.paycard = c.noid \
                    left join `customer` as ct on c.uid = ct.id \
                    left join `card` as cc on zz.incomecard = cc.noid \
                    left join `customer` as ctt on cc.uid = ctt.id \
                    "+where
        elif data['type'] == 1:
            sql = 'select ct.membername, c.noid, zz.amount, zz.cdate, zz.ctype, zz.balance, c.uid,\
                   IFNULL(zz.txt,"") as txt \
                   from cardcz as zz \
                   left join `card` as c on zz.cardid = c.noid \
                   left join `customer` as ct on c.uid = ct.id ' + where
        else:
            sql = 'select ct.membername, c.noid, zz.amount, zz.cdate, (zz.ctype + 2) as ctype, zz.balance, c.uid,\
                   IFNULL(zz.txt,"") as txt \
                   from cardtx as zz \
                   left join `card` as c on zz.cardid = c.noid \
                   left join `customer` as ct on c.uid = ct.id ' + where
        re = self.getAll(sql)
        if re:
            return {'stat':True,'data':re}
        else:
            return {'stat':False,'msg':'没有给定时期的转账记录！'}
        return re
        
        