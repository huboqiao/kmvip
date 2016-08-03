# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\T\Desktop\addgoods.ui'
#
# Created: Tue Oct 14 16:03:07 2014
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
        Dialog.resize(378, 529)
        Dialog.setMinimumSize(QtCore.QSize(378, 529))
        Dialog.setMaximumSize(QtCore.QSize(378, 529))
        self.label = QtGui.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(20, 40, 72, 15))
        self.label.setObjectName(_fromUtf8("label"))
        self.goodsname = QtGui.QLineEdit(Dialog)
        self.goodsname.setGeometry(QtCore.QRect(100, 30, 261, 30))
        self.goodsname.setObjectName(_fromUtf8("goodsname"))
        self.treeWidget = QtGui.QTreeWidget(Dialog)
        self.treeWidget.setGeometry(QtCore.QRect(100, 70, 261, 311))
        self.treeWidget.setObjectName(_fromUtf8("treeWidget"))
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(20, 400, 72, 15))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.unit = QtGui.QLineEdit(Dialog)
        self.unit.setGeometry(QtCore.QRect(100, 390, 261, 30))
        self.unit.setObjectName(_fromUtf8("unit"))
        self.pushButton = QtGui.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(270, 480, 93, 28))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.pushButton_2 = QtGui.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(170, 480, 93, 28))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(20, 440, 71, 16))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.ssn = QtGui.QLineEdit(Dialog)
        self.ssn.setGeometry(QtCore.QRect(100, 430, 261, 30))
        self.ssn.setText(_fromUtf8(""))
        self.ssn.setObjectName(_fromUtf8("ssn"))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "添加商品", None))
        self.label.setText(_translate("Dialog", "商品名称", None))
        self.treeWidget.headerItem().setText(0, _translate("Dialog", "选择商品分类名称", None))
        self.label_2.setText(_translate("Dialog", "计量单位", None))
        self.unit.setText(_translate("Dialog", "KG", None))
        self.pushButton.setText(_translate("Dialog", "关闭", None))
        self.pushButton_2.setText(_translate("Dialog", "添加商品", None))
        self.label_3.setText(_translate("Dialog", "商品条码", None))

