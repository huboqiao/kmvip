# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'quxianpwd.ui'
#
# Created: Thu Apr 09 17:52:35 2015
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
        Dialog.resize(416, 480)
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 3, 0, 1, 1)
        self.label = QtGui.QLabel(Dialog)
        self.label.setMinimumSize(QtCore.QSize(0, 30))
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 3, 1, 1, 1)
        self.money = QtGui.QLineEdit(Dialog)
        self.money.setMinimumSize(QtCore.QSize(0, 30))
        self.money.setObjectName(_fromUtf8("money"))
        self.gridLayout.addWidget(self.money, 3, 2, 1, 3)
        self.label_8 = QtGui.QLabel(Dialog)
        self.label_8.setMinimumSize(QtCore.QSize(0, 30))
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.gridLayout.addWidget(self.label_8, 4, 1, 1, 1)
        self.label_7 = QtGui.QLabel(Dialog)
        self.label_7.setMinimumSize(QtCore.QSize(0, 30))
        self.label_7.setText(_fromUtf8(""))
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout.addWidget(self.label_7, 4, 2, 1, 3)
        self.label_4 = QtGui.QLabel(Dialog)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 10, 1, 1, 1)
        self.txt = QtGui.QPlainTextEdit(Dialog)
        self.txt.setObjectName(_fromUtf8("txt"))
        self.gridLayout.addWidget(self.txt, 10, 2, 1, 3)
        self.pushButton = QtGui.QPushButton(Dialog)
        self.pushButton.setMinimumSize(QtCore.QSize(0, 30))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.gridLayout.addWidget(self.pushButton, 11, 3, 1, 2)
        self.lineEdit = QtGui.QLineEdit(Dialog)
        self.lineEdit.setMinimumSize(QtCore.QSize(0, 30))
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.gridLayout.addWidget(self.lineEdit, 5, 2, 1, 3)
        self.label_14 = QtGui.QLabel(Dialog)
        self.label_14.setMinimumSize(QtCore.QSize(0, 30))
        self.label_14.setObjectName(_fromUtf8("label_14"))
        self.gridLayout.addWidget(self.label_14, 6, 1, 1, 1)
        self.label_6 = QtGui.QLabel(Dialog)
        self.label_6.setMinimumSize(QtCore.QSize(0, 30))
        self.label_6.setStyleSheet(_fromUtf8("color:green;"))
        self.label_6.setText(_fromUtf8(""))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout.addWidget(self.label_6, 0, 2, 1, 1)
        self.label_11 = QtGui.QLabel(Dialog)
        self.label_11.setMinimumSize(QtCore.QSize(0, 30))
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.gridLayout.addWidget(self.label_11, 0, 1, 1, 1)
        self.label_9 = QtGui.QLabel(Dialog)
        self.label_9.setMinimumSize(QtCore.QSize(0, 30))
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.gridLayout.addWidget(self.label_9, 1, 1, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 2, 5, 1, 1)
        self.label_5 = QtGui.QLabel(Dialog)
        self.label_5.setMinimumSize(QtCore.QSize(0, 30))
        self.label_5.setStyleSheet(_fromUtf8("color:red\n"
""))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 2, 3, 1, 2)
        self.comboBox = QtGui.QComboBox(Dialog)
        self.comboBox.setMinimumSize(QtCore.QSize(0, 30))
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.comboBox, 2, 2, 1, 1)
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setMinimumSize(QtCore.QSize(0, 30))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 2, 1, 1, 1)
        self.label_10 = QtGui.QLabel(Dialog)
        self.label_10.setMinimumSize(QtCore.QSize(0, 30))
        self.label_10.setStyleSheet(_fromUtf8("color:green;\n"
""))
        self.label_10.setText(_fromUtf8(""))
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.gridLayout.addWidget(self.label_10, 1, 2, 1, 3)
        self.label_15 = QtGui.QLabel(Dialog)
        self.label_15.setMinimumSize(QtCore.QSize(0, 30))
        self.label_15.setObjectName(_fromUtf8("label_15"))
        self.gridLayout.addWidget(self.label_15, 8, 1, 1, 1)
        self.lineEdit_3 = QtGui.QLineEdit(Dialog)
        self.lineEdit_3.setMinimumSize(QtCore.QSize(0, 30))
        self.lineEdit_3.setObjectName(_fromUtf8("lineEdit_3"))
        self.gridLayout.addWidget(self.lineEdit_3, 8, 2, 1, 3)
        self.lineEdit_2 = QtGui.QLineEdit(Dialog)
        self.lineEdit_2.setMinimumSize(QtCore.QSize(0, 30))
        self.lineEdit_2.setObjectName(_fromUtf8("lineEdit_2"))
        self.gridLayout.addWidget(self.lineEdit_2, 6, 2, 1, 3)
        self.label_13 = QtGui.QLabel(Dialog)
        self.label_13.setMinimumSize(QtCore.QSize(0, 30))
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.gridLayout.addWidget(self.label_13, 5, 1, 1, 1)
        self.qxBankNoidLabel = QtGui.QLabel(Dialog)
        self.qxBankNoidLabel.setMinimumSize(QtCore.QSize(0, 30))
        self.qxBankNoidLabel.setObjectName(_fromUtf8("qxBankNoidLabel"))
        self.gridLayout.addWidget(self.qxBankNoidLabel, 9, 1, 1, 1)
        self.qxBankNoidInput = QtGui.QLineEdit(Dialog)
        self.qxBankNoidInput.setMinimumSize(QtCore.QSize(0, 30))
        self.qxBankNoidInput.setObjectName(_fromUtf8("qxBankNoidInput"))
        self.gridLayout.addWidget(self.qxBankNoidInput, 9, 2, 1, 3)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.comboBox, self.money)
        Dialog.setTabOrder(self.money, self.txt)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "提现", None))
        self.label.setText(_translate("Dialog", "提取金额：", None))
        self.label_8.setText(_translate("Dialog", "金额大写：", None))
        self.label_4.setText(_translate("Dialog", "备    注：", None))
        self.pushButton.setText(_translate("Dialog", "提    交", None))
        self.label_14.setText(_translate("Dialog", "开 户 名：", None))
        self.label_11.setText(_translate("Dialog", "卡中余额：", None))
        self.label_9.setText(_translate("Dialog", "余额大写：", None))
        self.label_5.setText(_translate("Dialog", "*请核对提现方式", None))
        self.comboBox.setItemText(0, _translate("Dialog", "现金提现", None))
        self.comboBox.setItemText(1, _translate("Dialog", "银行卡转账", None))
        self.label_3.setText(_translate("Dialog", "提现方式：", None))
        self.label_15.setText(_translate("Dialog", "银行账号：", None))
        self.label_13.setText(_translate("Dialog", "开 户 行：", None))
        self.qxBankNoidLabel.setText(_translate("Dialog", "流 水 号：", None))

