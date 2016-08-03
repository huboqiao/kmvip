# -*- coding: utf-8 -*-
'''
Created on 2014年6月11日

@author: chenyong
'''
from PyQt4 import QtGui
from application.lib.Commethods import *
from application.view.goodslist import Ui_Dialog
import time
from application.lib.PrintMy import printer
from application.model.goodslist_model import GoodslistModel

class GoodsListController(ControllerAction,Ui_Dialog):
    def __init__(self,parent=None):
        ControllerAction.__init__(self,parent)
        #self.setupUi(self)
        self.parent=parent
        self.connect(self.pushButton_2, SIGNAL("clicked()"),self.query)
        self.printname = self.cf.get('print_ini','defprint') #读取打印机配置
        self.connect(self.pushButton, SIGNAL("clicked()"),self.printTo)
        self.tableWidget.horizontalHeader().setResizeMode(QHeaderView.Stretch)      #铺满表格
        #parentWin = parent.geometry()
        #size = self.geometry()#此处的geometry()首字母必须要小写，否则无法测试通过。
        #self.move((parentWin.width()-size.width())/2,(parentWin.height()-size.height())/4) 
        try:
           # self.appdata['perspective'].callRemote('getAllClass',self)
            goodslistmodel = GoodslistModel()  
            self.connect(goodslistmodel,SIGNAL('getAllClass'),self.getAllClass)  
            goodslistmodel.start()
        except:
            self.boxWarning(u'提示', u'连接服务器超时，请重新登录！')
        try:
            #self.pushButton_2.setEnabled(False)
            #self.appdata['perspective'].callRemote('queryGoodsList',self,'','','')
            goodslistmodel = GoodslistModel()  
            self.connect(goodslistmodel,SIGNAL('queryGoodsList'),self.queryGoodsList)  
            goodslistmodel.start()
        except:
            self.boxWarning(u'提示', u'连接服务器超时，请重新登录！')
            
    def getAllClass(self):
        pass    
    
    def queryGoodsList(self):
        pass    
    #接收服务器返回来的所有商品分类
    def getGoodsClassAll(self,data):
        self.class_data=data
        self.tempd = {}
        for c_type in self.class_data:
            self.comboBox.addItem(c_type['name'])
            self.tempd[c_type['name']]=c_type['id']
        
    #查询
    def query(self):
        if str(self.comboBox.currentIndex())=='0':
            class_id=''
        else:
            class_id=str(self.comboBox.currentText())    #分类id
            class_id=self.tempd[unicode(class_id)]
        goodsname=str(self.lineEdit.text())
        membername=str(self.lineEdit_2.text())
#         try:
#            # self.pushButton_2.setEnabled(False)
#            # self.appdata['perspective'].callRemote('queryGoodsList',self,goodsname,str(class_id),membername)
#         except:
#              self.boxWarning(u'提示', u'连接服务器超时，请重新登录！')
#            goodslistmodel = GoodslistModel()
#            self.connect(goodslistmodel,SIGNAL("queryGoodsList"),self.queryGoodsList(goodsname,str(class_id),membername)) 
#          
           
    def queryGoodsList(self,goodsname,class_id,membername):
        pass    
           
    def goodlist(self,data):
        self.pushButton_2.setEnabled(True)
        self.tableWidget.setRowCount(0) 
        if data:
            for i in range(len(data)):
                self.updateTable(data[i])
            
        
    #更新表格
    def updateTable(self,data):
        counts = int(self.tableWidget.rowCount()) 
        self.tableWidget.setRowCount(counts+1)
        id = QTableWidgetItem(self.tr(str(data['id'])))
        id.setFlags(Qt.ItemIsEnabled)
        membername = QTableWidgetItem(self.tr(str(data['membername'])))
        membername.setFlags(Qt.ItemIsEnabled)
        classname = QTableWidgetItem(self.tr(str(data['classname'])))
        classname.setFlags(Qt.ItemIsEnabled)
        pname = QTableWidgetItem(self.tr(str(data['pname'])))
        pname.setFlags(Qt.ItemIsEnabled)
        price = QTableWidgetItem(self.tr(str(data['price'])))
        price.setFlags(Qt.ItemIsEnabled)
        countsnum = QTableWidgetItem(self.tr(str(data['counts'])))
        countsnum.setFlags(Qt.ItemIsEnabled)
        cdate=time.localtime(int(data['cdate']))
        cdate=time.strftime('%Y-%m-%d %H:%M:%S',cdate)
        cdate = QTableWidgetItem(cdate)
        cdate.setFlags(Qt.ItemIsEnabled)
        storagename = QTableWidgetItem(self.tr(str(data['storagename'])))
        storagename.setFlags(Qt.ItemIsEnabled)
        regiona = QTableWidgetItem(self.tr(str(data['regiona'])))
        regiona.setFlags(Qt.ItemIsEnabled)
        store = QTableWidgetItem(self.tr(str(data['store'])))
        store.setFlags(Qt.ItemIsEnabled)
      
        self.tableWidget.setItem(counts,0,id)
        self.tableWidget.setItem(counts,1,membername)
        self.tableWidget.setItem(counts,2,classname)
        self.tableWidget.setItem(counts,3,pname)
        self.tableWidget.setItem(counts,4,price)
        self.tableWidget.setItem(counts,5,countsnum)   
        self.tableWidget.setItem(counts,6,cdate) 
        self.tableWidget.setItem(counts,7,storagename) 
        self.tableWidget.setItem(counts,8,regiona) 
        self.tableWidget.setItem(counts,9,store) 
        
        
    #打印
    def printTo(self):
        self.html = '''
                <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
                <html xmlns="http://www.w3.org/1999/xhtml">
                
                <HEAD>
                <META http-equiv=Content-Type content="text/html; charset=utf-8" />
                <TITLE></TITLE>
                
                </HEAD>
                
                <BODY LEFTMARGIN=0 TOPMARGIN=0 MARGINWIDTH=0 MARGINHEIGHT=0>
                <table border="1" cellspacing="0">
                <tr>
                    <th width='100'>流水号</th>
                    <th width='80'>商户名称</th>
                    <th width='80'>产品名称</th>
                    <th width='100'>入库价</th>
                    <th width='80'>数量</th>
                    <th width='170'>入库日期</th>
                    <th width='80'>冷库名称</th>
                    <th width='80'>冷库区域</th>
                  </tr>
                  %s
                </table>
                </body>
                </html>
            '''
        counts = int(self.tableWidget.rowCount()) 
        self.htmldata=''
        if counts>0:
            for i in range(counts):
                self.htmldata+='''
                    <tr>
                        <td align="center">%s</td>
                        <td align="center">%s</td>
                        <td align="center">%s</td>
                        <td align="center">%s</td>
                        <td align="center">%s</td>
                        <td align="center">%s</td>
                        <td align="center">%s</td>
                        <td align="center">%s</td>
                      </tr>
                    '''
                self.htmldata=self.htmldata%(str(self.tableWidget.item(i,0).text()),str(self.tableWidget.item(i,1).text()),str(self.tableWidget.item(i,3).text()),str(self.tableWidget.item(i,4).text()),str(self.tableWidget.item(i,5).text()),str(self.tableWidget.item(i,6).text()),str(self.tableWidget.item(i,7).text()),str(self.tableWidget.item(i,8).text()))
            self.html=self.html%(str(self.htmldata))
            printer.printreport(self.printname,self.html)
            self.boxWarning(u'提示',u'打印报表中...完成后请关闭窗口！')
        else:
            self.boxWarning(u'提示',u'没有内容无需打印！')
       
    
        
