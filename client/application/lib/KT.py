#coding:utf-8
'''
Created on 2015年1月20日

@author: kylin 

KT类库 (KUnit...)

'''
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import math
import Image

class KButton(QPushButton):
    def __init__(self,text = "",parent = None):
        QPushButton.__init__(self,text,parent)
        qss = """QPushButton{
        border: 1px solid rgb(216,176,112);  
        background-color:rgb(216,176,112);  
        border-style:solid;  
        border-radius:5px;  
        padding:10px 10px;  
        }"""
        
        qss +="""
        QPushButton::hover{
        background-color:rgb(204,188,122);
        }
        """
        self.setStyleSheet(qss)
        self.setCursor(Qt.PointingHandCursor)

class KPwdLineEdit(QLineEdit):
    def __init__(self,parent = None):
        QLineEdit.__init__(self,parent)
        
        #设置无右键菜单
        self.setContextMenuPolicy(Qt.NoContextMenu)
        
        #设置密码提示
        self.setPlaceholderText(u"密码")
#         self.setToolTip(u"密码")

        #设置密码隐藏
        self.setEchoMode(QLineEdit.Password)
#         self.setEchoMode(QLineEdit.PasswordEchoOnEdit)

        #设置密码框样式
        style1 = "QLineEdit{border-radius:4px;padding:3px;font-size:12px;color:black;border:1px solid gray;}"
        style2 = "QLineEdit:hover{border:1px solid rgb(70, 200, 50);}"
        self.setStyleSheet(style1+style2)
        #设置最大长度16位
#         self.setMaxLength(6);
        
        #阴影边框
        
    def keyPressEvent(self,event):
        if event.matches(QKeySequence.SelectAll):
            return
        if event.matches(QKeySequence.Copy):
            return
        if event.matches(QKeySequence.Paste):
            return
        if event.key() == Qt.Key_Left :
            return
        if event.key() == Qt.Key_Right :
            return
        if event.key() == Qt.Key_Home :
            return
        if event.key() == Qt.Key_End:
            return
#        
        QLineEdit.keyPressEvent(self, event)


    def mouseDoubleClickEvent(self, event):
        return

    #主要设置鼠标位于密码框中时不可移动
    def mouseMoveEvent(self,event):
        return
    
    def mousePressEvent(self,event):
        #获得当前鼠标位置
        cursor_pos = self.cursorPositionAt(event.pos())
        #获取光标位置
        current_pos = self.cursorPosition()

        #鼠标点击位置在光标位置之前，则设置光标前移一格
#         if(cursor_pos < current_pos):
        self.setCursorPosition(current_pos)
        
    def focusInEvent(self, *args, **kwargs):
        return QLineEdit.focusInEvent(self, *args, **kwargs)
    def focusOutEvent(self, *args, **kwargs):
        return QLineEdit.focusOutEvent(self, *args, **kwargs)
    def focusNextChild(self, *args, **kwargs):
        return QLineEdit.focusNextChild(self, *args, **kwargs)
    def focusNextPrevChild(self, *args, **kwargs):
        return QLineEdit.focusNextPrevChild(self, *args, **kwargs)
    def focusPolicy(self, *args, **kwargs):
        return QLineEdit.focusPolicy(self, *args, **kwargs)
    def focusPreviousChild(self, *args, **kwargs):
        return QLineEdit.focusPreviousChild(self, *args, **kwargs)
    def focusProxy(self, *args, **kwargs):
        return QLineEdit.focusProxy(self, *args, **kwargs)
    def focusWidget(self, *args, **kwargs):
        return QLineEdit.focusWidget(self, *args, **kwargs)
    
class KDockWidget(QDockWidget):
    def __init__(self,parent = None):
        QDialog.__init__(self,parent)
#         self.setWindowFlags(Qt.MSWindowsFixedSizeDialogHint|Qt.FramelessWindowHint)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setFeatures(QDockWidget.NoDockWidgetFeatures)
        self.setFeatures(QDockWidget.DockWidgetVerticalTitleBar)
        self.setContentsMargins(0, 0, 0, 0)
        self.setTitleBarWidget(QWidget(self))#隐藏标题栏
        self.initStyleOption(QStyleOptionDockWidget())
        self.setStyleSheet("QDockWidget{border:0px solid #fff;padding:0px;margin-top:10px;}")

class KDialog(QDialog):
    pixmap = None
    color = None
    mouse_press = False
    is_move = True
    maxButton = None
    resizeAble = True
    resizeObj = None
    is_show = False
    
        
    def setMoveAble(self,b):
        self.is_move = b
        self.update()
    
    def __init__(self,parent = None,title=""):
        self.title= title
        QDialog.__init__(self,None)
        self.setWindowTitle(title)
        
        #1.设置标题栏隐藏
#         self.setWindowFlags(Qt.FramelessWindowHint);
       
#         self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
#         self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.CustomizeWindowHint)
        self.setWindowFlags(Qt.MSWindowsFixedSizeDialogHint | Qt.FramelessWindowHint)#
        self.setAttribute(Qt.WA_TranslucentBackground, True);


#         self.setStyleSheet("QDialog{background:transparent;}")
        #可获取鼠标跟踪效果

        self.setMouseTracking(True);
        
        #设置动画
        
#         self.setAnimate()

    def setCloseAble(self,widget,obj):
        self.resizeObj = obj
        self.addBMCButton(widget)

    def exec_(self,widget = None,closeAble = True):
        
        self.is_show = True
        self.setMoveAble(True)
        self.setColor(QColor.fromRgb(240,235,230))
        if closeAble:
            self.setCloseAble(widget, self)
        return QDialog.exec_(self)
    def show(self,widget = None,closeAble = True):
        
        self.is_show = True
        self.setMoveAble(True)
        self.setColor(QColor.fromRgb(240,235,230))
        if closeAble:
            self.setCloseAble(widget, self)
        return QDialog.show(self)
        
      
    def changeSize(self):
        if self.maxButton == None or self.resizeAble == False:
            return
        if(self.resizeObj.isMaximized()):
            self.maxButton.setIcon(QIcon(self.maxPix))
            self.resizeObj.showNormal()#窗口还原
        else:
            self.maxButton.setIcon(QIcon(self.normalPix))
            self.resizeObj.showMaximized()#窗口最大化

    def addBMCButton(self,contain):
        #1、自定义最小化、最大化按钮
        if contain == None:
            try:
                oldlay = self.findChildren(QLayout)[0]
                vlayout = QVBoxLayout()
                vlayout.setMargin(10)
                vlayout.setSpacing(0)
                contain = KWidget()
                contain.setFixedHeight(30)
                contain.setMoveAble(False)
                contain.setColor(QColor.fromRgb(220,180,115))
                oldcontain = QWidget()
                
                vlayout.addWidget(contain)
                vlayout.addWidget(oldcontain)
                oldcontain.setLayout(oldlay)
                self.setLayout(vlayout)
                
            except:
                vlayout = QVBoxLayout()
                vlayout.setMargin(10)
                vlayout.setSpacing(0)
                contain = KWidget()
                contain.setFixedHeight(30)
                contain.setMoveAble(False)
                contain.setColor(QColor.fromRgb(220,180,115))
                vlayout.addWidget(contain)
                
                self.setLayout(vlayout)
                
            
        lay = QHBoxLayout(contain)
        lay.setMargin(0)
