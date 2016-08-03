#coding:utf-8

from application.lib.Commethods import *
from application.controller.main_order import MainOrder
from PyQt4 import QtGui
'''
Created on 2015年1月20日

@author: kylin

左侧菜单

'''

class MainLeftMenu(KDialog):
    names = []
    def __init__(self,parent = None):
        KDialog.__init__(self, parent)
        self._setBackground()
        layout = QVBoxLayout(self)
        layout.setMargin(0)
        layout.setContentsMargins(0, 23, 0, 30)
        
        
        pixmap = QPixmap("./img/logo.png")
        logo = QLabel()
        logo.setPixmap(pixmap)
        logo.setContentsMargins(10, 30, 0,30)
        
        leftButtonList_name = MainOrder.getLeftOrder()
        MainLeftMenu.names = leftButtonList_name
        self.leftButtonList = []
#         l1 = KMLeftPushButton(u"资金管理","./img/leftbutton_bg.png")
#         
        pixmap = QPixmap("./img/leftmenu_label.png")
        
        for key,i in enumerate(leftButtonList_name):
            leftBtn = KMLeftPushButton(i,"./img/leftbutton_bg.png")
            leftBtn.setID(key)
            self.leftButtonList.append(leftBtn)
            layout.addWidget(leftBtn,0,Qt.AlignHCenter)
            self.connect(leftBtn, SIGNAL("clicked()"),self.btnClicked)
            if key == len(leftButtonList_name) - 1:
                continue
            label = QLabel()
            label.setPixmap(pixmap)
            label.setContentsMargins(0, 5, 0, 5)
            layout.addWidget(label,0,Qt.AlignHCenter)
        
        
        layout.addStretch()
        layout.addWidget(logo,0,Qt.AlignHCenter)
        self.setBack("./img/leftmenu_bg.png")
        self.is_move = False

    def keyPressEvent(self,event):
        if event.key() == Qt.Key_Escape:
            return
        return QDialog.keyPressEvent(self,event)
    
    def btnClicked(self):
        self.sender().hover = True
        for i in self.leftButtonList:
            if i != self.sender():
                i.hover = False
            i.update()
                
        self.emit(SIGNAL("btnClicked"),self.sender().id)
        
    def _setBackground(self):
#         palette.setBrush(self.backgroundRole(),QBrush(QPixmap("../img/leftmenu_bg.png")))
#         palette = QPalette()
#         self.setPalette(palette)
        self.setFixedWidth(163)
        
        
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainleftmenu = MainLeftMenu()
    mainleftmenu.show()
    sys.exit(app.exec_())