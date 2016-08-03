import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
import time
from distutils.tests.setuptools_build_ext import if_dl

class MyBrowser(QWebView):


    def formatlineEdit(self):
        
        self.lineEdit.setMaximumSize(1, 1)
        self.lineEdit.setWindowOpacity(1);  
        self.lineEdit.setWindowFlags(Qt.FramelessWindowHint);  
        self.lineEdit.setWindowFlags(Qt.Window | Qt.FramelessWindowHint); 
    
    
    
    def initThread(self):
        self.thread = MyThread()
        self.thread.sinOut.connect(self.checkLineEdit)
    
    def checkLineEdit(self,text):
        
#        print self.lineEdit.isVisible()
        if self.lineEdit.isVisible():
                
                self.thread.exit()
                self.thread.terminate()
                
                jsreturn =  self.page().mainFrame().evaluateJavaScript("helloWorld();").toString()
#                 print jsreturn.toUtf8()
                if jsreturn.toUtf8() != '1':
                    self.printStr=jsreturn
                else :
#                     print '1'
                        pass
                
                self.initPrinter()
                self.lineEdit.hide()
                self.thread.start()
    
    def __init__(self, parent = None):
        super(MyBrowser, self).__init__(parent)
        self.setWindowTitle("browser")
        self.id=10000
        self.search()
        self.setWindowOpacity(1);  
        self.setWindowFlags(Qt.FramelessWindowHint);  
        self.showFullScreen()
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint); 
        self.lineEdit = QLineEdit("xx")
        self.formatlineEdit()
        self.lineEdit.hide()
        self.initThread()
        self.connect(self.page().mainFrame(),SIGNAL("javaScriptWindowObjectCleared()"),self.test);
        self.connect(self.lineEdit,SIGNAL("textChanged(const QString&)"),self.pp)
        
            
        
    def test(self):
#         self.page().mainFrame().addToJavaScriptWindowObject("formExtractor", self);

        self.page().mainFrame().addToJavaScriptWindowObject("QLineEdit", self.lineEdit)
#         self.page().mainFrame().addToJavaScriptWindowObject("QDocument", self.doc)
#         self.page().mainFrame().evaluateJavaScript("helloWorld();")
#         self.page().mainFrame().addToJavaScriptWindowObject("QPrinter", self.p);
        
    def pp(self,string):
        print 'fefefef'
        
    def initPrinter(self):

        printerInfo = QPrinterInfo()
        self.p = QPrinter()
        num = 0
        for item in printerInfo.availablePrinters():
#             if "Samsung M267x 287x Series" == item.printerName():
            if num == 0:
                self.p = QPrinter(item)
                break
            num =num+1
        self.p.setOutputFormat(QPrinter.NativeFormat)
        self.p.setPageSize(self.p.B8)
        self.p.setPaperSize(QSizeF(200,1000),1)
        self.doc = QTextDocument()
        self.doc.setHtml(self.printStr)
        self.doc.setPageSize(QSizeF(self.p.logicalDpiX() * (80/ 25.4), self.p.logicalDpiY() * (297 / 25.4)))
        self.doc.print_(self.p)
        self.page().mainFrame().evaluateJavaScript("afterPrint();")

        
    def search(self):
        address = '192.168.1.111/index.php?id=9aa04016a565adcfbd3cae29e292657d'
        if address:
            if address.find('://') == -1:
                address = 'http://' + address
            url = QUrl(address)
            self.load(url)
            
class MyThread(QThread):
      
    sinOut = pyqtSignal(str)
      
    def __init__(self,parent=None):
        super(MyThread,self).__init__(parent)
        
        self.start()
    def run(self):
        while True:
            time.sleep(1)
            self.sinOut.emit("")
            
            

app = QApplication(sys.argv)
browser = MyBrowser()
browser.show()

sys.exit(app.exec_())
