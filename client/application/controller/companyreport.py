#coding: utf-8
'''
Created on 2015年2月1日

@author: kylin

公司资金报表
'''
from application.lib.Commethods import *
from application.view.companyreport import Ui_Dialog
from application.lib.commodel import getDataThread
from application.controller.companydetailreport import CompanyDetailReport


class CompanyReportContorller(ControllerAction,Ui_Dialog,PrintAction):
    def __init__(self,parent=None):
        #初始化界面
        ControllerAction.__init__(self,parent)
        #初始化打印
        PrintAction.__init__(self, u"公司资金统计表")
        #是否初始化经办人
        self.addComboBox = True
        #设置查询的 开始、结束时间
        self.dateEdit.setDate(QDate().currentDate())
        self.dateEdit.setCalendarPopup(True)
#         
        self.dateEdit_2.setDate(QDate().currentDate())
        self.dateEdit_2.setCalendarPopup(True)
        #设置信号槽
        self.setSIGNAL()
        #设置表单字段格式
        self.setTableFormat()
        #查询数据
        self.queryData()
       
    def setSIGNAL(self):
        self.connect(self.pushButton_4,SIGNAL("clicked()"),self.queryData)
#         #打印报表
        self.connect(self.pushButton_5,SIGNAL("clicked()"),self.printTo)
        #导出excel
        self.connect(self.pushButton_6,SIGNAL("clicked()"),self.generateExcel)
        #字段配置
        self.connect(self.pushButton_7,SIGNAL("clicked()"),self.configColumn)
        #打印预览
        self.connect(self.pushButton_8,SIGNAL("clicked()"),self.prePrint)
        #双击打开详情页
        self.connect(self.tableWidget,SIGNAL("itemDoubleClicked (QTableWidgetItem *)"),self.showDetail)
        #时间修改
#         self.connect(self.dateEdit,SIGNAL("dateChanged (const QDate&)"),self.queryData)
#         self.connect(self.dateEdit_2,SIGNAL("dateChanged (const QDate&)"),self.queryData)
        #经办人修改
        self.connect(self.comboBox_3,SIGNAL("currentIndexChanged (int)"),self.queryData)
        #点击详情
        self.connect(self.pushButton,SIGNAL("clicked()"),self.showDetail)
    
    def showDetail(self):
        try:
            #经办人id
            if(self.tableWidget.currentRow()<0):
                
                self.infoBox(u"请选择经办人")
                return
            uid =  int(self.tableWidget.currentItem().data(Qt.UserRole).toString())
        except:
            return
        
        #获取时间
        jbr = self.tableWidget.item(self.tableWidget.currentRow(),0).text()
        start = str(self.dateEdit.text())
        end = str(self.dateEdit_2.text())
        data = {"uid":uid,"start":start,"end":end,"jbr":jbr}
        
        self.detail = CompanyDetailReport(data,self)
        self.detail.show()
    
    def setTableFormat(self):
        #字段格式
        self.table_fmt_list = []
        self.table_fmt_list.append({"alignment":"center","color":"black","format":"general","count":False})
        self.table_fmt_list.append({"alignment":"right","color":"black","format":"#,##0.00","count":True})
        self.table_fmt_list.append({"alignment":"right","color":"black","format":"#,##0.00","count":True})
        self.table_fmt_list.append({"alignment":"right","color":"black","format":"#,##0.00","count":True})
        
        #需要汇总的字段
        self.countColumn = [key for key,value in enumerate(self.table_fmt_list) if value['count'] == True]
        
        #表格列匹配数据库字段
        self.columnName = ["nickname","czall","txall","jyall"]
        
        #初始化汇总字段的值为0
        self.countList = {}
        for i in self.countColumn:
            self.countList[str(i)] = 0
      
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
        
        #获取经办人
        index = self.comboBox_3.currentIndex()
        if  index== 0:
            uid = 0
        else:
            uid = self.comboBox_3.itemData(index).toString()
        data = {"start":str(start),"end":str(end),"uid":str(uid)}
        data = {'node':'logic','act_fun':'queryJingbanren','data':data}
        self.dayreportmodel = getDataThread(data,0,"queryJingbanren")
        self.connect(self.dayreportmodel,SIGNAL("queryJingbanren"),self.getData)
        self.dayreportmodel.start()
    
    #处理数据
    def getData(self,data):
        #清空表格
        #清空统计数据
        data = data
        self.clearData((self.tableWidget,(self.countList,0)))
        
        if not data["stat"]:
            self.boxWarning(u'提示', u'没有符合条件的记录')
            return
        data = data["data"]
        if self.addComboBox:
            for value in data:
                self.comboBox_3.addItem(value["nickname"],value["id"])
#         self.comboBox_3.clear()
            self.addComboBox = False
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
                    self.countList[str(j)] += value[self.columnName[j]]
                    
        if len(self.countColumn)>0:
            rowCount = self.tableWidget.rowCount()
            self.tableWidget.setRowCount(rowCount+1)
            self.tableWidget.setItem(rowCount,0,QTableWidgetItem(u"合计：共%s条记录"%len(data)))
            for key,value in self.countList.items():
                item = QTableWidgetItem(str(value))
                self.tableWidget.setItem(rowCount,int(key),item)
                self.formatTableItem(item,self.table_fmt_list[int(key)])
                
