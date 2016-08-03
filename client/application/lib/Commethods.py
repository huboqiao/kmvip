# -*- coding:utf8  -*-
'''
Created on 2015年1月20日

@author: kylin

加载公用的类库

'''
#-------公共模块-------------------------

import ConfigParser
import datetime
import locale
import os, sys
import time

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from pyExcelerator import *

from application.lib.KT import *
from application.lib.PrintMy import printer
from application.lib.openwin import Openwin
from application.lib.servicecontroller import ServiceControl


#-------QT模块    -------------------------
#------------lib------------------
QTextCodec.setCodecForTr(QTextCodec.codecForName("utf8"))

'''
    配置指定字段是否显示
'''
class ConfigColumn(KDialog):
    
    def __init__(self,parent = None):
        KDialog.__init__(self, None)
        #列表配置表格
        self.setColor(QColor.fromRgb(100,100,100))
        self.parent = parent
        self.tableWidget = parent.tableWidget
        self.vlayout = QVBoxLayout(self)
        self.vlayout.setMargin(5)
        self.vlayout.addWidget(QLabel(u'表格字段配置'))
        self.table = KTableWidget()
        column = [u'字段',u'显示']
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(QStringList(column))
        self.vlayout.addWidget(self.table)
        widget = QWidget()
        allbtn = KButton(u"全选")
        yesbtn = KButton(u"确定")
        nobtn = KButton(u"取消")
        hlayout = QHBoxLayout(widget)
        hlayout.setMargin(0)
        hlayout.addWidget(allbtn)
        hlayout.addStretch()
        hlayout.addWidget(yesbtn)
        hlayout.addWidget(nobtn)
        self.vlayout.addWidget(widget)
        
        header = []
        columncount = self.tableWidget.columnCount()
        self.table.setRowCount(columncount)
        for i in range(columncount):
            hitem = self.tableWidget.horizontalHeaderItem(i)
            header.append(str(hitem.text()))
            self.table.setItem(i,0,QTableWidgetItem(hitem.text()))
            cell = KCellWidget(QCheckBox(u"显示"),i)
            if self.tableWidget.isColumnHidden(i):
                cell.widget.setCheckState(Qt.Unchecked) 
            else:
                cell.widget.setCheckState(Qt.Checked) 
            self.table.setCellWidget(i,1,cell)
            cell = self.table.cellWidget(i, 1)
#         self.table.resizeRowsToContents()

        self.vlayout.addStretch()
#         self.table.resize(QSize(self.table.width(),self.table.rowHeight(0)*self.table.rowCount()))
            
        self.connect(allbtn, SIGNAL("clicked()"),self._selectAll)
        self.connect(yesbtn, SIGNAL("clicked()"),self._updateTable)
        self.connect(nobtn, SIGNAL("clicked()"),self.reject)
        
        self.exec_()
        
    #选中所有字段
    def _selectAll(self):    
        for i in range(self.table.rowCount()):
            self.table.cellWidget(i,1).widget.setCheckState(Qt.Checked)
    
    def _updateTable(self):
        
        self.parent.updateTable(self.table)
        self.accept()
        
            
