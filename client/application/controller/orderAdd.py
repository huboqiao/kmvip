# -*- coding: utf-8 -*-
'''
Created on 2015年2月4日

@author: LiuXinwu
'''
from PyQt4 import QtGui,QtCore
from PyQt4.QtCore import QDate, QString
from application.lib.Commethods import *
from application.view.orderAdd import Ui_Dialog
from application.controller.orderaddgoods import OrderAddGoodsController
from application.model.orderAddModel import OrderAddModel
from application.lib.commodel import  getDataThread
import time
_fromUtf8 = QString.fromUtf8
_toUtf8 = QString.toUtf8

class OrderAddController(ControllerAction,Ui_Dialog):
    def __init__(self,parent = None):
        ControllerAction.__init__(self,parent)
        self.tableWidget.setEditTriggers(QAbstractItemView.DoubleClicked)
        self.parent = parent
        self.tableWidget.horizontalHeader().setResizeMode(QHeaderView.Stretch)      #铺满表格
        self.dateEdit.setDate(QDate().currentDate())#创建日期、语气完成日期默认为当前日期
        self.dateEdit.setEnabled(False)
        self.dateEdit_2.setDate(QDate().currentDate())
        self.model = OrderAddModel()
        self.queryPurchaser()
        self.querySupplier()
        self.lineEdit_6.setText(QString('0.00'))
        self.label_4.setText(QString(u'订单总额： ' + '0.00' + ' ￥'))
        self.goodsIDs = []
        self.comboBox.setCurrentIndex(1)
        self.comboBox.setEnabled(False)
        
        self.connect(self.comboBox_2, SIGNAL('currentIndexChanged(int)'), self.biddingTypeChanged)
        self.connect(self.pushButton, SIGNAL('clicked()'), self.addOrder)
        self.connect(self.pushButton_2, SIGNAL('clicked()'), self.addGoods)
        self.connect(self.pushButton_3, SIGNAL('clicked()'), self.delGoods)
        self.connect(self.tableWidget, SIGNAL('cellChanged(int,int)'), self.cellValueChanged)
        self.connect(self.tableWidget, SIGNAL('cellDoubleClicked(int, int)'), self.cellDoubleClicked)

    #单价或数量改变、更新总价、订单总额、佣金
    def cellValueChanged(self, row, clon):
        if clon == 2 or clon == 3:
            try:
                price = self.tableWidget.item(row,2).text().toDouble()
                count = self.tableWidget.item(row,3).text().toDouble()
                total = "%.2f" % (price[0] * count[0])
                self.tableWidget.item(row,2).setText(QString(str("%.2f" %price[0])))
                self.tableWidget.item(row,5).setText(QString(str(total)))
                self.updateTotal()
            except:
                pass  
    #更新订单总额、佣金      
    def updateTotal(self):
        try:
            total = 0
            for index in range(0,self.tableWidget.rowCount()):
                total += self.tableWidget.item(index,5).text().toDouble()[0] 
            self.label_4.setText(QString(u'订单总额： ' + str("%.2f" %total) + ' ￥'))
        except :
            pass
            
    #双击第一列添加商品
    def cellDoubleClicked(self, row, clon):
        if clon == 0:
            self.addGoods()
        
    #改变竞价方式
    def biddingTypeChanged(self):
        if self.comboBox_2.currentIndex() == 0:
            self.comboBox_4.setCurrentIndex(1)
            self.comboBox_4.setEnabled(True)
        else:
            self.comboBox_4.setCurrentIndex(0)
            self.comboBox_4.setEnabled(False)
    
    #检查采购员ID是否存在
    def queryPurchaser(self):
        data = self.model.queryPurchasers()
        print 'data',data
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
            self.suppliersIDs = data
            self.comboBox_4.addItem(_fromUtf8(''))
            for i in range(0,len(data)):
                self.comboBox_4.addItem(_fromUtf8(data[i]['membername']))
                self.suppliersIDs[i] = data[i]['id']
            self.comboBox_4.setCurrentIndex(1)
        else:
            self.boxWarning(u'提示', data['msg'])
            
    #添加商品到订单        
    def addGoods(self):
        win = OrderAddGoodsController(self)
        win.exec_()
        
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
        price = QTableWidgetItem(self.tr(str('0.00'.decode('utf8'))))
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
        #self.boxInfo(u'提示', u'确定要删除选中的商品吗？')
        if self.boxConfirm(u'提示', u'确定要删除选中的商品吗？'):
            
            currentRow = self.tableWidget.currentIndex().row()
            self.tableWidget.removeRow(currentRow)
            del self.goodsIDs[currentRow]
            self.updateTotal()
        else:
            pass

    #发布订单
    def addOrder(self):
        ddh = str(self.lineEdit.text())
        if ddh.strip()=='':
            self.boxWarning(u'提示', u'订单号不能为空！')
            self.lineEdit.setFocus(True)
            return 
        else:
            try:
                int(ddh)
            except:
                self.boxWarning(u'提示', u'订单号只能由数字组成！')
                self.lineEdit.clear()
                self.lineEdit.setFocus(True)
                return 
        goodsList = []
        goodsCount = self.tableWidget.rowCount()
        if goodsCount == 0:
            self.boxWarning(u'提示', u'订单中没有商品，请往订单添加商品！')
            self.addGoods()
            return
        for i in range(0, goodsCount):
            goods =  {'goodsID':self.goodsIDs[i],
                      'price':str(self.tableWidget.item(i,2).text()),
                      'unit':str(self.tableWidget.item(i,4).text()),
                      'count':str(self.tableWidget.item(i,3).text())
                      }
            try :
                goods['price'] = float(goods['price'])
            except:
                self.boxWarning(u'提示', u'商品价格必须为阿拉伯数字！')
                self.tableWidget.setFocus()
                return
            try :
                goods['count'] = float(goods['count'])
            except:
                self.boxWarning(u'提示', u'商品数量必须为阿拉伯数字！')
