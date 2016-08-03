# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'suppliers.ui'
#
# Created: Wed Mar 11 14:25:48 2015
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

class Ui_suppliersList(object):
    def setupUi(self, suppliersList):
        suppliersList.setObjectName(_fromUtf8("suppliersList"))
        suppliersList.resize(759, 660)
        self.verticalLayout = QtGui.QVBoxLayout(suppliersList)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.frame = QtGui.QFrame(suppliersList)
        self.frame.setMinimumSize(QtCore.QSize(150, 50))
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(self.frame)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.lineEdit = QtGui.QLineEdit(self.frame)
        self.lineEdit.setMinimumSize(QtCore.QSize(80, 0))
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.horizontalLayout.addWidget(self.lineEdit)
        self.label_2 = QtGui.QLabel(self.frame)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout.addWidget(self.label_2)
        self.lineEdit_2 = QtGui.QLineEdit(self.frame)
        self.lineEdit_2.setMinimumSize(QtCore.QSize(80, 0))
        self.lineEdit_2.setObjectName(_fromUtf8("lineEdit_2"))
        self.horizontalLayout.addWidget(self.lineEdit_2)
        self.label_3 = QtGui.QLabel(self.frame)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout.addWidget(self.label_3)
        self.lineEdit_3 = QtGui.QLineEdit(self.frame)
        self.lineEdit_3.setMinimumSize(QtCore.QSize(80, 0))
        self.lineEdit_3.setObjectName(_fromUtf8("lineEdit_3"))
        self.horizontalLayout.addWidget(self.lineEdit_3)
        self.label_4 = QtGui.QLabel(self.frame)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.horizontalLayout.addWidget(self.label_4)
        self.lineEdit_4 = QtGui.QLineEdit(self.frame)
        self.lineEdit_4.setMinimumSize(QtCore.QSize(80, 0))
        self.lineEdit_4.setObjectName(_fromUtf8("lineEdit_4"))
        self.horizontalLayout.addWidget(self.lineEdit_4)
        self.pushButton = QtGui.QPushButton(self.frame)
        self.pushButton.setMinimumSize(QtCore.QSize(60, 0))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.horizontalLayout.addWidget(self.pushButton)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addWidget(self.frame)
        self.suppliersTable = QtGui.QTableWidget(suppliersList)
        self.suppliersTable.setAutoFillBackground(True)
        self.suppliersTable.setShowGrid(True)
        self.suppliersTable.setRowCount(0)
        self.suppliersTable.setColumnCount(6)
        self.suppliersTable.setObjectName(_fromUtf8("suppliersTable"))
        item = QtGui.QTableWidgetItem()
        self.suppliersTable.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.suppliersTable.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.suppliersTable.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.suppliersTable.setHorizontalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        self.suppliersTable.setHorizontalHeaderItem(4, item)
        item = QtGui.QTableWidgetItem()
        self.suppliersTable.setHorizontalHeaderItem(5, item)
        self.suppliersTable.horizontalHeader().setHighlightSections(True)
        self.verticalLayout.addWidget(self.suppliersTable)

        self.retranslateUi(suppliersList)
        QtCore.QMetaObject.connectSlotsByName(suppliersList)

    def retranslateUi(self, suppliersList):
        suppliersList.setWindowTitle(_translate("suppliersList", "供应商列表", None))
        self.label.setText(_translate("suppliersList", "商户编号", None))
        self.label_2.setText(_translate("suppliersList", "商户名", None))
        self.label_3.setText(_translate("suppliersList", "冷库名称", None))
        self.label_4.setText(_translate("suppliersList", "冷库区域", None))
        self.pushButton.setText(_translate("suppliersList", "查询", None))
        item = self.suppliersTable.horizontalHeaderItem(0)
        item.setText(_translate("suppliersList", "编号(ID)", None))
        item = self.suppliersTable.horizontalHeaderItem(1)
        item.setText(_translate("suppliersList", "商户名", None))
        item = self.suppliersTable.horizontalHeaderItem(2)
        item.setText(_translate("suppliersList", "冷库名称", None))
        item = self.suppliersTable.horizontalHeaderItem(3)
        item.setText(_translate("suppliersList", "冷库区域", None))
        item = self.suppliersTable.horizontalHeaderItem(4)
        item.setText(_translate("suppliersList", "冷库号数", None))
        item = self.suppliersTable.horizontalHeaderItem(5)
        item.setText(_translate("suppliersList", "商户状态", None))