#         width = self.width()#获取界面的宽度

        #构建最小化、最大化、关闭按钮
        minButton = KMPushButton(self)
        self.maxButton = KMPushButton(self)
        closeButton= KMPushButton(self)
        minButton.loadPixmap("./img/kt/min_button.png")
        self.maxButton.loadPixmap("./img/kt/max_button.png")
        closeButton.loadPixmap("./img/kt/close_button.png")
        
        #获取最小化、关闭按钮图标
        minPix = self.style().standardPixmap(QStyle.SP_TitleBarMinButton);
        self.maxPix = self.style().standardPixmap(QStyle.SP_TitleBarMaxButton);
        self.normalPix = self.style().standardPixmap(QStyle.SP_TitleBarNormalButton);
        closePix = self.style().standardPixmap(QStyle.SP_TitleBarCloseButton);
        
        #设置最小化、关闭按钮图标
        minButton.setIcon(QIcon(minPix));
        self.maxButton.setIcon(QIcon(self.maxPix));
        closeButton.setIcon(QIcon(closePix));
#         minButton.setStyleSheet("background:transparent") #透明显示
#         closeButton.setStyleSheet("background:transparent") #透明显示
        minButton.setFocusPolicy(Qt.NoFocus)
        self.maxButton.setFocusPolicy(Qt.NoFocus)
        closeButton.setFocusPolicy(Qt.NoFocus)
        self.connect(minButton, SIGNAL("clicked()"),self.resizeObj.showMinimized)#窗口最小化
        if self.resizeAble:
            self.connect(self.maxButton, SIGNAL("clicked()"),self.changeSize)#窗口最大化
        self.connect(closeButton, SIGNAL("clicked()"),self.resizeObj.close)
#         self.connect(closeButton, SIGNAL("clicked()"),self.closeWidget)
        
        #设置最小化、关闭按钮在界面的位置
#         minButton.setGeometry(0,0,20,20);
#         closeButton.setGeometry(20,0,20,20);\
        label = QLabel(self.title)
        label.setContentsMargins(10, 0, 0, 0)
        font = QFont()
        font.setPointSize(12)
        label.setFont(font)
        lay.addWidget(label)
        lay.addStretch()
        lay.setMargin(0)
        lay.setSpacing(0)
        lay.addWidget(minButton,0,Qt.AlignTop)
        lay.addWidget(self.maxButton,0,Qt.AlignTop)
        lay.addWidget(closeButton,0,Qt.AlignTop)
        
    def resizeEvent(self, event):
        return QDialog.resizeEvent(self, event)
     
    def closeWidget(self):
        animation = QPropertyAnimation(self, "windowOpacity")
        animation.setDuration(1000)
        animation.setStartValue(1)
        animation.setEndValue(0)
        
    def mousePressEvent(self,event):
        if(event.button() == Qt.LeftButton):
            self.mouse_press = True
            if self.is_move :
    
                #窗口位置
                self.move_point = event.globalPos() - self.pos()
            else:
                QDialog.mousePressEvent(self,event)
#             event.ignore();
    def mouseMoveEvent(self,event):
        #若鼠标左键被按下
        if(self.mouse_press):
            #获取位置
            move_pos = event.globalPos()
  
            if self.is_move:
                #移动主窗体位置
                self.move(move_pos - self.move_point)
            else :
                QDialog.mouseMoveEvent(self,event)

#         event.ignore();
        
    def mouseReleaseEvent(self,event):
        #设置鼠标为未被按下
        self.mouse_press = False;
        QDialog.mouseReleaseEvent(self,event)
   
#         event.ignore();

    def setBack(self,pixmap_name):
        self.pixmap = QPixmap(pixmap_name)
        
    def setColor(self,color):
        self.color = color
        
        
    def showShade(self):
        path = QPainterPath()
        path.setFillRule(Qt.WindingFill)
        path.addRect(10, 10, self.width()-20, self.height()-20)
    
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True);
#         painter.fillPath(path, QBrush(QColor(0, 0, 0)))
    
        color = QColor(0, 0, 0)
        for i in range(10):
            path = QPainterPath()
            path.setFillRule(Qt.WindingFill);
            path.addRect(10-i, 10-i, self.width()-(10-i)*2, self.height()-(10-i)*2);
            color.setAlpha(150 - (math.sqrt(i))*50);
#             color.setAlpha(0);
            painter.setPen(color);
            painter.drawPath(path);
#         return QDialog.paintEvent(self, event)
    def paintEvent(self,event):
        padding = 0
        if self.is_show:
            padding = 10
        painter = QPainter()
        painter.begin(self)
        '''
        self.pixmap.copy 第一个参数主要有三种情况
                        分别是宽度*1，*2，*3，对应鼠标的三种状态
        '''
        rect = QRect(self.rect().x()+padding,self.rect().y()+padding,self.rect().width(),self.rect().height())
        rect.setWidth(self.rect().width()-2*padding)
        rect.setHeight(self.rect().height()-2*padding)
        
        if self.pixmap !=None:
            painter.drawPixmap(rect, self.pixmap.copy(0,0,self.width(), self.height()))
        elif self.color !=None:
#             painter.setBrush(QBrush(self.color))
            painter.setPen(QPen(self.color))
            painter.setBrush(QBrush(self.color))
                
            painter.drawRect(rect)
        else:
#             painter.setPen(QPen(QColor(224,222,218)))
            painter.setPen(QPen(QColor(245,245,245)))
#             painter.setBrush(QBrush(QColor(224,222,218)))
            painter.setBrush(QBrush(QColor(245,245,245)))
            painter.drawRect(rect)
        painter.end()
        
        if self.is_show:
            self.showShade()
            pass
#         self.showShade()
        
class KLockDialog(QDialog):
    pixmap = None
    color = None
    mouse_press = False
    is_move = True
    maxButton = None
    resizeAble = True
    resizeObj = None
    is_show = False
    
    def infoBox(self,str):
    
        return KTipWidget(str)
     
    def setMoveAble(self,b):
        self.is_move = b
        self.update()
    
    def __init__(self,parent = None,title=""):
        self.title= title
        QDialog.__init__(self,None)
        
        #1.设置标题栏隐藏
#         self.setWindowFlags(Qt.FramelessWindowHint);
       
#         self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
#         self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.CustomizeWindowHint)
        self.setWindowFlags(Qt.MSWindowsFixedSizeDialogHint | Qt.FramelessWindowHint)#
        self.setAttribute(Qt.WA_TranslucentBackground, True);


#         self.setStyleSheet("QDialog{background:transparent;}")
        #可获取鼠标跟踪效果

        self.setMouseTracking(True);
        
        #设置动画
        
#         self.setAnimate()

    def setCloseAble(self,widget,obj):
        self.resizeObj = obj
