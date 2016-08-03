#coding: utf-8
'''
Created on 2015年2月1日

@author: kylin

客户资金报表
'''
import decimal
from application.lib.Commethods import *
from application.view.zhuanzhanglist import Ui_Dialog
from application.lib.commodel import getDataThread
import application.lib.formatCheck as check
from PyQt4.Qt import *

class ZhuanZhangAccount(ControllerAction,Ui_Dialog,PrintAction):
    
    def __init__(self,parent=None):
        #初始化界面
        ControllerAction.__init__(self,parent)
        #初始化打印
        PrintAction.__init__(self, u"客户资金统计表")

        #设置查询的 开始、结束时间
        self.dateEdit.setDate(QDate().currentDate())
        self.dateEdit.setCalendarPopup(True)
        
        self.dateEdit_2.setDate(QDate().currentDate())
        self.dateEdit_2.setCalendarPopup(True)
        
        dateTime = self.dateEdit_2.dateTime()
        dateTime = dateTime.addDays(1).addSecs(-1)
        self.dateEdit_2.setDateTime(dateTime)
        
        self.connect(self.webView, SIGNAL("loadProgress(int)"),self.init)   #打印替换内容
        filename = 'file:///'+os.getcwd()+'/print/print.html'
        self.webView.load(QUrl(filename.encode('cp936')))
        #设置信号槽
        self.setSIGNAL()
        
        #设置表单字段格式
        self.setTableFormat()
        #查询数据
        self.queryData()  
        check.stringFilter(self.lineEdit_2, "[\d\s]+$")
    
    #获取打印内容   
    def init(self,numbers):
        if numbers == 100:
            frame = self.webView.page().mainFrame()
            self.document = frame.documentElement()
        
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
        #重打印凭条
        self.connect(self.pushButton_6, SIGNAL("clicked()"), self.printhzd)
        
        self.connect(self.comboBox, SIGNAL("currentIndexChanged(int)"), self.queryData)
        
    def setTableFormat(self):
        #字段格式
        self.table_fmt_list = []
        self.table_fmt_list.append({"alignment":"center","color":"black","format":"general","count":False})
        self.table_fmt_list.append({"alignment":"center","color":"black","format":"general","count":False})
        self.table_fmt_list.append({"alignment":"center","color":"black","format":"general","count":False})
        self.table_fmt_list.append({"alignment":"center","color":"black","format":"general","count":False})
        self.table_fmt_list.append({"alignment":"right","color":"black","format":"#,##0.00","count":True})
        self.table_fmt_list.append({"alignment":"center","color":"black","format":"time","count":False,"time":"%Y-%m-%d %H:%M:%S"})
        self.table_fmt_list.append({"alignment":"center","color":"black","format":"enum","count":False,"enum":["结算中心转账","终端转账","终端支付"]})
        self.table_fmt_list.append({"alignment":"right","color":"black","format":"#,##0.00","count":False})
        self.table_fmt_list.append({"alignment":"right","color":"black","format":"#,##0.00","count":False})
        self.table_fmt_list.append({"alignment":"left","color":"black","format":"general","count":False})
        
        #需要汇总的字段
        self.countColumn = [key for key,value in enumerate(self.table_fmt_list) if value['count'] == True]
        
        #表格列匹配数据库字段
        self.columnName = ["payname","paycard","incomename","incomecard",
                           "amount","cdate","ctype","paybalance","payeebalance","txt"]
        self.tableWidget.setColumnCount(10)
        self.tableWidget.setHorizontalHeaderLabels([self.tr(u'转出用户'), self.tr(u'转出卡号'), self.tr(u'转入用户'), 
                                                   self.tr(u'转入卡号'), self.tr(u'转账金额'), self.tr(u'转账时间'), 
                                                   self.tr(u'转账类型'), self.tr(u'转出卡余额'), self.tr(u'转入卡余额'), self.tr(u'备注')])
        self.tableWidget.setAutoFillBackground(True)
        #初始化汇总字段的值为0
        self.countList = {}
        for i in self.countColumn:
            self.countList[str(i)] = 0
    
    def setTableFormat1(self):
        #字段格式
        self.table_fmt_list = []
        self.table_fmt_list.append({"alignment":"center","color":"black","format":"general","count":False})
        self.table_fmt_list.append({"alignment":"center","color":"black","format":"general","count":False})
        self.table_fmt_list.append({"alignment":"right","color":"black","format":"#,##0.00","count":True})
        self.table_fmt_list.append({"alignment":"center","color":"black","format":"time","count":False,"time":"%Y-%m-%d %H:%M:%S"})
        self.table_fmt_list.append({"alignment":"center","color":"black","format":"enum","count":False,"enum":["现金充值","POS机刷卡充值","现金提现","银行卡提现"]})
        self.table_fmt_list.append({"alignment":"center","color":"black","format":"#,##0.00","count":False})
        self.table_fmt_list.append({"alignment":"left","color":"black","format":"general","count":False})
        
        #需要汇总的字段
        self.countColumn = [key for key,value in enumerate(self.table_fmt_list) if value['count'] == True]
        
        #表格列匹配数据库字段
        self.columnName = ['membername', 'noid', 'amount', 'cdate', 'ctype', 'balance', 'txt']
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setHorizontalHeaderLabels([self.tr(u'用户名'), self.tr(u'金荣卡号'), self.tr(u'金额'), 
                                                   self.tr(u'交易时间'), self.tr(u'交易类型'), self.tr(u'卡内余额'), self.tr(u'备注')])
        self.tableWidget.setAutoFillBackground(True)
        #初始化汇总字段的值为0
        self.countList = {}
        for i in self.countColumn:
            self.countList[str(i)] = 0
    
    def queryData(self):
          
        #判断开始时间和结束时间
        sdate = self.dateEdit.dateTime()
         
        edate = self.dateEdit_2.dateTime()
        if sdate.toTime_t() > edate.toTime_t():
            self.boxWarning(u'提示', u'您输入的起始时间晚于截止时间!')
            return
        #获取时间
        start = str(self.dateEdit.text())
        end = str(self.dateEdit_2.text())
        name = str(self.lineEdit.text())
        noid = str(self.lineEdit_2.text())
        self.data = {"start":str(start),"end":str(end), 'type':self.comboBox.currentIndex(), 'name':name, 'noid':noid}
        data = {'node':'logic','act_fun':'queryZhuanZhangAccount','data':self.data}
        self.dayreportmodel = getDataThread(data,0,"queryZhuanZhangAccount")
        self.connect(self.dayreportmodel,SIGNAL("queryZhuanZhangAccount"),self.getData)
        self.dayreportmodel.start()
    
    def getData(self,data):  #清空表格
        data = data
        #清空统计数据
        self.clearData((self.tableWidget,(self.countList,0)))
        
        if not data["stat"]:
            self.infoBox(data["msg"])
            return
        data = data["data"]
        self.datas = data
        if self.data['type'] == 0:
            self.setTableFormat()
        else:
            self.setTableFormat1()
        self.insertTable(data)
    
    #插入数据到表格
    def insertTable(self,data):
        self.tableWidget.setRowCount(len(data))
        for i,value in enumerate(data):
            for j in range(self.tableWidget.columnCount()):
                item = QTableWidgetItem(unicode(str(value[self.columnName[j]])))
                self.formatTableItem(item,self.table_fmt_list[j])
