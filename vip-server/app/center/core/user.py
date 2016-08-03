# --*-- coding:utf-8 --*--
'''
Created on 2014年6月13日

@author: ivan
用户类
'''
import time,sys,json,hashlib
import MySQLdb as mdb
from card import Card
from lib.db import Mysql
sysConfig = json.load(open('config.json', 'r'))
authenticationKey = sysConfig.get("other")
authenticationKey = authenticationKey['authenticationKey']                #载入随机串

reload(sys)
sys.setdefaultencoding( "utf-8" )

class Users(Mysql):
    def __init__(self):
        Mysql.__init__(self)
    
    def alterMyPassword(self, data):
        pwd = hashlib.md5()
        pwd.update(data['newPwd'])
        newPwd = str(pwd.hexdigest())
        re = self.update('update user set password = %s where id = %s', (newPwd, data['id']))
        self.end()
        if re == 1:
            return {'stat': True, 'msg': u'密码修改成功！', 'password':newPwd}
        else:
            return {'stat': False, 'msg': u'密码修改失败！'}

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
            return {'stat':-1,'msg':'该员工名己经存在'}
        
        else:
            sql = '''INSERT INTO user (username, nickname,  \
            `password`, tel, sex, `status`, `group`, lasttime, ctime, finger, righter)VALUES( \
            %s, %s, %s, %s, %s, %s, %s, %s, UNIX_TIMESTAMP(), %s, %s )'''
            tmp = [username,nickname,password,tel,sex,status,group,lasttime,finger, data['righter']]
            try:
                ids = self.insertOne(sql,tmp)
            except:
                return {'stat':-1,'msg':'添加员工失败，请重试'}
            
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
                    return {'stat':1,'msg':'添加员工成功'}
                except:
                    return {'stat':-1,'msg':'系统错误，请重试'}
                
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
            return {'stat':1,'msg':'修改员工信息成功'}
        except:
            return {'stat':-1,'msg':'修改员工信息失败'}
    
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
            return {'stat':-1,'msg':'删除用户失败'}
        
    def queryUser(self,userId=''):
        sql = 'SELECT a1.righter, a1.id,a1.username,a1.nickname,a1.tel,a1.sex,a1.status,a1.`group` \
        ,a1.finger,a2.card,a2.birthday,a2.hukou,a2.adder,a2.useimg_path,a2.cardimg_path,a2.cardimgt_path,a3.group_name \
         FROM `user` AS a1 , userinfo AS a2,usergroup AS a3  WHERE a1.id =a2.useid AND a1.group = a3.id '
        try:
            re = self.getAll(sql)
            return {'stat':1,'data':re}
        except:
            return {'stat':-1,'msg':'查询错误，请检查参数是否正确'}
    
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
        
    def getGrantsFinger(self, groupId):
        if groupId != '':
            sql = 'select finger from `user` where `group` = %s'%groupId
        else:
            sql = 'select finger from `user`'
        re = self.getAll(sql)
        if re:
            return {'stat':True, 'data':re}
        else:
            return {'stat':False, 'msg':u'未找到用户指纹！'}
        
    def getRightersFingers(self):
        sql = 'select id, finger from `user` where `righter` = 1'
        re = self.getAll(sql)
        if re:
            return {'stat':True, 'data':re}
        else:
            return {'stat':False, 'msg':u'未找到用户指纹！'}
        
    def getInfosByFinger(self, finger):
        sql = 'select * from `user` where finger = "' + str(finger) + '"'
        returnUserData = self.getOne(sql)
        #否则返回用户信息 , [0]id, [1]user_name, [2]password
        userkeyStr = str(returnUserData['id'])+returnUserData['username']+authenticationKey
        userkeyStr = hashlib.md5(userkeyStr).hexdigest().upper()
        #查询用户组名
        group = self.getOne('select * from usergroup where id = '+str(returnUserData['group']))
        returnStr = '{"status":1,"userkey":"'+str(userkeyStr)+'","user_id":'+str(returnUserData['id'])+',"user_name":"'+str(returnUserData['username'])+'","nice_name":"'+str(returnUserData['nickname'])+'","group":"'+str(group['group_name'])+'","group_id":"'+str(group['id'])+'","password":"' + str(returnUserData['password']) + '"}'
        return returnStr
        
