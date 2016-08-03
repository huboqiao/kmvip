#coding:utf-8

from application.lib.Commethods import *
from application.view.rateslist import Ui_Dialog
from application.lib.commodel import getDataThread
import application.lib.formatCheck as check

class RatesList(ControllerAction,Ui_Dialog,PrintAction):
    
    def __init__(self,parent = None):
        ControllerAction.__init__(self, parent, u'利息列表')
        PrintAction.__init__(self, u'利息列表')
        self.setTableFormat()
        #设置查询的 开始、结束时间
        now = QDate().currentDate()
        self.dateEdit.setDate(now.addDays(-now.day() + 1))
#         
        self.dateEdit_2.setDate(now)
        self.connect(self.pushButton_2, SIGNAL("clicked()"), self.printTo)
        self.connect(self.pushButton,SIGNAL("clicked()"),self.queryData)
        self.connect(self.pushButton_3, SIGNAL("clicked()"), self.generateExcel)
        self.queryData()
        check.stringFilter(self.lineEdit, "[\d\s]+$")
                
    def queryData(self):
        self.tableWidget.setRowCount(0)
        # 起止时间
        start = str(self.dateEdit.text())
        end = str(self.dateEdit_2.text())
        # 金荣卡号
        noid = str(self.lineEdit.text()).replace(" ","")
        try:
            if noid != "":
                int(noid)
        except:
            self.infoBox("请输入正确卡号")
            return
        # 是否已经结算
        isPayed = self.comboBox.currentIndex()
        
        data = {"start":str(start),"end":str(end),"cardid":str(noid),"payed":isPayed}
        data = {'node':'logic','act_fun':'ratesList','data':data}
        self.dayreportmodel = getDataThread(data,0,"ratesList")
        self.connect(self.dayreportmodel,SIGNAL("ratesList"),self.getData)
        self.dayreportmodel.start()
    
    def getData(self, data):
        data = data
        if data['stat']:
            self.label_5.setText(self.tr('当前日利率：%s'%data['currentRate']))
            self.insertTable(data['data'])
        else:
            self.boxWarning(u'提示', data['msg'])
            
    # 插入数据到表格
    def insertTable(self,data):
        self.tableWidget.setRowCount(len(data))
        for i,value in enumerate(data):
            for j in range(self.tableWidget.columnCount()):
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
                    
    # 设置表格每列的格式
    def setTableFormat(self):
        # 字段格式
        self.table_fmt_list = []
        self.table_fmt_list.append({"alignment":"center","color":"black","format":"general","count":False})
        self.table_fmt_list.append({"alignment":"right","color":"black","format":"#,##0.00","count":True})
        self.table_fmt_list.append({"alignment":"center","color":"black","format":"enum","count":False,"enum":[u'未结算', u'已结算']})
        # 需要汇总的字段
        self.countColumn = [key for key,value in enumerate(self.table_fmt_list) if value['count'] == True]
        # 表格列匹配数据库字段
        self.columnName = ["membername", "rates", 'payed']
        # 初始化汇总字段的值为0
        self.countList = {}
        for i in self.countColumn:
            self.countList[str(i)] = 0