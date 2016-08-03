#coding:utf-8
'''
Created on 2015年1月29日

@author: King
'''
import hashlib, json
import time,sys
from lib.db import Mysql


reload(sys)
sys.setdefaultencoding( "utf-8" )

class System(Mysql):
    def __init__(self):
        Mysql.__init__(self)
    
    #删除权限表中的设置
    def delGoryset(self,data):
        sql = "DELETE FROM customercategory WHERE id = %s"
        data = mysql.delete(sql,data)
        mysql.end()
        if data>0:
            return {"stat":True,"msg":u"删除成功"}
        else:
            return {"stat":False,"msg":u"删除失败"}
        
    #添加权限
    def addGoryset(self,data):
        if int(data['isactive'])==0:
            data['isactive'] = "1"
        else:
            data['isactive'] = "0"
        dataList=(data['name'],data['isactive'],data['cdate']) 
        goryExsist = self.getAll('select * from customercategory where name = "' + data['name'] + '"') 
        if goryExsist:
            return {"stat":False,"msg":u"添加权限失败,\n该权限已经存在！"}
        sql = "INSERT into customercategory (name,isactive,cdate) VALUES (%s,%s,%s)"
        data = self.insertOne(sql,dataList)
        self.end()
        if data:
            return {'stat':True,'data':data}
        else:
            return {'stat':False,'msg':u'此类别没有添加任何商品！'} 
           
     #更新权限       
    def updateGoryset(self,data):
        sql = "update customercategory set name = %s ,isactive = %s ,cdate = %s where id = %s"
        data = mysql.update(sql,data)
        mysql.end()
        if data>0:
            return {"stat":True,"msg":u"修改成功"}
        else:
            return {"stat":False,"msg":u"修改失败"}
        
        
        
    
    #删除用户
    def delCustomer(self,data):
        if self.getAll('select id from customer where ugroup = %s', (data['id'])):
            return {'stat':False, 'msg':u'存在属于该类型的客户，\n不能删除该客户类型'}
        sql = "DELETE FROM customergroup where id = %s"
        data = self.delete(sql,data["id"])
        self.end()
        if data>0:
            return {"stat":True}
        else:
            return {"stat":False,"msg":u"删除失败"}
        
        

    #获取所有的类别    
    def getcumster(self, stat=''):
        if stat != '':
            sql = "select * from customergroup where isactive = %s"%stat
        else:
            sql = "select * from customergroup"
        data =  self.getAll(sql)
        msg = ""
        if data:
            return {'stat':True,'data':data}
        else:
            return {'stat':False,'msg':u'暂无客户类别，请添加！'}
    
    #修改权限
    def edigory(self,data):
     
        datalist = (data["name"],data["isactive"],data["cdate"],data["id"])
        goryExsist = self.getAll('select * from customercategory where id != "' + data['id'] + '" and name = "' + data['name'] + '"')
        if goryExsist:
            return {"stat":False,"msg":u"修改权限失败,\n该权限已经存在！"}
        sql = "update customercategory set name = %s ,isactive = %s ,cdate = %s where id = %s"
        data = self.update(sql,datalist)
        self.end()
        if data>0:
            return {"stat":True}
        else:
            return {"stat":False,"msg":u"修改权限失败"}
        
    #删除权限
    def delgory(self,data):
        sql = "DELETE FROM customercategory WHERE id = %s"
        data = self.delete(sql,data["id"])
        self.end()
        if data>0:
            return {"stat":True}
        else:
            return {"stat":False,"msg":u"删除权限失败"}
        

    #获取权限
    def getgory(self):
        sql = "SELECT * FROM customercategory"
        data = self.getAll(sql)
        if data>0:
            return {"stat":True,"data":data}
        else:
            return {"stat":False,"msg":u"未添加权限"}
    #获取已经启动了的权限
    def getsomegory(self):
        sql = "SELECT * FROM customercategory where isactive = 1"
        data = self.getAll(sql)
        if data>0:
            return {"stat":True,"data":data}
        else:
            return {"stat":False,"msg":u"没有启用中的权限"}
        
    #获取一个类别用户的权限的typelist
    def getonecumstomer(self,data):
        sql = "select typelist from customergroup where id = %s"
        data = self.getAll(sql,data["id"])
        if data>0:
            return {"stat":True,"data":data}
        else:
            return {"stat":False,"msg":u"该用户类型没有启用中的权限！"}
        
    #根据一个typelist获取一个权限列表
    def getonegory(self,data):
        sql = "SELECT * FROM customercategory where id in (" + data['list'].strip(',') + ") and isactive = 1 order by name"
        data = self.getAll(sql)
        if data>0:
            return {"stat":True,"data":data}
        else:
            return {"stat":False,"msg":u"权限不存在！"}
    #添加类别用户
    def addcustomer(self,data):
        datalist = (data["name"],data["typelist"],data["isactive"],data["isstorage"],data["cdate"])
        customerGroupExsist = self.getAll('select * from customergroup where name = "' + data['name'] + '"')
        if customerGroupExsist:
            return {"stat":False,"msg":u"该客户类别已经存在，\n请重新输入客户类别名称！"}
        sql = "INSERT customergroup (name,typelist,isactive,isstorage,cdate)VALUES (%s,%s,%s,%s,%s)"
        data = self.insertOne(sql,datalist)
        self.end()
        if data>0:
            return {"stat":True}
        else:
            return {"stat":False,"msg":u"添加失败"}
    #更新类别用户
    def updatecustomer(self,data):
        dataList = (data["isactive"],data["name"],data["isstorage"],data["typelist"],data["cdate"],data["id"])
        customerGroupExsist = self.getAll('select * from customergroup where id != "' + data['id'] + '" and name = "' + data['name'] + '"')
        if customerGroupExsist:
            return {"stat":False,"msg":u"该客户类别已经存在，\n请重新输入客户类别名称！"}
        sql = "UPDATE customergroup set isactive = %s ,`name` = '%s' ,isstorage = %s ,typelist = '%s',cdate = '%s' WHERE id =%s"
        data = self.update(sql % dataList)
        self.end()
        if data>0:
            return {"stat":True}
        else:
            return {"stat":False,"msg":u"修改失败"}
        
       
        
    
    