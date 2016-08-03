#coding:utf-8

from application.lib.Commethods import *
from application.view.quyuxiaoshoutongji import Ui_Dialog

    

class QuYuScale(ControllerAction,Ui_Dialog,PrintAction):
    def __init__(self,parent = None):
        ControllerAction.__init__(self, parent)
        PrintAction.__init__(self,u"区域销售统计表")
        self.setTable()
        self.setStyleSheet("""QGroupBox{font-size:18px;margin-top:10px;padding:14px;border:2px solid #6cb479;border-radius:10px;}
                                QGroupBox::indicator{width:130px;height:130px;}
                                QGroupBox::title{font-size:20px;left:15px;margin-top:-15px;}
                                QTableWidget{border:2px solid #6cb479;border-radius:5px;}
                                """)
        self.tableWidget.setAlternatingRowColors(True);
        
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows); #选择整行 【推荐】
        self.tableWidget.verticalHeader().hide()
#         self.connect(self.table, SIGNAL("cellPressed(int,int)"),self.test)
        self.connect(self.pushButton, SIGNAL("clicked()"),self.testdd)
        self.connect(self.pushButton_2, SIGNAL("clicked()"),self.generateExcel)
        self.connect(self.pushButton_3, SIGNAL("clicked()"),self.printTo)
        self.connect(self.pushButton_5, SIGNAL("clicked()"),self.prePrint)
        self.connect(self.pushButton_4, SIGNAL("clicked()"),self.configColumn)
    
        self.tableWidget.horizontalHeader().setResizeMode(QHeaderView.Stretch)
#         self.table.horizontalHeader().setResizeMode(QHeaderView.Stretch)#【推荐】
    def testdd(self):
        dlg = KDialog(self)
        dlg.exec_()
    
    def setTable(self):    
        
        self.tableWidget.setRowCount(10)
#         alignment,color,format,count
        self.table_fmt_list = []
        self.table_fmt_list.append({"alignment":"left","color":"black","format":"general","count":False})
        self.table_fmt_list.append({"alignment":"left","color":"black","format":"general","count":False})
        self.table_fmt_list.append({"alignment":"left","color":"black","format":"0","count":True})
        self.table_fmt_list.append({"alignment":"right","color":"black","format":"#,##0.00","count":True})
        self.table_fmt_list.append({"alignment":"right","color":"black","format":"#,##0.00","count":True})
        self.table_data_list = ["苹果","水果",11,123.2,123434321]
        
        #
        countColumn = [key for key,value in enumerate(self.table_fmt_list) if value['count'] == True]
        
        print countColumn
        countList = {}
        for i in countColumn:
            countList[str(i)] = 0
        
        for i in range(10):
            for j in range(5):
                item = QTableWidgetItem(unicode(str(self.table_data_list[j])))
                self.formatTableItem(item,self.table_fmt_list[j])
                self.tableWidget.setItem(i,j,item)
                if j in countColumn:
                    countList[str(j)] += self.table_data_list[j]
                    
        if len(countColumn)>0:
            rowCount = self.tableWidget.rowCount()
            self.tableWidget.setRowCount(rowCount+1)
            self.tableWidget.setItem(rowCount,0,QTableWidgetItem(u"共计："))
            for key,value in countList.items():
                item = QTableWidgetItem(str(value))
                self.tableWidget.setItem(rowCount,int(key),item)
                self.formatTableItem(item,self.table_fmt_list[int(key)])
    
    def test(self,x,y):
        print x,y
        
#         self.verticalLayout.addWidget()
            