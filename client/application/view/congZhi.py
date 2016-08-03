# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'congZhi.ui'
#
# Created: Tue May 26 11:17:44 2015
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
        Dialog.resize(414, 449)
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_5 = QtGui.QLabel(Dialog)
        self.label_5.setMinimumSize(QtCore.QSize(0, 30))
        self.label_5.setStyleSheet(_fromUtf8("color:red\n"
""))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 2, 3, 1, 1)
        self.txt = QtGui.QPlainTextEdit(Dialog)
        self.txt.setObjectName(_fromUtf8("txt"))
        self.gridLayout.addWidget(self.txt, 7, 2, 1, 2)
        self.label_4 = QtGui.QLabel(Dialog)
        self.label_4.setMinimumSize(QtCore.QSize(0, 30))
        self.label_4.setMaximumSize(QtCore.QSize(60, 16777215))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 7, 1, 1, 1)
        self.label_13 = QtGui.QLabel(Dialog)
        self.label_13.setMinimumSize(QtCore.QSize(0, 30))
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.gridLayout.addWidget(self.label_13, 6, 1, 1, 1)
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setMinimumSize(QtCore.QSize(0, 30))
        self.label_3.setMaximumSize(QtCore.QSize(60, 16777215))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 2, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 3, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 3, 4, 1, 1)
        self.label_16 = QtGui.QLabel(Dialog)
        self.label_16.setText(_fromUtf8(""))
        self.label_16.setObjectName(_fromUtf8("label_16"))
        self.gridLayout.addWidget(self.label_16, 0, 3, 1, 1)
        self.label_9 = QtGui.QLabel(Dialog)
        self.label_9.setMinimumSize(QtCore.QSize(0, 30))
        self.label_9.setMaximumSize(QtCore.QSize(60, 16777215))
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.gridLayout.addWidget(self.label_9, 1, 1, 1, 1)
        self.label = QtGui.QLabel(Dialog)
        self.label.setMinimumSize(QtCore.QSize(0, 30))
        self.label.setMaximumSize(QtCore.QSize(60, 16777215))
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 3, 1, 1, 1)
        self.label_7 = QtGui.QLabel(Dialog)
        self.label_7.setMinimumSize(QtCore.QSize(0, 30))
        self.label_7.setText(_fromUtf8(""))
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout.addWidget(self.label_7, 4, 2, 1, 2)
        self.label_8 = QtGui.QLabel(Dialog)
        self.label_8.setMinimumSize(QtCore.QSize(0, 30))
        self.label_8.setMaximumSize(QtCore.QSize(60, 16777215))
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.gridLayout.addWidget(self.label_8, 4, 1, 1, 1)
        self.comboBox = QtGui.QComboBox(Dialog)
        self.comboBox.setMinimumSize(QtCore.QSize(0, 30))
        self.comboBox.setMaximumSize(QtCore.QSize(100, 16777215))
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.comboBox, 2, 2, 1, 1)
        self.label_10 = QtGui.QLabel(Dialog)
        self.label_10.setMinimumSize(QtCore.QSize(0, 30))
        self.label_10.setStyleSheet(_fromUtf8("color:green;\n"
""))
        self.label_10.setText(_fromUtf8(""))
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.gridLayout.addWidget(self.label_10, 1, 2, 1, 2)
        self.label_11 = QtGui.QLabel(Dialog)
        self.label_11.setMinimumSize(QtCore.QSize(0, 30))
        self.label_11.setMaximumSize(QtCore.QSize(60, 16777215))
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.gridLayout.addWidget(self.label_11, 0, 1, 1, 1)
        self.pushButton = QtGui.QPushButton(Dialog)
        self.pushButton.setMinimumSize(QtCore.QSize(0, 30))
        self.pushButton.setAutoDefault(False)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.gridLayout.addWidget(self.pushButton, 9, 3, 1, 1)
        self.lineEdit_4 = QtGui.QLineEdit(Dialog)
        self.lineEdit_4.setMinimumSize(QtCore.QSize(0, 30))
        self.lineEdit_4.setObjectName(_fromUtf8("lineEdit_4"))
        self.gridLayout.addWidget(self.lineEdit_4, 6, 2, 1, 2)
        self.money = QtGui.QLineEdit(Dialog)
        self.money.setMinimumSize(QtCore.QSize(0, 30))
        self.money.setObjectName(_fromUtf8("money"))
        self.gridLayout.addWidget(self.money, 3, 2, 1, 2)
        self.label_6 = QtGui.QLabel(Dialog)
        self.label_6.setMinimumSize(QtCore.QSize(0, 30))
        self.label_6.setStyleSheet(_fromUtf8("color:green;"))
        self.label_6.setText(_fromUtf8(""))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout.addWidget(self.label_6, 0, 2, 1, 1)

        self.retranslateUi(Dialog)
        self.comboBox.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.comboBox, self.money)
        Dialog.setTabOrder(self.money, self.lineEdit_4)
        Dialog.setTabOrder(self.lineEdit_4, self.txt)
        Dialog.setTabOrder(self.txt, self.pushButton)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "充值", None))
        self.label_5.setText(_translate("Dialog", "*请核对充值方式", None))
        self.label_4.setText(_translate("Dialog", "备    注：", None))
        self.label_13.setText(_translate("Dialog", "流 水 号：", None))
        self.label_3.setText(_translate("Dialog", "充值方式：", None))
        self.label_9.setText(_translate("Dialog", "余额大写：", None))
        self.label.setText(_translate("Dialog", "充值金额：", None))
        self.label_8.setText(_translate("Dialog", "大写金额：", None))
        self.comboBox.setItemText(0, _translate("Dialog", "现金充值", None))
        self.comboBox.setItemText(1, _translate("Dialog", "银行卡转账", None))
        self.label_11.setText(_translate("Dialog", "可用余额：", None))
        self.pushButton.setText(_translate("Dialog", "充    值", None))

