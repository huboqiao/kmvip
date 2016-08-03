#coding:utf-8
'''
Created on 2015年4月10日

@author: huaan
'''
import hashlib
import time,sys
from app.center.core.card import Card
from app.center.core.member import Member
from lib.db import Mysql

reload(sys)
sys.setdefaultencoding( "utf-8" )

class Payment(Mysql):
    def __init__(self):
        Mysql.__init__(self)
    
    #根据条件检索缴费项目
    def queryPayTypes(self,data):
        where = ' where 1 = 1 '
        try:
            where += ' and typename = "' + str(data['typename']) + '"'
        except:
            pass
        try:
            where += ' and id != "' + str(data['id']) + '"'
        except:
            pass
        try:
            where += ' and stat = "' + str(data['typeStat']) + '"'
        except:
            pass
        sql = 'SELECT * FROM paytype' + where
        re = self.getAll(sql)
        if re:
            return {'stat':True, 'data':re}
        else:
            return {'stat':False, 'msg':u'没有收费项目，请添加'}
    #根据条件检索缴费记录
    def queryPaymentRecord(self,data):
        where = ' where 1 = 1 '
        try:
            where = ' where pp.cdate >= UNIX_TIMESTAMP("%s") and pp.cdate < (UNIX_TIMESTAMP("%s") + 86400) '%(data['startDate'], data['endDate'])
            if data['cardid'] != '':
                where += ' and c.noid like "%' + str(data['cardid']) + '%" '
            if data['name'] != '':
                where += ' and ct.membername like "%' + str(data['name']) + '%" '
            if data['type'] != '':
                where += ' and pp.typeid = "' + str(data['type']) + '" '
            if data['statu'] == 0:
                where += ' and pp.paydate is NULL'
            elif data['statu'] == 1:
                where += ' and pp.paydate is not NULL'
        except Exception as e:
            pass
            
        sql = "SELECT pp.typeid, pp.id, pp.cid, ct.idcard, ct.adder, case when pp.txt = NULL then 'Null' else pp.txt end txt, from_unixtime(pp.cdate, '%Y/%m/%d') as cdate, \
               from_unixtime(pp.edate, '%Y/%m/%d') as edate, pp.amount, ct.membername, c.noid, pt.typename,\
               case when pp.paydate is NULL then '未付款' else FROM_UNIXTIME(pp.paydate, '%Y/%m/%d') end as stat \
               FROM payplan as pp \
               left join customer as ct on ct.id = pp.cid \
               left join user as u on u.id = pp.uid \
               left join card as c on c.uid = pp.cid \
               left join paytype as pt on pt.id = pp.typeid " + where + ' order by id desc'
        re = self.getAll(sql)
        if re:
            return {'stat':True, 'data':re, 'sql':sql}
        else:
            return {'stat':False, 'msg':u'没有收费项目，请添加'}
    #添加缴费项目
    def addPayType(self,data):
        if self.queryPayTypes(data)['stat']:
            return {'stat':False, 'msg':u'该缴费项目已经存在！'}
        sql = 'insert into paytype(id, typename, stat, cdate) values(NULL, %s, %s, UNIX_TIMESTAMP())'
        temp = (data['typename'], data['stat'])
        re = self.insertOne(sql, temp)
        self.end()
        if re:
            return {'stat':True, 'msg':u'添加成功'}
        else:
            return {'stat':False, 'msg':u'添加失败'}
    #修改缴费项目
    def alterPayType(self,data):
        if self.queryPayTypes(data)['stat']:
            return {'stat':False, 'msg':u'该缴费项目已经存在！'}
        sql = 'update paytype set typename = %s, stat = %s where id = %s'
        temp = (data['typename'], data['stat'], data['id'])
        re = self.update(sql, temp)
        self.end()
        if re:
            return {'stat':True, 'msg':u'修改成功'}
        else:
            return {'stat':False, 'msg':u'修改失败'}
    # 删除缴费项目    
    def deletePayType(self, data):
        if self.getAll('select id from payplan where typeid = %s'%data['id']):
            return {'stat':False, 'msg':u'删除失败，系统有查询到缴纳该项费用的记录'}
        re = self.delete('delete from paytype where id = %s'%data['id'])
        self.end()
        if re:
            return {'stat':True, 'msg':u'删除成功'}
        else:
            return {'stat':False, 'msg':u'删除失败'}
        
    # 缴费付款
    def payNow(self, datas):
        okCount = 0
        failData = []
        for data in datas:
            data['zrid'] = 168
            data['zrcard'] = 1000000000
            sql = 'update payplan set payact = %s, paydate = UNIX_TIMESTAMP(), uid = %s, paytype = 0 where id = %s'
            temp = (data['method'], data['uid'], data['id'])
            payResult = self.update(sql, temp)
            if data['method'] == 2:
                zzResult = Card().transferUpdate(data)
                if zzResult['stat'] and payResult != 0:
                    self.end()
                    okCount += 1
                elif not zzResult['stat']:
                    return {'stat':False, 'msg':u'%s个费用缴纳失败(%s)'%(len(datas) - okCount,zzResult['msg'])}
            else:
                self.end()
                if payResult != 0:
                    okCount += 1
        if okCount == 0:
            return {'stat':False, 'msg':u'缴费失败'}
        else:
            return {'stat':True, 'msg':u'缴费成功'}
            
    # 生成待缴费单
    def addPayment(self, datas):
        okCount = 0
        failedPayments = []
        if len(datas['datas']) == 0:
            return {'stat':False, 'msg':u'没有可导入的数据'}
        for data in datas['datas']:
            
            if cmp(datas['method'], 'add') == 0:
                
                exists = self.getAll("select id from  payplan where cid = %s and typeid = %s and cdate = UNIX_TIMESTAMP(%s)", (data['id'], data['payType'], data['startDate']))
                if exists:
                    data['failReason'] = u'单据重复'
                    failedPayments.append(data)
                    return {'stat':False, 'msg':u'记录已存在', 'data':failedPayments}
                sql = 'insert into payplan(id, uid, cid, typeid, amount, txt, paytype, payact,ismessage, cdate, edate, paydate) \
                       values(NULL, NULL, %s, %s, %s, %s, NULL, NULL, 0, UNIX_TIMESTAMP(%s), UNIX_TIMESTAMP(%s), NULL)'
                       
                temp = (data['id'], data['payType'], data['payMoney'], data['txt'], data['startDate'], data['endDate'])
                re = self.insertOne(sql, temp)
            elif cmp(datas['method'], 'daoru') == 0:
                existsSql = 'select pl.id from  payplan as pl \
                                      left join paytype as pt on pl.typeid = pt.id\
                                      left join customer as ct on ct.id = pl.cid\
                                      where ct.membername = %s and pt.typename = %s and pl.cdate = UNIX_TIMESTAMP(%s)'
                existsTemp = (data['name'], data['payType'], data['startDate'])
                exists = self.getAll(existsSql, existsTemp)
                if exists:
                    data['failReason'] = u'单据重复'
                    failedPayments.append(data)
                    continue
                sql = 'insert into payplan(id, uid, cid, typeid, amount, txt, paytype, payact, ismessage, cdate, edate, paydate) \
                       values(NULL, NULL '
                # 根据姓名和金荣卡获取客户id
                sql1 = 'SELECT c.id FROM customer AS c \
                       LEFT JOIN customerinfo AS ci ON ci.cid = c.id \
                       LEFT JOIN card AS ca ON ca.uid = c.id \
                       WHERE c.membername = "' + str(data['name']) + '" AND ca.noid = "' + str('%.0f'%float(data['card'])) + '"'
                try:
                    memberId = self.getAll(sql1)
                    if len(memberId) == 1:
                        sql += ', ' + str(memberId[0]['id'])
                    else:
                        data['failReason'] = u'没有金荣卡号为%s、姓名为%s的客户!'%('%.0f'%float(data['card']), data['name'])
                        failedPayments.append(data)
                        continue
                except:
                    data['failReason'] = u'没有金荣卡号为%s、姓名为%s的客户!'%('%.0f'%float(data['card']), data['name'])
                    failedPayments.append(data)
                    continue
                # 根据缴费项目名称获取缴费项目id
                try:
                    payType = self.getAll('select id from paytype where typename = "' + str(data['payType']) + '"') 
                    if len(payType) == 1:
                        sql += ', ' + str(payType[0]['id'])
                    else:
                        data['failReason'] = u'不存在的缴费项目'%data['payType']
                        failedPayments.append(data)
                        continue
                except:
                    data['failReason'] = u'不存在的缴费项目'
                    failedPayments.append(data)
                    continue
                # 缴费金额
                try:
                    if float(data['payMoney']) <= 0:
                        data['failReason'] = u'缴费金额不能小于零！'
                        failedPayments.append(data)
                        continue
                    sql += ', ' + str(data['payMoney'])
                except:
                    data['failReason'] = u'缴费金额必须是大于零的实数！'
                    failedPayments.append(data)
                    continue
                #　备注
                try:
                    if data['txt'] != '':
                        sql += ', "' + str(data['txt']) + '"'
                    else:
                        sql += ', NULL'
                except:
                    sql += ', NULL'
                sql += ', NULL, NULL, 1, UNIX_TIMESTAMP("' + str(data['startDate']) + '")'
                # 最后缴费期限
                try:
                    sql += ', UNIX_TIMESTAMP("' + str(data['endDate']) + '")'
                except:
                    data['failReason'] = u'最后缴费期限格式不正确（yyyy/mm/dd）'
                    failedPayments.append(data)
                    continue
                sql += ', NULL+%s)'
                re = self.insertOne(sql, (" "))
            if re != 0:
                okCount += 1
            else:
                failedPayments.append(data)
        self.end()
        if okCount != len(datas['datas']):
            return {'stat':False, 'msg':u'%s条单据未添加成功，是否另存此次未添加成功的单据？'%len(failedPayments), 'data':failedPayments}
        else:
            return {'stat':True, 'msg':u'成功生成%s条待缴费单'%okCount}
            
    # 修改待缴费单
    def alterPayment(self, data):
        exists = self.getAll("select id from  payplan where cid = %s and typeid = %s and edate = UNIX_TIMESTAMP(%s) and id != %s", (data['cid'], data['payType'], data['endDate'], data['id']))
        if exists:
            data['failReason'] = u'单据重复'
            return {'stat':False, 'msg':u'记录已存在', 'data':exists}
        sql = 'update payplan set cid = %s, typeid = %s, amount = %s, txt = %s , cdate = UNIX_TIMESTAMP(%s), edate = UNIX_TIMESTAMP(%s) \
               where id = %s'
        temp = (data['cid'], data['payType'], data['payMoney'], data['txt'], data['startDate'], data['endDate'], data['id'])
        re = self.update(sql, temp)
        self.end()
        if re == 1:
            return {'stat':True, 'msg':u'修改成功'}
        else:
            return {'stat':False, 'msg':u'修改失败'}
    # 删除待缴费单
    def deletePayments(self, data):
        sql = 'delete from payplan where id in ' + str(tuple(data))
        if len(data) == 1:
            sql = sql.replace(',', '')
        re = self.delete(sql)
        self.end()
        if re != 0:
            ids = self.getAll('select id from payplan order by id desc')
            if ids:
                self.delete('alter table payplan AUTO_INCREMENT %s'%(ids[0]['id'] + 1))
            else:
                self.delete('truncate table payplan')
            return {'stat':True, 'msg':u'删除成功'}
        else:
            return {'stat':False, 'msg':u'删除失败'}
            