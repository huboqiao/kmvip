#coding:utf8
'''
Created on 2014-9-27

@author: ivan
'''
import sys,os
reload(sys)
sys.setdefaultencoding( "utf-8" )
   


def loadModule():
    clistdir = os.listdir(os.getcwd()+'/app/center')
    #遍历文件夹,自动加载模块方法
    for i in clistdir:
        if os.path.isdir(os.getcwd()+'/app/center'+'/'+i):
            zf = os.listdir(os.getcwd()+'/app/center'+'/'+i)
            if zf and zf !='core':
                for j in zf:
                    a = j.split('.')
                    if a[1] == 'py' and a[0] != '__init__':
                        exec("import "+i+'.'+a[0])
