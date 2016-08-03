#coding:utf8

from firefly.server.globalobject import rootserviceHandle,GlobalObject
import json

@rootserviceHandle
def forwarding(data,_conn):
    try:
        data = json.loads(data)
        node = data['node']
        act_fun = data['act_fun']
        data = data['data']
        return GlobalObject().root.callChild(node,act_fun,data,_conn)
    except:
        return u'参数不正确'
    
@rootserviceHandle
def saveImage(data,_conn):
    return GlobalObject().root.callChild('logic','saveImage',data,_conn)


@rootserviceHandle
def login(data,_conn):
    data = json.loads(data)
    data = data['data']
    return GlobalObject().root.callChild('logic','login',data,_conn)