#                 item.setData(Qt.UserRole,value["id"])
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

#人民币金额转大写
    def numtoCny(self,change_number):
        """
        .转换数字为大写货币格式( format_word.__len__() - 3 + 2位小数 )
        change_number 支持 float, int, long, string
        """
        format_word = ["分", "角", "元",
                   "拾","佰","仟","万",
                   "拾","佰","仟","亿",
                   "拾","佰","仟","万",
                   "拾","佰","仟","兆"]
    
        format_num = ["零","壹","贰","叁","肆","伍","陆","柒","捌","玖"]
        if type( change_number ) == str:
            # - 如果是字符串,先尝试转换成float或int.
            if '.' in change_number:
                try:    change_number = float( change_number )
                except: raise ValueError, '%s   can\'t change'%change_number
            else:
                try:    change_number = int( change_number )
                except: raise ValueError, '%s   can\'t change'%change_number
    
        if type( change_number ) == float:
            real_numbers = []
            for i in range( len( format_word ) - 3, -3, -1 ):
                if change_number >= 10 ** i or i < 1:
                    real_numbers.append( int( round( change_number/( 10**i ), 2)%10 ) )
    
        elif isinstance( change_number, (int, long) ):
            real_numbers = [ int( i ) for i in str( change_number ) + '00' ]
    
        else:
            raise ValueError, '%s   can\'t change'%change_number
    
        zflag = 0                       #标记连续0次数，以删除万字，或适时插入零字
        start = len(real_numbers) - 3
        change_words = []
        for i in range(start, -3, -1):  #使i对应实际位数，负数为角分
            if 0 <> real_numbers[start-i] or len(change_words) == 0:
                if zflag:
                    change_words.append(format_num[0])
                    zflag = 0
                change_words.append( format_num[ real_numbers[ start - i ] ] )
                change_words.append(format_word[i+2])
    
            elif 0 == i or (0 == i%4 and zflag < 3):    #控制 万/元
                change_words.append(format_word[i+2])
                zflag = 0
            else:
                zflag += 1
    
        if change_words[-1] not in ( format_word[0], format_word[1]):
            # - 最后两位非"角,分"则补"整"
            change_words.append("整")
    
        return ''.join(change_words)  
    
    #打印回执单    
    def printhzd(self):
        try:
            row = self.tableWidget.currentRow()
            data = self.datas[row]
            print data
        except:
            self.boxWarning(u'提示', u'请选择要打印的数据所在行')
            return
        type = self.comboBox.currentIndex()
        if  type == 0:
            cdate = str(self.tableWidget.item(row, 5).text())
            data = {"start":cdate,"noid":data['paycard'],"end":cdate,"uid":data['uid'],"beizhu":'',"ctype":type,"smoney":'',"bmoney":''}
        
        else:
            cdate = str(self.tableWidget.item(row, 3).text())
            data = {"start":cdate,"noid":data['noid'],"end":cdate,"uid":data['uid'],"beizhu":'',"ctype":type,"smoney":'',"bmoney":''}
        
        print data
        data = {'node':'logic','act_fun':'queryCustomerAccountDetail','data':data}
        self.dayreportmodel1 = getDataThread(data,0,"queryCustomerAccountDetail")
        self.connect(self.dayreportmodel1,SIGNAL("queryCustomerAccountDetail"),self.getPrintData)
        self.dayreportmodel1.start()
    def getPrintData(self, data):
        data = data 
        if not data['stat']:
            self.boxWarning(u'提示', u'获取打印数据失败，请稍后重试')
            return
        self.data = data['data'][0]
        print self.data
        if self.data['ctype'] < 2:
            self.printchongzhi()
        elif self.data['ctype'] < 4:
            self.printquxian()
        else:
            self.printzhuanzhang()
    
    #打印    
    def printchongzhi(self):
        print 'ctype1', self.data['ctype']
        self.printcdate=time.localtime(int(self.data['cdate']))
        self.printcdate=time.strftime('%Y-%m-%d %H:%M',self.printcdate)
        rechargeMoney=locale.format("%.2f",float(self.data['in']), 1)
        self.document.evaluateJavaScript(self.tr("document.getElementById('a1').innerHTML = '时间：")+check.separate(self.tr(str(self.printcdate)))+"'") 
        self.document.evaluateJavaScript(self.tr("document.getElementById('a21').innerHTML = '时间：")+check.separate(self.tr(str(self.printcdate)))+"'") 
        self.document.evaluateJavaScript(self.tr("document.getElementById('a12').innerHTML = '金荣卡号：")+check.separate(self.tr(self.data['cardid']))+"'")   #卡号
        self.document.evaluateJavaScript(self.tr("document.getElementById('a23').innerHTML = '金荣卡号：")+check.separate(self.tr(self.data['cardid']))+"'")   #卡号
        self.document.evaluateJavaScript(self.tr("document.getElementById('a2').innerHTML = '户名：")+check.separate(self.tr(self.data['nickname']))+"'")   #客户名
        self.document.evaluateJavaScript(self.tr("document.getElementById('a22').innerHTML = '户名：")+check.separate(self.tr(self.data['nickname']))+"'")   #客户名
        
        self.document.evaluateJavaScript(self.tr("document.getElementById('a3').innerHTML = '金额：")+check.separate(self.tr(str(rechargeMoney)))+"'") #充值金额
        self.document.evaluateJavaScript(self.tr("document.getElementById('a25').innerHTML = '金额：")+check.separate(self.tr(str(rechargeMoney)))+"'") #充值金额
        bigMoney = self.tr(check.numtoCny(float(self.data['in'])))
        self.document.evaluateJavaScript(self.tr("document.getElementById('a13').innerHTML = '大写："
                                                 )+check.separate(bigMoney.left(11))+"'") #取款金额大写
        if bigMoney.length() > 11:
            self.document.evaluateJavaScript(self.tr("document.getElementById('a14').innerHTML = '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
                                                     )+check.separate(bigMoney.mid(11, 11))+"'") #取款金额大写
        if bigMoney.length() > 22:
            self.document.evaluateJavaScript(self.tr("document.getElementById('a15').innerHTML = '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
                                                     )+check.separate(bigMoney.mid(22, 11))+"'") #取款金额大写
        if self.data['ctype']==0:
            self.document.evaluateJavaScript(self.tr("document.getElementById('a11').innerHTML = '充值方式：现金'")) #支付方式
            self.document.evaluateJavaScript(self.tr("document.getElementById('a24').innerHTML = '充值方式：现金'")) #支付方式
            self.document.evaluateJavaScript(self.tr("document.getElementById('a4').innerHTML = '备注：")+check.separate(self.tr(self.data['txt']))+"'")   #备注
            self.document.evaluateJavaScript(self.tr("document.getElementById('a5').innerHTML = '复核：'")) #支付方式
            self.document.evaluateJavaScript(self.tr("document.getElementById('a26').innerHTML = '备注：")+check.separate(self.tr(self.data['txt']))+"'")   #备注
            if bigMoney.length() > 22:
                self.document.evaluateJavaScript(self.tr("document.getElementById('a16').innerHTML = '经办人："
                                                         )+check.separate(self.tr(self.data['username']))+"'")   #经办人
            else:
                self.document.evaluateJavaScript(self.tr("document.getElementById('a15').innerHTML = '经办人："
                                                         )+check.separate(self.tr(self.data['username']))+"'")   #经办人
                
        else:
            self.document.evaluateJavaScript(self.tr("document.getElementById('a11').innerHTML = '充值方式：银行卡'")) #支付方式
            self.document.evaluateJavaScript(self.tr("document.getElementById('a24').innerHTML = '充值方式：银行卡'")) #支付方式
            self.document.evaluateJavaScript(self.tr("document.getElementById('a4').innerHTML = '流水号：")+check.separate(self.tr(self.data['bankno']))+"'")  #流水号
            self.document.evaluateJavaScript(self.tr("document.getElementById('a26').innerHTML = '流水号：")+check.separate(self.tr(self.data['bankno']))+"'")  #流水号
            self.document.evaluateJavaScript(self.tr("document.getElementById('a5').innerHTML = '备注：")+check.separate(self.tr(self.data['txt']))+"'")   #备注
            self.document.evaluateJavaScript(self.tr("document.getElementById('a6').innerHTML = '复核：'")) #支付方式
            self.document.evaluateJavaScript(self.tr("document.getElementById('a27').innerHTML = '备注：")+check.separate(self.tr(self.data['txt']))+"'")   #备注
            self.document.evaluateJavaScript(self.tr("document.getElementById('a16').innerHTML = '经办人："
                                                         )+check.separate(self.tr(self.data['username']))+"'")   #经办人
        #开始打印
        
        self.document.evaluateJavaScript("document.body.removeChild(document.getElementById('backimg'))")
        pname = self.cf.get('print_ini', 'defprint')
        if pname=='':
            self.boxWarning(u'提示',u'请选择打印机')
            return
        p = printer.printing(self.tr(pname))
        '保存打印信息到文件'
        try:
            self.webView.print_(p)
        except:
            self.boxWarning(u'提示', u'打印机未就绪，请检查打印服务是否开启')
            return
        self.boxWarning(u'提示',u'正在打印凭据，打印完成后请关闭此窗口！')
        