#         self.addBMCButton(widget)

    def exec_(self,widget = None,closeAble = True):
        
        self.is_show = True
        self.setMoveAble(True)
        self.setColor(QColor.fromRgb(240,235,230))
        if closeAble:
            self.setCloseAble(widget, self)
        return QDialog.exec_(self)
    def show(self,widget = None,closeAble = True):
        
        self.is_show = True
        self.setMoveAble(True)
        self.setColor(QColor.fromRgb(240,235,230))
        if closeAble:
            self.setCloseAble(widget, self)
        return QDialog.show(self)
        
      
    def changeSize(self):
        if self.maxButton == None or self.resizeAble == False:
            return
        if(self.resizeObj.isMaximized()):
            self.maxButton.setIcon(QIcon(self.maxPix))
            self.resizeObj.showNormal()#窗口还原
        else:
            self.maxButton.setIcon(QIcon(self.normalPix))
            self.resizeObj.showMaximized()#窗口最大化

    def addBMCButton(self,contain):
        #1、自定义最小化、最大化按钮
        if contain == None:
            try:
                oldlay = self.findChildren(QLayout)[0]
                vlayout = QVBoxLayout()
                vlayout.setMargin(10)
                vlayout.setSpacing(0)
                contain = KWidget()
                contain.setFixedHeight(30)
                contain.setMoveAble(False)
                contain.setColor(QColor.fromRgb(220,180,115))
                oldcontain = QWidget()
                
                vlayout.addWidget(contain)
                vlayout.addWidget(oldcontain)
                oldcontain.setLayout(oldlay)
                self.setLayout(vlayout)
                
            except:
                vlayout = QVBoxLayout()
                vlayout.setMargin(10)
                vlayout.setSpacing(0)
                contain = KWidget()
                contain.setFixedHeight(30)
                contain.setMoveAble(False)
                contain.setColor(QColor.fromRgb(220,180,115))
                vlayout.addWidget(contain)
                
                self.setLayout(vlayout)
                
            
        lay = QHBoxLayout(contain)
        lay.setMargin(0)
#         width = self.width()#获取界面的宽度

        #构建最小化、最大化、关闭按钮
        minButton = KMPushButton(self)
        self.maxButton = KMPushButton(self)
        closeButton= KMPushButton(self)
        minButton.loadPixmap("./img/kt/min_button.png")
        self.maxButton.loadPixmap("./img/kt/max_button.png")
        closeButton.loadPixmap("./img/kt/close_button.png")
        
        #获取最小化、关闭按钮图标
        minPix = self.style().standardPixmap(QStyle.SP_TitleBarMinButton);
        self.maxPix = self.style().standardPixmap(QStyle.SP_TitleBarMaxButton);
        self.normalPix = self.style().standardPixmap(QStyle.SP_TitleBarNormalButton);
        closePix = self.style().standardPixmap(QStyle.SP_TitleBarCloseButton);
        
        #设置最小化、关闭按钮图标
        minButton.setIcon(QIcon(minPix));
        self.maxButton.setIcon(QIcon(self.maxPix));
        closeButton.setIcon(QIcon(closePix));
#         minButton.setStyleSheet("background:transparent") #透明显示
#         closeButton.setStyleSheet("background:transparent") #透明显示
        self.connect(minButton, SIGNAL("clicked()"),self.resizeObj.showMinimized)#窗口最小化
        if self.resizeAble:
            self.connect(self.maxButton, SIGNAL("clicked()"),self.changeSize)#窗口最大化
        self.connect(closeButton, SIGNAL("clicked()"),self.resizeObj.close)
#         self.connect(closeButton, SIGNAL("clicked()"),self.closeWidget)
        
        #设置最小化、关闭按钮在界面的位置
#         minButton.setGeometry(0,0,20,20);
#         closeButton.setGeometry(20,0,20,20);\
        label = QLabel(self.title)
        label.setContentsMargins(10, 0, 0, 0)
        font = QFont()
        font.setPointSize(12)
        label.setFont(font)
        lay.addWidget(label)
        lay.addStretch()
        lay.setMargin(0)
        lay.setSpacing(0)
        lay.addWidget(minButton,0,Qt.AlignTop)
        lay.addWidget(self.maxButton,0,Qt.AlignTop)
        lay.addWidget(closeButton,0,Qt.AlignTop)
        
    def resizeEvent(self, event):
        return QDialog.resizeEvent(self, event)
     
    def closeWidget(self):
        animation = QPropertyAnimation(self, "windowOpacity")
        animation.setDuration(1000)
        animation.setStartValue(1)
        animation.setEndValue(0)
        
    def mousePressEvent(self,event):
        if(event.button() == Qt.LeftButton):
            self.mouse_press = True
            if self.is_move :
    
                #窗口位置
                self.move_point = event.globalPos() - self.pos()
            else:
                QDialog.mousePressEvent(self,event)
#             event.ignore();
    def mouseMoveEvent(self,event):
        #若鼠标左键被按下
        if(self.mouse_press):
            #获取位置
            move_pos = event.globalPos()
  
            if self.is_move:
                #移动主窗体位置
                self.move(move_pos - self.move_point)
            else :
                QDialog.mouseMoveEvent(self,event)

#         event.ignore();
        
    def mouseReleaseEvent(self,event):
        #设置鼠标为未被按下
        self.mouse_press = False;
        QDialog.mouseReleaseEvent(self,event)
   
#         event.ignore();

    def setBack(self,pixmap_name):
        self.pixmap = QPixmap(pixmap_name)
        
    def setColor(self,color):
        self.color = color
        
        
    def showShade(self):
        path = QPainterPath()
        path.setFillRule(Qt.WindingFill)
        path.addRect(10, 10, self.width()-20, self.height()-20)
    
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True);
#         painter.fillPath(path, QBrush(QColor(0, 0, 0)))
    
        color = QColor(0, 0, 0)
        for i in range(10):
            path = QPainterPath()
            path.setFillRule(Qt.WindingFill);
            path.addRect(10-i, 10-i, self.width()-(10-i)*2, self.height()-(10-i)*2);
            color.setAlpha(150 - (math.sqrt(i))*50);
#             color.setAlpha(0);
            painter.setPen(color);
            painter.drawPath(path);
#         return QDialog.paintEvent(self, event)
    def paintEvent(self,event):
        padding = 0
        if self.is_show:
            padding = 10
        painter = QPainter()
        painter.begin(self)
        '''
        self.pixmap.copy 第一个参数主要有三种情况
                        分别是宽度*1，*2，*3，对应鼠标的三种状态
        '''
        rect = QRect(self.rect().x()+padding,self.rect().y()+padding,self.rect().width(),self.rect().height())
        rect.setWidth(self.rect().width()-2*padding)
        rect.setHeight(self.rect().height()-2*padding)
        
        if self.pixmap !=None:
            painter.drawPixmap(rect, self.pixmap.copy(0,0,self.width(), self.height()))
        elif self.color !=None:
#             painter.setBrush(QBrush(self.color))
            painter.setPen(QPen(self.color))
            painter.setBrush(QBrush(self.color))
                
            painter.drawRect(rect)
        else:
