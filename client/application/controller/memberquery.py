# -*- coding: utf-8 -*-
'''
Created on 2014年9月28日

@author: huaan
'''
# from PyQt4 import QtGui
from application.lib.Commethods import *
from application.view.memberquery import Ui_Dialog
from application.lib.ImageProcess import ImageProcess
from application.controller.cardrecord import CardRecordController
from application.model.memberQuery import MemberQueryModel
from application.lib.commodel import getDataThread
from application.model.cardInfo_model import CardInfo
from application.controller.customerAccountDetail import CustomerAccountDetail
from application.controller.advancedQuery import AdvancedQueryController
import application.lib.formatCheck as check
import json

class MemberqueryContorller(ControllerAction,Ui_Dialog, PrintAction):
    def __init__(self,parent = None):
        ControllerAction.__init__(self,parent)
        self.parent = parent
        PrintAction.__init__(self, u'客户列表')
        self.queryData = {}
        
        self.idcardImage = QImage(self.shenfenzhengimage)            #加载身份证图片
        self.idcardimageLabel = QLabel(self.shenfenzhengimage)         #身份证图像标签 
        self.idcardImage_t = QImage(self.shenfenzhengimage_t)            #加载身份证反面图片
        self.idcardimageLabel_t = QLabel(self.shenfenzhengimage_t)         #身份证反面图像标签         
        self.zhaopian = QImage(self.groupBox_4)                      #加载照片图片
        self.zhaopianimageLabel = QLabel(self.groupBox_4) #照片图像标签 
        
        self.tableWidget.horizontalHeader().setResizeMode(QHeaderView.Stretch)      #铺满表格
        self.queryMemberModel = MemberQueryModel()
        self.move(0, 0)
        self.memberQuery()
        check.stringFilter(self.s_tel, "^[1][3-8]+\\d{9}$")
        check.stringFilter(self.s_idcard, "^[1-9]\d{5}[1-9]\d{3}((0\d)|(1[0-2]))(([0|1|2]\d)|3[0-1])\d{3}([0-9]|X)$")
        
        self.connect(self.pushButton, SIGNAL("clicked()"),self.memberQuery)
        self.connect(self.s_membername, SIGNAL("returnPressed()"),self.memberQuery)
        self.connect(self.s_tel, SIGNAL("returnPressed()"),self.memberQuery)
        self.connect(self.s_idcard, SIGNAL("returnPressed()"),self.memberQuery)
        self.connect(self.getcard, SIGNAL("clicked()"),self.memberCardList)
        self.connect(self.tableWidget, SIGNAL("itemClicked (QTableWidgetItem*)"), self.outSelect)
        self.connect(self.pushButton_2, SIGNAL('clicked()'), self.generateExcel)
        self.connect(self.pushButton_3, SIGNAL('clicked()'), self.printTo)
        self.connect(self.pushButton_4, SIGNAL('clicked()'), self.prePrint)
        self.connect(self.pushButton_5, SIGNAL('clicked()'), self.advancedQuery)
        self.connect(self.pushButton_6, SIGNAL('clicked()'), self.fundDetails)
    # 高级查询    
    def advancedQuery(self):
        AdvancedQueryController(self,u"高级查询").show()
    # 资金明细
    def fundDetails(self):
        model = CardInfo()
        data = model.getCardInfo(str(self.id))
        if data:
            for card in data:
                if card['stat']:
                    currentCard = card['uid']
                    cardDate = check.timeStamp(card['cdate'], '%Y/%m/%d')
                    start = QDateTime().fromString(cardDate, "yyyy/MM/dd")
                    break
        else:
            self.boxWarning(u'提示',u'该用户没有绑定卡！')
            return
        data = {
                'uid':currentCard,
                'start':start,
                'end':QDateTime().currentDateTime(),
                'name':self.tableWidget.item(self.tableWidget.currentRow(), 1).text(),
                'ctype':0}
        CustomerAccountDetail(data).show()

    #查询客户
    def memberQuery(self):
        self.tableWidget.setRowCount(0)
        self.emptyMemberInfo()
        self.getcard.setEnabled(True)
        self.queryData['name'] = str(self.s_membername.text())
        self.queryData['tel'] = str(self.s_tel.text())
        self.queryData['idCard'] = str(self.s_idcard.text())
        self.queryData['stat'] = 1
        self.queryNow()
    
    #查询
    def queryNow(self):
        data = {'node':'logic','act_fun':'getMemberInfoss','data':self.queryData}
        self.dayreportmodel = getDataThread(data,0,"getMemberInfoss")
        self.connect(self.dayreportmodel, SIGNAL("getMemberInfoss"), self.getSearchResults)
        self.dayreportmodel.start()
        
    #清空客户详情信息
    def emptyMemberInfo(self):
        self.getcard.setEnabled(False)
        self.pushButton_6.setEnabled(False)
        self.membername.setText('')
        self.sex.setCurrentIndex(0)
        self.nation.setText('')
        self.tel.setText('')
        self.amount.setText('')
        self.stat.setText('')
        self.idcard.setText('')
        self.ugroup.setText('')
        self.adduser.setText('')
        self.bankname.setText('')
        self.bankcard.setText('')
        self.adder.setText('')
        self.carddate.setText('')
        self.store.setText('')
        self.cdate.setText('')
        self.bankusername.setText('')
        self.bankadder.setText('')
        img = ImageProcess()
        img.showImage(os.getcwd()+'/image/111.png',self.zhaopianimageLabel,self.zhaopian,10,10,170,170)
        img.showImage(os.getcwd()+'/image/222.png',self.idcardimageLabel,self.idcardImage,10,0,330,170)
        img.showImage(os.getcwd()+'/image/222.png',self.idcardimageLabel_t,self.idcardImage_t,10,0,330,170)
       
    #查询客户用卡记录
    def memberCardList(self):
        model = CardInfo()
        data = model.getCardInfo(str(self.id))
        self.memberCardRecord(data)
    #客户用卡记录
    def memberCardRecord(self,data):
        if data:
            self.cardrecordlist = data
            win = CardRecordController(self)
            win = win.exec_()
        else:
            self.boxWarning(u'提示',u'该用户没有用卡记录！')
    #查询客户详情
    def memberInfo(self,data):
        self.emptyMemberInfo()
        self.getcard.setEnabled(True)
        self.pushButton_6.setEnabled(True)
        self.membername.setText(self.tr(str(data['membername'])))
        self.sex.setCurrentIndex(int(data['sex']))
        self.nation.setText(self.tr(str(data['nation'])))
        self.tel.setText(self.tr(str(data['tel'])))
        self.amount.setText(self.tableWidget.item(self.tableWidget.currentRow(), 3).text())
        self.stat.setText(self.tableWidget.item(self.tableWidget.currentRow(), 4).text())
        self.idcard.setText(self.tr(str(data['idcard'])))
        self.ugroup.setText(self.tr(str(data['groupName'])))
        if str(data['isstorage']) == '0':
            self.store.setText(u'该类型客户无仓位')
        else:
            storeSite = self.tr(str(data['storename']))
            self.store.setText(storeSite)
        addUser = self.tr(str(data['adduser'])) + ' ' + self.tr(str(data['nickname']))
        self.adduser.setText(addUser)
        self.bankname.setText(self.tr(str(data['bankname'])))
        self.bankcard.setText(self.tr(str(data['bankcard'])))
        self.adder.setText(self.tr(str(data['adder'])))
        
        carddate = time.localtime(int(data['carddate']))
        carddate = time.strftime('%Y-%m-%d ',carddate)
        self.carddate.setText(self.tr(str(carddate)))
        
        cdate = time.localtime(int(data['cdate']))
        cdate = time.strftime('%Y-%m-%d %H:%M:%S',cdate)
        self.cdate.setText(self.tr(str(cdate)))
        self.bankusername.setText(self.tr(str(data['bankusername'])))
        self.bankadder.setText(self.tr(str(data['bankadder'])))
        img = ImageProcess()
        if data['useimg_path']:
            fname = img.downloadImg(data['useimg_path'], 'useimg.png')
            if fname != False:
                img.showImage(fname,self.zhaopianimageLabel,self.zhaopian,20,20,150,150)
        if data['cardimg_path']:
            fname = img.downloadImg(data['cardimg_path'], 'cardimg.png')
            if fname != False:
                img.showImage(fname,self.idcardimageLabel,self.idcardImage,10,0,330,170)
        if data['cardimgt_path']:
            fname = img.downloadImg(data['cardimgt_path'], 'cardimgt.png')
            if fname != False:
                img.showImage(fname,self.idcardimageLabel_t,self.idcardImage_t,10,0,330,170)
    
    #接收查询结果
    def getSearchResults(self,data):
        data = data
        self.queryData = {}
        self.tableWidget.setRowCount(0) 
        if not data['stat']:
            return
        self.pushButton.setEnabled(True)
        self.getcard.setEnabled(False)
        self.memberListData = data['data']
        self.setTableFormat()
        self.insertTable(data['data'])
    
    #选择某单元格
    def outSelect(self,itme = None):
        self.emptyMemberInfo()
        self.getcard.setEnabled(True)
        self.pushButton_6.setEnabled(True)
        self.id = self.tableWidget.item(itme.row(),0).text()
        data = self.memberListData
        self.memberInfo(data[self.tableWidget.currentRow()])
                
    def setTableFormat(self):
        #字段格式
        self.table_fmt_list = []
        self.table_fmt_list.append({"alignment":"center","color":"black","format":"general","count":False})
        self.table_fmt_list.append({"alignment":"center","color":"black","format":"general","count":False})
        self.table_fmt_list.append({"alignment":"center","color":"black","format":"general","count":False})
        self.table_fmt_list.append({"alignment":"right","color":"black","format":"#,##0.00","count":True})
        self.table_fmt_list.append({"alignment":"center","color":"black","format":"enum","count":False, "enum":['', u'正常', u'冻结', u'注销']})
        
        #需要汇总的字段
        self.countColumn = [key for key,value in enumerate(self.table_fmt_list) if value['count'] == True]
        
        #表格列匹配数据库字段
        self.columnName = ["id","membername","card","amount",'stat']
        
        #初始化汇总字段的值为0
        self.countList = {}
        for i in self.countColumn:
            self.countList[str(i)] = 0
            
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
            self.tableWidget.setItem(rowCount,0,QTableWidgetItem(u"合计："))
            for key,value in self.countList.items():
                item = QTableWidgetItem(str(value))
                self.tableWidget.setItem(rowCount,int(key),item)
                self.formatTableItem(item,self.table_fmt_list[int(key)])
    