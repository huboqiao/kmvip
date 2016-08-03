#coding: utf-8
'''
Created on 2015年2月1日

@author: kylin

公司资金明细报表
'''
from application.lib.Commethods import *
from application.view.gongsizijinmingxi import Ui_Dialog
from application.lib.commodel import getDataThread

class CompanyDetailReport(ControllerAction,Ui_Dialog,PrintAction):
    
    def __init__(self,data,parent = None):
        ControllerAction.__init__(self, parent, u'公司资金明细')
        PrintAction.__init__(self, u"公司资金明细报表")
        self.title = u"公司资金明细报表"
        self.data = data
#         self.gridLayout.setSpacing(0)
#         self.gridLayout.setMargin(0)
        #设置查询的 开始、结束时间
        data["start"] = data["start"].replace("-","/")
        data["end"] = data["end"].replace("-","/")
        self.dateEdit.setDate(QDate.fromString(data["start"],"yyyy/M/d"))
        self.dateEdit_2.setDate(QDate.fromString(data["end"],"yyyy/M/d"))
        
        self.dateEdit.setCalendarPopup(True)
        self.dateEdit_2.setCalendarPopup(True)
        
        self.label_5.setText(data["jbr"])
        
        self.setSIGNAL()
        
        #设置表单字段格式
        self.setTableFormat()
        
        self.queryData()
    
    def setSIGNAL(self):
        self.connect(self.pushButton, SIGNAL("clicked()"),self.queryData)
        self.connect(self.pushButton_2, SIGNAL("clicked()"),self.generateExcel)
        self.connect(self.pushButton_3, SIGNAL("clicked()"),self.printTo)
        self.connect(self.pushButton_4, SIGNAL("clicked()"),self.prePrint)
        self.connect(self.pushButton_5, SIGNAL("clicked()"),self.configColumn)
        self.connect(self.comboBox,SIGNAL("currentIndexChanged (int)"),self.queryData)
        
    #查询数据
    def queryData(self):
        
        #判断开始时间和结束时间
        sdate = QDate.fromString(str(self.dateEdit.text()).replace("-","/"),"yyyy/M/d")
         
        edate = QDate.fromString(str(self.dateEdit_2.text()).replace("-","/"),"yyyy/M/d")
        if sdate.toJulianDay() > edate.toJulianDay():
            self.dateEdit.setDate(edate)
            
        #获取时间
        start = str(self.dateEdit.text())
        end = str(self.dateEdit_2.text())
        
        #交易方式
        type = self.comboBox.currentIndex()
        
        data = {"start":str(start),"end":str(end),"uid":str(self.data["uid"]),"type":str(type)}
        data = {'node':'logic','act_fun':'queryCompanyZiJinDetail','data':data}
        self.dayreportmodel = getDataThread(data,0,"queryCompanyZiJinDetail")
        self.connect(self.dayreportmodel,SIGNAL("queryCompanyZiJinDetail"),self.getData)
        self.dayreportmodel.start()
        
    #处理数据
    def getData(self,data):
        data = data
        #清空表格
        #清空统计数据
        self.clearData((self.tableWidget,(self.countList,0)))
        
        if not data["stat"]:
            self.boxWarning(u'提示', u'没有符合条件的记录')
            return
        data = data["data"]
        self.insertTable(data)
    
    #插入数据到表格
    def insertTable(self,data):
        self.tableWidget.setRowCount(len(data))
        print self.tableWidget.rowCount()
        for i,value in enumerate(data):
            
            for j in range(self.tableWidget.columnCount()):
#                 print self.columnName[j]
                
                item = QTableWidgetItem(unicode(str(value[self.columnName[j]])))
                self.formatTableItem(item,self.table_fmt_list[j])
                self.tableWidget.setItem(i,j,item)
                if j in self.countColumn:
                    self.countList[str(j)] += value[self.columnName[j]]
                    
        if len(self.countColumn)>0:
            rowCount = self.tableWidget.rowCount()
            self.tableWidget.setRowCount(rowCount+1)
            self.tableWidget.setItem(rowCount,0,QTableWidgetItem(u"合计：共%s条记录"%len(data)))
            for key,value in self.countList.items():
                item = QTableWidgetItem(str(value))
                self.tableWidget.setItem(rowCount,int(key),item)
                self.formatTableItem(item,self.table_fmt_list[int(key)])
                

    def setTableFormat(self):
        #字段格式
        self.table_fmt_list = []
        self.table_fmt_list.append({"alignment":"center","color":"black","format":"general","count":False})
        self.table_fmt_list.append({"alignment":"center","color":"black","format":"general","count":False})
        self.table_fmt_list.append({"alignment":"center","color":"black","format":"enum","count":False,"enum":["","现金充值","银行卡充值","现金提现","银行卡提现"]})
        self.table_fmt_list.append({"alignment":"center","color":"black","format":"general","count":False})
        self.table_fmt_list.append({"alignment":"center","color":"black","format":"time","count":False,"time":"%Y-%m-%d %H:%M:%S"})
        self.table_fmt_list.append({"alignment":"right","color":"black","format":"#,##0.00","count":True})
        
        #需要汇总的字段
        self.countColumn = [key for key,value in enumerate(self.table_fmt_list) if value['count'] == True]
        
        #表格列匹配数据库字段
        self.columnName = ["membername","cardid","type","nickname","cdate","amount"]
        
        #初始化汇总字段的值为0
        self.countList = {}
        for i in self.countColumn:
            self.countList[str(i)] = 0