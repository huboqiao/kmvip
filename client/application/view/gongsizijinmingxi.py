# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gongsizijinmingxi.ui'
#
# Created: Wed Apr 29 17:39:58 2015
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
        Dialog.resize(1060, 604)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.widget_2 = QtGui.QWidget(Dialog)
        self.widget_2.setMinimumSize(QtCore.QSize(0, 0))
        self.widget_2.setObjectName(_fromUtf8("widget_2"))
        self.gridLayout = QtGui.QGridLayout(self.widget_2)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_12 = QtGui.QLabel(self.widget_2)
        self.label_12.setMinimumSize(QtCore.QSize(0, 40))
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.gridLayout.addWidget(self.label_12, 0, 0, 1, 1)
        self.label_5 = QtGui.QLabel(self.widget_2)
        self.label_5.setMinimumSize(QtCore.QSize(0, 40))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 0, 1, 1, 1)
        self.label_11 = QtGui.QLabel(self.widget_2)
        self.label_11.setMinimumSize(QtCore.QSize(0, 40))
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.gridLayout.addWidget(self.label_11, 0, 2, 1, 1)
        self.dateEdit = QtGui.QDateEdit(self.widget_2)
        self.dateEdit.setMinimumSize(QtCore.QSize(0, 40))
        self.dateEdit.setCalendarPopup(True)
        self.dateEdit.setObjectName(_fromUtf8("dateEdit"))
        self.gridLayout.addWidget(self.dateEdit, 0, 3, 1, 1)
        self.label_10 = QtGui.QLabel(self.widget_2)
        self.label_10.setMinimumSize(QtCore.QSize(0, 40))
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.gridLayout.addWidget(self.label_10, 0, 4, 1, 1)
        self.dateEdit_2 = QtGui.QDateEdit(self.widget_2)
        self.dateEdit_2.setMinimumSize(QtCore.QSize(0, 40))
        self.dateEdit_2.setCalendarPopup(True)
        self.dateEdit_2.setObjectName(_fromUtf8("dateEdit_2"))
        self.gridLayout.addWidget(self.dateEdit_2, 0, 5, 1, 1)
        self.label_13 = QtGui.QLabel(self.widget_2)
        self.label_13.setMinimumSize(QtCore.QSize(0, 40))
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.gridLayout.addWidget(self.label_13, 0, 6, 1, 1)
        self.comboBox = QtGui.QComboBox(self.widget_2)
        self.comboBox.setMinimumSize(QtCore.QSize(0, 40))
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.comboBox, 0, 7, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 8, 1, 1)
        self.pushButton = QtGui.QPushButton(self.widget_2)
        self.pushButton.setMinimumSize(QtCore.QSize(0, 40))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.gridLayout.addWidget(self.pushButton, 0, 9, 1, 1)
        self.pushButton_2 = QtGui.QPushButton(self.widget_2)
        self.pushButton_2.setMinimumSize(QtCore.QSize(0, 40))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.gridLayout.addWidget(self.pushButton_2, 0, 10, 1, 1)
        self.pushButton_3 = QtGui.QPushButton(self.widget_2)
        self.pushButton_3.setMinimumSize(QtCore.QSize(0, 40))
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.gridLayout.addWidget(self.pushButton_3, 0, 11, 1, 1)
        self.pushButton_4 = QtGui.QPushButton(self.widget_2)
        self.pushButton_4.setMinimumSize(QtCore.QSize(0, 40))
        self.pushButton_4.setObjectName(_fromUtf8("pushButton_4"))
        self.gridLayout.addWidget(self.pushButton_4, 0, 12, 1, 1)
        self.pushButton_5 = QtGui.QPushButton(self.widget_2)
        self.pushButton_5.setMinimumSize(QtCore.QSize(0, 40))
        self.pushButton_5.setObjectName(_fromUtf8("pushButton_5"))
        self.gridLayout.addWidget(self.pushButton_5, 0, 13, 1, 1)
        self.verticalLayout.addWidget(self.widget_2)
        self.tableWidget = QtGui.QTableWidget(Dialog)
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, item)
        self.verticalLayout.addWidget(self.tableWidget)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "公司资金明细", None))
        self.label_12.setText(_translate("Dialog", "经办人", None))
        self.label_5.setText(_translate("Dialog", "xxx", None))
        self.label_11.setText(_translate("Dialog", "开始时间：", None))
        self.label_10.setText(_translate("Dialog", "结束时间：", None))
        self.label_13.setText(_translate("Dialog", " 交易方式 ", None))
        self.comboBox.setItemText(0, _translate("Dialog", "所有方式", None))
        self.comboBox.setItemText(1, _translate("Dialog", "现金充值", None))
        self.comboBox.setItemText(2, _translate("Dialog", "银行卡充值", None))
        self.comboBox.setItemText(3, _translate("Dialog", "现金提现", None))
        self.comboBox.setItemText(4, _translate("Dialog", "银行卡提现", None))
        self.pushButton.setText(_translate("Dialog", "查    询", None))
        self.pushButton_2.setText(_translate("Dialog", "导    出", None))
        self.pushButton_3.setText(_translate("Dialog", "打    印", None))
        self.pushButton_4.setText(_translate("Dialog", "打印预览", None))
        self.pushButton_5.setText(_translate("Dialog", "字段配置", None))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "客户姓名", None))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "金荣卡", None))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Dialog", "交易方式", None))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("Dialog", "经办人", None))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("Dialog", "操作时间", None))
        item = self.tableWidget.horizontalHeaderItem(5)
        item.setText(_translate("Dialog", "金额", None))