#             painter.setPen(QPen(QColor(224,222,218)))
            painter.setPen(QPen(QColor(245,245,245)))
#             painter.setBrush(QBrush(QColor(224,222,218)))
            painter.setBrush(QBrush(QColor(245,245,245)))
            painter.drawRect(rect)
        painter.end()
        
        if self.is_show:
            self.showShade()
            pass
#         self.showShade()
        
        
        
class KLoginDialog(QDialog):
    pixmap = None
    color = None
    mouse_press = False
    is_move = True
    maxButton = None
    resizeAble = True
    resizeObj = None
    is_show = False
    
        
    def setMoveAble(self,b):
        self.is_move = b
        self.update()
    
    def __init__(self,parent = None,title=""):
        self.title= title
        QDialog.__init__(self,None)
        self.setWindowTitle(title)
        
        #1.设置标题栏隐藏
#         self.setWindowFlags(Qt.FramelessWindowHint);
       
#         self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
#         self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.CustomizeWindowHint)
        self.setWindowFlags(Qt.MSWindowsFixedSizeDialogHint | Qt.FramelessWindowHint)#
        self.setAttribute(Qt.WA_TranslucentBackground, True);


#         self.setStyleSheet("QDialog{background:transparent;}")
        #可获取鼠标跟踪效果

        self.setMouseTracking(True);
        
        #设置动画
        
#         self.setAnimate()

    def setCloseAble(self,widget,obj):
        self.resizeObj = obj
        self.addBMCButton(widget)

    def exec_(self,widget = None,closeAble = True):
        
        self.is_show = True
        self.setMoveAble(True)
        self.setColor(QColor.fromRgb(240,235,230))
        if closeAble:
            self.setCloseAble(widget, self)
        return QDialog.exec_(self)
    def show(self,widget = None,closeAble = True):
        
        self.is_show = True
        self.setMoveAble(True)
        self.setColor(QColor.fromRgb(240,235,230))
        if closeAble:
            self.setCloseAble(widget, self)
        return QDialog.show(self)
        

    def addBMCButton(self,contain):
        #1、自定义最小化、最大化按钮
        if contain == None:
            try:
                oldlay = self.findChildren(QLayout)[0]
                vlayout = QVBoxLayout()
                vlayout.setMargin(10)
                vlayout.setSpacing(0)
                contain = KWidget()
                contain.setFixedHeight(30)
                contain.setMoveAble(False)
                contain.setColor(QColor.fromRgb(220,180,115))
                oldcontain = QWidget()
                
                vlayout.addWidget(contain)
                vlayout.addWidget(oldcontain)
                oldcontain.setLayout(oldlay)
                self.setLayout(vlayout)
                
            except:
                vlayout = QVBoxLayout()
                vlayout.setMargin(10)
                vlayout.setSpacing(0)
                contain = KWidget()
                contain.setFixedHeight(30)
                contain.setMoveAble(False)
                contain.setColor(QColor.fromRgb(220,180,115))
                vlayout.addWidget(contain)
                
                self.setLayout(vlayout)
                
            
        lay = QHBoxLayout(contain)
        lay.setMargin(0)
#         width = self.width()#获取界面的宽度

        #构建最小化、最大化、关闭按钮
        minButton = KMPushButton(self)
        closeButton= KMPushButton(self)
        minButton.loadPixmap("./img/kt/min_button.png")
        closeButton.loadPixmap("./img/kt/close_button.png")
        
        #获取最小化、关闭按钮图标
        minPix = self.style().standardPixmap(QStyle.SP_TitleBarMinButton);
        closePix = self.style().standardPixmap(QStyle.SP_TitleBarCloseButton);
        
        #设置最小化、关闭按钮图标
        minButton.setIcon(QIcon(minPix));
        closeButton.setIcon(QIcon(closePix));
#         minButton.setStyleSheet("background:transparent") #透明显示
#         closeButton.setStyleSheet("background:transparent") #透明显示
        minButton.setFocusPolicy(Qt.NoFocus)
        closeButton.setFocusPolicy(Qt.NoFocus)
        self.connect(minButton, SIGNAL("clicked()"),self.resizeObj.showMinimized)#窗口最小化
        self.connect(closeButton, SIGNAL("clicked()"),self.resizeObj.close)
#         self.connect(closeButton, SIGNAL("clicked()"),self.closeWidget)
        
        #设置最小化、关闭按钮在界面的位置
#         minButton.setGeometry(0,0,20,20);
#         closeButton.setGeometry(20,0,20,20);\
        label = QLabel(self.title)
        label.setContentsMargins(10, 0, 0, 0)
        font = QFont()
        font.setPointSize(12)
        label.setFont(font)
        lay.addWidget(label)
        lay.addStretch()
        lay.setMargin(0)
        lay.setSpacing(0)
        lay.addWidget(minButton,0,Qt.AlignTop)
        lay.addWidget(closeButton,0,Qt.AlignTop)
        
    def resizeEvent(self, event):
        return QDialog.resizeEvent(self, event)
     
    def closeWidget(self):
        animation = QPropertyAnimation(self, "windowOpacity")
        animation.setDuration(1000)
        animation.setStartValue(1)
        animation.setEndValue(0)
        
    def mousePressEvent(self,event):
        if(event.button() == Qt.LeftButton):
            self.mouse_press = True
            if self.is_move :
    
                #窗口位置
                self.move_point = event.globalPos() - self.pos()
            else:
                QDialog.mousePressEvent(self,event)
#             event.ignore();
    def mouseMoveEvent(self,event):
        #若鼠标左键被按下
        if(self.mouse_press):
            #获取位置
            move_pos = event.globalPos()
  
            if self.is_move:
                #移动主窗体位置
                self.move(move_pos - self.move_point)
            else :
                QDialog.mouseMoveEvent(self,event)

#         event.ignore();
        
    def mouseReleaseEvent(self,event):
        #设置鼠标为未被按下
        self.mouse_press = False;
        QDialog.mouseReleaseEvent(self,event)
   
#         event.ignore();

    def setBack(self,pixmap_name):
        self.pixmap = QPixmap(pixmap_name)
        
    def setColor(self,color):
        self.color = color
        
        
    def showShade(self):
        path = QPainterPath()
        path.setFillRule(Qt.WindingFill)
        path.addRect(10, 10, self.width()-20, self.height()-20)
    
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True);
#         painter.fillPath(path, QBrush(QColor(0, 0, 0)))
    
        color = QColor(0, 0, 0)
        for i in range(10):
            path = QPainterPath()
            path.setFillRule(Qt.WindingFill);
            path.addRect(10-i, 10-i, self.width()-(10-i)*2, self.height()-(10-i)*2);
            color.setAlpha(150 - (math.sqrt(i))*50);
#             color.setAlpha(0);
            painter.setPen(color);
            painter.drawPath(path);
