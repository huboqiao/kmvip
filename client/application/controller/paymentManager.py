# -*- coding: utf-8 -*-
'''
Created on 2015年4月15日
缴费管理
@author: huaan
'''
from PyQt4 import QtGui
from application.lib.Commethods import *
from application.view.paymentManager import Ui_Dialog
from application.controller.payNow import PayNow
from application.controller.paySelected import PaySelected
from application.controller.addPaymentToRecord import AddPaymentToRecord
from application.controller.alterPayment import AlterPayment
from application.lib.commodel import getDataThread
import application.lib.formatCheck as check
import xlrd, datetime

class PaymentManager(ControllerAction,PrintAction, Ui_Dialog):
    def __init__(self,parent=None):
        ControllerAction.__init__(self,parent)
        PrintAction.__init__(self, u'缴费管理')
        self.toPayRecord = [] # 保存要批量付款的单据编号
        self.tableWidget.horizontalHeader().setResizeMode(QHeaderView.Stretch)      #铺满表格
        self.parent=parent
        
        self.comboBox_2.setCurrentIndex(2)
        self.dateEdit.setCalendarPopup(True)
        self.dateEdit_2.setCalendarPopup(True)
        date = QDate().currentDate()
        self.dateEdit.setDate(date.addDays(1 - date.day()).addMonths(-1))
        self.dateEdit_2.setDate(date)
        
        self.connect(self.lineEdit, SIGNAL("returnPressed()"), self.structQueryFilter)
        self.connect(self.lineEdit_2, SIGNAL("returnPressed()"), self.structQueryFilter)
        self.connect(self.pushButton, SIGNAL("clicked()"), self.structQueryFilter)
        self.connect(self.pushButton_2, SIGNAL("clicked()"), self.importFromXls)
        self.connect(self.pushButton_3, SIGNAL("clicked()"), self.addPaymentToRecord)  #　添加缴费项目到记录
        self.connect(self.pushButton_4, SIGNAL("clicked()"), self.AlterPayment)  # 待缴费单详情
        self.connect(self.pushButton_5, SIGNAL("clicked()"), self.deletePayment)  # 删除待缴费单
        self.connect(self.pushButton_6, SIGNAL("clicked()"), self.printTo)  # 打印
        self.connect(self.pushButton_7, SIGNAL("clicked()"), self.generateExcel)  # 导出到Excel列表
        self.connect(self.tableWidget, SIGNAL("cellClicked(int, int)"), self.rowSelected)  # 单击一行
        self.connect(self.tableWidget, SIGNAL("cellDoubleClicked(int, int)"), self.paymentDetail)  # 单击一行
        self.queryData()
        check.stringFilter(self.lineEdit, "[\d\s]+$")
    
    #打印报表
    def printTo(self):
   
        if self._getHtml() == "":
            return
        try:
            printer.printreport(self.tr(self.printname),self.html)
            self.boxInfo(u'提示', u'打印完成')
        except:
            self.boxInfo(u'提示', u'打印未完成')
        
    # 删除待缴费单    
    def deletePayment(self):
        # 没有任意一行被勾选
        if len(self.toPayRecord) == 0:
            # 没有高亮状态的单元格
            if self.selectedRecord is None:
                self.boxWarning(u'提示', u'请选择要删除的带缴费单！')
                return
            # 有高亮状态的行
            else:
                if cmp(str(self.selectedRecord['stat']), u'未付款') == 0:
                    toDeleteIds = [self.selectedRecord['id']]
                else:
                    self.boxWarning(u'提示', u'已缴费记录不可以删除！')
                    return
                    
        # 勾选了最少一行
        else:
            toDeleteIds = []
            for record in self.toPayRecord:
                toDeleteIds.append(record['id'])
        if not self.boxConfirm(u'提示', u'确定要删除编号为%s的%s条待缴费单吗？'%(toDeleteIds, len(toDeleteIds))):
            return
        data = {'node':'logic','act_fun':'deletePayments','data':toDeleteIds}
        self.myThread = getDataThread(data,0,"deletePayments")
        self.connect(self.myThread, SIGNAL("deletePayments"), self.deleteResult)
        self.myThread.start()
    # 待缴费单删除结果处理    
    def deleteResult(self, data):
        data = data
        self.boxWarning(msg=data['msg'])
        if data['stat']:
            self.queryData(False)
    # 从excel导入待缴费单        
    def importFromXls(self):
        fileName = str(QFileDialog.getOpenFileName(self, u"请选择Excel文件", "/", self.tr("Excel Files(*.xls *.xlsx)"))) 
        fileName = fileName.decode('utf8').encode('cp936')
        bk = xlrd.open_workbook(fileName)
        try:
            sh = bk.sheet_by_name("Sheet1")
        except:
            self.boxWarning(msg = u"no sheet in %s named sheet1"%fileName.decode('cp936'))
            return 
        ncols = sh.ncols
        if ncols != 6:
            self.boxWarning(msg=u'选中文件的sheet1中表头应为6个字段')
            return
        headers = [u'用户名', u'金荣卡号', u'缴费项目', u'金额', u'最后缴费期限',  u'备注']
        headerNames = ['A', 'B', 'C', 'D', 'E', 'F']
        for col in range(6):
            if cmp(sh.cell_value(0, col), headers[col]) != 0:
                self.boxWarning(msg=u'请确保第%s列第一行为“%s”且相应的数据准确'%(headerNames[col], headers[col]))
                return
        nrows = sh.nrows
        datas = []
        for row in range(1, nrows):
            data = {}
            try:
                data['name'] = str(sh.cell_value(row, 0)).encode('utf8')
            except:
                self.boxWarning(u'提示', u'第%s行用户名不能为空'%(row+1))
                return
            try:
                data['card'] = str(sh.cell_value(row, 1)).encode('utf8')
            except:
                self.boxWarning(u'提示', u'第%s行金荣卡号不能为空'%(row+1))
                return
            try:
                data['payType'] = str(sh.cell_value(row, 2)).encode('utf8')
                if self.comboBox.findText(self.tr(data['payType'])) == -1:
                    self.boxWarning(u'提示', u'第%s行缴费项目不存在'%(row+1))
                    return
            except:
                self.boxWarning(u'提示', u'第%s行缴费项目不能为空'%(row+1))
                return
            try:
                data['payMoney'] = str(sh.cell_value(row, 3)).encode('utf8')
            except:
                self.boxWarning(u'提示', u'第%s行缴费金额不能为空'%(row+1))
                return
            try:
                data['endDate'] = xlrd.xldate_as_tuple(sh.cell_value(row, 4), 0)
                data['endDate'] = str(data['endDate'][0]) + '/' + str(data['endDate'][1]) + '/' + str(data['endDate'][2])
