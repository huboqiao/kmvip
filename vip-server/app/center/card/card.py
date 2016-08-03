# -*- coding: utf8 -*-
# Author:       ivan
# Created:      2014/09/25
#说明：资金管理模块
#
from firefly.server.globalobject import remoteserviceHandle
from app.center.core.card import Card
from app.center.core.member import Member
import json,time
#from lib.massage import MassageModel
import thread
from compiler.pycodegen import TRY_FINALLY

@remoteserviceHandle("gate")
def getMemberInfo(data,_conn):
    '''获取指定卡号的用户信息'''
    cardModel = Card()
    cardid = data['cardid']
    act = data['act']
    re = cardModel.queryCardinfo(cardid) #判断卡片状态
# rewrite:       huaan
# time:      2014/10/11
#说明：资金管理模块
    if re['stat'] == True:
        carddata = cardModel.queryCardRecord(cardid)
        re['data']['cardData'] = carddata
        if act == '':
            return json.dumps(re)
        else:
            return json.dumps(re['data'],act)
    else:
        if act == '':
            return json.dumps(re)
        else:
            return json.dumps(re['data'],act)
        
@remoteserviceHandle("gate")
def getMemberInfo1(data,_conn):
    '''获取指定卡号的用户信息'''
    cardModel = Card()
    cardid = data['cardid'] 
    re = cardModel.queryCardinfo(cardid) #判断卡片状态
    carddata = cardModel.queryCardRecord(cardid)
    re['data']['cardData'] = carddata
    return json.dumps((re, "#end"))

@remoteserviceHandle("gate")
def getMemberInfo2(data,_conn):
    '''获取指定卡号的用户信息'''
    cardModel = Card()
    cardid = data['cardid'] 
    re = cardModel.queryCardinfo(cardid) #判断卡片状态
    carddata = cardModel.queryCardRecord(cardid)
    re['data']['cardData'] = carddata
    return json.dumps(re)

@remoteserviceHandle("gate")
def bindCard(datas,_conn):
    '''绑定卡'''
    cardModel = Card()
    re = cardModel.bindingCard(datas)
    return json.dumps(re)

@remoteserviceHandle("gate")
def addCard(datas,_conn):
    '''添加会员卡'''
    cardModel = Card()
    card = datas['card']
    noid = datas['noid']
    addId = datas['addId']
    re  = cardModel.addCard(card,noid,addId)
    return json.dumps(re)

def sendMsg(msgData):
    try:
        a = MassageModel()
        a.checkMessageText(msgData)
    except :
        pass

@remoteserviceHandle("gate")
def lossCard(data,_conn):
    membermodel = Member()
    re = membermodel.lossUser(data)
    return json.dumps(re)

@remoteserviceHandle("gate")
def pwdCheck(datas,_conn):
    '''验证卡密码'''
    cardModel = Card()
    cardid = datas['cardid']
    pwd  = datas['pwd']
    re = cardModel.queryCardPasswd(cardid,pwd)
    return json.dumps(re)

@remoteserviceHandle("gate")
def pwdCheckzz(datas,_conn):
    '''验证卡密码'''
    cardModel = Card()
    cardid = datas['cardid']
    pwd  = datas['pwd']
    re = cardModel.pwdCheckzz(cardid,pwd)
    return json.dumps(re)

@remoteserviceHandle("gate")
def frozenCard(data,_conn):
    '''连错五次密码冻结卡'''
    cardModel = Card()
#20141008，华安，更新stat又2 改为3
    re = cardModel.updateCardStat(data, 3)#将卡琐定
    return json.dumps(re)