#         return QDialog.paintEvent(self, event)
    def paintEvent(self,event):
        padding = 0
        if self.is_show:
            padding = 10
        painter = QPainter()
        painter.begin(self)
        '''
        self.pixmap.copy 第一个参数主要有三种情况
                        分别是宽度*1，*2，*3，对应鼠标的三种状态
        '''
        rect = QRect(self.rect().x()+padding,self.rect().y()+padding,self.rect().width(),self.rect().height())
        rect.setWidth(self.rect().width()-2*padding)
        rect.setHeight(self.rect().height()-2*padding)
        
        if self.pixmap !=None:
            painter.drawPixmap(rect, self.pixmap.copy(0,0,self.width(), self.height()))
        elif self.color !=None:
#             painter.setBrush(QBrush(self.color))
            painter.setPen(QPen(self.color))
            painter.setBrush(QBrush(self.color))
                
            painter.drawRect(rect)
        else:
#             painter.setPen(QPen(QColor(224,222,218)))
            painter.setPen(QPen(QColor(245,245,245)))
#             painter.setBrush(QBrush(QColor(224,222,218)))
            painter.setBrush(QBrush(QColor(245,245,245)))
            painter.drawRect(rect)
        painter.end()
        
        if self.is_show:
            self.showShade()
            pass
#         self.showShade()
        
        

class KTesting(KDialog):
    def __init__(self,parent = None):
        KDialog.__init__(self,parent)
        self.setAttribute(Qt.WA_TranslucentBackground)
    
    def paintEvent(self, event):
        pass
    
   
class KWidget(QWidget):
    pixmap = None
    color = None
    mouse_press = False
    is_move = True
    maxButton = None
    resizeAble = True
    resizeObj = None
    def __init__(self,parent = None):
        QWidget.__init__(self,parent)
        
        #1.设置标题栏隐藏
#         self.setWindowFlags(Qt.FramelessWindowHint);
       
#         self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
#         self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.CustomizeWindowHint)
        self.setWindowFlags(Qt.MSWindowsFixedSizeDialogHint | Qt.FramelessWindowHint)#

        
        #可获取鼠标跟踪效果

        self.setMouseTracking(True);
        
        #设置动画
        
#         self.setAnimate()

    def setCloseAble(self,widget,obj):
        self.resizeObj = obj
        self.addBMCButton(widget)

      
    def changeSize(self):
        if self.maxButton == None or self.resizeAble == False:
            return
        if(self.resizeObj.isMaximized()):
            self.maxButton.setIcon(QIcon(self.maxPix))
            self.resizeObj.showNormal()#窗口还原
        else:
            self.maxButton.setIcon(QIcon(self.normalPix))
            self.resizeObj.showMaximized()#窗口最大化

    def addBMCButton(self,contain):
        #1、自定义最小化、最大化按钮
        lay = QHBoxLayout(contain)
        lay.setMargin(0)
#         width = self.width()#获取界面的宽度

        #构建最小化、最大化、关闭按钮
        minButton = KMPushButton(self)
        self.maxButton = KMPushButton(self)
        closeButton= KMPushButton(self)
        minButton.loadPixmap("./img/kt/min_button.png")
        self.maxButton.loadPixmap("./img/kt/max_button.png")
        closeButton.loadPixmap("./img/kt/close_button.png")
        
        #获取最小化、关闭按钮图标
        minPix = self.style().standardPixmap(QStyle.SP_TitleBarMinButton);
        self.maxPix = self.style().standardPixmap(QStyle.SP_TitleBarMaxButton);
        self.normalPix = self.style().standardPixmap(QStyle.SP_TitleBarNormalButton);
        closePix = self.style().standardPixmap(QStyle.SP_TitleBarCloseButton);
        
        #设置最小化、关闭按钮图标
        minButton.setIcon(QIcon(minPix));
        self.maxButton.setIcon(QIcon(self.maxPix));
        closeButton.setIcon(QIcon(closePix));
#         minButton.setStyleSheet("background:transparent") #透明显示
#         closeButton.setStyleSheet("background:transparent") #透明显示
        self.connect(minButton, SIGNAL("clicked()"),self.resizeObj.showMinimized)#窗口最小化
        if self.resizeAble:
            self.connect(self.maxButton, SIGNAL("clicked()"),self.changeSize)#窗口最大化
        self.connect(closeButton, SIGNAL("clicked()"),self.resizeObj.close)
#         self.connect(closeButton, SIGNAL("clicked()"),self.closeWidget)
        
        #设置最小化、关闭按钮在界面的位置
#         minButton.setGeometry(0,0,20,20);
#         closeButton.setGeometry(20,0,20,20);

        lay.addStretch()
        lay.setMargin(0)
        lay.setSpacing(0)
        lay.addWidget(minButton,0,Qt.AlignTop)
        lay.addWidget(self.maxButton,0,Qt.AlignTop)
        lay.addWidget(closeButton,0,Qt.AlignTop)
 
    def closeWidget(self):
        animation = QPropertyAnimation(self, "windowOpacity")
        animation.setDuration(1000)
        animation.setStartValue(1)
        animation.setEndValue(0)
        
        
    def setMoveAble(self,b):
        self.is_move = b
        self.update()
        
    def mousePressEvent(self,event):
        if(event.button() == Qt.LeftButton):
            self.mouse_press = True
            if self.is_move :
    
                #窗口位置
                self.move_point = event.globalPos() - self.pos()
            else:
                QWidget.mousePressEvent(self,event)
#             event.ignore();
    def mouseMoveEvent(self,event):
        #若鼠标左键被按下
        if(self.mouse_press):
            #获取位置
            move_pos = event.globalPos()
  
            if self.is_move:
                #移动主窗体位置
                self.move(move_pos - self.move_point)
            else :
                QWidget.mouseMoveEvent(self,event)

#         event.ignore();
        
    def mouseReleaseEvent(self,event):
        #设置鼠标为未被按下
        self.mouse_press = False
        QWidget.mouseReleaseEvent(self,event)
   
#         event.ignore();

    def setBack(self,pixmap_name):
        self.pixmap = QPixmap(pixmap_name)
        
    def setColor(self,color):
        self.color = color
    def paintEvent(self,event):
#         print 'dddd'
# #         pass
# #         self.setAttribute(Qt.WA_TranslucentBackground)
# #         path = QPainterPath()
# #         path.setFillRule(Qt.WindingFill);
# #         path.addRect(0, 0, self.width(), self.height());
# #           
# #         painter = QPainter(self)
# #         painter.setRenderHint(QPainter.Antialiasing,True)        
# #         painter.fillPath(path,QBrush(Qt.white))
# #          
# #         color = QColor(0, 0, 0, 50)
# #         for i in range(10):
# #             path = QPainterPath()
# #             path.setFillRule(Qt.WindingFill);
# #             path.addRect(10-i, 10-i, self.width()-(10-i)*2, self.height()-(10-i)*2);
# #             color.setAlpha(150 - math.sqrt(i)*50);
# #             painter.setPen(color);
# #             painter.drawPath(path);
# 
#         bitmap = QBitmap(self.size());
#         bitmap.fill();
#         painter = QPainter(self);
#         pixmap = QPixmap("./icons/login.png");
#         painter.drawPixmap(self.rect(), pixmap);
#         painter.end()
#         palette = QPalette()
#         palette.setBrush(self.backgroundRole(),QBrush(QPixmap(self.pixmap_name)))
#         self.setPalette(palette)
        
        painter = QPainter()
        painter.begin(self)
        '''
        self.pixmap.copy 第一个参数主要有三种情况
                        分别是宽度*1，*2，*3，对应鼠标的三种状态
        '''
        if self.pixmap !=None:
            painter.drawPixmap(self.rect(), self.pixmap.copy(0,0,self.width(), self.height()))
        elif self.color !=None:
