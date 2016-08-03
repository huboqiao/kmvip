#Coding:utf-8

from application.lib.Commethods import *
import time

class TimeThread(QThread):
    
    def run(self):
        while True:
            time.sleep(1)
            now = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            self.emit(SIGNAL("pudateTime"),now)