'''
客户操作类
'''
class Merchant(Mysql):
    def __init__(self):
        Mysql.__init__(self)
    
    #注销会员
    def offMerchant(self,uid,ctype,txt):
        #先将会员下面的卡状态变为2,并且添加actdate，操作时间，该时间为当前操作时间，预计三天后才能进行该记录操作
        #try:
        sql = 'update card set `stat` = 2 where uid = '+str(uid)
        self._cursor.execute(sql)
        
        #更改卡片状态为注销
        sql = ' update customer set `stat` =2,actdate = UNIX_TIMESTAMP() where id ='+str(uid)
        self._cursor.execute(sql)
        self._conn.commit()
        return True
        #except:
            #return False
    
    #查询挂失和注销用户信息
    def serviceQuery(self,name='',idcard=''):
        wheres = ''
        if name == '':
            wheres += ' 1=1 '
        else:
            '''修改：唐'''
 #           wheres += ' `membername` ="%'+name+'%"'
            wheres += ' `membername` like "%'+name+'%"'
            
        if idcard == '':
            wheres += ' and 1=1 '
        else:
            wheres += ' and idcard like "%'+str(idcard)+'%"'
            
        sql = "select * from customer where %s and (`stat` = 2 or `stat` = 3)"
        return self.getAll(sql % wheres)
    
    #注销后退款，三天后的操作
    def merchantClear(self,uid,ctype,txt):
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
    
    def queryAmount(self,uid):
        #查询有效会员用户的余额
        sql = 'SELECT a1.amount,a2.cardid FROM customer AS a1,card AS a2 WHERE a1.id = a2.uid AND a2.stat = 1 AND a2.uid = '+str(uid)
        return self.getOne(sql)
    def addMerchant(self,data,datainfo,user):
        '''添加新的会员'''
        membername = data['membername']
        sex = data['sex']
        nation = data['nation']
        tel = data['tel']
        idcard = str(data['idcard'])
        try:
            carddate = str(int(time.mktime(time.strptime(data['carddate'],'%Y-%m-%d'))))
        except:
            carddate = str(int(time.mktime(time.strptime(data['carddate'],'%Y/%m/%d'))))
            
        
        adduser = user
        adder = data['adder']
        cdate = str(int(time.time()))
        ugroup = data['ugroup']
        
        if self.queryIDcard(idcard):
            return {'stat':-1,'msg':'开卡失败，该身份己存在！'}
        else:
            #添加主表信息
            sql = '''INSERT INTO customer (membername, sex,  \
            `nation`, tel, idcard, `carddate`, `adduser`, adder, cdate,ugroup)VALUES( \
            %s, %s, %s, %s, %s, %s, %s, %s,UNIX_TIMESTAMP() ,%s)'''
            tmp = [membername,sex,nation,tel,idcard,carddate,adduser,adder,ugroup]
            try:
                ids = self.insertOne(sql,tmp)
            except:
                return {'stat':-1,'msg':'开卡失败，请重试'}
            
            if ids:
                #插客户扩展表
                bankcard = datainfo['bankcard']
                bankname = datainfo['bankname']
                bankadder = datainfo['bankadder']
                bankusername = datainfo['bankusername']
                relativesname = datainfo['relativesname']
                relativessex = datainfo['relativessex']
                relationship = datainfo['relationship']
                relationtem = datainfo['relationtem']
                useimg = datainfo['useimg']
                cardimg = datainfo['cardimg']
                cardimgt = datainfo['cardimgt']
                store = datainfo['store']
                storename = datainfo['storename']
                regiona = datainfo['regiona']
                
                sql = '''INSERT INTO customerinfo (cid,bankcard, \
                 bankname, bankadder, bankusername, relativesname,  relativessex,relationship,relationtem,useimg_path,cardimg_path,cardimgt_path,store,storename,regiona)VALUES( \
                 %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s)'''
                tmp = [ids,bankcard,bankname,bankadder,bankusername,relativesname,relativessex,relationship,relationtem,(useimg),(cardimg),(cardimgt),store,storename,regiona]
                try:
                    self.insertOne(sql , tmp)
                    self.end()
                    return {'stat':1,'id':ids}
                except:
                    return {'stat':-1,'msg':'开卡失败，请重试'}
    def checkIdCard(self,idcard):
        sql='select * from customer where idcard="'+str(idcard)+'"'
        return self.getAll(sql)
                

    def modifyMerchant(self,userdata,infodata):
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
    def lossUser(self,cardid):
        try:
        #更新卡片及用户状态
            cardmodel = Card()
            noid = cardmodel.getNoId(cardid)
            sql = 'update card set `stat` = 4 where noid = "'+str(noid['noid'])+'"'
            self._cursor.execute(sql)
            #更新用户状态及操作时间 
            carddata = cardmodel.queryCard(noid['noid'])
            uid = carddata['uid']
            sql = 'update customer set `stat` = 2,actdate=UNIX_TIMESTAMP() where id='+str(uid)
            self._cursor.execute(sql)
            self._conn.commit()
            return True
        except:
            return False
        
        
        
        
    def queryIDcard(self,idcard):
        '''根据身份证去查询是否存在会员'''
        sql = 'select * from customer where idcard ="'+idcard+'"'
        return self.getOne(sql)
    
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
        
    
    def queryMerchant(self,data,ext='',act=''):
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
        
    
    #查询供应商
    def querySuppliers(self, data):
     
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
        return self.getAll(sql)
    
    
    #查询供应商2
    def findSuppliers(self,data):
        #获取表单数据
        supplierID = data['supplierID']
        supplierName = data['supplierName']
        storageName = data['storageName']
        storageQuyu = data['storageQuyu']
        
        #查询条件的拼凑
        if supplierID=='':
            cid = '%%' 
        else:
            cid = '%'+supplierID+'%'
            
        if supplierName=='':
            cmembername = '%%'
        else:
            cmembername = '%'+supplierName+'%'
            
        if storageName=='':
            sname = '%%'
        else:
            sname = '%'+storageName+'%'
            
        if storageQuyu=='':
            qname = '%%'
        else:
            qname = '%'+storageQuyu+'%'
            
        sql='SELECT c.id,c.membername,s.name,q.name,h.name,c.stat FROM customer AS c, `storage` AS s, storage_hs AS h, storage_qy AS q WHERE c.storagenumber=s.id AND h.qid=q.id AND q.sid=sid AND c.id LIKE %s AND  c.membername LIKE %s AND s.name LIKE %s AND q.name LIKE %s'
        re = self.getAll(sql,(cid,cmembername,sname,qname))
        return re
    
        
        
        
        
        
        
        
        
        
        
        
        
        
        
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
        if self.getOne(sql):
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
            return self.getAll(sql)

    def queryGroup_info(self,groupid):
        sql = "select * from usergroup where id ="+str(groupid)
        return self.getOne(sql)
    
    def queryResource(self):
        '''获取所有权限资源'''
        sql = 'select * from resource'
        return self.getAll(sql)
    
   