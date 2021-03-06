# -*- coding: utf-8 -*-
'''
Created on 2015年2月4日

@author: LiuXinwu
'''
from PyQt4 import QtGui,QtCore
from PyQt4.QtCore import QDate, QString
from application.lib.Commethods import *
from application.view.orderDetail import Ui_Dialog
from application.controller.orderaddgoods import OrderAddGoodsController
from application.model.orderAlterModel import OrderAlterModel
from application.model.orderAddModel import OrderAddModel
from application.lib.commodel import  getDataThread
from application.model.orderlist_model import OrderListModel
import time
_fromUtf8 = QString.fromUtf8
_toUtf8 = QString.toUtf8

class OrderDetailController(ControllerAction,Ui_Dialog):
    def __init__(self,parent = None, orderID = None, orderSN = None):
        ControllerAction.__init__(self,parent)
        #实例化orderlist_model
        self.model = OrderAlterModel()
        self.model2 = OrderListModel()
        self.orderID = str(orderID)
        self.parent = parent
        self.tableWidget.horizontalHeader().setResizeMode(QHeaderView.Stretch)      #铺满表格
        self.goodsIDs = []    
        self.suppliersIDs = []
        self.queryPurchaser() 
        self.querySupplier()
#        self.dateEdit_2.setDate(QDate().currentDate())#创建日期、语气完成日期默认为当前日期
        self.lineEdit_6.setText(QString('0.00'))
        self.label_4.setText(QString(u'订单总额： ' + '0.00' + ' ￥'))
        self.connect(self.pushButton, SIGNAL('clicked()'), self.alterOrder)
       
        #查询某个订单详情