@remoteserviceHandle("gate")
def insertTaking(data,_conn):
    '''提现操作'''
    cardModel = Card()
    ctype = str(data['ctype'])
    re = cardModel.taking(data)
    if re['stat']:        
        msgData = {
                   'customerID':data['customerID'], 
                   'oparetion':u'现金提现',
                   'toMobile':data['toMobile'],
                   'content':{'customerName':data['customerName'],
                              'cardID':data['cardid'],
                              'time':re['time'], 
                              'amount':str(data['amount']),
                              'balance':data['balance']
                              }  # 短信内容参数
                   }
        if ctype == '1':
            msgData['oparetion'] = u'银行卡提现'
        thread.start_new_thread(sendMsg, (msgData, ))
        if ctype == '1':
            return json.dumps({'stat':True,'msg':re['msg'],'ctype':1,'times':re['time']})
        else:
            return json.dumps({'stat':True,'msg':re['msg'],'ctype':0,'times':re['time']})
    else:
        return json.dumps(re)

@remoteserviceHandle("gate")
def queryUserCard(data, _conn):
    '''查询用户id名下的所有卡信息'''
    cardmodel = Card()
    re = cardmodel.queryUserCardAll(data['uid'])
    return json.dumps(re)
    #self.client.callRemote('queryUserCard',obj,re)
    
@remoteserviceHandle("gate")
def transferMatch(data, _conn):
    '''验证转账是否合法'''
    cardmodel = Card()
    re = cardmodel.transferMatch(data)
    return json.dumps(re)
    #self.client.callRemote('queryUserCard',obj,re)
    
@remoteserviceHandle("gate")
def transferMoney(data,_conn):
    cardmodel = Card()
    re = cardmodel.transferUpdate(data)
    if re['stat']:
        # 转入方短信
        try:
            zcMsgData = {
                       'customerID':data['zcid'], 
                       'oparetion':u'转出',
                       'toMobile':data['zctel'],
                       'content':{'customerName':data['zcname'],
                                  'cardID':data['zccard'],
                                  'time':re['time'], 
                                  'amount':data['money'],
                                  'balance':data['zcbalance']
                                  }  # 短信内容参数
                       }
            thread.start_new_thread(sendMsg, (zcMsgData, ))
            # 转入方短信
            zrMsgData = {
                       'customerID':data['zrid'], 
                       'oparetion':u'转入',
                       'toMobile':data['zrtel'],
                       'content':{'customerName':data['zrname'],
                                  'cardID':data['zrcard'],
                                  'time':re['time'], 
                                  'amount':data['money'],
                                  'balance':data['zrbalance']
                                  }  # 短信内容参数
                       }
            thread.start_new_thread(sendMsg, (zrMsgData, ))
        except:
            pass
    return json.dumps(re)
    
@remoteserviceHandle("gate")
def getCardInfo(data, _conn):
    '''查询会员卡信息'''
    cards = Card()
    re = cards.queryCardinfo(data['cardid'])
    return json.dumps(re)

@remoteserviceHandle("gate")
def inRecharge(data, _conn):
    '''充值操作'''
    carddata = Card()
    uid = data['uid']
    cardid = data['cardid']
    amount = data['amount']
    ctype = str(data['ctype'])
    txt = data['txt']
    bankno=data['bankno']
    bankname=data['bankname']
    bankcard=data['bankcard']
    bankadder='-'
    bankusername= data['bankusername']
    
    re = carddata.recharge(uid, cardid, amount, ctype, txt,bankno,bankname,bankcard,bankadder,bankusername)
    if re['stat']:
        # 转入方短信
        msgData = {
                   'customerID':data['customerID'], 
                   'oparetion':u'现金充值',
                   'toMobile':data['toMobile'],
                   'content':{'customerName':data['customerName'],
                              'cardID':cardid,
                              'time':re['time'], 
                              'amount':str(amount),
                              'balance':data['balance']
                              }  # 短信内容参数
                   }
        if ctype == '1':
            msgData['oparetion'] = u'从银行卡充值'
        thread.start_new_thread(sendMsg, (msgData, ))
        
        if ctype == '1':
            return json.dumps({'stat':True,'ctype':1,'times':re['time']})
        else:
            return json.dumps({'stat':True,'data':re,'ctype':0,'times':re['time']})
    else:
        return json.dumps(re)
