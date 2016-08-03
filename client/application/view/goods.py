# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\www\kmvip\src\ui\goods.ui'
#
# Created: Fri Aug 15 14:58:42 2014
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
        Dialog.resize(844, 611)
        Dialog.setMinimumSize(QtCore.QSize(844, 611))
        Dialog.setMaximumSize(QtCore.QSize(844, 611))
        self.groupBox = QtGui.QGroupBox(Dialog)
        self.groupBox.setGeometry(QtCore.QRect(16, 10, 271, 581))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.treeWidget = QtGui.QTreeWidget(self.groupBox)
        self.treeWidget.setGeometry(QtCore.QRect(10, 63, 256, 511))
        self.treeWidget.setObjectName(_fromUtf8("treeWidget"))
        self.pushButton = QtGui.QPushButton(self.groupBox)
        self.pushButton.setGeometry(QtCore.QRect(12, 21, 75, 28))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.pushButton_3 = QtGui.QPushButton(self.groupBox)
        self.pushButton_3.setEnabled(False)
        self.pushButton_3.setGeometry(QtCore.QRect(190, 21, 75, 28))
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.pushButton_6 = QtGui.QPushButton(self.groupBox)
        self.pushButton_6.setEnabled(False)
        self.pushButton_6.setGeometry(QtCore.QRect(100, 21, 75, 28))
        self.pushButton_6.setObjectName(_fromUtf8("pushButton_6"))
        self.groupBox_2 = QtGui.QGroupBox(Dialog)
        self.groupBox_2.setGeometry(QtCore.QRect(299, 9, 530, 581))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.tableWidget = QtGui.QTableWidget(self.groupBox_2)
        self.tableWidget.setGeometry(QtCore.QRect(10, 63, 511, 510))
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.tableWidget.setColumnCount(5)
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
        self.pushButton_2 = QtGui.QPushButton(self.groupBox_2)
        self.pushButton_2.setGeometry(QtCore.QRect(10, 20, 93, 28))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.pushButton_4 = QtGui.QPushButton(self.groupBox_2)
        self.pushButton_4.setEnabled(False)
        self.pushButton_4.setGeometry(QtCore.QRect(110, 20, 93, 28))
        self.pushButton_4.setObjectName(_fromUtf8("pushButton_4"))
        self.pushButton_5 = QtGui.QPushButton(self.groupBox_2)
        self.pushButton_5.setEnabled(False)
        self.pushButton_5.setGeometry(QtCore.QRect(210, 20, 93, 28))
        self.pushButton_5.setObjectName(_fromUtf8("pushButton_5"))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "商品资料", None))
        self.groupBox.setTitle(_translate("Dialog", "分类", None))
        self.treeWidget.headerItem().setText(0, _translate("Dialog", "蔬菜分类名称", None))
        self.pushButton.setText(_translate("Dialog", "添加分类", None))
        self.pushButton_3.setText(_translate("Dialog", "删除分类", None))
        self.pushButton_6.setText(_translate("Dialog", "修改分类", None))
        self.groupBox_2.setTitle(_translate("Dialog", "商品资料", None))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "编号", None))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "商品名称", None))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Dialog", "分类名称", None))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("Dialog", "计量单位", None))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("Dialog", "条形码", None))
        self.pushButton_2.setText(_translate("Dialog", "添加商品", None))
        self.pushButton_4.setText(_translate("Dialog", "修改商品", None))
        self.pushButton_5.setText(_translate("Dialog", "删除商品", None))

