#coding:utf-8
'''
Created on 2015年1月20日

@author: kylin

顶部工具栏

'''
from application.lib.Commethods import *
from application.view.main_tool import Ui_Dialog
from application.controller.addcard import AddcardContorller
from application.controller.shopsys import ShopSysController
from application.controller.storagelist import StorageList
from application.controller.servicequery import ServiceQueryController
from application.controller.main.maintab import MainTab
from application.controller.congZhi import CongZhiContorller

class MainTool(ControllerAction,Ui_Dialog):
    def __init__(self,parent = None):
        ControllerAction.__init__(self, parent)
        self.setColor(QColor(204,188,122))
        
        self.horizontalLayout.setContentsMargins(30, 5, 0, 5)
        
        self.setStyleSheet("QDialog{background:#ccbc7a;}")
        
        css = "QToolButton{background:transparent;font-size:14px;font-family:Microsoft YaHei;}"+"QToolButton:hover{color:white;}"
        
        self.toolButton.setStyleSheet(css)
        self.toolButton_2.setStyleSheet(css)
        self.toolButton_3.setStyleSheet(css)
        
        self.toolButton.setCursor(Qt.PointingHandCursor)
        self.toolButton_2.setCursor(Qt.PointingHandCursor)
        self.toolButton_3.setCursor(Qt.PointingHandCursor)
        
        icon = QIcon("./img/tool_1.png")
        self.toolButton.setIcon(icon)
        self.toolButton.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        
        icon = QIcon("./img/tool_2.png")
        self.toolButton_2.setIcon(icon)
        self.toolButton_2.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        
        icon = QIcon("./img/tool_3.png")
        self.toolButton_3.setIcon(icon)
        self.toolButton_3.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        
        
        self.connect(self.toolButton, SIGNAL("clicked()"), self.addCard)  # 添加金荣卡
        self.connect(self.toolButton_2, SIGNAL("clicked()"), self.yewu)  # 添加金荣卡
        self.connect(self.toolButton_3, SIGNAL("clicked()"), self.kecun)  # 添加金荣卡
        
    #业务查询
    def yewu(self):
        ControllerAction.openTab(ServiceQueryController(),u"业务进度查询")
    
    #库存查询
    def kecun(self):
        ControllerAction.openTab(StorageList(),u"库存列表")
    
    # 添加金荣卡
    def addCard(self):
        
        ControllerAction.openTab(CongZhiContorller(),u"充值")
        


if __name__ == "__main__":
    app = QApplication(sys.argv)
    maintool = MainTool()
    maintool.show()
    sys.exit(app.exec_())