'''
    打印，导出，打印预览
'''
class PrintAction():
    
    def __init__(self,tablename):
        self.tablename = tablename
        self.printname = self.cf.get('print_ini','defprint') #读取打印机配置
        
    #格式化表格数据
    def formatTableItem(self,item,format_list):
        if format_list["alignment"] == "left":
            alignment = Qt.AlignLeft | Qt.AlignVCenter
        if format_list["alignment"] == "right":
            alignment = Qt.AlignRight | Qt.AlignVCenter
        if format_list["alignment"] == "center":
            alignment = Qt.AlignHCenter | Qt.AlignVCenter
        item.setTextAlignment(alignment)
        
        if format_list["color"] == "black":
            color = QColor.fromRgb(0,0,0)
        if format_list["color"] == "red":
            color = QColor.fromRgb(255,0,0)
            
        item.setTextColor(color)
        
        if format_list['format'] == "#,##0.00":
            locale.setlocale(locale.LC_ALL, '')
            item.setText(locale.format("%.2f", float(str(item.text())),True))
        
        if format_list['format'] == "enum":
            item.setText(unicode(format_list['enum'][int(str(item.text()))]))
        
        
        if format_list['format'] == "time":
            if(int(str(item.text())) == 0):
               
                item.setText("")
            else:
                ltime=time.localtime(int(str(item.text())))
                item.setText(time.strftime(format_list["time"], ltime))
        
    def configColumn(self):
        ConfigColumn(self)
        
    #更新原表格字段显示与否
    def updateTable(self,table):
        for i in range(table.rowCount()):
            cell = table.cellWidget(i, 1)
            if cell.widget.checkState()== Qt.Unchecked:
                self.tableWidget.setColumnHidden(i,True)
            else:
                self.tableWidget.setColumnHidden(i,False)
                
    #打印报表
    def printTo(self):
   
        if self._getHtml() == "":
            return
        try:
            printer.printreport(self.tr(self.printname),self.html)
            QMessageBox.information(self, u'提示',u'打印完成',u'确    定')
        except:
            QMessageBox.information(self, u'提示',u'打印未完成',u'确    定')
    #打印预览
    def prePrint(self):
            
        if self._getHtml() == "":
            return
        printer.preprint(self.tr(self.printname),self)
        
     
    #打印内容
    def _getHtml(self):
        
        rowcounts = int(self.tableWidget.rowCount())  
        columncounts = int(self.tableWidget.columnCount())
        visibleColumn = [ i for i in range(columncounts) if not self.tableWidget.isColumnHidden(i)]

            
        self.html = '''
                <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
                <html xmlns="http://www.w3.org/1999/xhtml">
                
                <HEAD>
                <META http-equiv=Content-Type content="text/html; charset=utf-8" />
                <TITLE>
                <h4>报表头</h4>
                </TITLE>
                </HEAD>
                
                <BODY LEFTMARGIN=0 TOPMARGIN=0 MARGINWIDTH=0 MARGINHEIGHT=0>
                <table border="1" cellspacing="0" width="100%%" >
                %s
                %s
                %s
                </table>
                </body>
                </html>
            '''
        html_head_1 = """
            <tr> 
                <td colspan='%s' align='center'><h2>%s</h2></td>
            </tr>
            """
        html_head_1 = html_head_1 % (len(visibleColumn),self.tablename) 
       
        html_head_2 = ""
        for i in visibleColumn:
            html_head_2 +="<th>%s</th>" % str(self.tableWidget.horizontalHeaderItem(i).text())
        html_head_2 = "<tr>%s</tr>" % html_head_2
        
        self.htmldata=''
        
        if rowcounts <= 0 or len(visibleColumn) <= 0:
            return ""
    
        for i in range(rowcounts):
            rowdata = ""
            for j in visibleColumn:
                try:
                    rowdata +='<td align="center">%s</td>' % str(self.tableWidget.item(i,j).text())
                except:
                    rowdata +='<td align="center"></td>'
            rowdata = "<tr>%s</tr>" % rowdata
            
            self.htmldata += rowdata
        
        self.html=self.html % (html_head_1,html_head_2,self.htmldata)
        
        return self.html
    
    #导出Excel
    def generateExcel(self):
        counts = int(self.tableWidget.rowCount()) 
        if counts>0:
            filename = QFileDialog.getSaveFileName(self,u'导出excel', './',"*.xls;;*.xlsx")
            if filename!='':
                try:
                    
                    rowcounts = int(self.tableWidget.rowCount())  
                    columncounts = int(self.tableWidget.columnCount())
                    
                    self.columnWidth = [2696 for i in range(columncounts)]
                    visibleColumn = [ i for i in range(columncounts) if not self.tableWidget.isColumnHidden(i)]
                    
                    w = Workbook()     #创建一个工作簿
                    ws = w.add_sheet('Sheet1')     #创建一个工作表
                    style=Style.XFStyle()
