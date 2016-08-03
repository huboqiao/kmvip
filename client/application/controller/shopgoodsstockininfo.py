#coding: utf-8
'''
Created on 2015年2月1日

@author: kylin

客户资金报表
'''
import decimal

from application.lib.Commethods import *
from application.lib.commodel import getDataThread
from application.view.shopgoodsstockininfo import Ui_Dialog


class ShopGoodsStockinInfo(ControllerAction,Ui_Dialog,PrintAction):
    
    def __init__(self,data={},parent=None):
        #初始化界面
        self.data = data
        ControllerAction.__init__(self,parent)
        #初始化打印
        PrintAction.__init__(self, u"商品入库单详情")
        
        self.lineEdit.setText(str(data["stock_on"]))
        
        locale.setlocale(locale.LC_ALL, '')
#         
        #设置信号槽
        self.setSIGNAL()
#         
        #设置表单字段格式
        self.setTableFormat()
        
        
        self.queryData()
        
        
#         
#         
    def setTableFormat(self):
        #字段格式
        self.table_fmt_list = []
        self.table_fmt_list.append({"alignment":"left","color":"black","format":"general","count":False})
        self.table_fmt_list.append({"alignment":"left","color":"black","format":"general","count":False})
        self.table_fmt_list.append({"alignment":"left","color":"black","format":"general","count":False})
        self.table_fmt_list.append({"alignment":"left","color":"black","format":"0","count":False})
        self.table_fmt_list.append({"alignment":"left","color":"black","format":"general","count":False})
        self.table_fmt_list.append({"alignment":"left","color":"black","format":"time","count":False,"time":"%Y-%m-%d %H:%M:%S"})
        self.table_fmt_list.append({"alignment":"left","color":"black","format":"general","count":False})
         
        #需要汇总的字段
        self.countColumn = [key for key,value in enumerate(self.table_fmt_list) if value['count'] == True]
         
        #表格列匹配数据库字段
        self.columnName = ["goods_name","goods_sn","cat_name","goods_numbers","suppliers_name","cdate","editor"]
         
        #初始化汇总字段的值为0
        self.countList = {}
        for i in self.countColumn:
            self.countList[str(i)] = 0
#     



    def setSIGNAL(self):
        self.connect(self.pushButton,SIGNAL("clicked()"),self.queryData)
        #导出excel
        self.connect(self.pushButton_2,SIGNAL("clicked()"),self.generateExcel)
#         #打印报表
        self.connect(self.pushButton_3,SIGNAL("clicked()"),self.printTo)
        #打印预览
        self.connect(self.pushButton_4,SIGNAL("clicked()"),self.prePrint)
        #字段配置
        self.connect(self.pushButton_5,SIGNAL("clicked()"),self.configColumn)
        
    
    def hideSearch(self):
        if self.groupBox.isHidden():
            self.groupBox.show()
            self.pushButton_9.setText(u"隐藏")
        else:
            self.groupBox.hide()
            self.pushButton_9.setText(u"显示")
            
        
        
        
    def queryData(self):    
     
        data = {"sid":self.data["sid"]}
        
        data = {'node':'logic','act_fun':'queryGoodsStockinInfo','data':data}
        self.dayreportmodel = getDataThread(data,0,"queryGoodsStockinInfo")
        self.connect(self.dayreportmodel,SIGNAL("queryGoodsStockinInfo"),self.getData)
        self.dayreportmodel.start()
     
    def getData(self,data):  #清空表格
        #清空统计数据
        self.clearData((self.tableWidget,(self.countList,0)))
         
        if not data["stat"]:
            self.infoBox(data["msg"])
            return
        self.insertTable(data['data'])
     
    #插入数据到表格
    def insertTable(self,data):
        print len(data)
        self.tableWidget.setRowCount(len(data))
        for i,value in enumerate(data):
             
            for j in range(self.tableWidget.columnCount()):
                item = QTableWidgetItem(unicode(str(value[self.columnName[j]])))
                self.formatTableItem(item,self.table_fmt_list[j])
                item.setData(Qt.UserRole,value)
                self.tableWidget.setItem(i,j,item)
                if j in self.countColumn:
                    self.countList[str(j)] += value[self.columnName[j]]
                     
        if len(self.countColumn)>0:
            rowCount = self.tableWidget.rowCount()
            self.tableWidget.setRowCount(rowCount+1)
            self.tableWidget.setItem(rowCount,0,QTableWidgetItem(u"合计："))
            for key,value in self.countList.items():
                item = QTableWidgetItem(str(value))
                self.tableWidget.setItem(rowCount,int(key),item)
                self.formatTableItem(item,self.table_fmt_list[int(key)])
#                 