#             painter.setBrush(QBrush(self.color))
            painter.setPen(QPen(self.color))
            painter.setBrush(QBrush(self.color))
            painter.drawRect(self.rect())
        else:
            painter.setPen(QPen(QColor(224,222,218)))
            painter.setBrush(QBrush(QColor(224,222,218)))
            painter.drawRect(self.rect())
        painter.end()
        

        
class KOUTDialog(KDialog):
    maxButton= None
    def setLayout(self,layout):
        main = QWidget()
        main.setLayout(layout)
        blayout = QVBoxLayout()
        contain = self.addBMCButton()
        
        blayout.setMargin(0)
        blayout.addWidget(contain)
        blayout.addWidget(main)
        
        blayout.addStretch()
#         spacerItem1 = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
#         blayout.addItem(spacerItem1)
        
        return QDialog.setLayout(self,blayout)
      
    def changeEvent(self, event):
        if self.maxButton == None:
            return
        if(self.isMaximized()):
            self.maxButton.setIcon(QIcon(self.normalPix));
            self.disconnect(self.maxButton, SIGNAL("clicked()"),self.showMaximized)#窗口最大化
            self.connect(self.maxButton, SIGNAL("clicked()"),self.showNormal)#窗口还原
        else:
            
            self.maxButton.setIcon(QIcon(self.maxPix))
            self.connect(self.maxButton, SIGNAL("clicked()"),self.showMaximized)#窗口最大化
            self.disconnect(self.maxButton, SIGNAL("clicked()"),self.showNormal)#窗口还原
        
      
    def addBMCButton(self):
        #1、自定义最小化、最大化按钮
        contain = QWidget()
        lay = QHBoxLayout(contain)
        lay.setMargin(0)
#         width = self.width()#获取界面的宽度

        #构建最小化、最大化、关闭按钮
        minButton = QToolButton(self)
        self.maxButton = QToolButton(self)
        closeButton= QToolButton(self)
        
        #获取最小化、关闭按钮图标
        minPix = self.style().standardPixmap(QStyle.SP_TitleBarMinButton);
        self.maxPix = self.style().standardPixmap(QStyle.SP_TitleBarMaxButton);
        self.normalPix = self.style().standardPixmap(QStyle.SP_TitleBarNormalButton);
        closePix = self.style().standardPixmap(QStyle.SP_TitleBarCloseButton);
        
        #设置最小化、关闭按钮图标
        minButton.setIcon(QIcon(minPix));
        self.maxButton.setIcon(QIcon(self.maxPix));
        closeButton.setIcon(QIcon(closePix));
#         minButton.setStyleSheet("background:transparent") #透明显示
#         closeButton.setStyleSheet("background:transparent") #透明显示
        self.connect(minButton, SIGNAL("clicked()"),self.showMinimized)#窗口最小化
        self.connect(self.maxButton, SIGNAL("clicked()"),self.showMaximized)#窗口最大化
        self.connect(closeButton, SIGNAL("clicked()"),self.close)
#         self.connect(closeButton, SIGNAL("clicked()"),self.closeWidget)
        
        #设置最小化、关闭按钮在界面的位置
#         minButton.setGeometry(0,0,20,20);
#         closeButton.setGeometry(20,0,20,20);
        lay.addStretch()
        lay.setMargin(1)
        lay.addWidget(minButton,0,Qt.AlignTop)
        lay.addWidget(self.maxButton,0,Qt.AlignTop)
        lay.addWidget(closeButton,0,Qt.AlignTop)
        return contain
        
    def mouseDoubleClickEvent(self, event):
        if self.maxButton == None:
            return
        if(self.isMaximized()):
            self.maxButton.setIcon(QIcon(self.maxPix))
            self.showNormal()#窗口还原
        else:
            self.maxButton.setIcon(QIcon(self.normalPix))
            self.showMaximized()#窗口还原
        

class KWorkspace(QWorkspace):
    def __init__(self,parent = None):
        QWorkspace.__init__(self,parent)
        self.setWindowFlags(Qt.MSWindowsFixedSizeDialogHint | Qt.FramelessWindowHint)#

        
class KGroupBox(QGroupBox):
    def __init__(self,parent = None):
        QGroupBox.__init__(self,parent)
        
        #为子部件添加阴影比较简单，使用如下方式：
#         shadow_effect = QGraphicsDropShadowEffect(self);
#         shadow_effect.setOffset(5, 5);
#         shadow_effect.setColor(Qt.gray);
#         shadow_effect.setBlurRadius(8);
#         self.setGraphicsEffect(shadow_effect)
        
class KApplication(QApplication):
    
    def __init__(self, parent = None):
        QApplication.__init__(self,parent)
    
    def GET_X_LPARAM(self, param):
        #define LOWORD(l)           ((WORD)((DWORD_PTR)(l) & 0xffff))
        #define HIWORD(l)           ((WORD)((DWORD_PTR)(l) >> 16))
        #define GET_X_LPARAM(lp)                        ((int)(short)LOWORD(lp))
        #define GET_Y_LPARAM(lp)                        ((int)(short)HIWORD(lp))
        return param & 0xffff

    def GET_Y_LPARAM(self, param):
        return param >> 16
    
    def winEventFilter(self, msg):
        if msg.message == 0x84: #WM_NCHIT 
            form = self.activeWindow()
            if form:
                xPos = self.GET_X_LPARAM(msg.lParam) - form.frameGeometry().x()
                yPos = self.GET_Y_LPARAM(msg.lParam) - form.frameGeometry().y()
#                鼠标在窗体自定义标题范围内，窗体自定义一个isInTitle的方法判断 
#                if yPos < 30 and xPos < 456:
                if not form.isMaximized() and hasattr(form, 'isInTitle') and form.isInTitle(xPos, yPos):
                    return True, 0x2 #HTCAPTION
            
        return False, 0
class KErrorWidget(QDialog):
    def __init__(self,parent = None):
        QDialog.__init__(self,parent)
        if parent == None:
            width = 200
        else:
            width =parent.width();
        self.resize(200, 28);
        #设置标题栏隐藏
#         self.setWindowFlags(Qt.FramelessWindowHint);
        #设置背景色透明
        palette = QPalette();
        color = QColor(190, 230, 250);
        color.setAlphaF(0.6);
        palette.setBrush(self.backgroundRole(),color);
        self.setPalette(palette);
        self.setAutoFillBackground(True);
