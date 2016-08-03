# -*- coding: utf-8 -*-
'''
Created on 2015年3月4日

@author: LiuXinwu
'''
from PyQt4.QtCore import QThread
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from application.lib.commodel import Socket_model,Connection_Stock
import json
class MemberManagerModel(Socket_model):
    def __init__(self):
        Socket_model.__init__(self)
        self.conn = Connection_Stock().getConnection()
        
    def idcardQueryMerchant(self, id):
        data={'idcard':id,'flag':'False'}
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'checkIdCard','data':data}),0) )
        r = self.conn.recv(self.recvBuff)
        r = self.resolveRecvdata(r)
        return json.loads(r)
    
    def sendImg(self,imgbyte):
        self.conn.sendall(self.sendData(imgbyte,1) )
        r = self.conn.recv(self.recvBuff)
        r = self.resolveRecvdata(r)  
        return json.loads(r)
    
    def updateMerchant(self,data,data_info):
        datas={'data':data,'data_info':data_info}
        
        print 'datas=',datas
        
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'updateMember','data': datas}),0) )
        r = self.conn.recv(self.recvBuff)
        r = self.resolveRecvdata(r)
        return json.loads(r)
    
    def getMemberinfo(self,idcard): 
        data={"idcard":idcard,"flag":'False'}
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'idcardQueryMember','data':data}),0))
        r = self.conn.recv(self.recvBuff)
        r = self.resolveRecvdata(r)
        return json.loads(r)
    
    def offCustomer(self,data):
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'offCustomer','data':data}),0))
        r = self.conn.recv(self.recvBuff)
        r = self.resolveRecvdata(r)
        return json.loads(r)
    
    def queryService(self,name,idcard):
        data={'name':name,'idcard':idcard}
        print data
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'queryService','data':data}),0))
        r = self.conn.recv(self.recvBuff)
        r = self.resolveRecvdata(r)
        return json.loads(r)
    
    
    
    