#        data = self.model2.queryOrderDetail(str(orderID))

        
        #查询商品表与订单_info表相关内容
        data2 = self.model2.queryGoodsAndOrderinfo(str(orderID))
        
        #由于data2['data']是一个元组，即
        if data2['stat'] == True:
            self.orderInfo(data2['data'])

        data = {'node':'logic','act_fun':'queryOrderDetail','data':str(orderID)}   
        self.record = getDataThread(data,0,"queryOrderDetail")
        self.connect(self.record,SIGNAL("queryOrderDetail"),self.cardRecord)
        self.record.start() 
        
    def cardRecord(self,data):
        #将获取的数据分解开，
        if data['stat']:
           #order表中数据 
           #佣金
           self.lineEdit_6.setText(self.tr(str("%.2f" %data['data'][0]['price'])))
           #订单号 
           self.ordersn = data['data'][0]['ordersn']
           #采购员
           self.uid = data['data'][0]
           self.comboBox_3.setCurrentIndex(self.userIDs.index(self.uid['uid']))
           
           self.comboBox_5.setCurrentIndex(data['data'][0]['hstat'])
           
           self.comboBox_6.setCurrentIndex(data['data'][0]['cstat'])
           #竞价方式
           self.comboBox_2.setCurrentIndex(data['data'][0]['pstat'])
           #订单状态
           if data['data'][0]['ostat'] == 1:
               self.comboBox.removeItem(4)
           self.comboBox.setCurrentIndex(data['data'][0]['ostat'])
           #供应商
           id = data['data'][0]
           print id,'订单信息'
           if id['cid'] == None or id['cid'] == 0:
               self.comboBox_4.setCurrentIndex(0)
           else:
               self.comboBox_4.setCurrentIndex(self.suppliersIDs.index(id['cid'])+1)
          
           #创建日期
           cdate = data['data'][0]['cdate']
           cdate=time.localtime(cdate)
           cdate=time.strftime('%Y/%m/%d',cdate)
           date = QDate(int(cdate[:4]),int(cdate[5:7]),int(cdate[8:]))
           self.dateEdit.setDate(date)
           #预计完成 
           pdate = data['data'][0]['pdate']
           pdate=time.localtime(pdate)
           pdate=time.strftime('%Y/%m/%d',pdate)
           date = QDate(int(pdate[:4]),int(pdate[5:7]),int(pdate[8:]))
           self.dateEdit_2.setDate(date)

           #设值到对应的框框
           self.lineEdit.setText(self.tr(str(self.ordersn)))
           self.lineEdit.setEnabled(False)

        else:
            #弹出提示框，显示没有无订单详情可供查询
            self.boxWarning(u'提示',u'无订单详情可供查询！')
            self.close()
            return

        self.label_4.setText(QString(u'订单总额： ' + str('%.2f'%self.total) + ' ￥'))
        
    #接受所有商品表与订单_info信息
    def orderInfo(self,data):
        self.tableWidget.setRowCount(0) 
        self.total = 0.00
        if data:
            for i in range(len(data)):
                #选出其中一个字典就更新表格
                self.updateTable(data[i]) 
                self.total += data[i]['price'] * data[i]['counts']
                self.goodsIDs.append(data[i]['goodsid'])
              
    
    #更新表格
    def updateTable(self,data):
        countss = int(self.tableWidget.rowCount()) 
        self.tableWidget.setRowCount(countss+1)
        #order_info表中数据
        #            #单价
        self.signalprice = QTableWidgetItem(self.tr(str("%.2f" %data['price'])))
        self.signalprice.setFlags(Qt.ItemIsEnabled)
        self.signalprice.setTextAlignment(Qt.AlignRight|Qt.AlignVCenter)
        #            #采购数量
        self.counts = QTableWidgetItem(self.tr(str(data['counts'])))
        self.counts.setTextAlignment(Qt.AlignRight|Qt.AlignVCenter)
        self.counts.setFlags(Qt.ItemIsEnabled)
        #         
        #            #单位
        self.unit = QTableWidgetItem(self.tr(str(data['b.unit'])))
        self.unit.setTextAlignment(Qt.AlignCenter|Qt.AlignVCenter)
        self.unit.setFlags(Qt.ItemIsEnabled)
        #            
        #            #总价
        self.zongjia = QTableWidgetItem(self.tr(str("%.2f" %(data['counts']*data['price']))))
        self.zongjia.setFlags(Qt.ItemIsEnabled)
        self.zongjia.setTextAlignment(Qt.AlignRight|Qt.AlignVCenter)
        #分解商品与订单info数据
        #goods表中数据
        #条形码
        goodssn = QTableWidgetItem(self.tr(str(data['goodssn'])))
        goodssn.setFlags(Qt.ItemIsEnabled)
        #            #商品名称
        pname = QTableWidgetItem(self.tr(str(data['pname'])))
        pname.setFlags(Qt.ItemIsEnabled)
        
        #向表格插入值
        self.tableWidget.setItem(countss,0,goodssn)
        self.tableWidget.setItem(countss,1,pname)
        self.tableWidget.setItem(countss,2,self.signalprice)
        self.tableWidget.setItem(countss,3,self.counts)
        self.tableWidget.setItem(countss,4,self.unit)
        self.tableWidget.setItem(countss,5,self.zongjia)
#############################################################################         
        
    #单价或数量改变、更新总价、订单总额、佣金
    def cellValueChanged(self, row, clon):
        if clon == 2 or clon == 3:
            try:
                price = self.tableWidget.item(row,2).text().toDouble()
                self.tableWidget.item(row,2).setText(QString(str("%.2f" %price[0])))
                count = self.tableWidget.item(row,3).text().toDouble()
                self.tableWidget.item(row,5).setText(QString(str("%.2f" %(price[0] * count[0]))))
                self.updateTotal()
            except:
                pass  
    #更新订单总额、佣金      
    def updateTotal(self):
        try:
            total = 0
            for index in range(0,self.tableWidget.rowCount()):
                total += self.tableWidget.item(index,5).text().toDouble()[0] 
            self.lineEdit_6.setText(QString(str('%.2f'%total)))
            self.label_4.setText(QString(u'订单总额： ' + str("%.2f" %total) + ' ￥'))
        except :
            pass
