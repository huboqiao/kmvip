# -*- coding:utf8  -*-
'''
Created on 2015年3月11日

@author: kylin

管理window服务

'''

import win32service


class ServiceControl(object):
    
    def __init__(self):
        self.scm = win32service.OpenSCManager(None,None,win32service.SC_MANAGER_ALL_ACCESS);

    # 检查服务是否停止
    def isStop(self,name):
        flag = False;
        try:
            handle = win32service.OpenService(self.scm,name,win32service.SC_MANAGER_ALL_ACCESS);
            if handle:
                ret = win32service.QueryServiceStatus(handle);
                flag = ret[1]!=win32service.SERVICE_RUNNING;
                win32service.CloseServiceHandle(handle);
        except Exception,e:
            print "ServiceControl检查服务失败"
            return False
        return flag;

    # 开启服务
    def start(self,name):
        flag = True
        try:
            handle = win32service.OpenService(self.scm,name,win32service.SC_MANAGER_ALL_ACCESS);
            if handle:
                win32service.StartService(handle,None);
                win32service.CloseServiceHandle(handle);
        except Exception,e:
            print "ServiceControl开启服务失败"
            print e
            return False
        return flag

    # 退出
    def close(self):
        try:
            if self.scm:
                win32service.CloseServiceHandle(self.scm);
        except Exception,e:
            print e


if __name__ == "__main__":
        #管理window服务
        serviceController = ServiceControl()
        #打印服务是否关闭
        print serviceController.isStop("Spooler")
