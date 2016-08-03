# --*-- coding:utf-8 --*--
'''
Created on 2014年6月18日

@author: ivan
'''
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from application.lib.servicecontroller import ServiceControl

class KPrintPreviewDialog(QPrintPreviewDialog):
    def __init__(self,parent = None):
        QPrintPreviewDialog.__init__(self,parent)
        toolbarlist =  self.findChildren(QToolBar)
        if len(toolbarlist)>0:
            toolbar = toolbarlist[0]
            for key,i in enumerate(toolbar.actions()):
                print key,i.objectName()
                
#             toolbar.actions()[19].setDisabled(True);
#             toolbar.actions()[20].setDisabled(True);
            toolbar.actions()[21].setDisabled(True);
#     toolbarlist.first()->actions().at(4)->setDisabled(true);
#     toolbarlist.first()->actions().at(5)->setDisabled(true);
            
            
class printer():
    
    
    #打印机列表
    @staticmethod
    def printerList():
        printer = []
        printerInfo = QPrinterInfo()
        for item in printerInfo.availablePrinters():
            printer.append(item.printerName())
        return printer
    
    #打印任务
    @staticmethod
    def printing(printer):
        printerInfo = QPrinterInfo()
        p = QPrinter()
        if len(printerInfo.availablePrinters()) == 0:
            return False
        for item in printerInfo.availablePrinters():
            if printer == item.printerName():
                p = QPrinter(item)
                return p
            
            
    #报表打印任务
    @staticmethod
    def printreport(pname, context):
        
        #管理window服务
        serviceController = ServiceControl()
        #打印服务是否关闭
        if serviceController.isStop("Spooler"):
            #开启打印服务
            if not serviceController.start("Spooler"):
                return
            else:
                printer.printreport(pname, context)
                return
        
        printerInfo = QPrinterInfo()
        for item in printerInfo.availablePrinters():
            if pname == item.printerName():
                p = QPrinter(item)
        doc = QTextDocument()
        doc.setHtml(u'%s' % context)
#        doc.setPageSize(QSizeF(p.logicalDpiX() * (210/ 25.4), p.logicalDpiY() * (297 / 25.4)))
        p.setOutputFormat(QPrinter.NativeFormat)
        p.setPageSize(p.A4)
        p.setPaperSize(QSizeF(210*2.54,297*2.54),1)
#        p.setFullPage(True)
        doc.print_(p)
        
               
    
     
    @staticmethod
    def preprint(pname,parent):
        '''
                    打印预览
        '''
        
        #管理window服务
        serviceController = ServiceControl()
        #打印服务是否关闭
        if serviceController.isStop("Spooler"):
            #开启打印服务
            if not serviceController.start("Spooler"):
                print "开启服务失败"
                return 
            else:
                printer.preprint(pname, parent)
                return
        
        try:
            printerInfo = QPrinterInfo()
            printer.p = QPrinter()
            for item in printerInfo.availablePrinters():
                if pname == item.printerName():
                    printer.p = QPrinter(item)
    #        doc.setPageSize(QSizeF(p.logicalDpiX() * (210/ 25.4), p.logicalDpiY() * (297 / 25.4)))
            printer.p.setOutputFormat(QPrinter.NativeFormat)
            printer.p.setPageSize(printer.p.A4)
            printer.p.setPaperSize(QSizeF(210*2.54,297*2.54),1)
    #        p.setFullPage(True)
            printer.html = parent.html
            
            pdialog = QPrintPreviewDialog(printer.p)
            parent.connect(pdialog,SIGNAL("paintRequested (QPrinter *)"),printer.dd)
            pdialog.showMaximized()
            pdialog.exec_()
            return True
        except Exception,e:
            print e
        
    @staticmethod
    def dd():
        doc = QTextDocument()
        doc.setHtml(u'%s' % printer.html)
        doc.print_(printer.p)