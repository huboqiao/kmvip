# --*-- coding:utf-8 --*--
'''
Created on 2015年2月7日

@author: kylin

'''

# import hashlib,struct
import time,sys
from lib.db import Mysql
import datetime
from lib.massage import MassageModel
from app.center.core.card import Card
import json
reload(sys)
sys.setdefaultencoding( "utf-8" )

class Rate(Mysql):
    def __init__(self):
        Mysql.__init__(self)
        
    def payRates(self, datas):
        okCount = 0
        failData = []
        dateWhere = ' and `date` >= unix_timestamp("%s") and `date` <= unix_timestamp("%s") '%(datas['start'], datas['end'])
        for data in datas['data']:
            data['zcid'] = 168
            data['zccard'] = 1000000000
            data['zrcard'] = data['noid']
            data['zrid'] = data['cid']
            data['money'] = data['rates']
            data['uid'] = datas['uid']
            sql = 'update interests set payed = 1, rate = %s where cid = %s and payed = 0 '%(datas['rate'], data['cid']) + dateWhere
            payResult = self.update(sql)
            zzResult = Card().transferUpdate(data)
            if zzResult['stat']:
                self.end()
                okCount += 1
            else:
                self.end('rollback')
                data['failReason'] = zzResult['msg']
                failData.append(data)
        if okCount != len(datas['data']):
            return {'stat':False, 'msg':u'%s个客户的利息结算失败'%(len(datas['data']) - okCount), 'data':failData}
        else:
            return {'stat':True, 'msg':u'利息结算成功'}
           
    def queryRate(self,data):
        sql = "select * from `rates` where 1 = 1 limit 1"
        re = self.getOne(sql)
        if re :
            return {'stat':True,'data':re}
        else:
            return {'stat':False,'msg':'没有设置利率！'}
        
    def getOrdersID(self,orderSN):
        sql = 'select ordersn from `order` where ordersn = "' + orderSN + '"'
        re = self.getAll(sql)
        return re
        
    def updateRate(self,data):
#         try:
            id = int(data["id"])
            rates = float(data["rates"])
            if id >0:
                #update
                sql = "UPDATE `rates` SET `rates` = %s WHERE id = %s " % (rates,id)
                re = self.update(sql)
            else:
                #insert
                sql = "INSERT INTO `rates` (`rates`) values(%s) " % rates
                re = self.insertOne(sql,())
                
            self.end()
            
            if re>0:
                return {"stat":True,"msg":"设置成功"}
            else:
                return {"stat":False,"msg":"设置失败"}
                
#         except:
#             return {"stat":False,"msg":"设置失败"}

    def queryRatesList(self,data):
        start = data["start"].replace("-","/")
        end = data["end"].replace("-","/")
        starttime = time.mktime(time.strptime("%s 23:59:59" % start,'%Y/%m/%d %H:%M:%S'))
        sendtime = time.mktime(time.strptime("%s 23:59:59" % end,'%Y/%m/%d %H:%M:%S'))
        today = datetime.date.today() 
        today = time.mktime(today.timetuple())-1
        
        
        if today<sendtime:
            sendtime = today
            
        sqlCustomer = "\
                    SELECT cm.id as uid,cc.bdate, cc.noid from card as cc \
                    left join customer as cm on cc.uid = cm.id \
                    where cc.stat = 1 and cc.noid != 1000000000 \
                    "
        cusList = self.getAll(sqlCustomer)
        
        for key,value in enumerate(cusList):
            cusList[key]["ye"] = []
            endtime = sendtime
            cardid = value["noid"]
            sstarttime = starttime
            if starttime<value["bdate"]:
                sstarttime = value["bdate"]
            i = 0
            while True:
                if today<sstarttime:
                    break;
                sqltime = endtime - (3600*24)*i
                if sqltime < sstarttime:
                    break;
                
                
                sqlYe = '\
                select IFNULL(amount,0) AS `ye` FROM ( \
                    SELECT SUM(a3.amount) AS `amount` \
                    FROM cardcz AS a3 \
                    WHERE a3.cdate <= %s  \
                    AND a3.cardid = %s \
                    UNION ALL  \
                    SELECT SUM(-1*a3.amount) AS `amount` \
                    FROM cardtx AS a3 \
                    WHERE a3.cdate <= %s  \
                    AND a3.cardid = %s \
                    UNION ALL  \
                    SELECT SUM(if(a3.paycard = %s,-1*a3.amount,a3.amount)) AS `amount` \
                    FROM cardzz AS a3 \
                    WHERE a3.cdate <= %s  \
                    AND (a3.paycard = %s OR a3.incomecard = %s) \
                ) AS `y` \
                 where 1 = 1  ' %(sqltime,cardid,sqltime,cardid,cardid,sqltime,cardid,cardid)
                ye = self.getOne(sqlYe)
                cusList[key]["ye"].append({"amount":ye["ye"],"time":sqltime})
                #查询余额
                
                i+=1
                            
        return cusList
    
    def queryAllMerchant(self,data):
            membername = data['membername']     #客户中
            cardid = data['cardid']     #卡号
            tel = data['tel']           #电话
            idcard = data['idcard']     #身份证
            
            where = ''
            if membername == "":
                where += '  1 = 1'
            else:
                where += ' a1.membername like "%'+membername+'%"'
    
            if cardid == "":
                where += ' and 1 = 1'
            else:
                where += ' and a3.cardid like "%'+cardid+'%"'
    
            if idcard == "":
                where += ' and 1 = 1'
            else:
                where += ' and a1.idcard like "%'+idcard+'%"'
            
            if tel == "":
                where += ' and 1 =1'
            else:
                where += ' and a1.tel like "%'+tel+'%"'
