# -*- coding: utf8 -*-

from PyQt4 import Qt
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from threading import Event
from application.view.test import Ui_Dialog

import time,sys

class MyTest(QDialog, Ui_Dialog):
    def __init__(self,parent = None):
        QDialog.__init__(self)
        self.setupUi(self)
        self.Falg = True
        self.connect(self.pushButton, SIGNAL("clicked()"),self.doStart)
        self.connect(self.pushButton_2, SIGNAL("clicked()"),self.doPause)
        self.connect(self.pushButton_3, SIGNAL("clicked()"),self.doStop)
        
        self.t = MyThread()
        self.connect(self.t, SIGNAL("LCD_NUMBER"),self.chageLcd)
    
    def doStart(self):
        self.t.start()

    def doPause(self):
        if self.Falg:
            self.Falg = False
            self.pushButton_2.setText('restore')
            self.t.pause()
        else:
            self.Falg = True
            self.pushButton_2.setText('pause')
            self.t.restore()
    
    def doStop(self):
        self.t.stop()
    
    def chageLcd(self,data):
        self.lcdNumber.setProperty("intValue", data)

class MyThread(QThread):
    def __init__(self):
        QThread.__init__(self)
        self.isStop = False
        self.event = Event()
        self.event.set()
    
    def run(self):
        i = 0
        while 1:
            i += 1
            if self.isStop:
                break
            if not self.event.isSet():
                self.event.wait()
            self.emit(SIGNAL("LCD_NUMBER"),i)
            time.sleep(0.1)
    def stop(self):
        self.isStop = True
    
    def pause(self):
        self.event.clear()
    
    def restore(self):
        self.event.set()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myThread = MyTest()
    myThread.show()
    sys.exit(app.exec_())