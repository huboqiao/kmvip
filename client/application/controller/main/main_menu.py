#coding:utf-8
'''
Created on 2015年1月20日

@author: kylin

顶部菜单

'''
from application.lib.Commethods import *
from application.lib.KT import KDialog
from application.view.main_menu import Ui_Dialog

from application.controller.systemseting import Systemseting
from application.controller.upver import upVerController
from application.controller.setting import SettingController
from application.controller.shopsys import ShopSysController
from application.controller.userlist import UserListController
from application.controller.addcard import AddcardContorller
from application.controller.main.maintab import MainTab

class MainMenu(ControllerAction,Ui_Dialog):
    def __init__(self,parent = None):
        ControllerAction.__init__(self, parent)
#         self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setContentsMargins(30, 0, 0, 0)
        
        
        #设置背景
        self._setBackground()
        
        #设置logo
        self._setLogo()
        
        #设置间隔
#         self._setLabel()
        
        #设置菜单
#         self._setMenu()
        
        #
#         self._setSIGNAL()
        
        self.setBack("./img/main_menu_bg.png")
        
        self.is_move = False
        
        self.setCloseAble(self.widget,parent)
        
    def _setSIGNAL(self):
        self.connect(self.pushButton_4,SIGNAL("clicked()"),self.setting)
        self.connect(self.pushButton_6,SIGNAL("clicked()"),self.updateVer)
        self.connect(self.pushButton_5,SIGNAL("clicked()"),self.lock)
        self.connect(self.pushButton_3,SIGNAL("clicked()"),self.user)
        self.connect(self.pushButton_2,SIGNAL("clicked()"),self.addCard)
        
        # 添加金荣卡
    def addCard(self):
        MainTab.openDialog(AddcardContorller(self),u"添加金荣卡")
        
        #锁屏
    def lock(self):
        MainTab.openDialog(ShopSysController(self),u"锁屏")
        #权限
    def user(self):
        ControllerAction.openTab(UserListController(),u"用户")
        
    def setting(self):
        ControllerAction.openTab(SettingController(),u"设置")
        
    def updateVer(self):
        upVerController(self).exec_()
        
    def _setBackground(self):
#         palette = QPalette()
#         palette.setBrush(self.backgroundRole(),QBrush(QPixmap("../img/main_menu_bg.png")))
#         self.setPalette(palette)
        self.setFixedHeight(53)
        
    def _setLogo(self):
        pixmap = QPixmap("./img/logo_main_menu.png")
        self.label.setPixmap(pixmap)
        self.label.setContentsMargins(0,0,0,0)
        pass
    
    def _setLabel(self):
        pixmap = QPixmap("./img/main_menu_label.png")
        self.label_3.setPixmap(pixmap)
        self.label_4.setPixmap(pixmap)
        self.label_5.setPixmap(pixmap)
        self.label_6.setPixmap(pixmap)
        self.label_3.setContentsMargins(2, 0, 2, 0)
        self.label_4.setContentsMargins(2, 0, 2, 0)
        self.label_5.setContentsMargins(2, 0, 2, 0)
        self.label_6.setContentsMargins(2, 0, 2, 0)
        
    def _setMenu(self):
        css = "QPushButton{background:transparent;font-size:14px;font-family:Microsoft YaHei;}"+"QPushButton:hover{color:white;}"
        self.pushButton_2.setStyleSheet(css)
        self.pushButton_3.setStyleSheet(css)
        self.pushButton_4.setStyleSheet(css)
        self.pushButton_5.setStyleSheet(css)
        self.pushButton_6.setStyleSheet(css)
        self.pushButton_2.setCursor(Qt.PointingHandCursor)
        self.pushButton_3.setCursor(Qt.PointingHandCursor)
        self.pushButton_4.setCursor(Qt.PointingHandCursor)
        self.pushButton_5.setCursor(Qt.PointingHandCursor)
        self.pushButton_6.setCursor(Qt.PointingHandCursor)
        
if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    mainmenu = MainMenu()
    mainmenu.show()
    sys.exit(app.exec_())