#            self.tableWidget.item(row,3).setText(_fromUtf8(str(price * count)))
            
    #双击第一列添加商品
    def cellDoubleClicked(self, row, clon):
        if clon == 1:
            self.addGoods()
        
    #改变竞价方式
    def biddingTypeChanged(self):
        if self.comboBox_2.currentIndex() == 0:
            self.comboBox_4.setCurrentIndex(1)
            self.comboBox_4.setEnabled(True)
        else:
            self.comboBox_4.setCurrentIndex(0)
            self.comboBox_4.setEnabled(False)
    
    #填充采购员
    def queryPurchaser(self):
        data = self.model.queryPurchasers()
        if data['stat'] == True:
            data = data['data']
            self.userIDs = data
            for i in range(0,len(data)):
                self.comboBox_3.addItem(_fromUtf8(data[i]['nickname']))
                self.userIDs[i] = data[i]['id']   
        else:
            self.boxWarning(u'提示', data['msg'])

    #检查供应商是否存在
    def querySupplier(self):
        data = self.model.querySuppliers()
        if data['stat'] == True:
            data = data['data']
            self.comboBox_4.addItem(_fromUtf8(''))
            for i in range(0,len(data)):
                self.comboBox_4.addItem(_fromUtf8(data[i]['membername']))
                self.suppliersIDs.append(data[i]['id'])
            self.comboBox_4.setCurrentIndex(1)
        else:
            self.boxWarning(u'提示', data['msg'])
            
    #添加商品到订单        
    def addGoods(self):
        self.parent.parent.win.openWin(OrderAddGoodsController(self))
    #添加一种商品
    def addAGoods(self,goodsName, unit, goodsID):
        rowIndex = self.tableWidget.rowCount()
        for i in range(0, rowIndex):
            if goodsName == self.tableWidget.item(i,1).text():
                return
        self.tableWidget.setRowCount(rowIndex + 1)
        goodsName = unicode(QtCore.QString(goodsName).toUtf8())
        sn = self.model.getGoodsSN(str(goodsID))
        snItem = QTableWidgetItem(self.tr(str(sn['data']['goodssn'])))
        snItem.setFlags(Qt.ItemIsEnabled)
        name = QTableWidgetItem(goodsName)
        name.setFlags(Qt.ItemIsEnabled)
        
        unit = unicode(QtCore.QString(unit).toUtf8())
        unit = QTableWidgetItem(self.tr(str(unit.decode('utf8'))))
        price = QTableWidgetItem(self.tr(str('0'.decode('utf8'))))
        count = QTableWidgetItem(self.tr(str('1'.decode('utf8'))))
        total = QTableWidgetItem(self.tr(str('0.00'.decode('utf8'))))
        total.setFlags(Qt.ItemIsEnabled)
        
        self.tableWidget.setItem(rowIndex, 0, snItem)
        self.tableWidget.setItem(rowIndex, 1, name)
        self.tableWidget.setItem(rowIndex, 2, price)
        self.tableWidget.setItem(rowIndex, 3, count)
        self.tableWidget.setItem(rowIndex, 4, unit)
        self.tableWidget.setItem(rowIndex, 5, total)
        self.goodsIDs.append(goodsID.toLong()[0])
                                 
    #从订单删除商品        
    def delGoods(self):
        self.boxInfo(u'提示', u'确定要删除选中的商品吗？')
        currentRow = self.tableWidget.currentIndex().row()
        self.tableWidget.removeRow(currentRow)
#        self.goodsIDs= (self.goodsIDs[i] for i in range(len(self.goodsIDs)) if i != currentRow - 1)
        del self.goodsIDs[currentRow]
        self.updateTotal()

    #发布订单
    def alterOrder(self):
        self.parent.alterOrder()
        self.close()