#打印    
    def printquxian(self):
        print 'ctype2', self.data['ctype']
        self.printcdate=time.localtime(int(self.data['cdate']))
        self.printcdate=time.strftime('%Y-%m-%d %H:%M',self.printcdate)
        self.document.evaluateJavaScript(self.tr("document.getElementById('a1').innerHTML = '时间：")+check.separate(self.tr(str(self.printcdate)))+"'")
        self.document.evaluateJavaScript(self.tr("document.getElementById('a21').innerHTML = '时间：")+check.separate(self.tr(str(self.printcdate)))+"'")
        self.document.evaluateJavaScript(self.tr("document.getElementById('a12').innerHTML = '金荣卡号：")+check.separate(self.tr(self.data['cardid']))+"'")   #卡号
        self.document.evaluateJavaScript(self.tr("document.getElementById('a23').innerHTML = '金荣卡号：")+check.separate(self.tr(self.data['cardid']))+"'")   #卡号
        self.document.evaluateJavaScript(self.tr("document.getElementById('a2').innerHTML = '户名：")+check.separate(self.tr(self.data['nickname']))+"'")
        self.document.evaluateJavaScript(self.tr("document.getElementById('a22').innerHTML = '户名：")+check.separate(self.tr(self.data['nickname']))+"'")   #客户名
        
        quxianMoney=locale.format("%.2f",float(self.data['out']), 1)
        if self.data['ctype']==2:
            self.document.evaluateJavaScript(self.tr("document.getElementById('a11').innerHTML = '取款方式：现金'")) #支付方式
            self.document.evaluateJavaScript(self.tr("document.getElementById('a24').innerHTML = '取款方式：现金'")) #支付方式
            self.document.evaluateJavaScript(self.tr("document.getElementById('a3').innerHTML = '金额：")+check.separate(self.tr(str(quxianMoney)))+"'") #取款金额
            self.document.evaluateJavaScript(self.tr("document.getElementById('a25').innerHTML = '金额：")+check.separate(self.tr(str(quxianMoney)))+"'") #取款金额
            self.document.evaluateJavaScript(self.tr("document.getElementById('a4').innerHTML = '备注：")+check.separate(self.tr(self.data['txt']))+"'") #备注
            self.document.evaluateJavaScript(self.tr("document.getElementById('a26').innerHTML = '备注：")+check.separate(self.tr(self.data['txt']))+"'") #备注
            self.document.evaluateJavaScript(self.tr("document.getElementById('a5').innerHTML = '复  核：'")) #复核
            bigMoney = self.tr(check.numtoCny(float(self.data['out'])))
            self.document.evaluateJavaScript(self.tr("document.getElementById('a13').innerHTML = '大写："
                                                     )+check.separate(bigMoney.left(11))+"'") #取款金额大写
            if bigMoney.length() > 11:
                self.document.evaluateJavaScript(self.tr("document.getElementById('a14').innerHTML = '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
                                                         )+check.separate(bigMoney.mid(11, 11))+"'") #取款金额大写
            if bigMoney.length() > 22:
                self.document.evaluateJavaScript(self.tr("document.getElementById('a15').innerHTML = '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
                                                         )+check.separate(bigMoney.mid(22, 11))+"'") #取款金额大写
                self.document.evaluateJavaScript(self.tr("document.getElementById('a16').innerHTML = '经办人："
                                                         )+check.separate(self.tr(self.data['username']))+"'")   #经办人
            else:
                self.document.evaluateJavaScript(self.tr("document.getElementById('a15').innerHTML = '经办人："
                                                         )+check.separate(self.tr(self.data['username']))+"'")   #经办人
        else:
            self.document.evaluateJavaScript(self.tr("document.getElementById('a11').innerHTML = '取款方式：银行卡'")) #支付方式
            self.document.evaluateJavaScript(self.tr("document.getElementById('a24').innerHTML = '取款方式：银行卡'")) #支付方式
            self.document.evaluateJavaScript(self.tr("document.getElementById('a3').innerHTML = '转入银行：")+check.separate(self.tr(self.data['bankname']))+"'") #银行名称
            self.document.evaluateJavaScript(self.tr("document.getElementById('a25').innerHTML = '转入银行：")+check.separate(self.tr(self.data['bankname']))+"'") #银行名称
            self.document.evaluateJavaScript(self.tr("document.getElementById('a14').innerHTML = '转入卡号：")+check.separate(self.tr(self.data['bankcard']))+"'")         #银行账号
            self.document.evaluateJavaScript(self.tr("document.getElementById('a27').innerHTML = '转入卡号：")+check.separate(self.tr(self.data['bankcard']))+"'")         #银行账号
            self.document.evaluateJavaScript(self.tr("document.getElementById('a4').innerHTML = '转入户名：")+check.separate(self.tr(self.data['bankusername']))+"'")  #银行账户开户人
            self.document.evaluateJavaScript(self.tr("document.getElementById('a26').innerHTML = '转入户名：")+check.separate(self.tr(self.data['bankusername']))+"'")  #银行账户开户人
            self.document.evaluateJavaScript(self.tr("document.getElementById('a5').innerHTML = '金额：")+check.separate(self.tr(str(quxianMoney)))+"'") #取款金额
            self.document.evaluateJavaScript(self.tr("document.getElementById('a28').innerHTML = '金额：")+check.separate(self.tr(str(quxianMoney)))+"'") #取款金额
            self.document.evaluateJavaScript(self.tr("document.getElementById('a6').innerHTML = '备注：")+check.separate(self.tr(self.data['txt']))+"'") #备注
            self.document.evaluateJavaScript(self.tr("document.getElementById('a29').innerHTML = '备注：")+check.separate(self.tr(self.data['txt']))+"'") #备注
            self.document.evaluateJavaScript(self.tr("document.getElementById('a7').innerHTML = '复  核：'")) #复核
            bigMoney = self.tr(str(check.numtoCny(float(self.data['out']))))
            self.document.evaluateJavaScript(self.tr("document.getElementById('a15').innerHTML = '大写："
                                                     )+check.separate(bigMoney.left(11))+"'") #取款金额大写
            if bigMoney.length() > 11:
                self.document.evaluateJavaScript(self.tr("document.getElementById('a16').innerHTML = '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
                                                         )+check.separate(bigMoney.mid(11, 11))+"'") #取款金额大写
            if bigMoney.length() > 22:
                self.document.evaluateJavaScript(self.tr("document.getElementById('a17').innerHTML = '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
                                                         )+check.separate(bigMoney.mid(22, 11))+"'") #取款金额大写
                self.document.evaluateJavaScript(self.tr("document.getElementById('a18').innerHTML = '经办人："
                                                         )+check.separate(self.tr(self.data['username']))+"'")   #经办人
            else:
                self.document.evaluateJavaScript(self.tr("document.getElementById('a17').innerHTML = '经办人："
                                                         )+check.separate(self.tr(self.data['username']))+"'")   #经办人
        #开始打印
        self.document.evaluateJavaScript("document.body.removeChild(document.getElementById('backimg'))")
        pname = self.cf.get('print_ini', 'defprint')
        if pname=='':
            self.boxWarning(u'提示',u'请选择打印机')
            return
        p = printer.printing(self.tr(pname))
        '保存打印信息到文件'
        try:
            self.webView.print_(p)
        except:
            self.boxWarning(u'提示', u'打印机未就绪，请检查打印服务是否开启')
            return
        self.boxWarning(u'提示',u'正在打印凭据，打印完成后请关闭此窗口！')

    #打印    
    def printzhuanzhang(self):
        print 'ctype3', self.data['ctype']
        self.printcdate=time.localtime(int(self.data['cdate']))
        self.printcdate=time.strftime('%Y-%m-%d %H:%M',self.printcdate)
        self.document.evaluateJavaScript(self.tr("document.getElementById('a1').innerHTML = '时间：")+check.separate(self.tr(str(self.printcdate)))+"'") 
        self.document.evaluateJavaScript(self.tr("document.getElementById('a21').innerHTML = '时间：")+check.separate(self.tr(str(self.printcdate)))+"'") 
        self.document.evaluateJavaScript(self.tr("document.getElementById('a12').innerHTML = '金荣卡号：")+check.separate(self.tr(self.data['cardid']))+"'")   #转出卡号
        self.document.evaluateJavaScript(self.tr("document.getElementById('a23').innerHTML = '金荣卡号：")+check.separate(self.tr(self.data['cardid']))+"'")   #转出卡号
        self.document.evaluateJavaScript(self.tr("document.getElementById('a13').innerHTML = '转入卡号：")+check.separate(self.tr(self.data['othercard']))+"'")   #转入卡号
        self.document.evaluateJavaScript(self.tr("document.getElementById('a25').innerHTML = '转入卡号：")+check.separate(self.tr(self.data['othercard']))+"'")   #转入卡号
        self.document.evaluateJavaScript(self.tr("document.getElementById('a2').innerHTML = '户名：")+check.separate(self.tr(self.data['nickname']))+"'")   #客户名
        self.document.evaluateJavaScript(self.tr("document.getElementById('a22').innerHTML = '户名：")+check.separate(self.tr(self.data['nickname']))+"'")   #客户名
        self.document.evaluateJavaScript(self.tr("document.getElementById('a3').innerHTML = '转入户名：")+check.separate(self.tr(self.data['othername']))+"'")   #转入客户名
        self.document.evaluateJavaScript(self.tr("document.getElementById('a24').innerHTML = '转入户名：")+check.separate(self.tr(self.data['othername']))+"'")   #转入客户名
        self.document.evaluateJavaScript(self.tr("document.getElementById('a5').innerHTML = '备注：'"))  #备注
        self.document.evaluateJavaScript(self.tr("document.getElementById('a27').innerHTML = '备注：'"))   #备注
        self.document.evaluateJavaScript(self.tr("document.getElementById('a6').innerHTML = '复核：'")) #复核
        amount = self.data['in']
        if self.data['in'] == 0:
            amount = self.data['out']
        bigMoney = self.tr(check.numtoCny(float(amount)))
        zmoney=locale.format("%.2f",float(amount), 1)
        self.document.evaluateJavaScript(self.tr("document.getElementById('a4').innerHTML = '金额：")+check.separate(self.tr(zmoney))+"'") #充值金额
        self.document.evaluateJavaScript(self.tr("document.getElementById('a26').innerHTML = '金额：")+check.separate(self.tr(zmoney))+"'") #充值金额
        
        self.document.evaluateJavaScript(self.tr("document.getElementById('a14').innerHTML = '大写："
                                                 )+check.separate(bigMoney.left(11))+"'") #取款金额大写
        if bigMoney.length() > 11:
            self.document.evaluateJavaScript(self.tr("document.getElementById('a15').innerHTML = '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
                                                     )+check.separate(bigMoney.mid(11, 11))+"'") #取款金额大写
        if bigMoney.length() > 22:
            self.document.evaluateJavaScript(self.tr("document.getElementById('a16').innerHTML = '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
                                                     )+check.separate(bigMoney.mid(22, 11))+"'") #取款金额大写
            self.document.evaluateJavaScript(self.tr("document.getElementById('a17').innerHTML = '经办人："
                                                     )+check.separate(self.tr(self.data['username']))+"'")   #经办人
        else:
            self.document.evaluateJavaScript(self.tr("document.getElementById('a16').innerHTML = '经办人："
                                                         )+check.separate(self.tr(self.data['username']))+"'")   #经办人
        self.document.evaluateJavaScript(self.tr("document.getElementById('a11').innerHTML = '转账方式：转账'")) #支付方式
             
        #开始打印
        self.document.evaluateJavaScript("document.body.removeChild(document.getElementById('backimg'))")
        pname = self.cf.get('print_ini', 'defprint')
        if pname=='':
            self.boxWarning(u'提示',u'请选择打印机')
            return
        p = printer.printing(self.tr(pname))
        '保存打印信息到文件'
        try:
            self.webView.print_(p)
        except:
            self.boxWarning(u'提示', u'打印机未就绪，请检查打印服务是否开启')
            return
        self.boxWarning(u'提示',u'正在打印凭据，打印完成后请关闭此窗口！')