#
    def close(self):
        QDialog.close(self)
        
    def reject(self):
        QDialog.reject(self)
        
    def keyPressEvent(self,event):
        if event.key() == Qt.Key_Escape:
            self.close()
        else:
            return QDialog.keyPressEvent(self,event)
    
    
class KMLeftPushButton(QPushButton):
    
    id = None
    hover = False
    def __init__(self,text,pic_name = None,parent = None):
        QPushButton.__init__(self,parent)
#         super(KPushButton,self).__init__(parent)
        
        #记录状态
        '''
        0 代表正常状态
        1 鼠标经过
        2 鼠标点击
        '''
        self.status = 0
        self.setCursor(Qt.PointingHandCursor)
        #计步器
        self.text = text
        self.i = 0
        self.pixmap = QPixmap(pic_name)
        self.btn_width = self.pixmap.width() #???
        self.btn_height = self.pixmap.height() #???
        font = QFont()
        font.setBold(True)
        self.setFont(font)
        self.setContentsMargins(0,0, 0, 0)
        self.setStyleSheet("QPushButton{font-family:Microsoft YaHei;}")
        '''
                        如果不固定大小,拖动父控件是，按钮和背景会缩放
        '''
        self.setFixedSize(self.btn_width,self.btn_height)
        
    '''
        loadPixmap
                        自定义方法
    '''
    
    def setID(self,id):    
        self.id = id
    
    def loadPixmap(self,pic_name):
        '''
                        获取按钮背景图片路径，通过背景图片重置按钮宽高，宽
        '''
        pass
        
    
    '''
            重写按钮绘制方法，
                        当第一次执行是，会调用一次，
                        切换改窗口，会调用两次，
                        点击按钮时，会调用两次（应该是up和down）
                        当鼠标down时，进或出按钮会调用一次该事件
                        鼠标up时，进出该按钮不会调用该事件
            
            改方法应该是在其父窗口绘制方法后执行
            如果直接return掉，则按钮不会被绘制出来
            
            如果不掉用painter的end()方法，则不能用self.painter,如果有用end()方法结束绘制，则可以用临时变量，也可以用属性
    
            如果把 painter = QPainter() 写成 self.painter = QPainter()
            那么当缩放父级窗口时，会报名-->
            
    QPaintDevice: Cannot destroy paint device that is being painted
    
            错误
            
            我们得记住重载paintEvent()函数的时候，里面的Qpainter()对象一定不能带self，不然就会出现析构错误.
    '''
    def paintEvent(self,event):
        self.i += 1
#         print 'child',self.i
        #绘制按钮背景
        self.drawBackground(event)
        
    '''
            鼠标hover事件，且是当鼠标为up的
            因为不会调用paintEvent方法，所以使用self.update方法，强制执行paintEvent方法
    '''
    def enterEvent(self,event):
        self.status = 1
        
#         self.hover = True
        self.update()
    
    def leaveEvent(self,event):
        self.status = 0
        
#         self.hover = False
        self.update()
    
    '''
            鼠标点击事件,使用pass重写，则不响应点击事件
            默认鼠标左击会触发paintEvent，右击不会触发
    '''
        
    def mousePressEvent(self,event):    
        #若点击鼠标左键
        if event.button() == Qt.LeftButton:
            self.status = 2
            self.update()
        QPushButton.mousePressEvent(self,event)
            
        
    def mouseReleaseEvent(self,event):
        
        if event.button() == Qt.LeftButton:
            self.status = 1
            self.update()
        QPushButton.mouseReleaseEvent(self,event)
        
    '''
    private 绘制按钮背景，只能是paintEvent事件调用
    '''
    def drawBackground(self,event):
        painter = QPainter()
        painter.begin(self)
        '''
        self.pixmap.copy 第一个参数主要有三种情况
                        分别是宽度*1，*2，*3，对应鼠标的三种状态
        '''
        if(self.hover):
            painter.drawPixmap(self.rect(), self.pixmap.copy(0,0,self.btn_width, self.btn_height))
        
        painter.drawText(QRectF(0,0,self.btn_width,self.btn_height),Qt.AlignCenter, self.text)
        painter.end()
    
    
class KMPushButton(QPushButton):
    def __init__(self,parent = None):
        QPushButton.__init__(self,parent)
        
        #鏋氫妇鍊�
        self.status = 0 #self.NORMAL
        #self.pixmap = QPixmap()
        #self.btn_width = 40 #鎸夐挳瀹藉害
        #self.btn_height = 20#鎸夐挳楂樺害
        #self.mouse_press = False #鎸夐挳宸﹂敭鏄惁鎸変笅        

    def loadPixmap(self, pic_name):    
        self.pixmap = QPixmap(pic_name)
        self.btn_width = self.pixmap.width()/4
        self.btn_height = self.pixmap.height()
        self.setFixedSize(self.btn_width, self.btn_height)
        
    
    def enterEvent(self,event):    
        self.status = 1 #self.ENTER
        self.update()
    

    def mousePressEvent(self,event):    
        #鑻ョ偣鍑婚紶鏍囧乏閿�
        if(event.button() == Qt.LeftButton):        
            self.mouse_press = True
            self.status = 2 #self.PRESS
            self.update()        

    def mouseReleaseEvent(self,event):    
        #鑻ョ偣鍑婚紶鏍囧乏閿�
        if(self.mouse_press):        
            self.mouse_press = False
            self.status = 3 #self.ENTER
            self.update()
            self.clicked.emit(True)        

    def leaveEvent(self,event):    
        self.status = 0 #self.NORMAL
        self.update()
    

    def paintEvent(self,event):    
        self.painter = QPainter()
        self.painter.begin(self)
        self.painter.drawPixmap(self.rect(), self.pixmap.copy(self.btn_width * self.status, 0, self.btn_width, self.btn_height))
        self.painter.end()
        

class KPushButton(QPushButton):
    string = ""
    title = ""
    window = None
    def __init__(self,parent = None):
        QPushButton.__init__(self,parent)
        
        #鏋氫妇鍊�
        self.status = 0 #self.NORMAL
        self.setCursor(Qt.PointingHandCursor)

    def loadPixmap(self, pic_name):    
        self.pixmap = QPixmap(pic_name)
        self.btn_width = self.pixmap.width()
        self.btn_height = self.pixmap.height()
        self.setFixedSize(self.btn_width, self.btn_height)
        
    def loadText(self,string):
        self.string = string
        
    
    def enterEvent(self,event):    
        self.status = 1 #self.ENTER
        self.update()
    

    def mousePressEvent(self,event):    
        #鑻ョ偣鍑婚紶鏍囧乏閿�
        if(event.button() == Qt.LeftButton):        
            self.mouse_press = True
            self.status = 2 #self.PRESS
            self.update()        

    def mouseReleaseEvent(self,event):    
        #鑻ョ偣鍑婚紶鏍囧乏閿�
        if(self.mouse_press):        
            self.mouse_press = False
            self.status = 3 #self.ENTER
            self.update()
            self.clicked.emit(True)        

    def leaveEvent(self,event):    
        self.status = 0 #self.NORMAL
        self.update()
    

    def paintEvent(self,event):    
        painter = QPainter()
        painter.begin(self)
        painter.drawPixmap(self.rect(), self.pixmap)
        if self.string !="":
            painter.drawText(self.rect(),Qt.AlignCenter, self.string)
        painter.end()

