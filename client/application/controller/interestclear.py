#coding:utf-8

from application.lib.Commethods import *
from application.view.interestclear import Ui_Dialog
from application.lib.commodel import getDataThread
from application.controller.interestpayinfo import InterestPayInfoController
from PyQt4 import QtGui

class InterestClear(ControllerAction,Ui_Dialog,PrintAction):
    
    def __init__(self,parent = None):
        ControllerAction.__init__(self, parent, u'利息列表')
        PrintAction.__init__(self, u'利息列表')
        self.pushButton_2.setEnabled(False)
        #设置查询的 开始、结束时间
        now = QDate().currentDate()
        self.dateEdit.setDate(now.addDays(-now.day() + 1))
        self.dateEdit_2.setDate(now)
        
        self.setSIGNAL()
        self.queryData()
    # 设置信号槽            
    def setSIGNAL(self):
        self.connect(self.pushButton,SIGNAL("clicked()"),self.queryData)
        self.connect(self.pushButton_2,SIGNAL("clicked()"),self.pay)
        self.connect(self.checkBox, SIGNAL("stateChanged(int)"), self.selectAll)
        self.connect(self.pushButton_3, SIGNAL("clicked()"), self.printTo)
        self.connect(self.pushButton_4, SIGNAL("clicked()"), self.generateExcel)
        
    def selectAll(self, stat):
        checkBoxs = self.findChildren(QtGui.QCheckBox)
        for checkBox in checkBoxs:
            checkBox.setCheckState(stat)
        
    # 定义表格样式和数据
    def setTableFormat(self):
        #字段格式
        self.table_fmt_list = []
        self.table_fmt_list.append({"alignment":"center","color":"black","format":"general","count":False})
        self.table_fmt_list.append({"alignment":"right","color":"black","format":"#,##0.00","count":True})
        self.table_fmt_list.append({"alignment":"center","color":"black","format":"enum","count":False,"enum":["未结算","已结算"]})
        #需要汇总的字段
        self.countColumn = [key for key,value in enumerate(self.table_fmt_list) if value['count'] == True]
        #表格列匹配数据库字段
        self.columnName = ["membername","rates","payed"]
        #初始化汇总字段的值为0
        self.countList = {}
        for i in self.countColumn: 
            self.countList[str(i)] = 0
    # 检索时间段内未结算的利息        
    def queryData(self):
        self.setTableFormat()
        self.pushButton_2.setEnabled(False)
        #获取时间
        start = str(self.dateEdit.text())
        end = str(self.dateEdit_2.text())
        data = {"start":str(start),"end":str(end),"cardid":"","payed":0}
        data = {'node':'logic','act_fun':'ratesList','data':data}
        self.dayreportmodel = getDataThread(data,0,"ratesList")
        self.connect(self.dayreportmodel,SIGNAL("ratesList"),self.getData)
        self.dayreportmodel.start()
    # 检索结果处理    
    def getData(self,data):
        data = data
        #清空统计数据
        self.clearData((self.tableWidget,))
        if not data["stat"]:
            self.infoBox(u'该时间段内没有未结算的利息！')
            return
        self.currentRate = data['currentRate']
        self.label_3.setText(u'当前利率：' + str(data['currentRate']))
        
        self.pushButton_2.setEnabled(True)
        self.data = data['data']
        self.start = data['start']
        self.end = data['end']
        self.insertTable(self.data)
    # 插入数据到表格
    def insertTable(self,data):
        self.tableWidget.setRowCount(len(data))
        for i,value in enumerate(data):
            for j in range(self.tableWidget.columnCount()):
                try:
                    item = QTableWidgetItem(unicode(str(value[self.columnName[j]])))
                    self.formatTableItem(item,self.table_fmt_list[j])
    #                 item.setData(Qt.UserRole,value["id"])
                    self.tableWidget.setItem(i,j,item)
                    if j in self.countColumn:
                        self.countList[str(j)] += value[self.columnName[j]]
                except:
                    cbox = QCheckBox(u"结    算")
                    cbox.setCheckState(Qt.Unchecked)
                    item = KCellWidget(cbox,value["cid"])
                    self.tableWidget.setCellWidget(i,j,item)
                    
        if len(self.countColumn)>0:
            rowCount = self.tableWidget.rowCount()
            self.tableWidget.setRowCount(rowCount+1)
            item = QTableWidgetItem(u"合计：%s条记录"%len(data))
            item.setTextAlignment(Qt.AlignCenter)
            self.tableWidget.setItem(rowCount, 0, item)
            for key,value in self.countList.items():
                item = QTableWidgetItem(str(value))
                self.tableWidget.setItem(rowCount,int(key),item)
                self.formatTableItem(item,self.table_fmt_list[int(key)])
    # 点击结算按钮            
    def pay(self):
        self.toPayRates = []
        counts = int(self.tableWidget.rowCount()) 
        if counts==0:
            self.boxWarning(u'提示', u'此时间段没有需要支付的利息！')
            return
        self.conunt_price = 0
        for i in range(counts):
            try:
                item = self.tableWidget.cellWidget(i, 3)
                if item.widget.checkState() == Qt.Checked:
                    self.toPayRates.append(self.data[i])
                    self.conunt_price += self.data[i]['rates']
            except:
                continue
        if len(self.toPayRates) <= 0:
            self.boxWarning(u'提示', u'没有选择结算用户！')
            return
        self.dates=u'发放'+self.tr(str(self.start)+u'日至 '+self.tr(str(self.end)))+u'日的利息'
        win=InterestPayInfoController(self)
        win.exec_()
    # 去结算    
    def goPay(self):
        data = {'rate':self.currentRate,"start":self.start,"end":self.end,'data':self.toPayRates, 'uid':self.appdata['user']['user_id']}
        data = {'node':'logic','act_fun':'payRates','data':data}
        self.dayreportmodel = getDataThread(data,0,"payRates")
        self.connect(self.dayreportmodel,SIGNAL("payRates"),self.afterPay)
        self.dayreportmodel.start()
        self.waitingbox = self.infoBox(u"结算中，请稍候......")
    # 结算结果处理
    def afterPay(self,data):
        data = data 
        self.waitingbox.close()
        self.boxWarning(u'提示', data['msg'])
        if data['stat']:
            self.queryData()
        else:
            self.tableWidget.setRowCount(0)
            self.tableWidget.setHorizontalHeaderLabels([self.tr(u'姓名'), self.tr(u'利息'), 
                                                        self.tr(u'是否结算'), self.tr(u'结算失败原因')])
            self.resetTableFormat()
            self.insertTable(data['data'])
    # 定义表格样式和数据
    def resetTableFormat(self):
        #字段格式
        self.table_fmt_list = []
        self.table_fmt_list.append({"alignment":"center","color":"black","format":"general","count":False})
        self.table_fmt_list.append({"alignment":"right","color":"black","format":"#,##0.00","count":True})
        self.table_fmt_list.append({"alignment":"center","color":"black","format":"enum","count":False,"enum":["未结算","已结算"]})
        self.table_fmt_list.append({"alignment":"left","color":"black","format":"general","count":False})
        #需要汇总的字段
        self.countColumn = [key for key,value in enumerate(self.table_fmt_list) if value['count'] == True]
        #表格列匹配数据库字段
        self.columnName = ["membername","rates","payed","failReason"]
        #初始化汇总字段的值为0
        self.countList = {}
        for i in self.countColumn: 
            self.countList[str(i)] = 0
        
