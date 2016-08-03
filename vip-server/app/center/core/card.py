# --*-- coding:utf-8 --*--
'''
Created on 2014年6月13日

@author: 逗逗

会员卡操作类
'''
from __future__ import division
import hashlib,struct
import time,sys
from lib.db import Mysql

import json
reload(sys)
sys.setdefaultencoding( "utf-8" )

class Card(Mysql):
    def __init__(self):
        Mysql.__init__(self)
          
    
    def queryCardinfo(self,card):
        '''查询会员卡信息'''
        sql = "SELECT a1.freezen, a1.id,a1.membername,a1.sex,a1.nation,a1.adder,a1.idcard,a1.carddate,a1.amount,a1.tel,a1.freezen,\
        a2.stat AS cardstat ,a2.password,a2.cardid as card,a2.noid,\
        a3.bankcard,a3.bankname,a3.bankadder,a3.bankusername,a3.useimg_path,a3.cardimg_path, a3.finger1, a3.finger2, a3.finger3, \
        CONCAT_WS(':', a4.name, a5.name, a6.name) as storename \
        FROM customer AS a1 \
        left join card AS a2 on a1.id = a2.uid\
        left join customerinfo as a3 on a1.id = a3.cid\
        left join storage_hs as a6 on a1.storagenumber = a6.id \
        left join storage_qy as a5 on a6.qid = a5.id\
        left join storage as a4 on a5.sid = a4.id\
        WHERE a2.stat = 1\
        and (a2.cardid = '" + str(card) +"' or a2.noid = '" + str(card) + "')"
        re = self.getOne(sql)
        if re:
            stat = self.queryCardStat(re['cardstat'])
            data = {'data':re,'stat':str(stat)}
            return data
        else:
            return {'stat':-1,'msg':'该会员卡不存在,或者处于【注销，未激活】状态','data':{}}
    def getNoId(self,cardid):
        try:
            cardid = cardid['noid']
        except:
            pass
        sql = 'select noid from card where cardid='+str(cardid)+' or noid='+str(cardid)
        return self.getOne(sql)
    
    def updateCardStat(self,data,stat=3):
        try:
            card = self.getNoId(data['noid'])
        except:
            card = self.getNoId(data)
        sql = 'update card set `stat`='+str(stat)+' where noid='+card['noid']
        try:
            self.update(sql)
            if stat == 3:
                try:
                    self.update('update customer set `stat` = 2 where id = %s', (int(data['cid'])))
                    sql = 'insert into statu_changes(id, cid, uid, type, noid, cdate) values(NULL, %s, %s, 2, %s, UNIX_TIMESTAMP())'
                    temp = (data['cid'], data['uid'], card['noid'])
                    self.insertOne(sql, temp)
                except:
                    pass
            self.end()
            return {'stat':1}
        except:
            return {'stat':-1,'msg':'冻结卡失败'}

    def queryCard(self,card): 
        noid = self.getNoId(card)
        if noid:
            '''查询卡信息'''
            sql = 'select * from card where noid ="'+noid['noid']+'" '
            return self.getOne(sql)
        else:
            return False
    
    def queryUserCardAll(self,uid):
        '''查询该UID下的所属卡'''
        sql = 'select * from card where uid = "'+str(uid) + '"'
        return self.getAll(sql)
    
    def queryCardRecord(self,cardid,datewhere=7):
        '''查询某卡的交易流水'''
        datewhere = self.dateQuery(datewhere)
        cardid = self.getNoId(cardid)
        try:
            cardid = cardid['noid']
        except:
            return False
        
        #查询充值记录
        sql = 'SELECT * FROM cardcz WHERE cardid = "'+cardid+'" and  '+datewhere+' order by cdate desc'
        cardcz = self.getAll(sql)
        if not cardcz:
            cardcz = ''
        #查询提现记录
        sql = 'SELECT * FROM cardtx WHERE cardid = "'+cardid+'" and '+datewhere+' order by cdate desc'
        cardtx = self.getAll(sql)
        if not cardtx:
            cardtx = ''
        #查询转出记录
        sql = 'SELECT * FROM cardzz WHERE paycard = "'+cardid+'" and '+datewhere+' order by cdate desc'
        cardzc = self.getAll(sql)
        if not cardzc:
            cardzc = ''
        #查询转入记录
        sql = 'SELECT * FROM cardzz WHERE incomecard = "'+cardid+'" and '+datewhere+' order by cdate desc'
        cardin = self.getAll(sql)
        if not cardin:
            cardin = ''
        
        return {'cz':cardcz,'tx':cardtx,'zz':cardzc,'in':cardin}
    
    
    def dateQuery(self,datewhere,enddate = 0):
        if datewhere == 30: #近30天
            datewhere = ' DATE_SUB(CURDATE(), INTERVAL 30 DAY) <= date(FROM_UNIXTIME(cdate))'
        elif datewhere == 1:
            datewhere = ' to_days(FROM_UNIXTIME(cdate)) = to_days(now())'
        elif datewhere == -1:
            datewhere = 'DAY( NOW( ) ) - DAY( FROM_UNIXTIME(cdate)) = 1 '
        elif datewhere == 7:
            datewhere = 'DATE_SUB(CURDATE(), INTERVAL 7 DAY) <= date(FROM_UNIXTIME(cdate))'
        elif datewhere == 31:    #本月
            datewhere = "DATE_FORMAT( FROM_UNIXTIME(cdate), '%Y%m' ) = DATE_FORMAT( CURDATE( ) , '%Y%m' )"
        elif datewhere == 90:
            datewhere = "PERIOD_DIFF( date_format( now( ) , '%Y%m' ) , date_format( FROM_UNIXTIME(cdate), '%Y%m' ) ) =1"    #本季度数据
        elif datewhere == 0:
            datewhere =' 1=1 '
        if enddate !=0:
            datewhere = ' cdate <= '+enddate +' and cdate >= '+ datewhere
        return datewhere
    
    def dateQuery2(self,datewhere,enddate = 0):
        if datewhere == 30: #近30天
            datewhere = ' DATE_SUB(CURDATE(), INTERVAL 30 DAY) <= date(FROM_UNIXTIME(a1.cdate))'
        elif datewhere == 1:
            datewhere = ' to_days(FROM_UNIXTIME(a1.cdate)) = to_days(now())'
        elif datewhere == -1:
            datewhere = 'DAY( NOW( ) ) - DAY( FROM_UNIXTIME(a1.cdate)) = 1 '
        elif datewhere == 7:
            datewhere = 'DATE_SUB(CURDATE(), INTERVAL 7 DAY) <= date(FROM_UNIXTIME(a1.cdate))'
        elif datewhere == 31:    #本月
            datewhere = "DATE_FORMAT( FROM_UNIXTIME(a1.cdate), '%Y%m' ) = DATE_FORMAT( CURDATE( ) , '%Y%m' )"
        elif datewhere == 90:
            datewhere = " quarter( FROM_UNIXTIME( a1.cdate ) ) = quarter( curdate( ))"    #本季度数据
        elif datewhere == 0:
            datewhere =' 1=1 '
        if enddate !=0:
            datewhere = ' a1.cdate <= UNIX_TIMESTAMP("'+enddate +'") and a1.cdate >= UNIX_TIMESTAMP("'+ datewhere+'")'
        return datewhere    
    
    
    
    def zzReport(self,cardid = '',ctype=0,datewhere=1,enddate=0):
        '''
                查询金荣卡指定日期的转出转入明细
                @cardid 查询卡号
                @ctype 1为转出，2为转入
                @datewhere 开始日期 如果是单一数字并且enddate为空时，就查固定数据
                @enddate    结束日期
        '''
        wheres = ''
        if cardid != '':
            noid = self.getNoId(cardid)
            try:
                cardid = noid['noid']
            except:
                return False
        
        
        if enddate != 0:
            wheres += self.dateQuery2(datewhere,enddate)
        else:
            wheres += self.dateQuery2(datewhere)

        if ctype == 1 and cardid !='':
            wheres += ' and a1.paycard = '+str(cardid)
        elif ctype == 2 and cardid !='':
            wheres += ' and a1.incomecard = '+str(cardid)
        
        if ctype == 0:
            if cardid!='':
                wheres += ' and a1.paycard ='+str(cardid)
            sql = 'SELECT * FROM cardzz AS a1,card AS a2,customer AS a3 WHERE a1.paycard = a2.noid AND a2.uid = a3.id and '+wheres
            zzdate = self.getAll(sql)
            if cardid!='':
                wheres += ' and a1.incomecard ='+str(cardid)
            sql = 'SELECT * FROM cardzz AS a1,card AS a2,customer AS a3 WHERE a1.incomecard = a2.noid AND a2.uid = a3.id and '+wheres
            zrdata = self.getAll(sql)
            return {'zz':zzdate,'zr':zrdata}
        elif ctype == 1:
            sql = 'SELECT * FROM cardzz AS a1,card AS a2,customer AS a3 WHERE a1.paycard = a2.noid AND a2.uid = a3.id and '+wheres
            zzdate = self.getAll(sql)
            return {'data':zzdate}
        elif ctype == 2:
            sql = 'SELECT * FROM cardzz AS a1,card AS a2,customer AS a3 WHERE a1.incomecard = a2.noid AND a2.uid = a3.id and '+wheres
            zrdata = self.getAll(sql)
            return {'data':zrdata}
            
    def transferMatch(self,data):
        pass
    def reportList(self,cardid='',userid='',ctype=2,paytype=0,datewhere=1,enddate = 0):
        '''
                查询充值、提现的流水报表，默认是查询当天的流水
        @cardid 查询卡号
        @ctype 查询表名 1为充值 1为提现
        @paytype 付款方式
        @datewhere 开始日期 如果是单一数字并且enddate为空时，就查固定数据
        @enddate    结束日期
        '''
        wheres = ''
        ttable = ''
        redata = {}
        #判断是哪个类型
        if ctype == 0:
            ttable = 'cardcz'
        elif ctype == 1:
            ttable = 'cardtx'
        elif ctype == 2:
            ttable = ''
        if enddate !=0:
            wheres += self.dateQuery2(datewhere,enddate)
        else:
            wheres += self.dateQuery2(datewhere)
        
        if cardid != '':
            noid = self.getNoId(cardid)
            try:
                cardid = noid['noid']
                wheres += ' and (a1.cardid =' + str(cardid)+' or a2.noid ='+str(cardid)+')'
            except:
                return False
        
        if userid != '':
            wheres += ' and a1.uid = '+str(userid)
        if paytype == 0:
            wheres += ' and a1.ctype = 0'
        elif paytype == 1:
            wheres += ' and a1.ctype = 1'
        else:
            wheres += ' and 1 = 1'
            
        if ttable == "":
            #查询充值记录
            sql = 'SELECT a1.*,a3.membername,a4.nickname,a2.noid,a3.idcard,a3.tel FROM cardcz AS a1,card AS a2 ,customer AS a3,`user` AS a4 WHERE a1.cardid = a2.noid AND a2.uid = a3.id AND a1.uid = a4.id AND '\
                 +wheres +' order by a1.ctype asc ,cdate desc'
            redata[0] = self.getAll(sql)
            #查询提现记录
            sql = 'SELECT a1.*,a3.membername,a4.nickname,a2.noid,a3.idcard,a3.tel,a5.bankname,a5.bankcard FROM cardtx AS a1,card AS a2 ,customer AS a3,`user` AS a4 , customerinfo as a5 WHERE a1.cardid = a2.noid AND a2.uid = a3.id AND a1.uid = a4.id AND  a3.id = a5.cid AND '\
                +wheres +' order by a1.ctype,cdate desc'
            redata[1] = self.getAll(sql)
            return {'data':redata}
        else:
            sql = 'SELECT a1.*,a3.membername,a4.nickname,a2.noid,a3.idcard,a3.tel FROM '+ttable+' AS a1,card AS a2 ,customer AS a3,`user` AS a4, customerinfo as a5  WHERE a1.cardid = a2.noid AND a2.uid = a3.id AND a1.uid = a4.id AND  a3.id = a5.cid AND  '\
                +wheres +' order by ctype,cdate desc'
            data = self.getAll(sql)
            return {'data':data}


    def bindingCard(self,datas):
        '''绑定会员卡'''
        cid = datas['user_id']
        card = datas['card']
        pwd = datas['pwd']
        addid = datas['addid']
            
        re = self.queryCard(card)   #查询卡片信息
        if re:
            cardstat = re['stat']
            if cardstat == 0:   #判断卡是否未绑定 
                sql = 'update card set uid = %s,stat = 1,`password` =%s,addid = %s, bdate = UNIX_TIMESTAMP()  where noid = %s'
                noid = self.getNoId(card)
                tmp = [cid,pwd,addid, noid['noid']]
                ids = self.insertOne(sql,tmp)
                sql = 'UPDATE customer SET stat = 1 WHERE id = '+cid
                self.update(sql)
                sql = 'insert into statu_changes(id, cid, uid, type, noid, cdate) values(NULL, %s, %s, 0, %s, UNIX_TIMESTAMP())'
                temp = (cid, addid, noid['noid'])
                self.insertOne(sql, temp)
                self.end()
                return {'stat':1,'msg':'绑定成功'}
            elif cardstat == 1:
                return {'stat':-1,'msg':'该卡己经被占用'}
            else:
                return self.queryCardStat(cardstat)
        else:
            return {'stat':-1,'msg':'该卡不存在'}

    def queryCardStat(self,cardstat):
        '''查询卡片状态'''
        if cardstat == 0 or cardstat == '':
            return u'无效'
        if cardstat == 1:
            return True
        if cardstat == 2:
            return u'注销'
        if cardstat == 3:
            return u'冻结'
    
    def modifyCardPasswd(self,card,passwd):
        pwds=hashlib.md5()
        pwds.update(passwd)
        cards = self.getNoId(card)
        noid = cards['noid']
        sql = "update card set `password`='"+str(pwds.hexdigest())+"' where noid ="+str(noid)
        try:
            self.update(sql)
            self.end()
            return True
        except:
            return False
    
    def pwdCheckzz(self, card, passwd):
        '''匹配卡片密码'''
        sql = "SELECT `PASSWORD` as pwd FROM card WHERE cardid = "+card +' or noid='+card
        re = self.getOne(sql)
        
        if re:
            password = re['pwd']
            pwds=hashlib.md5()
            pwds.update(str(passwd))
            if pwds.hexdigest() == password:
                return  {'stat':2}
            else:
                return {'stat':-1,'msg':'用户密码输入错误！'}
        
    def queryCardPasswd(self,card,passwd):
        '''匹配卡片密码'''
        sql = "SELECT `PASSWORD` as pwd FROM card WHERE cardid = "+card +' or noid='+card
        re = self.getOne(sql)
        
        if re:
            password = re['pwd']
            pwds=hashlib.md5()
            pwds.update(str(passwd))
            if pwds.hexdigest() == password:
                return  {'stat':1}
            else:
                return {'stat':-1,'msg':'用户密码输入错误！'}
    
    def qeuryAmount(self,uid):
        sql = 'SELECT amount FROM customer where id = "' + str(uid) + '"'
        return self.getOne(sql)
        
    def recharge(self,uid,card,amount,ctype,txt='',bankno='',bankname='',bankcard='',bankadder='',bankusername=''):
        '''充值操作
            @setup1 更新用户余额
            @setup2 添加充值明细
            @retun 逻辑真假
            @card 会员卡
            @amount 金额
            @ctype 类型 0 为现金，1为pos刷卡
            @txt 备注    
        '''
        try:
            amount = str('%0.2f'%float(amount))
            sql = 'select uid from card where cardid = '+str(card)+' or noid = '+str(card)
            re = self.getOne(sql)
            sql = ' UPDATE customer SET amount = amount + '+amount+' WHERE  id = "'+str(re['uid'])+'"'
            self.update(sql)
            balance = self.getOne('select amount, freezen from customer where id = "' + str(re['uid']) + '"')
            balance = '%0.2f'%(balance['amount'] + balance['freezen'])
            sql = "insert into cardcz(cardid,amount,cdate,ctype,txt,bankno,bankname,bankcard,bankadder,bankusername,uid,balance)values(%s,%s,UNIX_TIMESTAMP(),%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            tmp = [card,amount,ctype,txt,bankno,bankname,bankcard,bankadder,bankusername,str(uid),balance]
            self.insertOne(sql,tmp)
            t = int(time.time())
            self.end()
            return {'stat':True,'msg':u'充值成功！开始打印小票', 'time':t}
        except:
            return {'stat':False,'msg':u'系统内部错误，请稍后再试'}
            
    def taking(self,data):
        '''提现操作
            @setup1 更新用户余额
            @setup2 添加提现明细
            @retun 逻辑真假
            @card 会员卡
            @amount 金额
            @ctype 类型 0 为现金，1为转账方式
            @txt 备注    
        '''
        try:
            cid = self.getOne('select uid from card where noid = "' + str(data['cardid']) + '" or cardid = "' + str(data['cardid']) + '"')
            if cid['uid'] != '':
                oldamount = self.qeuryAmount(cid['uid'])
            else:
                return {'stat':False,'msg':u'转出卡不存在'}
                
            if float(oldamount['amount']) < float(data['amount']):
                return {'stat':False,'msg':u'余额不足，无法提现'}
            
            sql = ' UPDATE customer SET amount= amount - '+str(data['amount'])+' WHERE  id = "'+str(cid['uid'])+'"'
            self.update(sql)
            balance = self.getOne('select amount from customer where id = "' + str(cid['uid']) + '"')
            balance = '%0.2f'%(balance['amount'])
            sql = "insert into cardtx(cardid,amount,cdate,ctype,txt,bankno,uid,balance,bankname,bankusername, bankcard)values(%s,%s,UNIX_TIMESTAMP(),%s,%s,%s,%s,%s,%s,%s,%s)"
            tmp = [data['cardid'],data['amount'],data['ctype'],data['txt'],data['bankno'],data['uid'],balance,data['bankname'],data['bankusername'],data['bankcard']]
            self.insertOne(sql,tmp)
            t = int(time.time())
            self.end()
            return {'stat':True,'msg':'提现成功,开始打印!', 'time':t}
        except:
            return {'stat':False,'msg':'系统内部错误，请稍后再试'}

    def updateBankNo(self,ids,bankno,inType= 0):
        if inType == 0:
            sql = "update cardtx set bankno ='"+bankno+"' where id="+str(ids)
        else:
            sql = "update cardcz set bankno ='"+bankno+"' where id="+str(ids)
        try:    
            self.__query(sql)
            return 1
        except:
            return 2
    
    def transfer(self,zzcard,zrcard,amount):
        '''转账操作
                    流程：
                1、接收转出人卡号及收账人卡号，判断转出和收账人的卡状态
                            只有都为正常才能转账
                2、判断转出人余额是否正常
                3、返回状态，进行下一步验证密码及授权
        '''
        zzcardStat = self.queryCardinfo(zzcard)
        if zzcardStat['stat'] == u'无效':
            return {'stat':False,'msg':zzcard+zzcardStat['stat']}
        zrcardStat = self.queryCardinfo(zrcard)
        if zrcardStat['stat'] == u'无效':
            return {'stat':False,'msg':zrcard+zrcardStat['stat']}
        zzcardAmount = self.qeuryAmount(zzcard)
        if float(zzcardAmount['amount']) < float(amount):
            return {'stat':False,'msg':u'卡号：'+zzcard+u'，余额不足'}
        return {'stat':True}
    
    def transferUpdate(self,data):
        '''转账成功操作
            1、更新转出人，收账人余额
            2、添加转账明细
            '''      
        try:
            if data['money'] == 0:
                return {'stat':False, 'msg':u'转账金额不能为零'}
            amount = '%0.2f'%float(data['money'])
            oldamount = self.qeuryAmount(data['zcid'])
            if float(oldamount['amount']) < float(data['money']):
                return {'stat':False,'msg':u'余额不足，无法转账'}
            sql = ' UPDATE customer SET amount = amount - '+ str(amount) +' WHERE  id = "'+str(data['zcid'])+'"'
            self.update(sql)
            paybalance = self.getOne('select amount, freezen from customer where id = "' + str(data['zcid']) + '"')
            paybalance = '%0.2f'%(paybalance['amount'] + paybalance['freezen'])
            sql= ' UPDATE customer SET amount= amount + '+str(amount)+' WHERE  id = "'+str(data['zrid'])+'"'
            self.update(sql)
            payeebalance = self.getOne('select amount, freezen from customer where id = "' + str(data['zrid']) + '"')
            payeebalance = '%0.2f'%(payeebalance['amount'] + payeebalance['freezen'])
            sql = 'insert into cardzz(paycard,incomecard,amount,cdate,uid,ctype,paybalance,payeebalance)values(%s, %s, %s, UNIX_TIMESTAMP(), %s, %s, %s, %s)'
            temp = (data['zccard'],data['zrcard'],amount, data['uid'],0,paybalance, payeebalance)
            self.update(sql,temp)
            t = int(time.time())
            self.end()
            return {'stat':True,'msg':u'转账成功','time':t}
        except Exception as e:
            return {'stat':False,'msg':u"转账失败，请稍后再试"}
            
    
        
    def insertCardzz(self,card1,card2,meony,ctype=1):
        '''添加转账明细'''
        if ctype == 1:
            sql = "INSERT INTO cardzz(`cardid`,`sendcardid`,`amount`,`cdate`,`ctype`) VALUES ('"+str(card1)+"','"+str(card2)+"',"+str(meony)+",UNIX_TIMESTAMP(),'1')"
        elif ctype == 2:
            sql = "INSERT INTO cardzz(`cardid`,`sendcardid`,`amount`,`cdate`,`ctype`) VALUES ('"+str(card2)+"','"+str(card1)+"',"+str(meony)+",UNIX_TIMESTAMP(),'2')"
        self.__query(sql)
        
           
    
    def addCard(self,card,noid,addId):
        '''添加会员卡入库'''
        if self.queryCard(card):    #判断卡位是否存在
            return {'stat':-1,'msg':'该卡己经存在'}
        else:
            #sql = "INSERT INTO     card (cardid, noid,cdate)VALUES('"+str(card)+"','"+str(noid)+"','"+str(int(time.time()))+"')"
            sql = "INSERT INTO card (cardid, noid,cdate,addid)VALUES(%s,%s,UNIX_TIMESTAMP(),%s)"
            tmp = [str(card),str(noid),addId]
            if self.insertOne(sql,tmp):
                sql = 'insert into statu_changes(id, cid, uid, type, noid, cdate) values(NULL, NULL, %s, 4, %s, UNIX_TIMESTAMP())'
                temp = (addId, noid)
                self.insertOne(sql, temp)
                self.end()
                return {'stat':1,'msg':'添加成功'}
            else:
                return {'stat':-1, 'msg':u'添加失败'}
    
    def updateCard(self,card,ctype):
        '''更新卡状态 0未绑定，1为正常，2为注销 3为冻结-挂失'''
        sql = 'update card set `stat` = '+str(ctype) + ' where cardid = "'+str(card)+'"'
        re =  self.update(sql)
        self.end()
        return re
    
    
    def logoutCard(self,card,pwd):
        '''注销会员卡'''
        pass
    
    def queryJingbanren(self):
        sql = 'select id,nickname from `user` '
        re = self.getAll(sql)
        return re
    
    #查询某经办人当天处理的充值总额
    def queryCZAmountToday(self,id):
        sql = 'SELECT SUM(a2.amount) FROM cardcz AS a2 WHERE TO_DAYS(FROM_UNIXTIME(a2.cdate)) = TO_DAYS(NOW()) AND uid = '+id
        re = self.getOne(sql)
        return re
    
    #查询某经办人一段时间内的充值总额
    def queryCZAmountSpan(self,data):
        id = data['id']
        start = data['start']
        end = data['end']
        
        sql = 'SELECT SUM(a2.amount) FROM cardcz AS a2 WHERE a2.cdate <= UNIX_TIMESTAMP("'+end+' 23:59:59") AND a2.cdate >= UNIX_TIMESTAMP("'+start+' 00:00:00") AND uid = '+id
        re = self.getOne(sql)
        return re
    
    
    #查询某经办人当天处理的提现总额
    def queryTXAmountToday(self,id):
        sql = 'SELECT SUM(a2.amount) FROM cardtx AS a2 WHERE TO_DAYS(FROM_UNIXTIME(a2.cdate)) = TO_DAYS(NOW()) AND uid = '+id
        re = self.getOne(sql)
        return re
    
    #查询某经办人一段时间内的提现总额
    def queryTXAmountSpan(self,data):
        id = data['id']
        start = data['start']
        end = data['end']
        
        sql = 'SELECT SUM(a2.amount) FROM cardtx AS a2 WHERE a2.cdate <= UNIX_TIMESTAMP("'+end+' 23:59:59") AND a2.cdate >= UNIX_TIMESTAMP("'+start+' 00:00:00") AND uid = '+id
        re = self.getOne(sql)
        return re
        
    #查询某经办人周期类处理的充值总额
    def queryCZAmountPeriod(self,data):
         #获取经办人id值
         id = data['id']
         #获取周期
         period = data['period']
         #判断周期
         if period == '1':
             #今天
             sql = 'SELECT SUM(a2.amount) FROM cardcz AS a2 WHERE TO_DAYS(FROM_UNIXTIME(a2.cdate)) = TO_DAYS(NOW()) AND uid = '+id
         if period == '2':
             #昨天到今天
             sql = 'SELECT SUM(a2.amount) FROM cardcz AS a2 WHERE TO_DAYS(NOW())-TO_DAYS(FROM_UNIXTIME(a2.cdate))<=1 AND uid = '+id
         if period == '3':
             #本周
             sql = 'SELECT SUM(a2.amount) FROM cardcz AS a2 WHERE DATE_SUB(CURDATE(),INTERVAL 7 DAY)<=DATE(FROM_UNIXTIME(a2.cdate)) AND uid = '+id
         if period == '4':
             #近30天
             sql = 'SELECT SUM(a2.amount) FROM cardcz AS a2 WHERE DATE_SUB(CURDATE(),INTERVAL 30 DAY)<=DATE(FROM_UNIXTIME(a2.cdate)) AND uid = '+id
         if period == '5':
             #本月
             sql = 'SELECT SUM(a2.amount) FROM cardcz AS a2 WHERE DATE_FORMAT(FROM_UNIXTIME(a2.cdate),"%Y%m")=DATE_FORMAT(CURDATE(),"%Y%m") AND uid = '+id
         if period == '6':
             #上个月               
             sql = 'SELECT SUM(a2.amount) FROM cardcz AS a2 WHERE PERIOD_DIFF(DATE_FORMAT(NOW(),"%Y%m"),DATE_FORMAT(FROM_UNIXTIME(a2.cdate),"%Y%m"))=1 AND uid = '+id
         re = self.getOne(sql)
         return re
     
     
     
     #查询某经办人周期类处理的提现总额
    def queryTXAmountPeriod(self,data):
         #获取经办人id值
         id = data['id']
         #获取周期
         period = data['period']
         #判断周期
         if period == '1':
             #今天
             sql = 'SELECT SUM(a2.amount) FROM cardtx AS a2 WHERE TO_DAYS(FROM_UNIXTIME(a2.cdate)) = TO_DAYS(NOW()) AND uid = '+id
         if period == '2':
             #昨天到今天
             sql = 'SELECT SUM(a2.amount) FROM cardtx AS a2 WHERE TO_DAYS(NOW())-TO_DAYS(FROM_UNIXTIME(a2.cdate))<=1 AND uid = '+id
         if period == '3':
             #本周
             sql = 'SELECT SUM(a2.amount) FROM cardtx AS a2 WHERE DATE_SUB(CURDATE(),INTERVAL 7 DAY)<=DATE(FROM_UNIXTIME(a2.cdate)) AND uid = '+id
         if period == '4':
             #近30天
             sql = 'SELECT SUM(a2.amount) FROM cardtx AS a2 WHERE DATE_SUB(CURDATE(),INTERVAL 30 DAY)<=DATE(FROM_UNIXTIME(a2.cdate)) AND uid = '+id
         if period == '5':
             #本月
             sql = 'SELECT SUM(a2.amount) FROM cardtx AS a2 WHERE DATE_FORMAT(FROM_UNIXTIME(a2.cdate),"%Y%m")=DATE_FORMAT(CURDATE(),"%Y%m") AND uid = '+id
         if period == '6':
             #上个月               
             sql = 'SELECT SUM(a2.amount) FROM cardtx AS a2 WHERE PERIOD_DIFF(DATE_FORMAT(NOW(),"%Y%m"),DATE_FORMAT(FROM_UNIXTIME(a2.cdate),"%Y%m"))=1 AND uid = '+id
         re = self.getOne(sql)
         return re
     
     #查询某经办人处理的所有用户（某段时间内）
    def  queryMoneyDetail(self,data):
         #经办人id
         id = data['id']
         #开始时间
         start = data['start']
         #结束时间
         end = data['end']
         #表名
         tablename = data['tablename']
         #ivan修改 按查询数据的cdate倒序排列
         sql = 'SELECT a.cardid,a.ctype, a.amount, a.cdate, b.membername FROM  '+tablename+'  AS a,customer AS b,card AS c WHERE c.uid = b.id AND c.noid = a.cardid and a.cdate <= UNIX_TIMESTAMP("'+end+' 23:59:59") AND a.cdate >= UNIX_TIMESTAMP("'+start+' 00:00:00") AND a.uid = '+id + ' order by a.cdate desc'
         re = self.getAll(sql)
         return re
    
    
    #查询某经办人处理的部分用户（金额交易方式）（某段时间内）
    def queryMoneyTypeDetail(self,data):
        #经办人id
         id = data['id']
         #开始时间
         start = data['start']
         #结束时间
         end = data['end']
         #表名
         tablename = data['tablename']
         #方式
         ctype = data['ctype']
        
         sql = 'SELECT a.cardid,a.ctype, a.amount, a.cdate, b.membername FROM  '+tablename+'  AS a,customer AS b,card AS c WHERE c.uid = b.id AND c.noid = a.cardid and a.cdate <= UNIX_TIMESTAMP("'+end+' 23:59:59") AND a.cdate >= UNIX_TIMESTAMP("'+start+' 00:00:00") AND a.ctype= '+ctype+' AND a.uid = '+id
         re = self.getAll(sql)
         return re
        
        
        
        
        
    
