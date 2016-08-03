# -*- coding: utf-8 -*-
'''
Created on 2015年2月4日

@author: LiuXinwu
'''
from PyQt4 import QtGui
from application.lib.Commethods import *
from application.view.orderlist import Ui_Dialog
from application.model.orderlist_model import OrderListModel
from application.controller.orderAlter import OrderAlterController
from application.controller.orderDetail import OrderDetailController
from application.lib.commodel import getDataThread

import time

class OrderListController(ControllerAction,Ui_Dialog):
    def __init__(self,parent=None):
        ControllerAction.__init__(self,parent)
        self.tableWidget.horizontalHeader().setResizeMode(QHeaderView.Stretch)      #铺满表格
        self.parent=parent

        #实例化Model类
        self.model = OrderListModel()

        self.connect(self.pushButton, SIGNAL("clicked()"),self.alterOrder)
        self.connect(self.pushButton_2, SIGNAL("clicked()"),self.detailOrder)
        self.connect(self.pushButton_3, SIGNAL("clicked()"),self.delOrder)
        self.connect(self.pushButton_4, SIGNAL("clicked()"),self.selectOrderList)
     
        self.connect(self.tableWidget, SIGNAL("itemClicked (QTableWidgetItem*)"), self.outSelect)
        self.connect(self.tableWidget, SIGNAL("cellDoubleClicked (int,int)"), self.detailOrder)
        self.iid = []
        self.fillCombox()
        
        data = {'node':'logic','act_fun':'getOrderList','data':''}   
        self.dayreportmodel = getDataThread(data,0,"getOrderList")
        self.connect(self.dayreportmodel,SIGNAL("getOrderList"),self.init)
        self.dayreportmodel.start() 
        
    
    #初始化立即查询订单列表
    def init(self,re):
        try:
            if re['stat'] == True:
                self.storeInfo(re['data'])
        except:
            self.boxWarning(u'提示', u'连接服务器超时，请重新登录！')
            
    #初始化即填满订单生成者也是采购员的comboBox 
    def fillCombox(self):
        #调用的model类方法，查询出所有订单生成者姓名
        datas = self.model.queryNickname()
        #对数据进行处理
        if datas['stat']==True:
           for i in range(len(datas['data'])):
               #取出一行真名
               data = datas['data'][i]
               name = data['nickname']   
               #将名字插入comboBox_3里
               self.comboBox_3.addItem(name)
               
               #取id
               id = data['id']
               #将id添加到元组中
               self.iid.append(id)

    #接收到所有订单信息
    def storeInfo(self,data):
        self.tableWidget.setRowCount(0) 
        self.pushButton.setEnabled(False)   #修改按钮
        self.pushButton_2.setEnabled(False) #详情按钮
        self.pushButton_3.setEnabled(False) #删除按钮
        if data:
            for i in range(len(data)):
                self.updateTable(data[i])
            
    #更新表格
    def updateTable(self,data):
        #根据uid取出对应的用户真名
        try:
            username = self.model.queryOrderUsername(str(data['uid']))
            username = username['data']['nickname']
        except:
            username = '无'
        
        counts = int(self.tableWidget.rowCount()) 
        self.tableWidget.setRowCount(counts+1)
        #id
        id = QTableWidgetItem(self.tr(str(data['id'])))
        id.setTextAlignment(Qt.AlignCenter|Qt.AlignVCenter)
        id.setFlags(Qt.ItemIsEnabled)
        #订单编码
        ordersn = QTableWidgetItem(self.tr(str(data['ordersn'])))
        ordersn.setFlags(Qt.ItemIsEnabled)
        #佣金"%.2f" % a
        price = QTableWidgetItem(self.tr(str("%.2f" % data['price'])))
        price.setTextAlignment(Qt.AlignRight|Qt.AlignVCenter)
        price.setFlags(Qt.ItemIsEnabled)
        #订单生成者
        nickname = QTableWidgetItem(self.tr(str(username)))
        nickname.setTextAlignment(Qt.AlignCenter|Qt.AlignVCenter)
        nickname.setFlags(Qt.ItemIsEnabled)
        #订单方式
        if data['pstat'] == 0:
            self.way = "指派"
        else:
            self.way = "竞价"
        pstat = QTableWidgetItem(self.tr(str(self.way)))
        pstat.setTextAlignment(Qt.AlignCenter|Qt.AlignVCenter)
        pstat.setFlags(Qt.ItemIsEnabled)
        #订单接收者
        result = self.model.queryApplyName(str(data['cid']))
        try:
            result = result['data']['membername']
        except:
            result='无接收者'
        orderrec = QTableWidgetItem(self.tr(str(result)))
        orderrec.setTextAlignment(Qt.AlignCenter|Qt.AlignVCenter)
        orderrec.setFlags(Qt.ItemIsEnabled)
        
        #查询这一订单下所有商品的总价和，即订单总额
        rez = self.model.querySumZongjia(str(data['id']))
        amount =  "%.2f" % rez['data']['amount']
        amounts = QTableWidgetItem(self.tr(str(amount)))
        amounts.setTextAlignment(Qt.AlignRight|Qt.AlignVCenter)
        amounts.setFlags(Qt.ItemIsEnabled)
        
        #判断状态
        if data['ostat']==0:
           ostat = QTableWidgetItem(self.tr(str("关闭")))
           ostat.setFlags(Qt.ItemIsEnabled)
        if data['ostat']==1:
           ostat = QTableWidgetItem(self.tr(str("未入库")))
           ostat.setFlags(Qt.ItemIsEnabled)
        if data['ostat']==2:
           ostat = QTableWidgetItem(self.tr(str("已入库")))
           ostat.setFlags(Qt.ItemIsEnabled)
        if data['ostat']==3:
           ostat = QTableWidgetItem(self.tr(str("发货中")))
           ostat.setFlags(Qt.ItemIsEnabled)
        if data['ostat']==4:
           ostat = QTableWidgetItem(self.tr(str("完成")))
           ostat.setFlags(Qt.ItemIsEnabled)
        ostat.setTextAlignment(Qt.AlignCenter|Qt.AlignVCenter)
          
        hstat = u'否'
        if data['hstat'] != 0:
            hstat = u'是'
        hstat = QTableWidgetItem(self.tr(hstat))
        hstat.setTextAlignment(Qt.AlignCenter|Qt.AlignVCenter)
        hstat.setFlags(Qt.ItemIsEnabled)
           
        self.tableWidget.setItem(counts,0,id)
        self.tableWidget.setItem(counts,1,ordersn)
        self.tableWidget.setItem(counts,2,price)
        self.tableWidget.setItem(counts,3,nickname)
        self.tableWidget.setItem(counts,4,ostat)
        self.tableWidget.setItem(counts,5,pstat)
        self.tableWidget.setItem(counts,6,orderrec)
        self.tableWidget.setItem(counts,7,amounts)
        self.tableWidget.setItem(counts,8,hstat)
        
    #选择某单元格
    def outSelect(self,itme=None):
        self.id=self.tableWidget.item(itme.row(),0).text()
        self.ordersn=self.tableWidget.item(itme.row(),1).text()
        self.nickname=self.tableWidget.item(itme.row(),3).text()
        self.pushButton.setEnabled(True)
        self.pushButton_2.setEnabled(True)
        self.pushButton_3.setEnabled(True)


    #修改订单
    def alterOrder(self):
        win=OrderAlterController(self, self.id, self.ordersn)
        win.exec_()
        
    #订单详情与订单_info详情
    def detailOrder(self):
        win = OrderDetailController(self, self.id, self.ordersn)
        win.exec_()
        
    #删除订单
    def delOrder(self):
        button=QMessageBox.question(self,u"提示",u"确定要删除id为："+self.tr(str(self.id))+u"的订单?",QMessageBox.Ok|QMessageBox.Cancel,QMessageBox.Ok) 
        #获得订单状态
        data = self.model.getOneOrder(str(self.id))
        orderstat = data['data']['ostat']  
        if orderstat>1:
           #订单状态已入库，不能被删除了
           self.boxWarning(u'提示', u'订单状态已入库或以上，不能删除！')    
        else:          
           if button==QMessageBox.Ok:
                re = self.model.delOrder(str(self.id))
                self.delInfo(re)
                return
                try:
                    re = self.model.delOrder({'id':self.id})
                    self.delInfo(re)
                except:
                    self.boxWarning(u'提示', u'连接服务器超时，请重新登录！')
                
    #删除结果信息
    def delInfo(self,data):
        if data['stat'] == 1:
            self.boxInfo(u'提示',u'删除订单成功！')
        else:
            self.boxWarning(u'提示',data['msg'])
            
        data = {'node':'logic','act_fun':'getOrderList','data':''}   
        self.dayreportmodel = getDataThread(data,0,"getOrderList")
        self.connect(self.dayreportmodel,SIGNAL("getOrderList"),self.init)
        self.dayreportmodel.start() 
    
    #接收经过筛选后的所有订单
    def ordersInfo(self,data):
        self.tableWidget.setRowCount(0) 
        if data:
            for i in range(len(data)):
                self.updateTable(data[i])
    
    
    #根据条件筛选orderlist
    def selectOrderList(self):
        #获取查询条件
        index = self.comboBox_3.currentIndex()-1
        ostat = self.comboBox_2.currentIndex()-1
        pstat = self.comboBox.currentIndex()-1
        if ostat==-1:
           ostat='' 
        if pstat==-1:
           pstat=''
        #整理参数(讲汉子全转换成数字)
        if index >= 0:
           uid = self.iid[index]
        else:
           uid=''
        
        #组装参数
        param = {'uid':str(uid),'ostat':str(ostat),'pstat':str(pstat)}
        #调用model类函数查询数据
#         datas = self.model.filterOrderList(param) 
        #self.xx(datas)
        data = {'node':'logic','act_fun':'filterOrderList','data':param}   
        self.fo = getDataThread(data,0,"filterOrderList")
        self.connect(self.fo,SIGNAL("filterOrderList"),self.xx)
        self.fo.start()
        
    def xx(self,data):  
        #处理数据，数据位元组 
        if data['stat']==True:
           self.ordersInfo(data['data'])
        else:
            #清楚以前数据
            self.tableWidget.setRowCount(0) 
            #提示用户没有信息
            self.boxWarning(u'提示', u'没有符合查询条件的订单，请重新选择查询条件！')
        
        
        
        
        
