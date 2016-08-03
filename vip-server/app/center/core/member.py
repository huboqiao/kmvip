# --*-- coding:utf-8 --*--
'''
Created on 2014年6月13日

@author: ivan
用户类
'''
from __future__ import division
import time,sys
import MySQLdb as mdb
from card import Card
from lib.db import Mysql

reload(sys)
sys.setdefaultencoding( "utf-8" )

class Users(Mysql):
    def __init__(self):
        Mysql.__init__(self)
    
    
    def addUser(self,data):
        #插主表
        username = data['username']
        nickname = data['nickname']
        password = data['password']
        tel = data['tel']
        sex = data['sex']
        status = data['status']
        group = data['group']
        lasttime = data['lasttime']
        ctime = data['ctime']
        finger = data['finger']
        card = data['card']
        #判断用户名是否存在
        checkuser = self.queryName(username)
        if checkuser:
            return {'stat':-1,'msg':u'该员工名己经存在'}
        
        else:
            sql = '''INSERT INTO user (username, nickname,  \
            `password`, tel, sex, `status`, `group`, lasttime, ctime, finger)VALUES( \
            %s, %s, %s, %s, %s, %s, %s, %s, UNIX_TIMESTAMP(), %s )'''
            tmp = [username,nickname,password,tel,sex,status,group,lasttime,finger]
            try:
                ids = self.insertOne(sql,tmp)
            except:
                return {'stat':-1,'msg':u'添加员工失败，请重试'}
            
            if ids:
                try:
                    birthday = str(int(time.mktime(time.strptime(data['birthday'],'%Y-%m-%d'))))
                except:
                    birthday = str(int(time.mktime(time.strptime(data['birthday'],'%Y/%m/%d'))))
                hukou = data['hukou']
                adder = data['adder']
                useimg = data['useimg']
                cardimg = data['cardimg']
                cardimgt = data['cardimgt'] 
                
                sql = '''INSERT INTO userinfo (useid,card, \
                 birthday, hukou, adder, useimg_path,  cardimg_path,cardimgt_path)VALUES( \
                 %s,%s, %s, %s, %s, %s, %s, %s)'''
                tmp = [ids,card,birthday,hukou,adder,(useimg),(cardimg),(cardimgt)]
                try:
                    self.insertOne(sql , tmp)
                    self.end()
                    return {'stat':1,'msg':u'添加员工成功'}
                except:
                    return {'stat':-1,'msg':u'系统错误，请重试'}
                
    def userLastTime(self,uid):
        sql = 'update `user` set lasttime = UNIX_TIMESTAMP() where id = %s'
        tmp = [uid,]
        self.update(sql,tmp)
        self.end()
    
    def modifyUser(self,userdata,infodata):
        '''修改员工资料'''
        strs = ''
        userid = ''
        
        #更新用户主表
        for k,v in userdata.items():
            if k == 'userid':
                userid = v
                k = 'id'
            if v == '':
                strs = strs + '`'+k+'`'+'="",'
            else:
                strs = strs + '`'+k+'`'+'= "'+str(v)+'",'
        sql = 'UPDATE `user` SET %s where id ='+str(userid)
        self.update(sql % strs[:-1])
        strs = ''
        #更新用户详情表
        for k,v in infodata.items():
            if v == '':
                strs = strs + '`'+k+'`' + '="",'
            else:
                if k == 'useimg_path':
                    strs = strs + '`'+k+'`' + '= "'+(v)+'",'
                elif k == 'cardimg_path':
                    strs = strs + '`'+k+'`' + '= "'+(v)+'",'
                elif k == 'cardimgt_path':
                    strs = strs + '`'+k+'`' + '= "'+(v)+'",'
                else:
                    strs = strs + '`'+k+'`' + '= "'+str(v)+'",'
        sql = 'UPDATE userinfo SET %s where useid =' +str(userid)
        try:
            self.update(sql % strs[:-1])
            self.end()
            return {'stat':1,'msg':u'修改员工信息成功'}
        except:
            return {'stat':-1,'msg':u'修改员工信息失败'}
    
    def delUser(self,userId):
        '''删除用户主表'''
        try:
            sql = 'delete from `user` where id ='+str(userId)
            self._cursor.execute(sql)
            sql = 'delete from `userinfo` where useid ='+str(userId)
            self._cursor.execute(sql)
            self._conn.commit()
            return {'stat':1}
        except:
            return {'stat':-1,'msg':u'删除用户失败'}
    def queryUser(self,userId=''):
        sql = 'SELECT a1.id,a1.username,a1.nickname,a1.tel,a1.sex,a1.status,a1.`group` \
        ,a1.finger,a2.card,a2.birthday,a2.hukou,a2.adder,a2.useimg_path,a2.cardimg_path,a2.cardimgt_path,a3.group_name \
         FROM `user` AS a1 , userinfo AS a2,usergroup AS a3  WHERE a1.id =a2.useid AND a1.group = a3.id '
        try:
            re = self.getAll(sql)
            return {'stat':1,'data':re}
        except:
            return {'stat':-1,'msg':u'查询错误，请检查参数是否正确'}
    
    def queryUserAndAdmin(self,uid):
        '''查询指定用户权限及所有管理员权限'''
        sql1 = "SELECT a1.id,a1.username,a1.nickname,a1.`group`,a1.finger,a2.group_name,role_list FROM `user` AS a1,usergroup AS a2 WHERE a1.group = a2.id and a1.id = '"+uid+"'"
        sql2 = "SELECT a1.id,a1.username,a1.nickname,a1.`group`,a1.finger,a2.group_name,role_list FROM `user` AS a1  JOIN usergroup AS a2 ON a1.group = a2.id  AND (`group` = 1 OR `group` = 2)"   
        try:
            re = self.getOne(sql1)
            re2 = self.getAll(sql2)
            return {'user':re,'admin':re2}
        except:
            return False
    
    def queryName(self,name):
        sql = 'select * from user where username ="'+str(name)+'"'
        
        if self.getOne(sql):
            return True
        else:
            return False
        
