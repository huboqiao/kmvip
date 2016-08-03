# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'cardrecord.ui'
#
# Created: Mon Mar 16 18:00:27 2015
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
        Dialog.resize(673, 381)
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.cardtableWidget = QtGui.QTableWidget(Dialog)
        self.cardtableWidget.setObjectName(_fromUtf8("cardtableWidget"))
        self.cardtableWidget.setColumnCount(4)
        self.cardtableWidget.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.cardtableWidget.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.cardtableWidget.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.cardtableWidget.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.cardtableWidget.setHorizontalHeaderItem(3, item)
        self.gridLayout.addWidget(self.cardtableWidget, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "客户用卡记录", None))
        item = self.cardtableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "金荣卡号", None))
        item = self.cardtableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "金荣卡芯片号", None))
        item = self.cardtableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Dialog", "开卡日期", None))
        item = self.cardtableWidget.horizontalHeaderItem(3)
        item.setText(_translate("Dialog", "状态", None))

