# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\www\kmvip\src\ui\goodclass.ui'
#
# Created: Wed Jun 18 03:56:19 2014
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
        Dialog.resize(374, 473)
        Dialog.setMinimumSize(QtCore.QSize(374, 473))
        Dialog.setMaximumSize(QtCore.QSize(374, 473))
        self.treeWidget = QtGui.QTreeWidget(Dialog)
        self.treeWidget.setGeometry(QtCore.QRect(96, 70, 261, 331))
        self.treeWidget.setObjectName(_fromUtf8("treeWidget"))
        self.label = QtGui.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(19, 30, 72, 15))
        self.label.setObjectName(_fromUtf8("label"))
        self.classname = QtGui.QLineEdit(Dialog)
        self.classname.setGeometry(QtCore.QRect(96, 21, 261, 31))
        self.classname.setObjectName(_fromUtf8("classname"))
        self.pushButton = QtGui.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(266, 420, 93, 28))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.pushButton_2 = QtGui.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(166, 420, 93, 28))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "添加分类", None))
        self.treeWidget.headerItem().setText(0, _translate("Dialog", "选择父类名称", None))
        self.label.setText(_translate("Dialog", "类别名称：", None))
        self.pushButton.setText(_translate("Dialog", "关闭", None))
        self.pushButton_2.setText(_translate("Dialog", "添加分类", None))