'''
客户操作类
'''
class Member(Mysql):
    def __init__(self):
        Mysql.__init__(self)
        
    def queryMembername(self, name):
        sql = 'select membername from customer where membername like "%' + str(name) + '%"'
        re = self.getAll(sql)
        if re:
            return {'stat':True, 'data':re}
        else:
            return {'stat':False}
    def balanceAfterChanges(self):
        cz = self.getAll('select * from cardcz order by cdate')
        for c in cz:
            b = self.balance(c['cardid'], c['cdate'])
            self.update('update cardcz set balance = %s where id = %s', (b, c['id']))
            self.end()
        cz = self.getAll('select * from cardtx order by cdate')
        for c in cz:
            b = self.balance(c['cardid'], c['cdate'])
            self.update('update cardtx set balance = %s where id = %s', (b, c['id']))
            self.end()
        cz = self.getAll('select * from cardzz order by cdate')
        for c in cz:
            b = self.balance(c['paycard'], c['cdate'])
            p = self.balance(c['incomecard'], c['cdate'])
            self.update('update cardzz set paybalance = %s, payeebalance = %s where id = %s', (b, p, c['id']))
            self.end()
    
    def balance(self, noid, dt):
        balance = 0
        uid = self.getOne('select uid from card where noid = %s', noid)['uid']
        cards = self.getAll('select noid from card where uid = %s', (uid))
        for card in cards:
            temp = (card['noid'], dt)
            balance += float('%0.2f'%self.getOne('select ifnull(sum(amount), 0) as a from cardcz where cardid = %s and cdate <= %s', temp)['a'])
            balance -= float('%0.2f'%self.getOne('select ifnull(sum(amount), 0) as a from cardtx where cardid = %s and cdate <= %s', temp)['a'])
            balance += float('%0.2f'%self.getOne('select ifnull(sum(amount), 0) as a from cardzz where incomecard = %s and cdate <= %s', temp)['a'])
            balance -= float('%0.2f'%self.getOne('select ifnull(sum(amount), 0) as a from cardzz where paycard = %s and cdate <= %s', temp)['a'])
        return balance
     
    
    # 解冻超过3天的客户余额
    def unfreezeAmount(self):
        s = int(time.time())
        sql = 'select id, amount, freezen from customer where (%s - actdate) >= 259200 and (freezen != 0 or stat = 2)'
        re = self.getAll(sql%s)
        if re:
            for i in re:
                sql = 'update customer set amount = %s, stat = 1, freezen = 0 where id = %s'
                self.update(sql, (i['amount'] + i['freezen'], i['id']))
                self.end()
        
    # 查询客户类型, 可筛选状态、id
    def queryMemberGroup(self, condition=None):
        where = ' where 1 = 1 '
        try:
            if condition.has_key('statu'):
                statu = int(condition['statu'])
                if statu == 1 or statu == 0:
                    where += ' isactive = %s '%statu
        except:
            pass
        
        try:
            if condition.has_key('id'):
                try:
                    where = ' id = %s '%int(id)
                except:
                    pass
        except:
            pass
        sql = 'select * from customergroup ' + where
        
        re = self.getAll(sql)
        if re:
            return {'stat': True, 'data': re}
        else:
            return {'stat': False, 'msg': u'没有符合条件的用户组！'}
        
    #注销会员
    def offMember(self,data):
        #先将会员下面的卡状态变为2,并且添加actdate，操作时间，该时间为当前操作时间，预计三天后才能进行该记录操作
        #try:
        sql = 'update card set `stat` = 2 where uid = '+str(data['cid'])
        self._cursor.execute(sql)
        
        
        sql = 'insert into statu_changes(id, cid, uid, type, noid, cdate) values(NULL, %s, %s, 3, %s, UNIX_TIMESTAMP())'
        temp = (data['cid'], data['uid'], data['noid'])
        self.insertOne(sql, temp)
        #更改客户状态为注销
        sql = ' update customer set `stat` =3,actdate = UNIX_TIMESTAMP() where id ='+str(data['cid'])
        self._cursor.execute(sql)
        self._conn.commit()
        return True
        #except:
            #return False
    
    #查询挂失和注销用户信息
    def serviceQuery(self,data):
        if data['type'] == 4:
            wheres = ' where 1 = 1 '
        else:
            wheres = ' where s.type = ' + str(data['type']) + ' '
        try:
            wheres += ' and cu.membername like "%'+str(data['name']) + '%" '
        except:
            pass 
        try:
            wheres += ' and cu.idcard like "%'+str(data['idcard']) + '%" '
        except:
            pass
        try:
            wheres += ' and s.noid like "%' + str(data['noid']) + '%"'
        except:
            pass
        try:
            wheres += ' and (u.username like "%' + str(data['orderName']) + '%" or u.nickname like "%' + str(data['orderName']) + '%") '
        except:
            pass
        wheres += ' order by s.id desc '
        sql = '''select u.username, s.id, cu.membername, cu.idcard, cu.tel, cu.amount, s.noid, s.type, FROM_UNIXTIME(s.cdate, '%Y/%m/%d') as cdate
                 from statu_changes as s
                 left join customer as cu on s.cid = cu.id
                 left join `user` as u on s.uid = u.id ''' + wheres
        re = self.getAll(sql)
        if re:
            return {'stat':True, 'data':re}
        else:
            return {'stat':False, 'msg':u'没有记录'}
    
    #注销后退款，三天后的操作
    def memberClear(self,uid,ctype,txt):
        '''
                  退款：清空用户余额，返回状态以及退款的金额
        '''
        try:
            userAmount = self.queryAmount(uid)
            sql = ' update `customer` set `amount` = 0 where id ='+str(uid)
            self._cursor.execute(sql)
            sql = "insert into cardtx(cardid,amount,cdate,ctype,txt)values('"+str(userAmount['cardid'])+"','"+str(userAmount['amount'])+"',UNIX_TIMESTAMP(),"+str(ctype)+",'"+txt+"')"
            self._cursor.execute(sql)
            self._conn.commit()
            data = {'stat':True,'amount':userAmount['amount']}
        except:
            data = {'stat':False,'amount':0}
        return data
    
    def queryAmount(self, uid):
        #查询有效会员用户的余额
        sql = 'SELECT a1.amount,a2.cardid FROM customer AS a1,card AS a2 WHERE a1.id = a2.uid AND a2.stat = 1 AND a2.uid = '+str(uid)
        return self.getOne(sql)
    
    # 添加客户
    def addMember(self, data):
        basic = data['data']
        other = data['dataInfo']
        if self.checkIdCard(basic['idCard']):
            return {'stat': False, 'msg':u'添加客户失败, 该身份证已经被占用'}
        if basic['storeType'] != '':
            sql = 'insert into customer(id, membername, sex, nation, tel, idcard, carddate, adduser, amount, adder, \
                   stat, cdate, ugroup, lasttime, actdate, freezen, storagenumber, typeid) values(NULL, %s, %s, %s, \
                   %s, %s, %s, %s, 0, %s, 1, %s, %s, NULL, NULL, 0, %s, %s)'
            param = (basic['name'], basic['sex'], basic['nation'], basic['mobile'],
                    basic['idCard'], basic['cardDate'], data['addUser'], basic['address'],
                    int(time.time()), basic['memberGroup'],basic['storeNumber'], basic['storeType'])
        else:
            sql = 'insert into customer(id, membername, sex, nation, tel, idcard, carddate, adduser, amount, adder, \
                   stat, cdate, ugroup, lasttime, actdate, freezen, storagenumber, typeid) values(NULL, %s, %s, %s, \
                   %s, %s, %s, %s, 0, %s, 1, %s, %s, NULL, NULL, 0, NULL, NULL)'
            param = (basic['name'], basic['sex'], basic['nation'], basic['mobile'],
                    basic['idCard'], basic['cardDate'], data['addUser'], basic['address'],
                    int(time.time()), basic['memberGroup'])
        try:
            self.insertOne(sql, param)
            memberId = self.getOne('select id from customer where idcard = "%s" order by id desc'%basic['idCard'])['id']
        except:
            return {'stat': False, 'msg':u'添加客户失败', 'data':sql%param}
        
        sql1 = 'insert into customerinfo values(NULL, %s, %s, %s, "-", \
                                              %s, %s, %s, %s, %s, \
                                              %s, %s, %s, %s, %s, \
                                              %s)'
        param1 = (memberId, other['bankAccount'], other['bankName'], 
                 other['accountOwner'], other['head'], other['front'], other['back'],
                 other['finger1'], other['finger2'], other['finger3'], other['relative'],
                 other['relativeSex'], other['relationShip'], other['relationMobile'])
        try:
            self.insertOne(sql1, param1)
            self.end()
            return {'stat': True, 'msg':u'添加客户成功', 'data': memberId}
        except:
            return {'stat': False, 'msg':u'添加客户失败', 'data': [sql%param, sql1%param1]}
    # 修改客户资料
    def alterMember(self, data):
        basic = data['data']
        other = data['dataInfo']
        cardIdExsist = self.checkIdCard(basic['idCard'])
        if cardIdExsist:
            for customer in cardIdExsist:
                if customer['id'] != basic['id']:
                    return {'stat': False, 'msg':u'修改客户失败，该身份证已经被占用'}
        if basic.has_key('storeType'):
            sql = 'update customer set membername = %s, sex = %s, nation = %s, tel = %s, idcard = %s, \
                   carddate = %s, adder = %s, storagenumber = %s, typeid = %s, ugroup = %s where id = "%s"'
            param = (basic['name'], basic['sex'], basic['nation'], basic['mobile'],
                    basic['idCard'], basic['cardDate'], basic['address'],
                    basic['storeNumber'], basic['storeType'], basic['memberGroup'], basic['id'])
        else:
            sql = 'update customer set membername = %s, sex = %s, nation = %s, tel = %s, idcard = %s, \
                   carddate = %s, adder = %s, ugroup = %s where id = "%s"'
            param = (basic['name'], basic['sex'], basic['nation'], basic['mobile'],
                    basic['idCard'], basic['cardDate'], basic['address'], basic['memberGroup'], basic['id'])
        
        sql1 = 'update customerinfo set bankcard = %s, bankname = %s, bankusername = %s, \
                useimg_path = %s, cardimg_path = %s, cardimgt_path = %s, relativesname = %s, \
                relativessex = %s, relationship = %s, relationtem = %s, finger1 = %s, finger2 = %s, finger3 = %s \
                where cid = "%s"'
        if other['finger1'] == 'null':
            other['finger1'] = ''
        if other['finger2'] == 'null':
            other['finger2'] = ''
        if other['finger3'] == 'null':
            other['finger3'] = ''
        param1 = (other['bankAccount'], other['bankName'],other['accountOwner'], 
                  other['head'],other['front'], other['back'], other['relative'],
                  other['relativeSex'], other['relationShip'], other['relationMobile'], other['finger1'],
                  other['finger2'], other['finger3'], basic['id'])
        try:
            self.update(sql, param)
            self.update(sql1, param1)
            self.end()
            return {'stat': True, 'msg':u'修改客户资料成功'}
        except:
            return {'stat': False, 'msg':u'修改客户资料失败', 'data': [sql%param, sql1%param1]}
    # 根据用户名称， 电话号码， 身份证号模糊查询客户信息    
    def getMemberInfos(self, data):
        where = ' where 1 = 1 '
        if data.has_key('stat'):
            where += ' and ca.stat = "' + str(data['stat']) + '" '
        if data.has_key('idCard'):
            if data['idCard'] != '':
                where += ' and c.idcard LIKE "%' + str(data['idCard']) + '%" ' 
        if data.has_key('tel'):
            if data['tel'] != '':
                where += ' and c.tel like "%' + str(data['tel']) + '%" '
        if data.has_key('name'):
            if data['name'] != '':
                where += ' and c.membername like "%' + str(data['name']) + '%" '
        if data.has_key('card'):
            if data['card'] != '':
                where += ' and ca.noid like "%' + str(data['card']) + '%" '
        if data.has_key('storage'):
            if data['storage'] != '':
                where += ' and s.name like "%' + str(data['storage']) + '%" '
        if data.has_key('storageRegion'):
            if data['storageRegion'] != '':
                where += ' and q.name like "%' + str(data['storageRegion']) + '%" '
        if data.has_key('storageNumber'):
            if data['storageNumber'] != '':
                where += ' and h.name like "%' + str(data['storageNumber']) + '%" '
        if data.has_key('storageType'):
            if data['storageType'] != '':
                where += ' and t.name like "%' + str(data['storageType']) + '%" '
        sql = '''SELECT c.*, ci.bankcard, ci.bankname, ci.bankusername, ci.useimg_path, ci.cardimg_path, ci.bankadder,ug.isstorage, 
               ci.cardimgt_path, ci.relativesname, ci.relativessex, ci.relationship, ci.relationtem, u.nickname, ug.name as groupName,
               ci.finger1, ci.finger2, ci.finger3, q.id AS region, s.id AS store, concat_ws("：", s.name, q.name, h.name) as storename
               FROM customer AS c
               left join customergroup as ug on c.ugroup = ug.id
               LEFT JOIN card as ca ON ca.uid = c.id
               LEFT JOIN customerinfo AS ci ON c.id = ci.cid 
               LEFT JOIN storage_hs AS h ON c.storagenumber = h.id 
               LEFT JOIN storage_qy AS q ON h.qid = q.id
               LEFT JOIN `storage` AS s ON  q.sid = s.id 
               LEFT JOIN storagetype as t ON t.id = c.typeid
               LEFT JOIN user as u on c.adduser = u.id''' + where
        re = self.getAll(sql)
        if re:
            return {'stat':True, 'data':re}
        else:
            return {'stat':False, 'msg':u'该身份证未注册'}
    # 根据用户名称， 电话号码， 身份证号模糊查询客户信息    
    def getMemberInfoss(self, data):
        where = ' where 1 = 1 '
        if data.has_key('idCard'):
            if data['idCard'] != '':
                where += ' and c.idcard like "%' + str(data['idCard']) + '%" ' 
        if data.has_key('tel'):
            if data['tel'] != '':
                where += ' and c.tel like "%' + str(data['tel']) + '%" '
        if data.has_key('name'):
            if data['name'] != '':
                where += ' and c.membername like "%' + str(data['name']) + '%" '
        if data.has_key('storage'):
            if data['storage'] != '':
                where += ' and s.name like "%' + str(data['storage']) + '%" '
        if data.has_key('storageRegion'):
            if data['storageRegion'] != '':
                where += ' and q.name like "%' + str(data['storageRegion']) + '%" '
        if data.has_key('storageNumber'):
            if data['storageNumber'] != '':
                where += ' and h.name like "%' + str(data['storageNumber']) + '%" '
        if data.has_key('storageType'):
            if data['storageType'] != '':
                where += ' and t.name like "%' + str(data['storageType']) + '%" '
        sql = '''SELECT c.*, ci.bankcard, ci.bankname, ci.bankusername, ci.useimg_path, ci.cardimg_path, ci.bankadder,ug.isstorage,
               ci.cardimgt_path, ci.relativesname, ci.relativessex, ci.relationship, ci.relationtem, u.nickname, ug.name as groupName,
               ci.finger1, ci.finger2, ci.finger3, q.id AS region, s.id AS store, concat_ws("：", s.name, q.name, h.name) as storename
               FROM customer AS c
               left join customergroup as ug on c.ugroup = ug.id
               LEFT JOIN customerinfo AS ci ON c.id = ci.cid 
               LEFT JOIN storage_hs AS h ON c.storagenumber = h.id 
               LEFT JOIN storage_qy AS q ON h.qid = q.id
               LEFT JOIN `storage` AS s ON  q.sid = s.id 
               LEFT JOIN storagetype as t ON t.id = c.typeid
               LEFT JOIN user as u on c.adduser = u.id''' + where
        re = self.getAll(sql)
        result = []
        if re:
            re = list(re)
            for member in re:
                card = self.getOne('select noid, password from card where stat = 1 and uid = "' + str(member['id']) + '"')
                try:
                    member['card'] = card['noid']
                    member['password'] = card['password']
                except:
                    member['card'] = u'无可用金荣卡'
                try:
                    if str(data['card']).strip() != '':
                        if str(member['card']).find(str(data['card'])) != -1:
                            result.append(member)
                    else:
                        result.append(member)
                except:
                    result.append(member)
            return {'stat':True, 'data':result}
        else:
            return {'stat':False, 'msg':u'该身份证未注册'}
        
    def getMemberBaseInfo(self, data):
        sql = 'SELECT ct.id, ct.membername, ct.idcard, ct.tel, c.noid, CONCAT_WS("：", s.name, q.name, h.name) AS storename FROM customer AS ct\
                LEFT JOIN storage_hs h ON h.id = ct.storagenumber\
                LEFT JOIN storage_qy AS q ON h.qid = q.id\
                LEFT JOIN `storage` AS s ON s.id = q.sid\
                LEFT JOIN customerinfo AS ci ON ci.cid = ct.id\
                LEFT JOIN card AS c ON c.uid = ct.id'
        try:
            sql += ' where c.stat like"%' + str(data['stat']) + '%" '
        except:
            sql += ' where c.stat = 1 '
        try:
            if data['name'] != '':
                sql += ' and ct.membername like "%' + str(data['name']) + '%" '
        except:
            pass
        try:
            if data['card'] != '':
                sql += ' and c.noid like "%' + str(data['card']) + '%" '
        except:
            pass
        try:
            if data['idCard'] != '':
                sql += ' and ct.idcard like "%' + str(data['idCard']) + '%" '
        except:
            pass
        re = self.getAll(sql)
        if re:
            return {'stat':True, 'data':re}
        else:
            return {'stat':False, 'msg':u'没有符合条件的客户'}
        
    def checkIdCard(self,idcard):
        sql='select * from customer where idcard = "'+ idcard + '"'
        return self.getAll(sql)
                

    def modifyMember(self,userdata,infodata):
        '''修改客户资料'''
        strs = ''
        userid = ''
        try:
            userdata['carddate'] = str(int(time.mktime(time.strptime(userdata['carddate'],'%Y-%m-%d'))))
        except:
            userdata['carddate'] = str(int(time.mktime(time.strptime(userdata['carddate'],'%Y/%m/%d'))))
        
        #更新客户主表
        for k,v in userdata.items():
            if k == 'id':
                userid = v
            if v == '':
                strs = strs + '`'+k+'`'+'="",'
            else:
                strs = strs + '`'+k+'`'+'= "'+str(v)+'",'
        sql = 'UPDATE `customer` SET %s where id ='+str(userid)
        self._cursor.execute(sql % strs[:-1])
        strs = ''
        #更新客户详情表
        for k,v in infodata.items():
            if v == '':
                strs = strs + '`'+k+'`' + '="",'
            else:
                #修改： 唐
                if k == 'useimg_path':
                    strs = strs + '`'+k+'`' + '= "'+mdb.escape_string(v)+'",'
                elif k == 'cardimg_path':
                    strs = strs + '`'+k+'`' + '= "'+mdb.escape_string(v)+'",'
                elif k ==  'cardimgt_path':
                    strs = strs + '`'+k+'`' + '= "'+mdb.escape_string(v)+'",'
                #修改结束： 唐
                else:
                    strs = strs + '`'+k+'`' + '= "'+str(v)+'",'
        sql = 'UPDATE customerinfo SET %s where cid =' +str(userid)
        try:
            self._cursor.execute(sql % strs[:-1])
            self._conn.commit()
            return True
        except:
            return False
                
    #用户挂失
    def lossUser(self,data):
        try:
            #更新卡的状态
            sql = 'update card set `stat` = 4 where noid = "'+str(data['noid'])+'"'
            self._cursor.execute(sql)
            
            #更新用户状态
            sql = 'update customer set `stat` = 2,actdate=UNIX_TIMESTAMP() where id='+str(data['cid'])
            self._cursor.execute(sql)
            
            
            sql = 'insert into statu_changes(id, cid, uid, type, noid, cdate) values(NULL, %s, %s, 1, %s, UNIX_TIMESTAMP())'
            temp = (data['cid'], data['uid'], data['noid'])
            self.insertOne(sql, temp)
            
            self._conn.commit()
            return {'stat':1,'msg':'挂失卡('+str(data['noid'])+u')成功'}
        except:
            return {'stat':-1,'msg':'挂失卡('+str(data['noid'])+u')失败'}
        
    def queryIDcard(self,idcard):
        '''根据身份证去查询是否存在会员'''
        sql = 'select * from customer where idcard ="'+idcard+'"'
        return self.getOne(sql)
    
    def queryAllMember(self,data):
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
        
    
    def queryMember(self,data,ext='',act=''):
        '''根据条件查询客户表'''
        #ext为空时，不判断卡片状态
        where = ' '      
        if type(data) == type({}):
            membername = data['membername']     #客户中
            cardid = data['cardid']     #卡号
            tel = data['tel']           #电话
            idcard = data['idcard']     #身份证
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
            sql = "SELECT a1.id AS uid,a1.amount AS amounts,a1.stat AS userstat,a1.actdate AS actdate,a1.*,a2.*,a3.*,a4.nickname \
                    FROM customer AS a1  \
                    LEFT JOIN customerinfo AS a2 ON a1.id = a2.cid \
                    LEFT JOIN card AS a3 ON a1.id = a3.uid \
                    LEFT JOIN `user` AS a4 ON a1.adduser = a4.id where ("+where+") \
                    GROUP BY a1.id "
            return self.getAll(sql)
        else:
            
            idcard = data   #身份证
            if idcard == "":
                where += ' 1 = 1'
            else:
                where += ' a1.idcard = "'+idcard+'"'
            if act == 'changecard':
                sql = "SELECT a1.id AS uid,a1.amount AS amounts,a1.stat AS userstat,a1.actdate AS actdate,a1.*,a2.*,a4.nickname \
                FROM customer AS a1,customerinfo AS a2 ,`user` AS \
                a4 WHERE a1.id = a2.cid  AND a1.adduser =a4.id and ("+where+") \
                GROUP BY a1.id "
            else:
                sql = "SELECT a1.id AS uid,a1.amount AS amounts,a1.stat AS userstat,a1.actdate AS actdate,a1.*,a2.*,a3.*,a4.nickname \
                FROM customer AS a1,customerinfo AS a2 ,card AS a3,`user` AS \
                a4 WHERE a1.id = a2.cid AND a1.id = a3.uid  AND a1.adduser =a4.id and ( a1.stat = 1 and  a3.stat = 1 and "+where+") \
                    GROUP BY a1.id "
            return self.getOne(sql)
        

    def querySuplliers(self, data):
        '''
        2014.10.11    
        huaan
                    获取所有供应商（商户）名称、状态、仓库名称、区域、仓位
        '''
        wheres = ''
        if data['supplierID'] != '':
