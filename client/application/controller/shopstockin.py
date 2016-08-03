# -*- coding: utf-8 -*-
'''
Created on 2015年3月18日

@author: kylin
'''
from application.lib.Commethods import *
from application.view.shopstockin import Ui_Dialog
from application.controller.shopstockaddgoods import ShopStockAddGoodsController
from application.model.shoporderAddModel import OrderAddModel
# from application.model.orderAddModel import OrderAddModel
# from application.lib.commodel import  getDataThreadfrom PyQt4 import QtCore
from PyQt4 import QtCore
import time
_fromUtf8 = QString.fromUtf8
_toUtf8 = QString.toUtf8

class ShopStockInController(ControllerAction,Ui_Dialog):
    def __init__(self,parent = None):
        ControllerAction.__init__(self,parent)
        self.tableWidget.setEditTriggers(QAbstractItemView.DoubleClicked)
        self.parent = parent
        self.tableWidget.horizontalHeader().setResizeMode(QHeaderView.Stretch)      #铺满表格
        self.model = OrderAddModel()
        self.goodsIDs = []
        
        self.connect(self.pushButton, SIGNAL('clicked()'), self.addGoods)
        self.connect(self.pushButton_2, SIGNAL('clicked()'), self.delGoods)
        self.connect(self.pushButton_3, SIGNAL('clicked()'), self.addOrder)
        self.connect(self.tableWidget, SIGNAL('cellChanged(int,int)'), self.cellValueChanged)
        self.connect(self.tableWidget, SIGNAL('cellDoubleClicked(int, int)'), self.cellDoubleClicked)

    #单价或数量改变、更新总价、订单总额、佣金
    def cellValueChanged(self, row, clon):
        if clon == 4:
            try:
                count = int(str(self.tableWidget.item(row,clon).text()))
                self.tableWidget.item(row,4).setText(count)
            except:
                pass  
            
    #双击第一列添加商品
    def cellDoubleClicked(self, row, clon):
        if clon == 0:
            self.addGoods()

            
    #添加商品到订单        
    def addGoods(self):
        pass
        win = ShopStockAddGoodsController(self)
        win.exec_()
        
    #添加一种商品
    def addAGoods(self,goodsName, unit, goodsID):
        rowIndex = self.tableWidget.rowCount()
        for i in range(0, rowIndex):
            if goodsName == self.tableWidget.item(i,1).text():
                return
        self.tableWidget.setRowCount(rowIndex + 1)
        goodsName = unicode(QtCore.QString(goodsName).toUtf8())
        gdata = self.model.getGoodsData(str(goodsID))
        snItem = QTableWidgetItem(self.tr(str(gdata['goods_sn'])))
        snItem.setFlags(Qt.ItemIsEnabled)
        name = QTableWidgetItem(goodsName)
        name.setFlags(Qt.ItemIsEnabled)
        
        unit = unicode(QtCore.QString(unit).toUtf8())
        unit = QTableWidgetItem(self.tr(str(unit.decode('utf8'))))
        unit.setFlags(Qt.ItemIsEnabled)
        provider = QTableWidgetItem(gdata["suppliers_name"])
#         provider = QTableWidgetItem("888888888888888")
        provider.setFlags(Qt.ItemIsEnabled)
        count = QTableWidgetItem(self.tr(str('1'.decode('utf8'))))
        
        
        
        self.tableWidget.setItem(rowIndex, 0, snItem)
        self.tableWidget.setItem(rowIndex, 1, name)
        self.tableWidget.setItem(rowIndex, 2, provider)
        self.tableWidget.setItem(rowIndex, 3, unit)
        self.tableWidget.setItem(rowIndex, 4, count)
        self.goodsIDs.append(goodsID.toLong()[0])
                                 
    #从订单删除商品        
    def delGoods(self):
        #self.boxInfo(u'提示', u'确定要删除选中的商品吗？')
        if self.boxConfirm(u'提示', u'确定要删除选中的商品吗？'):
            
            currentRow = self.tableWidget.currentIndex().row()
            self.tableWidget.removeRow(currentRow)
            del self.goodsIDs[currentRow]
            print self.goodsIDs
        else:
            pass

    #发布订单
    def addOrder(self):
        goodsList = []
        goodsCount = self.tableWidget.rowCount()
        if goodsCount == 0:
            self.boxWarning(u'提示', u'中没有商品，请添加商品入库！')
            self.addGoods()
            return
        for i in range(0, goodsCount):
            goods =  {'goods_id':self.goodsIDs[i],
                      'count':str(self.tableWidget.item(i,4).text())
                      }
            try :
                goods['count'] = int(goods['count'])
            except:
                self.boxWarning(u'提示', u'商品数量必须为阿拉伯数字！')
#                self.tableWidget.item(i,2).setFocus()
                return
            if int(goods['count']) <= 0:
                self.boxWarning(u'提示', u'商品数量要大于 0！')
#                self.tableWidget.item(i,2).setFocus()
                return
                
            goodsList.append(goods)
            
        info = {}
        info["cid"] = ControllerAction.appdata['user']["user_id"]
        data = {'goods':goodsList,"info":info}
        data = self.model.addOrder(data)
        self.boxWarning(u'提示',data['msg'])
        if data['stat']:
            self.closeTab()
