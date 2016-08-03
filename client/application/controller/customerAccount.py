#coding: utf-8
'''
Created on 2015年2月1日

@author: kylin

客户资金报表
'''
from application.lib.Commethods import *
from application.view.kehuzijinbaobiao import Ui_Dialog
from application.lib.commodel import getDataThread
from application.controller.customerAccountDetail import CustomerAccountDetail
import application.lib.formatCheck as check


class CustomerAccount(ControllerAction,Ui_Dialog,PrintAction):
    
    def __init__(self,parent=None):
        #初始化界面
        ControllerAction.__init__(self,parent)
        #初始化打印
        PrintAction.__init__(self, u"客户资金统计表")
        
        #设置查询的 开始、结束时间
        self.dateTimeEdit.setDate(QDate().currentDate())
        self.dateTimeEdit.setCalendarPopup(True)
        
        self.dateTimeEdit_2.setDate(QDate().currentDate())
        self.dateTimeEdit_2.setCalendarPopup(True)
        
        dateTime = self.dateTimeEdit_2.dateTime()
        dateTime = dateTime.addDays(1).addSecs(-1)
        self.dateTimeEdit_2.setDateTime(dateTime)
        
        #设置信号槽
        self.setSIGNAL()
        
        #设置表单字段格式
        self.setTableFormat()
        #查询数据
        self.queryData()
        check.stringFilter(self.lineEdit, "[\d\s]+$")
        
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
        
        #输入姓名
        self.connect(self.lineEdit,SIGNAL("returnPressed()"),self.queryData)
        self.connect(self.lineEdit_2,SIGNAL("returnPressed()"),self.queryData)
        
#         #双击打开详情页
        self.connect(self.tableWidget,SIGNAL("cellDoubleClicked (int, int)"),self.showDetail)
        #时间修改
#         self.connect(self.dateTimeEdit,SIGNAL("dateTimeChanged(const QDateTime&)"),self.queryData)
#         self.connect(self.dateTimeEdit_2,SIGNAL("dateTimeChanged(const QDateTime&)"),self.queryData)
#         #点击详情
#         self.connect(self.pushButton,SIGNAL("clicked()"),self.showDetail)
        
    def setTableFormat(self):
        #字段格式
        self.table_fmt_list = []
        self.table_fmt_list.append({"alignment":"center","color":"black","format":"general","count":False})
        self.table_fmt_list.append({"alignment":"right","color":"black","format":"#,##0.00","count":True})
        self.table_fmt_list.append({"alignment":"right","color":"black","format":"#,##0.00","count":True})
        self.table_fmt_list.append({"alignment":"right","color":"black","format":"#,##0.00","count":True})
        self.table_fmt_list.append({"alignment":"right","color":"black","format":"#,##0.00","count":True})
        
        #需要汇总的字段
        self.countColumn = [key for key,value in enumerate(self.table_fmt_list) if value['count'] == True]
        
        #表格列匹配数据库字段
        self.columnName = ["nameAndCard","startAmount","in","out","endAmount"]
        
        #初始化汇总字段的值为0
        self.countList = {}
        for i in self.countColumn:
            self.countList[str(i)] = 0
    
    def queryData(self):
          
        #判断开始时间和结束时间
        sdate = self.dateTimeEdit.dateTime()
         
        edate = self.dateTimeEdit_2.dateTime()
        if sdate.toTime_t() > edate.toTime_t():
            self.boxWarning(u'提示', u'您输入的起始时间晚于截止时间!')
            return
        #获取时间
        start = str(self.dateTimeEdit.text())
        end = str(self.dateTimeEdit_2.text())
        
        
        #获取卡号
        noid = str(self.lineEdit.text().replace(' ',''))
        
        #获取客户名称
        customername = str(self.lineEdit_2.text().replace(' ',''))
        
        #获取变更类型
        
        ctype  = str(self.comboBox.currentIndex())
        
        data = {"start":str(start),"end":str(end),"name":str(customername),"ctype":str(ctype),"noid":str(noid)}
        data = {'node':'logic','act_fun':'queryCustomerAccount','data':data}
        self.dayreportmodel = getDataThread(data,0,"queryCustomerAccount")
        self.connect(self.dayreportmodel,SIGNAL("queryCustomerAccount"),self.getData)
        self.dayreportmodel.start()
    
    def getData(self,data):  #清空表格
        data = data 
        #清空统计数据
        self.clearData((self.tableWidget,(self.countList,0)))
        
        if not data["stat"]:
            self.boxWarning(u'提示', u'没有符合条件的记录')
            return
        data = data["data"]
        self.names = []
        for d in data:
            d['nameAndCard'] = d['name'] + '(' + d['noid'] + ')'
            self.names.append(d['name'])
        self.insertTable(data)
    
    #插入数据到表格
    def insertTable(self,data):
        self.tableWidget.setRowCount(len(data))
        for i,value in enumerate(data):
            for j in range(self.tableWidget.columnCount()):
                item = QTableWidgetItem(unicode(str(value[self.columnName[j]])))
                self.formatTableItem(item,self.table_fmt_list[j])
                item.setData(Qt.UserRole,value["id"])
                self.tableWidget.setItem(i,j,item)
                if j in self.countColumn:
                    self.countList[str(j)] += float(value[self.columnName[j]])
                    
        if len(self.countColumn)>0:
            rowCount = self.tableWidget.rowCount()
            self.tableWidget.setRowCount(rowCount+1)
            self.tableWidget.setItem(rowCount,0,QTableWidgetItem(u"合计：%s条记录"%len(data)))
            for key,value in self.countList.items():
                item = QTableWidgetItem(str(value))
                self.tableWidget.setItem(rowCount,int(key),item)
                self.formatTableItem(item,self.table_fmt_list[int(key)])
    
    def showDetail(self, row, col):
        uid =  int(self.tableWidget.currentItem().data(Qt.UserRole).toString())
        data = {
                'uid':uid,
                'ctype':self.comboBox.currentIndex(),
                'start':self.dateTimeEdit.dateTime(),
                'end':self.dateTimeEdit_2.dateTime(),
                'name':self.tr(self.names[row])}
        CustomerAccountDetail(data).show()
