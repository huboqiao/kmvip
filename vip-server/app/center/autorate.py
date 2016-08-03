# -*- coding: utf8 -*-
# Author:       kylin
# Created:      20141/10/14
#说明：每日利息统计线程
#
import threading  
import time  
from lib.db import Mysql
from app.center.core.rate import Rate
import datetime 

class Timer(threading.Thread, Mysql): 
    def __init__(self):  
        Mysql.__init__(self)
        threading.Thread.__init__(self)  
        self.thread_stop = False
        
    def run(self):
        
        # 按客户id和日期查询余额
        sql = '''
            SELECT balance FROM (
            SELECT cz.balance, cz.cdate FROM cardcz AS cz
            LEFT JOIN card AS ca ON ca.noid = cz.cardid
            LEFT JOIN customer AS cu ON cu.id = ca.uid
            WHERE cz.cdate < %s AND cu.stat != 3 AND cu.id = %s
            
            UNION ALL 
            SELECT zz.payeebalance AS balance, zz.cdate FROM cardzz AS zz
            LEFT JOIN card AS ca ON ca.noid = zz.incomecard
            LEFT JOIN customer AS cu ON cu.id = ca.uid
            WHERE zz.cdate < %s AND cu.stat != 3 AND cu.id = %s
            
            UNION ALL 
            SELECT tx.balance, tx.cdate FROM cardtx AS tx
            LEFT JOIN card AS ca ON ca.noid = tx.cardid
            LEFT JOIN customer AS cu ON cu.id = ca.uid
            WHERE tx.cdate < %s AND cu.stat != 3 AND cu.id = %s
            
            UNION ALL 
            SELECT zz.paybalance AS balance, zz.cdate FROM cardzz AS zz
            LEFT JOIN card AS ca ON ca.noid = zz.paycard
            LEFT JOIN customer AS cu ON cu.id = ca.uid
            WHERE zz.cdate < %s AND cu.stat != 3 AND cu.id = %s
            ) AS re ORDER BY cdate DESC LIMIT 1
            '''
        # 插入每日利息表interests
        insertSql = '''
                    INSERT INTO interests(id, cid, `date`, amount, rate, payed) 
                    VALUES(NULL, %s, %s, %s, 0, 0)'''
        while not self.thread_stop:
            # 查询利率
            rate = self.getAll('select rates, latest_date from rates')
            if not rate:
                time.sleep(86400)
                continue
            # 要计算利息的日期
            theDay = datetime.date.fromtimestamp(rate[0]['latest_date'])
            # 今天
            today = datetime.date.today()
            # 查询所有客户id和创建时间
            members = self.getAll('select id, cdate from customer where id != 133')
            if not members:
                time.sleep(86400)
                continue
            members = list(members)
            while theDay < today:
                theDayTimeStamp = int(time.mktime(theDay.timetuple()))
                for member in members:
                    # 如果在要计算利息的日期还不存在该用户，这天不计算其利息
                    if member['cdate'] >= theDayTimeStamp + 86400:
                        continue
                    # 如果在要计算利息的日期之前该户已经注销，这天及以后不再计算利息
                    if self.getAll('select * from statu_changes where cid = %s and type = 3 and cdate < %s', (member['id'], theDayTimeStamp)):
                        del members[members.index(member)]
                        continue
                    # 如果那天已经计算过该用户利息，不重复计算那天利息
                    exists = self.getAll('select id from interests where cid = %s and date = %s', (member['id'], theDayTimeStamp))
                    if exists:
                        continue
                    else:
                        # 获取那天余额
                        blance = self.getAll(sql, (theDayTimeStamp, member['id'], 
                                                   theDayTimeStamp, member['id'], 
                                                   theDayTimeStamp, member['id'], 
                                                   theDayTimeStamp, member['id']))
                        # 如果那天之前都没有过账户流通记录，那天不计算利息
                        if not blance:
                            continue
                        # 如果那天余额为0，那天不计算利息
                        if blance[0]['balance'] == 0:
                            continue
                        temp = (member['id'], theDayTimeStamp, blance[0]['balance'])
                        self.insertOne(insertSql, temp)
                        self.end()
                theDay += datetime.timedelta(1)
                self.update('update rates set latest_date = %s'%theDayTimeStamp)
                self.end()
            time.sleep(86400)
            continue
        
    def stop(self):  
        self.thread_stop = True  