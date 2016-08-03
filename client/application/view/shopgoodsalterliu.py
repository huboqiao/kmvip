# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/shopgoodsalterliu.ui'
#
# Created: Fri Mar 20 11:21:59 2015
#      by: PyQt4 UI code generator 4.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(336, 523)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.widget = QtGui.QWidget(Dialog)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.widget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(self.widget)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.goodsname = QtGui.QLineEdit(self.widget)
        self.goodsname.setObjectName(_fromUtf8("goodsname"))
        self.horizontalLayout.addWidget(self.goodsname)
        self.verticalLayout.addWidget(self.widget)
        self.treeWidget = QtGui.QTreeWidget(Dialog)
        self.treeWidget.setObjectName(_fromUtf8("treeWidget"))
        self.verticalLayout.addWidget(self.treeWidget)
        self.widget_5 = QtGui.QWidget(Dialog)
        self.widget_5.setObjectName(_fromUtf8("widget_5"))
        self.horizontalLayout_5 = QtGui.QHBoxLayout(self.widget_5)
        self.horizontalLayout_5.setMargin(0)
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.label_4 = QtGui.QLabel(self.widget_5)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.horizontalLayout_5.addWidget(self.label_4)
        self.comboBox = QtGui.QComboBox(self.widget_5)
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.comboBox.addItem(_fromUtf8(""))
        self.horizontalLayout_5.addWidget(self.comboBox)
        self.verticalLayout.addWidget(self.widget_5)
        self.widget_7 = QtGui.QWidget(Dialog)
        self.widget_7.setObjectName(_fromUtf8("widget_7"))
        self.horizontalLayout_7 = QtGui.QHBoxLayout(self.widget_7)
        self.horizontalLayout_7.setMargin(0)
        self.horizontalLayout_7.setObjectName(_fromUtf8("horizontalLayout_7"))
        self.label_6 = QtGui.QLabel(self.widget_7)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.horizontalLayout_7.addWidget(self.label_6)
        self.comboBox_2 = QtGui.QComboBox(self.widget_7)
        self.comboBox_2.setObjectName(_fromUtf8("comboBox_2"))
        self.comboBox_2.addItem(_fromUtf8(""))
        self.comboBox_2.addItem(_fromUtf8(""))
        self.horizontalLayout_7.addWidget(self.comboBox_2)
        self.verticalLayout.addWidget(self.widget_7)
        self.widget_2 = QtGui.QWidget(Dialog)
        self.widget_2.setObjectName(_fromUtf8("widget_2"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.widget_2)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_2 = QtGui.QLabel(self.widget_2)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_2.addWidget(self.label_2)
        self.unit = QtGui.QLineEdit(self.widget_2)
        self.unit.setObjectName(_fromUtf8("unit"))
        self.horizontalLayout_2.addWidget(self.unit)
        self.verticalLayout.addWidget(self.widget_2)
        self.widget_6 = QtGui.QWidget(Dialog)
        self.widget_6.setObjectName(_fromUtf8("widget_6"))
        self.horizontalLayout_6 = QtGui.QHBoxLayout(self.widget_6)
        self.horizontalLayout_6.setMargin(0)
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.label_5 = QtGui.QLabel(self.widget_6)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.horizontalLayout_6.addWidget(self.label_5)
        self.price = QtGui.QLineEdit(self.widget_6)
        self.price.setObjectName(_fromUtf8("price"))
        self.horizontalLayout_6.addWidget(self.price)
        self.verticalLayout.addWidget(self.widget_6)
        self.widget_3 = QtGui.QWidget(Dialog)
        self.widget_3.setObjectName(_fromUtf8("widget_3"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.widget_3)
        self.horizontalLayout_3.setMargin(0)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.label_3 = QtGui.QLabel(self.widget_3)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_3.addWidget(self.label_3)
        self.ssn = QtGui.QLineEdit(self.widget_3)
        self.ssn.setObjectName(_fromUtf8("ssn"))
        self.horizontalLayout_3.addWidget(self.ssn)
        self.verticalLayout.addWidget(self.widget_3)
        self.widget_4 = QtGui.QWidget(Dialog)
        self.widget_4.setObjectName(_fromUtf8("widget_4"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout(self.widget_4)
        self.horizontalLayout_4.setMargin(0)
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.pushButton = QtGui.QPushButton(self.widget_4)
        self.pushButton.setMinimumSize(QtCore.QSize(0, 25))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.horizontalLayout_4.addWidget(self.pushButton)
        self.pushButton_2 = QtGui.QPushButton(self.widget_4)
        self.pushButton_2.setMinimumSize(QtCore.QSize(0, 25))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.horizontalLayout_4.addWidget(self.pushButton_2)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem1)
        self.verticalLayout.addWidget(self.widget_4)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "添加商品", None))
        self.label.setText(_translate("Dialog", "商品名称：", None))
        self.treeWidget.headerItem().setText(0, _translate("Dialog", "选择商品分类名称", None))
        self.label_4.setText(_translate("Dialog", "供应商：", None))
        self.comboBox.setItemText(0, _translate("Dialog", "请选择", None))
        self.label_6.setText(_translate("Dialog", "显示：", None))
        self.comboBox_2.setItemText(0, _translate("Dialog", "是", None))
        self.comboBox_2.setItemText(1, _translate("Dialog", "否", None))
        self.label_2.setText(_translate("Dialog", "计量单位：", None))
        self.label_5.setText(_translate("Dialog", "价格(元)：", None))
        self.label_3.setText(_translate("Dialog", "商品条形码：", None))
        self.pushButton.setText(_translate("Dialog", "修改", None))
        self.pushButton_2.setText(_translate("Dialog", "关闭", None))

