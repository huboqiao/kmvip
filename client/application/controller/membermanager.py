# -*- coding: utf-8 -*-
'''
Created on 2015年2月27日

@author: LiuXinwu
'''
from PyQt4 import QtGui
from application.lib.Commethods import *
from application.view.membermanager import Ui_Dialog
from application.model.party_model import PartyModel
from application.lib.commodel import getDataThread
from application.controller.membermanageradd import MemberManagerAddController
from PyQt4.Qt import SIGNAL


class MembermanagerController(ControllerAction,Ui_Dialog):
    def __init__(self,parent=None):
        ControllerAction.__init__(self,parent)
        self.tableWidget.horizontalHeader().setResizeMode(QHeaderView.Stretch)      #铺满表格
        self.parent = parent
        #声明数据
        self.idList = []
        self.startQuery = True
        #实例化model
        self.model=PartyModel()
        #初始化
        self.pushButton_3.setEnabled(False)
        self.pushButton_4.setEnabled(False) 
        #绑定事件
        self.connect(self.pushButton_2, SIGNAL("clicked()"),self.adds)
        self.connect(self.pushButton_4, SIGNAL("clicked()"),self.update)
        self.connect(self.pushButton, SIGNAL("clicked()"),self.query)
        self.connect(self.lineEdit, SIGNAL("returnPressed ()"),self.query)
        self.connect(self.pushButton_3, SIGNAL("clicked()"),self.delete)
        self.connect(self.tableWidget, SIGNAL("itemClicked (QTableWidgetItem*)"), self.outSelect)
        self.query()
        
        
    #添加 
    def adds(self):
        self.eid=''
        win = MemberManagerAddController(self)
        win.exec_()
        
    #修改
    def update(self):
        win = MemberManagerAddController(self)
        win.exec_()
        
    #查询数据
    def query(self):
        if not self.startQuery:
            return
        where=str(self.lineEdit.text())

        data = {'node':'logic','act_fun':'getparty','data':where}   
        self.record = getDataThread(data,0,"getparty")
        self.connect(self.record,SIGNAL("getparty"),self.cardRecord)
        self.record.start() 
        self.startQuery = False  #正在查询，标志设为false
    
    def cardRecord(self,data):
        #查询完成，标志设为true
        self.startQuery = True 
        if data['stat']==-1:
            self.boxWarning(u'提示',u'无数据可供查询！')
            return
        self.getSearchResults(data['data'])
     
    #接收查询结果
    def getSearchResults(self,data):
        self.memberListData = data
        self.idList = []#保存供应商id
        self.tableWidget.setRowCount(0) 
        if data:
            for i in range(len(data)):
                self.updateTable(data[i])   
                self.idList.append(data[i]['suppliers_id'])
     
    #更新表格
    def updateTable(self,data):
        counts = int(self.tableWidget.rowCount()) 
        self.tableWidget.setRowCount(counts+1)
        #供应商名称
        comname = QTableWidgetItem(self.tr((data['suppliers_name']).decode('utf8')))
        comname.setFlags(Qt.ItemIsEnabled)
        self.tableWidget.setItem(counts,0,comname)
        #电话
        tel = QTableWidgetItem(self.tr((data['tel']).decode('utf8')))
        tel.setFlags(Qt.ItemIsEnabled)
        self.tableWidget.setItem(counts,1,tel)
        #手机
        phone = QTableWidgetItem(self.tr(str(data['mobile'])))
        phone.setFlags(Qt.ItemIsEnabled)
        self.tableWidget.setItem(counts,2,phone)
        #邮箱 
        email = QTableWidgetItem(self.tr(str(data['email'])))
        email.setFlags(Qt.ItemIsEnabled)
        self.tableWidget.setItem(counts,3,email)
        #地址
        adder = QTableWidgetItem(self.tr(str(data['address'])))
        adder.setFlags(Qt.ItemIsEnabled)
        self.tableWidget.setItem(counts,4,adder)
        #联系人
        man = QTableWidgetItem(self.tr(str(data['linkman'])))
        man.setFlags(Qt.ItemIsEnabled)
        man.setTextAlignment(Qt.AlignCenter|Qt.AlignVCenter)
        self.tableWidget.setItem(counts,5,man)
        #是否停用
        if data['is_check']=='1':
            cf = '否'
        else:
             cf = '是'
        check = QTableWidgetItem(self.tr(str(cf)))
        check.setFlags(Qt.ItemIsEnabled)
        check.setTextAlignment(Qt.AlignCenter|Qt.AlignVCenter)
        self.tableWidget.setItem(counts,6,check)
        #备注
        if data['suppliers_desc']=='null':
            dc = ''
        else:
            dc = data['suppliers_desc']
        desc = QTableWidgetItem(self.tr(str(dc)))
        desc.setFlags(Qt.ItemIsEnabled)
        self.tableWidget.setItem(counts,7,desc)
        
    #点击单元格选中公司
    def outSelect(self,itme):
        self.did = self.idList[itme.row()]
        self.name = self.tableWidget.item(itme.row(),0).text()
        
        self.eid = self.idList[itme.row()]
        self.ename=self.tableWidget.item(itme.row(),0).text()
        self.etel=self.tableWidget.item(itme.row(),1).text()
        self.ephone=self.tableWidget.item(itme.row(),2).text()
        self.eemail=self.tableWidget.item(itme.row(),3).text()
        self.eaddress=self.tableWidget.item(itme.row(),4).text()
        self.eman=self.tableWidget.item(itme.row(),5).text()
        self.ety=self.tableWidget.item(itme.row(),6).text()
        self.edesc=self.tableWidget.item(itme.row(),7).text()
        
        self.pushButton_3.setEnabled(True)
        self.pushButton_4.setEnabled(True) 
    
    #删除   
    def delete(self):
        button=QMessageBox.question(self,"Question",  
                                    self.tr("确定要删除供应商："+str(self.name)+"?"),  
                                    QMessageBox.Ok|QMessageBox.Cancel,  
                                    QMessageBox.Ok)  
        if button==QMessageBox.Ok:
            #先判断该供应商有没有提供货物
            re = self.model.querySupGoods({'suppliers_id':str(self.did)})
            if re['stat']==False:
                json=self.model.delete(str(self.did))
                if json['stat']==-1:
                    self.boxWarning(u'提示',u'删除失败！')
                    return
                self.boxInfo(u'提示',u'删除成功！')
                self.query()
            else:
                self.boxInfo(u'提示', re['msg'])
        