#            wheres += ' and c.id = ' + '%s',data['supplierID']
            wheres += ' and c.id like "%'+data['supplierID']+'%"'
        if data['supplierName'] != '':
#            wheres += ' and c.username = ' + '%s',data['supplierName']  
            wheres += ' and c.membername like "%'+data['supplierName']+'%"'      
        if data['storeName'] != '':
#            wheres += ' and s.name = ' + '%s',data['storeName']
            wheres += ' and s.name like "%'+data['storeName']+'%"'
        if data['storeRegiona'] != '':
#            wheres += ' and ci.regiona = ' + '%s',data['storeRegiona'] 
            wheres += ' and ci.regiona like "%'+data['storeRegiona']+'%"'       
        sql = "select c.membername, c.stat, ci.store, ci.regiona, s.name, c.id \
                from customer as c, customerinfo as ci, storage as s \
                where ci.storename = s.id and c.id = ci.cid and ci.storename != 0 " + wheres
#        return sql
        return self.getAll(sql)
    
     

        
class UserGroup(Mysql):
    def __init__(self):
        Mysql.__init__(self)
    
    def addGroup(self,name,role_list,txt=''):
        groupname = self.qeuryGroup(name)
        if groupname:
            return {'stat':False,'msg':u'用户组名存在，请换个组名'}
        sql = 'insert into usergroup (group_name,role_list,role_describe) values(%s,%s,%s)'
        tmp = [name,role_list,txt]
        try:
            self.insertOne(sql,tmp)
            self.end()
            return {'stat':1,'msg':'添加用户组成功'}
        except:
            return {'stat':-1,'msg':'系统错误，请稍后重试'}
        
    
    def delGroup(self,groupID):
        sql = 'select * from `user` where `group` = '+str(groupID)
        
        if self.getAll(sql):
            return {'stat':-1,'msg':'该用户组下有用户，无法删除'}
        sql = 'delete from usergroup where id ='+str(groupID)
        self.delete(sql)
        self.end()
        return {'stat':1,'msg':'删除用户组成功！'}
    
    def modifyGroup(self,data):
        '''
            @data    封装数据 id role_list
        '''
        strs = ''
        for k,v in data.items():
                strs += '`'+k+'`'+'= "'+str(v)+'",'
        sql = 'UPDATE `usergroup` SET %s where id ='+str(data['id'])
        re = self.update(sql % strs[:-1])
        self.end()
        return re
    
    def qeuryGroup(self,name=''):
        '''获取所有用户组'''
        if name == '':
            sql = "select * from usergroup "
            return self.getAll(sql)
        else:
            sql = "select * from usergroup where group_name ='"+name+"'"
            return self.getOne(sql)

    def queryGroup_info(self,groupid):
        sql = "select * from usergroup where id ="+str(groupid)
        return self.getOne(sql)
    
    def queryResource(self):
        '''获取所有权限资源'''
        sql = 'select * from resource'
        return self.getAll(sql)
    
   