#                     style.alignment = Formatting.Alignment.HORZ_CENTER
                    style.alignment.horz = Formatting.Alignment.HORZ_CENTER
                    style.font.height = 300
                    
                    ws.write_merge(0,0,0,len(visibleColumn)-1,unicode(str(self.tablename)),style)
                    
                    style=Style.XFStyle()
#                     style.alignment = Formatting.Alignment.HORZ_CENTER
                    style.alignment.horz = Formatting.Alignment.HORZ_CENTER
                    for key,value in enumerate(visibleColumn):
                        ws.write(1,key,unicode(str(self.tableWidget.horizontalHeaderItem(value).text())),style)  
                    
                    for i in range(rowcounts):
                        
                        for key,value in enumerate(visibleColumn):
                            try:
                                data,style = self.formatExcelItem(self.tableWidget.item(i,value),key)
                                ws.write(i+2,key,data,style)     #在i行1列
                            except:
                                ws.write(i+2,key,"")     #在i行1列
#                         ws.write(i+1,1,(float(unicode(str(self.tableWidget.item(i,2).text()).replace(',','')))))     #在i行2列
                    for key,value in enumerate(self.columnWidth):
                        ws.col(key).width =value 
                    w.save(unicode(filename))     #保存
                    self.boxInfo(u'提示',u'导出excel成功！')
                except:
                    self.boxWarning(u'提示',u'生成excel文件失败！请关闭excel文件再试！')
        else:
            self.boxWarning(u'提示',u'没有数据不要生成excel文件')
            
    #格式化导出Excel单元格数据    
    def formatExcelItem(self,item,key):
        
        style=Style.XFStyle()
        formatformat = self.table_fmt_list[key]["format"]
        try:
            fontwidth = QFontMetrics(item.font()).width(item.text())
            if fontwidth*45 > self.columnWidth[key]:
                self.columnWidth[key] = fontwidth*45
        except:
            pass
        data = ""
        if formatformat == "general":
            data = unicode(str(item.text()))
        elif formatformat == "0":
            try:
                data = int(str(item.text()))
            except:
                data = float(str(item.text()))
        elif formatformat == "#,##0.00":
            data = float(str(item.text()).replace(",",""))
        else:
            data = unicode(str(item.text()))
            
        formatcolor = self.table_fmt_list[key]["color"]
        if formatcolor == "red":
            style.font.colour_index = 0x0A
        style.num_format_str = formatformat
        return data,style
    
class ControllerAction(KDialog):
    """
        @param appdata:dict    存放用户数据（用户登陆信息）
    """
    _tabWidget = None
    appdata = {}
    def __init__(self,parent=None,title=""):
        KDialog.__init__(self,parent,title)
        self.tabid = 0
        self.cf = ConfigParser.ConfigParser()
        self.cf.read('config.ini')
        self.is_move = False
        try:
            self.setupUi(self)
        except:
            pass
        self._updateUi()
        
    def eventFilter(self, event):
            
        return 

        
    def keyPressEvent(self,event):
        if event.key() == Qt.Key_Escape or event.key() == Qt.Key_Return:
            if self.tabid != 0:
                return
        return QDialog.keyPressEvent(self,event)
        
    @staticmethod
    def setTabWidget(tabwidget):
        ControllerAction._tabWidget = tabwidget
        ControllerAction.tabWidget = tabwidget
    
    '''
                    警告弹窗
        @param title: 弹窗标题
        @param msg  : 显示内容  
    '''
    
    def boxWarning(self,title=u'提示',msg=u'您好！'):
        QMessageBox.warning(self, title,msg,u'确    定')
    
    '''
                 提示弹窗
        @param title: 弹窗标题
        @param msg  : 显示内容  
    '''
    def boxInfo(self,title=u'提示',msg=u'您好'):
        QMessageBox.information(self, title,msg,u'确    定')
        
    '''
                   确认弹窗
        @param title: 弹窗标题
        @param msg  : 显示内容  
                    点击OK返回True，Cancel返回False
    '''
        
    def boxConfirm(self, title=u'提示', msg=u'您好', btn1='确    定', btn2='取    消'):
        button = QMessageBox.question(self, title,msg,self.tr(btn1), self.tr(btn2))
        if button == 0:
            return True
        else:
            return False
   
        
    @staticmethod
    def openTab(obj,string):
        for i in range(ControllerAction.tab.count()):
            if str(ControllerAction.tab.tabText(i)) == string:
                ControllerAction.tab.setCurrentIndex(i)
                break
        else:
            obj.setMargin(0)
            ControllerAction.tab.addTab(obj, string)
            ControllerAction.tab.setCurrentIndex(ControllerAction.tab.count() - 1)

    #格式化ui
    def _updateUi(self):
