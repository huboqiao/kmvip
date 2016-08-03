#coding:utf8
'''
Created on 2015年2月10日

@author: LiuXinwu

'''
import json
from application.lib.commodel import Socket_model,Connection_Stock,getDataThread
class CompanyReportModel(Socket_model):
    def __init__(self):
        Socket_model.__init__(self)
        self.conn = Connection_Stock().getConnection()
    
    #查询经办人真实姓名及id
    def queryJingbanren(self):
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'queryJingbanren','data':''}),0) )
        r = self.conn.recv(self.recvBuff)
        data = json.loads(r[17:])
        return data
    
    def queryReportList(self):
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'report','data':''}),0) )
        r = self.conn.recv(self.recvBuff)
        data = json.loads(r[17:])
        return data[0]
    
    #查询此经办人，今天处理的充值总额
    def queryCZAmountToday(self,data):
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'queryCZAmountToday','data':data}),0) )
        r = self.conn.recv(self.recvBuff)
        data = json.loads(r[17:])
        return data
    
    #查询此经办人，周期类处理的充值总额
    def queryCZAmountPeriod(self,data):
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'queryCZAmountPeriod','data':data}),0) )
        r = self.conn.recv(self.recvBuff)
        data = json.loads(r[17:])
        return data
    
    #查询此经办人，时间段内处理的充值总额
    def queryCZAmountSpan(self,data):
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'queryCZAmountSpan','data':data}),0) )
        r = self.conn.recv(self.recvBuff)
        data = json.loads(r[17:])
        return data
    
    
    #查询此经办人，今天处理的提现总额
    def queryTXAmountToday(self,data):
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'queryTXAmountToday','data':data}),0) )
        r = self.conn.recv(self.recvBuff)
        data = json.loads(r[17:])
        return data
    
    #查询此经办人，周期类处理的提现总额
    def queryTXAmountPeriod(self,data):
        self.conn.sendall(self.sendData(json.dumps({'node':'capital','act_fun':'queryTXAmountPeriod','data':data}),0) )
        r = self.conn.recv(self.recvBuff)
        data = json.loads(r[17:])
        return data
    
    
    
    #查询此经办人，时间段内处理的提现总额
    def queryTXAmountSpan(self,data):
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'queryTXAmountSpan','data':data}),0) )
        r = self.conn.recv(self.recvBuff)
        data = json.loads(r[17:])
        return data
    
    
    def getUser(self):
        self.conn.sendall(self.sendData(json.dumps({'node':'logic','act_fun':'queryUser','data':''}),0) )
        r = self.conn.recv(self.recvBuff)
        data = json.loads(r[17:])
        return data[0]
    
    
    
        