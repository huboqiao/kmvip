#coding:utf-8
'''
Created on 2015年1月29日

@author: king
'''
import hashlib
import time,sys
from lib.db import Mysql


reload(sys)
sys.setdefaultencoding( "utf-8" )

class Shots(Mysql):
    def __init__(self):
        Mysql.__init__(self)
    
    #�޸���Ϣ
    def edishots(self,data):
        datalist = (data["url"],data["username"],data["password"],data["type"],data["content"],data["isactive"],data["id"])
        sql = "update shortset set url = %s ,username = %s ,password = %s,type = %s,content = %s, isactive = %s where id = %s"
        data = self.update(sql,datalist)
        self.end()
        if data>0:
            return {"stat":True}
        else:
            return {"stat":False,"msg":u"修改失败"}
        

        

    #��ȡ���е��û���Ϣ    
    def getshots(self):
        sql = "SELECT * FROM shortset"
        data = self.getAll(sql)
        if data>0:
            return {"stat":True,"data":data}
        else:
            return {"stat":False,"msg":u"获取失败"}
        
        
    #�����Ϣ
    def addshots(self,data):
        if int(data["id"])>0:
            datalist = (data["url"],data["username"],data["password"],data["type"],data["content"],data["isactive"],data["id"])
            sql = "update shortset set url = %s ,username = %s ,password = %s,type = %s,content = %s, isactive = %s where id = %s"
            data = self.update(sql,datalist)            
        else:
            dataList=(data['username'],data['password'],data['type'],data['content'],data['isactive'],data['url'])    
            sql = "INSERT shortset (username,password,type,content,isactive,url) VALUES (%s,%s,%s,%s,%s,%s)"
            data = self.insertOne(sql,dataList)
        self.end()
        if data>0:
            return {'stat':True,"msg":u"添加成功"}
        else:
            return {'stat':False,'msg':u'添加失败'} 
        
    #ɾ����Ϣ
    def delshots(self,data):
        sql = "DELETE FROM shortset WHERE id = %s"
        data = self.delete(sql,data["id"])
        self.end()
        if data>0:
            return {"stat":True}
        else:
            return {"stat":False,"msg":u"删除失败"}
        
    # ���Ͷ��ż�¼��huaan�� 2015.3.4��
    def noteMassage(self, data):
        temp = (data['customerID'], data['oparetion'], data['toMobile'],
                data['content'], data['statu'], data['time'])
        sql = 'insert into msglist(id, cid, stype, mtel, content, wtype, cdate) values(NULL, %s, %s, %s, %s, %s, %s)'
        re = self.insertOne(sql, temp)
        self.end()
        if re:
            return {'stat':True, 'msg':u'记录短信成功'}
        else:
            return {'stat':False, 'msg':u'记录短信失败'}
    # ��ȡ����״̬Ϊ���ύʧ�ܡ��Ķ��ż�¼
    def getFailedMassages(self):
        try:
            failedMassages = self.getAll("select * from msglist where wtype = '提交失败'")
            return failedMassages
        except:
            pass
    # ���¶��ŷ���״̬�ͷ���ʱ��
    def updateMassageRecord(self, data):
        try:
            sql = "update msglist set wtype = %s, cdate = %s where id = %s"
            self.update(sql, data)
            self.end()
        except:
            pass