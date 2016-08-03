# -*- coding: utf8 -*-
# Author:       huaan
# Created:      2015/3/19
#说明：解冻到期余额
#
import threading  
import time  
from app.center.core.member import Member

class ActiveFrozenAmount(threading.Thread): 
    def __init__(self):  
        threading.Thread.__init__(self)  
   
    def run(self): 
        while True:
            member = Member()
            member.balanceAfterChanges()
#             member.unfreezeAmount()
            time.sleep(3600)
            
                    
    def stop(self):  
        pass