class KTipWidget(KDialog):
    def __init__(self,string = "demo",parent = None):
        KDialog.__init__(self, parent)
        self.setColor(QColor.fromRgb(239,235,231))
        self.setFixedWidth(420)
        layout = QVBoxLayout(self)
        layout.setMargin(0)
        layout.setContentsMargins(0, 0, 0, 20)
        widget = KDialog()
        widget.is_move = False
        widget.setFixedHeight(57)
        widget.setBack("./img/kt/kt_error_line.png")
        layout.addWidget(widget,0,Qt.AlignTop)
        
        widget2 = QWidget()
        layout.addWidget(widget2)
        hlayout = QHBoxLayout(widget2)
        hlayout.setContentsMargins(20, 20, 20, 20)
        
        label = QLabel()
        pixmap = QPixmap("./img/kt/kt_tip1.png")
        label.setPixmap(pixmap)
        hlayout.addWidget(label)
        
        label2 = QLabel(string)
        label2.setStyleSheet("padding-left:20px;font-size:18px;font-family:Microsoft YaHei;")
        hlayout.addWidget(label2)
        hlayout.addStretch()
        
        
        layout.addStretch()
        button = KPushButton()
        button.loadPixmap("./img/kt/kt_login_btn.png")
        button.loadText(u"确　定")
        button.setStyleSheet("color:#fff;font-size:16px;font-family:Times New Roman;")
        layout.addWidget(button,0,Qt.AlignHCenter)
        
        self.setLayout(layout)
        
        self.setModal(True)#ui阻塞
        self.connect(button, SIGNAL("clicked()"),self.close)
        self.show()
        
class KMainWindow(QMainWindow):
    is_move = True
    color = None
    
    def __init__(self,parent = None):
        QMainWindow.__init__(self,parent)
        self.setWindowFlags(Qt.MSWindowsFixedSizeDialogHint|Qt.FramelessWindowHint)
        
    
    def setColor(self,color):    
        self.color = color
    
    def mouseDoubleClickEvent(self, event):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()
        return QMainWindow.mouseDoubleClickEvent(self, event)
    
    def mousePressEvent(self,event):
        if(event.button() == Qt.LeftButton):
            self.mouse_press = True

            #窗口位置
            self.move_point = event.globalPos() - self.pos()
#             event.ignore();
    def mouseMoveEvent(self,event):
        #若鼠标左键被按下
        if(self.mouse_press):
            #获取位置
            move_pos = event.globalPos()
  
            if self.is_move:
                #移动主窗体位置
                self.move(move_pos - self.move_point)

    def mouseReleaseEvent(self,event):
        #设置鼠标为未被按下
        self.mouse_press = False;
        
    def paintEvent(self, event):
        
        painter = QPainter()
        painter.begin(self)
        if self.color != None:
            painter.setPen(QPen(self.color))
            painter.setBrush(QBrush(self.color))
            painter.drawRect(self.rect())
        painter.end()
        
class KTabBar(QTabBar):
    def __init__(self,parent = None):
        QTabBar.__init__(self,parent)
        
    def mouseDoubleClickEvent(self,event):
        #双击关闭Tab
        print self.tabAt(event.pos())
        self.emit(SIGNAL("tabCloseRequested(int)"),self.tabAt(event.pos()))
        
class KTabWidget(QTabWidget):
    def __init__(self,parent = None):
        QTabWidget.__init__(self,parent)
        
        tabBarStyle ="QTabWidget::pane{border-width:1px 1px 1px 0px;border-color:#666666;\
                                    border-style: outset;background-color: rgb(132, 171, 208);\
                                    background: transparent;}"
        tabBarStyle += "QTabBar::tab {\
                        min-width:80px;color: #666;\
                        margin-right:2px;\
                        background-color:qlineargradient(x1:0, y1:0, x2:0, y2:1, stop: 0 #eeeeee, stop: 1 gray);\
                        border: 1px solid #666;border-bottom:0px;\
                        border-top-left-radius:2px;\
                        border-top-right-radius:2px;\
                        padding:3px;}    \
                        QTabBar::tab:!selected {margin-top:4px;border:1px solid #b7b5b5;background:#8eb995;} \
                        QTabBar::tab:selected {color: #000;background:#6cb479;}"

        self.setStyleSheet(tabBarStyle)



class KCellWidget(QWidget):
    def __init__(self,widget,id,parent = None):
        
        QWidget.__init__(self,parent)
        self.widget = widget
        self.id = id
        vlayout = QVBoxLayout(self)
        vlayout.setMargin(0)
        vlayout.addWidget(self.widget,0,Qt.AlignCenter)
#     def mousePressEvent(self,event):
#         QCheckBox.mousePressEvent(self,event)
#     def eventFilter(self,event):
#          pass

    def mousePressEvent(self,event):
        self._changeChildStatus()
        
        return QWidget.mousePressEvent(self, event)
    
    def _changeChildStatus(self):
        if type(self.widget) == type(QCheckBox()):
            self._changeCheckBox()
            return 
        
    def _changeCheckBox(self):
        if self.widget.checkState() == Qt.Checked:
            self.widget.setCheckState(Qt.Unchecked)
        else:
            self.widget.setCheckState(Qt.Checked)

class KCheckBox(QCheckBox):
    def __init__(self,text="",id = 0,parent = None):
        QCheckBox.__init__(self,text,parent)
        self.__id = id
    def getId(self):
        return self.__id
    
class KTableWidget(QTableWidget):
    def __init__(self,parent = None):
        QTableWidget.__init__(self,parent)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
    pass
class KLeadButton(QToolButton):
    def __init__(self,pic_name,parent = None):
        QToolButton.__init__(self,parent)
        
        self.setCursor(Qt.PointingHandCursor)
        
        self.pixmap = QPixmap(pic_name)
        self.btn_width = self.pixmap.width()
        self.btn_height = self.pixmap.height()
        self.setFixedSize(self.btn_width, self.btn_height)
        
    def setTitle(self,title):
        self.title = title
        
    def setWindow(self,window):
        self.window = window
        
    def paintEvent(self,event):    
        painter = QPainter()
        painter.begin(self)
        painter.drawPixmap(self.rect(), self.pixmap)
        painter.end()
        
class KLeadLabel(QToolButton):
    def __init__(self,pic_name,parent = None):
        QToolButton.__init__(self,parent)
        
#         self.setCursor(Qt.PointingHandCursor)
        
        self.pixmap = QPixmap(pic_name)
        self.btn_width = self.pixmap.width()
        self.btn_height = self.pixmap.height()
        self.setFixedSize(self.btn_width, self.btn_height)
        
    def paintEvent(self,event):    
        painter = QPainter()
        painter.begin(self)
        painter.drawPixmap(self.rect(), self.pixmap)
        painter.end()