#                self.tableWidget.item(i,2).setFocus()
                return
            if float(goods['price']) < 0:
                self.boxWarning(u'提示', u'商品价格不能为负数！')
#                self.tableWidget.item(i,1).setFocus()
                return
            if float(goods['count']) <= 0:
                self.boxWarning(u'提示', u'商品数量要大于 0！')
#                self.tableWidget.item(i,2).setFocus()
                return
                
            goodsList.append(goods)
        orderInfo = {'orderSN':str(self.lineEdit.text()),
                     'purchaserID':self.userIDs[self.comboBox_3.currentIndex()],
                     'biddingType':self.comboBox_2.currentIndex(), 
                     'orderStatu':self.comboBox.currentIndex(),
                     'supplierID':self.comboBox_4.currentIndex(),
                     'startDate':str(self.dateEdit.text()),
                     'exceptDate':str(self.dateEdit_2.text()),
                     'total':self.lineEdit_6.text().toDouble()[0]
                     }
        #订单号为空不能添加订单
        if orderInfo['orderSN'].replace(' ', '') == '':
            self.boxWarning(u'提示', u'订单号不能为空！')
            self.lineEdit.setText('')
            self.lineEdit.setFocus()
            return
        orderExists = self.model.getOrderID({'orderSN':orderInfo['orderSN']})
        if orderExists['orderExists'] == True:
            self.boxWarning(u'提示',u'订单号已经存在，请从新输入！')
            return
        #指派供应商，供应商不能为空
        if orderInfo['biddingType'] == 0:
            if orderInfo['supplierID'] == 0:
                self.boxWarning(u'提示', u'竞价方式为指派供应商，供应商不能为空！')
                self.comboBox_4.setFocus()
                return 
            orderInfo['supplierID'] = self.suppliersIDs[orderInfo['supplierID'] - 1]
        
        data = {'goods':goodsList, 'orderInfo': orderInfo}
        data = self.model.addOrder(data)
        self.boxWarning(u'提示',data['msg'])
        if data['stat']:
            self.closeTab()
