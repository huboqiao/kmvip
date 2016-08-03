# --*-- coding:utf-8 --*--
'''
Created on 2014年6月16日

@author: ivan
'''

class PowerAct(object):
    def __init__(self,role_list,resource):
        self.role_list = role_list
        self.resource = resource
        self.getUserAct()
        
    def getUserAct(self):
        act = []  
        lists = self.role_list.split(',')
        for i in self.resource:
            if str(i['id']) in lists:
                act.append(i['re_name'])
        self.act = act
    
    def matching(self,act):
        if act in self.act:
            return True
        else:
            return False
        
    