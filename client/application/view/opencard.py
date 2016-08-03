# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'opencard.ui'
#
# Created: Thu Apr 30 14:43:18 2015
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
        Dialog.resize(416, 198)
        Dialog.setMinimumSize(QtCore.QSize(0, 0))
        Dialog.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.pwd = QtGui.QLineEdit(Dialog)
        self.pwd.setMinimumSize(QtCore.QSize(200, 30))
        self.pwd.setEchoMode(QtGui.QLineEdit.Password)
        self.pwd.setObjectName(_fromUtf8("pwd"))
        self.gridLayout.addWidget(self.pwd, 2, 2, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 0, 2, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 1, 4, 1, 1)
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setMinimumSize(QtCore.QSize(0, 30))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 3, 1, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 2, 0, 1, 1)
        self.pwd2 = QtGui.QLineEdit(Dialog)
        self.pwd2.setMinimumSize(QtCore.QSize(200, 30))
        self.pwd2.setEchoMode(QtGui.QLineEdit.Password)
        self.pwd2.setObjectName(_fromUtf8("pwd2"))
        self.gridLayout.addWidget(self.pwd2, 3, 2, 1, 1)
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setMinimumSize(QtCore.QSize(0, 30))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 2, 1, 1, 1)
        self.card = QtGui.QLineEdit(Dialog)
        self.card.setMinimumSize(QtCore.QSize(200, 30))
        self.card.setObjectName(_fromUtf8("card"))
        self.gridLayout.addWidget(self.card, 1, 2, 1, 1)
        self.label = QtGui.QLabel(Dialog)
        self.label.setMinimumSize(QtCore.QSize(0, 30))
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 1, 1, 1, 1)
        self.pushButton_2 = QtGui.QPushButton(Dialog)
        self.pushButton_2.setMinimumSize(QtCore.QSize(0, 30))
        self.pushButton_2.setAutoDefault(False)
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.gridLayout.addWidget(self.pushButton_2, 1, 3, 1, 1)
        self.pushButton = QtGui.QPushButton(Dialog)
        self.pushButton.setMinimumSize(QtCore.QSize(0, 30))
        self.pushButton.setAutoDefault(False)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.gridLayout.addWidget(self.pushButton, 4, 2, 1, 1)
        spacerItem3 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem3, 5, 2, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.card, self.pwd)
        Dialog.setTabOrder(self.pwd, self.pwd2)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "绑定会员卡", None))
        self.label_3.setText(_translate("Dialog", "确定密码", None))
        self.label_2.setText(_translate("Dialog", "密    码", None))
        self.label.setText(_translate("Dialog", "客户卡号", None))
        self.pushButton_2.setText(_translate("Dialog", "开新卡", None))
        self.pushButton.setText(_translate("Dialog", "绑    卡", None))