#         for i in self.findChildren(QLayout):
#             print i
# #             print i.getMargin()
#             i.setContentsMargins(0,0,0,0)

        try:
            self.findChildren(QLayout)[0].setMargin(5)
        except:
            pass
        
        qss = """QPushButton{
        border: 1px solid rgb(216,176,112);
        border: 1px solid #ccc;  
        background-color:rgb(216,176,112); 
        background-color:rgb(255,255,255);  
        border-radius:5px;
        padding:5px 5px;  
        }"""
        
        qss +="""
        QPushButton::hover{
        background-color:rgb(204,188,122);
        background-color:rgb(220,220,220);
        border: 1px solid #fff;  

        }
        """
        for i in self.findChildren(QPushButton):
#             print i.getMargin()
            i.setStyleSheet(qss)
            i.setCursor(Qt.PointingHandCursor)
            
        for i in self.findChildren(QTableWidget):
#             print i.getMargin()
            i.setEditTriggers(QAbstractItemView.NoEditTriggers)
            i.setAlternatingRowColors(True);
        
            i.setSelectionBehavior(QAbstractItemView.SelectRows); #选择整行 【推荐】
                            
            i.verticalHeader().hide()
            i.setStyleSheet("""
                    QTableWidget{border:2px solid gray;border-radius:5px;}
                    """)
            i.horizontalHeader().setResizeMode(QHeaderView.Stretch)      #铺满表格
        
        for i in self.findChildren(QGroupBox):
            i.setStyleSheet("""QGroupBox{font-size:16px;margin-top:10px;padding:5px;border:1px solid #6cb479;border-radius:10px;}
                                QGroupBox::indicator{width:130px;height:130px;}
                                QGroupBox::title{font-size:16px;left:15px;margin-top:-15px;}
                            """)
            
            
            
    @staticmethod
    def _closeTab(tabid):
        ControllerAction._tabWidget.removeTab(tabid)
        
    def closeTab(self):
        #关闭当前tab
        ControllerAction._tabWidget.removeTab(ControllerAction._tabWidget.indexOf(self))
        
    def infoBox(self,str):
        
        return KTipWidget(str)
    
    @staticmethod    
    def ffBox(str):
        
        return KTipWidget(str)
        
    def setMargin(self,margin):
        try:
            self.findChildren(QLayout)[0].setMargin(margin)
        except:
            pass
    """
                清空，或者重置数据 
    """
    def clearData(self,dataList):
        ControllerAction.SclearData(dataList)
        
    @staticmethod
    def SclearData(dataList):
        type_tableWidget = type(QTableWidget())
        type_dict = type({})
        type_list = type([])
        for i in dataList:
            try:
                data = i[0]
            except:
                data = i
            try:
                value = i[1]
            except:
                value = None
                
            datatype = type(data) 
            if datatype == type_tableWidget:
#                 data.clearContents()
                data.setRowCount(0)
                continue
            elif datatype == type_dict:
                if value == None:
                    data.clear()
                else :
                    for key in data.keys():
                        data[key] = value
                continue      
            elif datatype == type_list:
                data.clear()
                continue
                
   
            