#                 data['endDate'] = data['endData'].encode('utf8')
                if check.checkDate(data['endDate']) is None:
                    self.boxWarning(u'提示', u'第%s行最后缴费日期格式不支持，支持格式（yyyy/mm/dd）'%(row+1))
                    return
            except:
                self.boxWarning(u'提示', u'第%s行最后缴费日期格式不支持，正确格式（yyyy/mm/dd）'%(row+1))
                return
            try:
                data['txt'] = str(sh.cell_value(row, 5)).encode('utf8')
            except:
                pass
            today = datetime.datetime.now()
            data['startDate'] = today.strftime("%Y/%m/%d").encode('utf8')
            datas.append(data)
        if len(datas) == 0:
            self.boxWarning(u'提示', u'没有可导入的数据，请确认数据正确性')
            return
        self.addPaymentToRecord1({'method':'daoru', 'datas':datas})
    # 组装查询条件
    def structQueryFilter(self):
        index = self.comboBox.currentIndex()
        data = {'cardid':str(self.lineEdit.text()),
                'name':str(self.lineEdit_2.text()),
                'type':self.types[index - 1]['id'],
                'statu':self.comboBox_2.currentIndex(),
                'startDate':str(self.dateEdit.text()),
                'endDate':str(self.dateEdit_2.text())}
        if index == 0:
            data['type'] = ''
        self.queryData(False, data)
    # 检索缴费单和缴费类型    
    def queryData(self, isQueryType=True, data=''):
        self.selectedRecord = None
        self.toPayRecord = []
        self.pushButton_4.setEnabled(False)
        self.pushButton_5.setEnabled(False)
        
        self.tableWidget.setColumnCount(8)
        self.setTableFormat()
        self.tableWidget.setRowCount(0)
        data = {'isQueryType':isQueryType, 'data':data}
        data = {'node':'logic','act_fun':'queryData','data':data}
        self.myThread = getDataThread(data,0,"queryData")
        self.connect(self.myThread, SIGNAL("queryData"), self.dataHandling)
        self.myThread.start()
    # 添加缴费项目到记录
    def addPaymentToRecord(self):
        self.toAddRecordData = ''
        if AddPaymentToRecord(self).exec_():
            self.addPaymentToRecord1({'method':'add', 'datas':[self.toAddRecordData]})
    # 添加缴费项目到记录
    def addPaymentToRecord1(self, data):
        data = {'node':'logic','act_fun':'addPayment','data':data}
        self.myThread = getDataThread(data,0,"addPayment")
        self.connect(self.myThread, SIGNAL("addPayment"), self.addResult)
        self.myThread.start()
    # 添加待缴费记录的结果处理    
    def addResult(self, data):
        if data['stat']:
            self.boxWarning(u'提示', data['msg'])
            self.queryData(False)
        else:
            self.boxConfirm(u'提示', data['data'][0]['failReason'], u'确定', u'取消')
    # 缴费单详细信息    
    def AlterPayment(self):
        if cmp(self.selectedRecord['stat'], u'未付款') == 0:
            if AlterPayment(self).exec_():
                self.queryData(False)
        else:
            self.boxWarning(u'提示', u'已付款单据不可修改！')
    # 存在缴费项目则显示在表格，不存在则提示
    def dataHandling(self, data):
        data = data 
        try:
            if data['payTypes']['stat']:
                self.comboBox.clear()
                self.comboBox.addItem(u'所有')
                self.types = data['payTypes']['data']
                for payType in self.types:
                    self.comboBox.addItem(payType['typename'])
        except Exception as e:
            print e
        if data['record']['stat']:
            self.paymentRecord = data['record']['data']
            self.insertTable(self.paymentRecord)
            self.insertEighthColumn()
        else:
            self.boxWarning(u'提示', u'无记录')
    # 插入第八列（操作）
    def insertEighthColumn(self):
        try:
            self.disconnect(self.tableWidget, SIGNAL('cellChanged(int, int)'), self.statChanged)
        except:
            pass
        self.tableWidget.setColumnCount(9)
        self.tableWidget.setHorizontalHeaderLabels([self.tr(u'编号'), self.tr(u'金荣卡号'), 
                                                    self.tr(u'用户名'), self.tr(u'缴费项目'), 
                                                    self.tr(u'付款日期'), self.tr(u'录单日期'), 
                                                    self.tr(u'金额'), self.tr(u'备注'), self.tr(u'操作')])
        # 添加最后一列复选框、付款按钮
        for row in range(self.tableWidget.rowCount() - 1):
            if cmp(self.paymentRecord[row]['stat'].decode('utf-8'), u'未付款') == 0:
                ckb = QCheckBox()
                ckb.setStatusTip(self.tr(str(row)))
                btn = QPushButton(self.tr('付    款'))
                btn.setStatusTip(self.tr(str(row)))
                hLayout = QHBoxLayout()
                hLayout.setMargin(0)
                hLayout.addWidget(ckb)
                hLayout.setAlignment(ckb, Qt.AlignCenter)
                hLayout.addWidget(btn)
                wgt = QWidget()
                wgt.setLayout(hLayout)
                self.tableWidget.setCellWidget(row, 8, wgt)
                self.connect(ckb, SIGNAL('stateChanged(int)'), self.statChanged)
                self.connect(btn, SIGNAL('clicked()'), self.payNow)
                
        # 最后一行的全选、批量付款按钮
        self.ckb = QCheckBox()
        self.btn = QPushButton(self.tr('批量付款'))
        hLayout = QHBoxLayout()
        hLayout.setMargin(0)
        hLayout.addWidget(self.ckb)
        hLayout.setAlignment(self.ckb, Qt.AlignCenter)
        hLayout.addWidget(self.btn)
        wgt = QWidget()
        wgt.setLayout(hLayout)
        self.tableWidget.setCellWidget(self.tableWidget.rowCount() - 1, 8, wgt)
        self.connect(self.ckb, SIGNAL('stateChanged(int)'), self.changeAllState)
        self.connect(self.btn, SIGNAL('clicked()'), self.paySelected)
        self.btn.setEnabled(False)
    # 全选/取消全选
    def changeAllState(self, state):
        if state == 2:
            for ckb in self.findChildren(QtGui.QCheckBox):
                ckb.setCheckState(Qt.Checked)
        elif state == 0:
            for ckb in self.findChildren(QtGui.QCheckBox):
                ckb.setCheckState(Qt.Unchecked)
            
    # 勾选/取消勾选
    def statChanged(self, state):
        row = self.sender().statusTip()
        # 勾选
        if state == 2:
            self.btn.setEnabled(True)
            for ckb in self.findChildren(QtGui.QCheckBox):
                if ckb.statusTip() == row:
                    ckb.setCheckState(Qt.Checked)
                    self.pushButton_5.setEnabled(True)
                    self.toPayRecord.append(self.paymentRecord[row.toInt()[0]])
        # 取消勾选           
        elif state == 0:
            for ckb in self.findChildren(QtGui.QCheckBox):
                if ckb.statusTip() == row:
                    ckb.setCheckState(Qt.Unchecked)
                    self.toPayRecord.remove(self.paymentRecord[row.toInt()[0]])
            if len(self.toPayRecord) == 0:
                self.ckb.setCheckState(Qt.Unchecked)
                self.btn.setEnabled(False)
                self.pushButton_5.setEnabled(False)
                self.pushButton_4.setEnabled(False)
                    
    # 单据详情
    def paymentDetail(self, row):
        if row == self.tableWidget.rowCount() - 1:
            return
        self.toPayRecord = [self.paymentRecord[row]]
        if cmp(str(self.paymentRecord[row]['stat']), u'未付款') == 0:
            self.AlterPayment()
            return 
        PayNow(self, u'单据详情').exec_()
        self.toPayRecord = []
            
    # 单独付款
    def payNow(self):
        self.toPayRecord = [self.paymentRecord[self.sender().statusTip().toInt()[0]]]
        self.payAct = 1
        if PayNow(self, u'缴费').exec_():
            self.pay()
        else:
            self.selectedRecord = None
    
    # 批量付款
    def paySelected(self):
        self.payAct = 1       
        selectedId = [] 
        print 'self.toPayRecord', self.toPayRecord
        self.selectedRecordPaytype = []
        self.selectedRecordCount = 0
        for record in self.toPayRecord:
            print self.tr(record['typename'])
            try:
                selectedId.append(record['cid'])
                self.selectedRecordPaytype.append(record['typename'])
                self.selectedRecordCount += record['amount']
                if len(set(selectedId)) != 1:
                    self.boxWarning(msg=u'您选择了不同客户的待缴费项目，批量缴\n费只支持缴纳单个客户的一项或多项费用！')
                    self.selectedRecordPaytype = []
                    self.selectedRecordCount = 0
                    return
            except:
                pass
        if PaySelected(self).exec_():
            self.pay()

    # 缴费
    def pay(self):
        datas = []
        for record in self.toPayRecord:
            data = {'method': self.payAct, 'zcid' : record['cid'],
                    'zccard': record['noid'], 'uid': self.appdata['user']['user_id'],
                    'id': record['id'], 'money':record['amount']}
            datas.append(data)
        
        self.myThread = getDataThread({'node':'logic','act_fun':'payNow','data':datas},0,"payNow")
        self.connect(self.myThread, SIGNAL("payNow"), self.payResult)
        self.myThread.start()
    
    # 付款结果
    def payResult(self, data):
        data = data
        self.boxWarning(u'提示', data['msg'])
        self.queryData()
    
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
            self.tableWidget.setItem(rowCount,0,QTableWidgetItem(u"合计：%s条记录"%len(data)))
            for key,value in self.countList.items():
                item = QTableWidgetItem(str(value))
                self.tableWidget.setItem(rowCount,int(key),item)
                self.formatTableItem(item,self.table_fmt_list[int(key)])
    # 设置表格每列的格式
    def setTableFormat(self):
        #字段格式
        self.table_fmt_list = []
        self.table_fmt_list.append({"alignment":"center","color":"black","format":"general","count":False})
        self.table_fmt_list.append({"alignment":"center","color":"black","format":"general","count":False})
        self.table_fmt_list.append({"alignment":"center","color":"black","format":"general","count":False})
        self.table_fmt_list.append({"alignment":"center","color":"black","format":"general","count":False})
        self.table_fmt_list.append({"alignment":"center","color":"black","format":"general","count":False})
        self.table_fmt_list.append({"alignment":"center","color":"black","format":"general","count":False})
        self.table_fmt_list.append({"alignment":"right","color":"black","format":"#,##0.00","count":True})
        self.table_fmt_list.append({"alignment":"left","color":"black","format":"general","count":False})
        #需要汇总的字段
        self.countColumn = [key for key,value in enumerate(self.table_fmt_list) if value['count'] == True]
        #表格列匹配数据库字段
        self.columnName = ["id","noid","membername",'typename','stat','cdate','amount','txt']
        #初始化汇总字段的值为0
        self.countList = {}
        for i in self.countColumn:
            self.countList[str(i)] = 0
    # 点击表格   
    def rowSelected(self, row, col):
        if row == self.tableWidget.rowCount() - 1:
            self.selectedRecord = None
            self.pushButton_4.setEnabled(False)
            try:
                if len(self.toPayRecord) == 0:
                    self.pushButton_5.setEnabled(False)
            except:
                self.pushButton_5.setEnabled(False)
            return
        self.pushButton_4.setEnabled(True)
        self.pushButton_5.setEnabled(True)
        self.selectedRecord = self.paymentRecord[row]
        
