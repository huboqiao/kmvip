# -*- coding: utf-8 -*-
'''
@Created date on 2014-5-27
主程序入口文件
@author: ivan
'''

from application.lib.Commethods import *
from application.controller.login import Login
from application.controller.main.mainwindow import MainWindow
from PyQt4.Qt import QDialog, QApplication

if __name__ == "__main__":
    
    reload(sys)
    sys.setdefaultencoding( "utf-8" )
    
    app = QApplication(sys.argv)
#     QApplication.setStyle("Plastique")
#     QApplication.setStyle("CDE")
#     print QStyleFactory.keys()
#     for i in range(QStyleFactory.keys().count()):
#         print QStyleFactory.keys().takeAt(i)
    
#     print QApplication.setStyle(QStyleFactory.create(styleName))
    
    login=Login()
    if login.exec_():
        win = MainWindow()
        win.show()
    sys.exit(app.exec_())   
        