#coding:utf8

import time

from socket import AF_INET,SOCK_STREAM,socket
from thread import start_new
import struct

def sendData(sendstr,commandId):
    HEAD_0 = chr(0)
    HEAD_1 = chr(0)
    HEAD_2 = chr(0)
    HEAD_3 = chr(0)
    ProtoVersion = chr(0)
    ServerVersion = 0
    sendstr = sendstr
    data = struct.pack('!sssss3I',HEAD_0,HEAD_1,HEAD_2,\
                       HEAD_3,ProtoVersion,ServerVersion,\
                       len(sendstr)+4,commandId)
    senddata = data+sendstr
    return senddata

def resolveRecvdata(data):
    head = struct.unpack('!sssss3I',data[:17])
    length = head[6]
    data = data[17:17+length]
    return data

if __name__ == "__main__":
    HOST='localhost'
    PORT=11000
    BUFSIZE=1024
    ADDR=(HOST , PORT)
    client = socket(AF_INET,SOCK_STREAM)
    client.connect(ADDR)
    client.sendall(sendData("{'node':'login','act_fun':'login','data':'123'}",0))
    msg = client.recv(1024)
    msg = resolveRecvdata(msg)
    client.sendall(sendData("{'node':'test','act_fun':'test','data':'123'}",0))
    msg = client.recv(1024)
    msg = resolveRecvdata(msg)
    client.close()


