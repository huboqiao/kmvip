# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'addPayType.ui'
#
# Created: Fri Apr 10 15:19:28 2015
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
        Dialog.resize(400, 217)
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 2, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 1, 3, 1, 1)
        self.label = QtGui.QLabel(Dialog)
        self.label.setMinimumSize(QtCore.QSize(0, 30))
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 1, 1, 1, 1)
        self.pushButton = QtGui.QPushButton(Dialog)
        self.pushButton.setMinimumSize(QtCore.QSize(0, 30))
        self.pushButton.setAutoDefault(False)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.gridLayout.addWidget(self.pushButton, 3, 2, 1, 1)
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setMinimumSize(QtCore.QSize(0, 30))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 2, 1, 1, 1)
        self.lineEdit = QtGui.QLineEdit(Dialog)
        self.lineEdit.setMinimumSize(QtCore.QSize(0, 30))
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.gridLayout.addWidget(self.lineEdit, 1, 2, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 0, 1, 1, 1)
        self.comboBox = QtGui.QComboBox(Dialog)
        self.comboBox.setMinimumSize(QtCore.QSize(0, 30))
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.comboBox, 2, 2, 1, 1)
        spacerItem3 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem3, 4, 2, 1, 1)

        self.retranslateUi(Dialog)
        self.comboBox.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "添加缴费项目", None))
        self.label.setText(_translate("Dialog", "项目名称：", None))
        self.pushButton.setText(_translate("Dialog", "提    交", None))
        self.label_2.setText(_translate("Dialog", "启用状态：", None))
        self.comboBox.setItemText(0, _translate("Dialog", "未启用", None))
        self.comboBox.setItemText(1, _translate("Dialog", "启用", None))