#2014.10.9 17:55 添加查询字段storeName
            sql = "SELECT a1.id AS uid,a1.stat AS userstat,a1.*,a2.*,a3.name as storeName,a4.nickname FROM customer AS a1,customerinfo AS a2 ,storage as a3, user AS a4 WHERE a1.id = a2.cid and a1.adduser =a4.id and a2.storename = a3.id and ("+where+")  \
                    GROUP BY a1.id "
            return self.getAll(sql)

    def addInterest(self,uid,amount,rates,cdate):
        interest=float(amount)*rates/365
        sql='insert into interest (uid,Interest,cdate,stype) values ('+str(uid)+','+str(interest)+','+str(cdate)+',0)'
        try:
            self._cursor.execute(sql)
            self._conn.commit()
        except:
            pass
    #更新上次计算利息时间    
    def updateLatestDate(self,latestdate):  
        try:
            sql = "UPDATE `rates` SET `latest_date` = %s WHERE id = 1 " % latestdate
            re = self.update(sql)
            self.end()
        except:
            pass
        
    #计算出来的利息列表    
    def ratesList(self,data):
        currentRate = self.getOne('select rates from rates')['rates']
        wheres = ' where a.date >= UNIX_TIMESTAMP("%s") and a.date < UNIX_TIMESTAMP("%s") + 86400 '%(data['start'], data['end'])
        wheres += ' and ca.noid != "1000000000" and ca.noid like "%' + str(data['cardid']) + '%" '
        wheres += ' and (c.stat != 3 or (select s.cdate from statu_changes as s where s.type = 3 and s.cid = c.id) > UNIX_TIMESTAMP("%s") + 86400) '%data['start']
        
        sql0 = 'SELECT SUM(a.amount*'+str(currentRate)+') AS rates, c.membername, a.payed, a.cid, ca.noid, a.id\
               FROM interests AS a \
               LEFT JOIN customer AS c ON a.cid = c.id \
               LEFT JOIN card as ca on ca.uid = c.id ' + wheres + ' \
               and a.payed = 0 \
               GROUP BY a.cid, a.payed \
               ORDER BY a.cid ASC'
        sql1 = 'SELECT SUM(a.amount*a.rate) AS rates, c.membername, a.payed, a.cid, ca.noid, a.id\
               FROM interests AS a \
               LEFT JOIN customer AS c ON a.cid = c.id \
               LEFT JOIN card as ca on ca.uid = c.id ' + wheres + ' \
               and a.payed = 1 \
               GROUP BY a.cid, a.payed \
               ORDER BY a.cid ASC'
        if data['payed'] == 0:
            re = self.getAll(sql0)
        elif data['payed'] == 1:
            re = self.getAll(sql1)
        else:
            re = self.getAll(sql0)
            re1 = self.getAll(sql1)
            if re:
                if re1:
                    re = list(re)
                    re.extend(list(re1))
            else:
                if re1:
                    re = re1
        if re :
            return {'stat':True,'data':re,'start':data['start'], 'end':data['end'], 'currentRate':currentRate}
        else:
            return {'stat':False,'msg':'无利息记录！'}
        
    #利息结算
    def interestclear(self,data):
        wheres=[]
        if data['start'] !='':
            wheres.append(' cdate > UNIX_TIMESTAMP("'+str(data['start'])+'") ')
        
        if data['end'] !='':
            wheres.append(' cdate < UNIX_TIMESTAMP("'+str(data['end'])+'") ')
        if data['userlist'] != '':
            wheres.append(' uid in ('+str(data["userlist"])+') ')
            wheres.append(' stype = 0 ')
        
        if len(wheres)<=0:
            wheres = ''
        else:
            wheres = ' where '+" and ".join(wheres)
        #修改利息状态
        sql=' update `Interest` set stype = 1 '+wheres
        try:
            re = self.update(sql)
            
        except:
            return {'stat':False,'msg':'结算失败！'}
        userlist = data["userlist"].split(",")
        amountlist = data["amountlist"].split(",")
        now = str(int(time.time()))
        massageModel = MassageModel()
        try:
            for k,i in enumerate(userlist):
                #查询用户卡号
                sql = "select noid,uid,tel,membername,amount from card as a \
                        left join customer as b \
                        on a.uid = b.id where b.id = %s " % i
                user = self.getOne(sql)
                sql = "select a1.amount,a2.uid from `customer` as a1 \
                        left join `card` as a2 on a1.id = a2.uid \
                        where a2.noid = 1000000000 "
                        
                company = self.getOne(sql)
                #插入转账记录
                value = ("1000000000",str(user["noid"]),str(amountlist[k]),now,
                         str(0),data["uid"],"利息结算",
                         str(company["amount"]-float(amountlist[k])),
                         str(user["amount"]+float(amountlist[k])))
                sql = "insert into cardzz\
                        (paycard,incomecard,amount,cdate,ctype,uid,txt,paybalance,payeebalance)\
                         values (%s,%s,%s,%s,%s,%s,%s,%s,%s) "
                self.insertOne(sql, value)
                
                uid = user["uid"]
                tel = user["tel"]
                membername = user["membername"]
                amount = user["amount"]
                
                #更新用户余额
                sql = "update customer set amount = amount + %s where id = %s " % (amountlist[k],uid)
                self.update(sql)
                #更新公司余额
                sql = "update customer set amount = amount - %s where id = %s " % (amountlist[k],company["uid"])
                self.update(sql)
            self.end()
            return {'stat':True,'msg':'结算成功！'}
        except:
            return {'stat':False,'msg':'结算失败！'}
                