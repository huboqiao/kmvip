# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'memberquery.ui'
#
# Created: Mon Mar 02 10:40:44 2015
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
        Dialog.resize(1149, 543)
        Dialog.setMinimumSize(QtCore.QSize(0, 0))
        Dialog.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.gridLayout_2 = QtGui.QGridLayout(Dialog)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.groupBox = QtGui.QGroupBox(Dialog)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.groupBox)
        self.horizontalLayout.setSpacing(3)
        self.horizontalLayout.setMargin(3)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setMinimumSize(QtCore.QSize(0, 30))
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.s_membername = QtGui.QLineEdit(self.groupBox)
        self.s_membername.setMinimumSize(QtCore.QSize(60, 30))
        self.s_membername.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.s_membername.setText(_fromUtf8(""))
        self.s_membername.setObjectName(_fromUtf8("s_membername"))
        self.horizontalLayout.addWidget(self.s_membername)
        self.label_4 = QtGui.QLabel(self.groupBox)
        self.label_4.setMinimumSize(QtCore.QSize(0, 30))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.horizontalLayout.addWidget(self.label_4)
        self.s_tel = QtGui.QLineEdit(self.groupBox)
        self.s_tel.setMinimumSize(QtCore.QSize(80, 30))
        self.s_tel.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.s_tel.setText(_fromUtf8(""))
        self.s_tel.setObjectName(_fromUtf8("s_tel"))
        self.horizontalLayout.addWidget(self.s_tel)
        self.label_3 = QtGui.QLabel(self.groupBox)
        self.label_3.setMinimumSize(QtCore.QSize(0, 30))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout.addWidget(self.label_3)
        self.s_idcard = QtGui.QLineEdit(self.groupBox)
        self.s_idcard.setMinimumSize(QtCore.QSize(120, 30))
        self.s_idcard.setText(_fromUtf8(""))
        self.s_idcard.setObjectName(_fromUtf8("s_idcard"))
        self.horizontalLayout.addWidget(self.s_idcard)
        self.pushButton = QtGui.QPushButton(self.groupBox)
        self.pushButton.setMinimumSize(QtCore.QSize(60, 30))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.horizontalLayout.addWidget(self.pushButton)
        self.pushButton_5 = QtGui.QPushButton(self.groupBox)
        self.pushButton_5.setMinimumSize(QtCore.QSize(0, 30))
        self.pushButton_5.setObjectName(_fromUtf8("pushButton_5"))
        self.horizontalLayout.addWidget(self.pushButton_5)
        self.gridLayout_2.addWidget(self.groupBox, 0, 0, 1, 3)
        self.groupBox_2 = QtGui.QGroupBox(Dialog)
        self.groupBox_2.setMinimumSize(QtCore.QSize(550, 0))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.gridLayout = QtGui.QGridLayout(self.groupBox_2)
        self.gridLayout.setSpacing(3)
        self.gridLayout.setContentsMargins(6, 3, 3, 3)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_11 = QtGui.QLabel(self.groupBox_2)
        self.label_11.setMinimumSize(QtCore.QSize(0, 0))
        self.label_11.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.gridLayout.addWidget(self.label_11, 2, 0, 1, 1)
        self.membername = QtGui.QLineEdit(self.groupBox_2)
        self.membername.setEnabled(True)
        self.membername.setMinimumSize(QtCore.QSize(80, 20))
        self.membername.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.membername.setText(_fromUtf8(""))
        self.membername.setReadOnly(True)
        self.membername.setObjectName(_fromUtf8("membername"))
        self.gridLayout.addWidget(self.membername, 0, 1, 1, 1)
        self.label_10 = QtGui.QLabel(self.groupBox_2)
        self.label_10.setMinimumSize(QtCore.QSize(0, 0))
        self.label_10.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.gridLayout.addWidget(self.label_10, 0, 0, 1, 1)
        self.groupBox_4 = QtGui.QGroupBox(self.groupBox_2)
        self.groupBox_4.setObjectName(_fromUtf8("groupBox_4"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.groupBox_4)
        self.horizontalLayout_3.setSpacing(3)
        self.horizontalLayout_3.setMargin(3)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.zhaopianimage = QtGui.QWidget(self.groupBox_4)
        self.zhaopianimage.setMinimumSize(QtCore.QSize(150, 150))
        self.zhaopianimage.setObjectName(_fromUtf8("zhaopianimage"))
        self.horizontalLayout_3.addWidget(self.zhaopianimage)
        self.gridLayout.addWidget(self.groupBox_4, 0, 2, 6, 2)
        self.sex = QtGui.QComboBox(self.groupBox_2)
        self.sex.setEnabled(False)
        self.sex.setMinimumSize(QtCore.QSize(0, 20))
        self.sex.setMaximumSize(QtCore.QSize(80, 16777215))
        self.sex.setObjectName(_fromUtf8("sex"))
        self.sex.addItem(_fromUtf8(""))
        self.sex.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.sex, 2, 1, 1, 1)
        self.label_12 = QtGui.QLabel(self.groupBox_2)
        self.label_12.setMinimumSize(QtCore.QSize(0, 0))
        self.label_12.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.gridLayout.addWidget(self.label_12, 3, 0, 1, 1)
        self.nation = QtGui.QLineEdit(self.groupBox_2)
        self.nation.setEnabled(True)
        self.nation.setMinimumSize(QtCore.QSize(0, 20))
        self.nation.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.nation.setText(_fromUtf8(""))
        self.nation.setReadOnly(True)
        self.nation.setObjectName(_fromUtf8("nation"))
        self.gridLayout.addWidget(self.nation, 3, 1, 1, 1)
        self.label_13 = QtGui.QLabel(self.groupBox_2)
        self.label_13.setMinimumSize(QtCore.QSize(0, 0))
        self.label_13.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.gridLayout.addWidget(self.label_13, 4, 0, 1, 1)
        self.tel = QtGui.QLineEdit(self.groupBox_2)
        self.tel.setEnabled(True)
        self.tel.setMinimumSize(QtCore.QSize(0, 20))
        self.tel.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.tel.setText(_fromUtf8(""))
        self.tel.setReadOnly(True)
        self.tel.setObjectName(_fromUtf8("tel"))
        self.gridLayout.addWidget(self.tel, 4, 1, 1, 1)
        self.label_6 = QtGui.QLabel(self.groupBox_2)
        self.label_6.setMinimumSize(QtCore.QSize(0, 0))
        self.label_6.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout.addWidget(self.label_6, 5, 0, 1, 1)
        self.amount = QtGui.QLineEdit(self.groupBox_2)
        self.amount.setEnabled(True)
        self.amount.setMinimumSize(QtCore.QSize(0, 20))
        self.amount.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.amount.setAutoFillBackground(False)
        self.amount.setStyleSheet(_fromUtf8(""))
        self.amount.setText(_fromUtf8(""))
        self.amount.setReadOnly(True)
        self.amount.setObjectName(_fromUtf8("amount"))
        self.gridLayout.addWidget(self.amount, 5, 1, 1, 1)
        self.label_7 = QtGui.QLabel(self.groupBox_2)
        self.label_7.setMinimumSize(QtCore.QSize(0, 0))
        self.label_7.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout.addWidget(self.label_7, 6, 0, 1, 1)
        self.stat = QtGui.QLineEdit(self.groupBox_2)
        self.stat.setEnabled(True)
        self.stat.setMinimumSize(QtCore.QSize(0, 20))
        self.stat.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.stat.setAutoFillBackground(False)
        self.stat.setStyleSheet(_fromUtf8(""))
        self.stat.setText(_fromUtf8(""))
        self.stat.setReadOnly(True)
        self.stat.setObjectName(_fromUtf8("stat"))
        self.gridLayout.addWidget(self.stat, 6, 1, 1, 1)
        self.label_14 = QtGui.QLabel(self.groupBox_2)
        self.label_14.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label_14.setObjectName(_fromUtf8("label_14"))
        self.gridLayout.addWidget(self.label_14, 6, 2, 1, 1)
        self.adder = QtGui.QLineEdit(self.groupBox_2)
        self.adder.setEnabled(True)
        self.adder.setMinimumSize(QtCore.QSize(0, 20))
        self.adder.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.adder.setText(_fromUtf8(""))
        self.adder.setReadOnly(True)
        self.adder.setObjectName(_fromUtf8("adder"))
        self.gridLayout.addWidget(self.adder, 6, 3, 1, 1)
        self.label_5 = QtGui.QLabel(self.groupBox_2)
        self.label_5.setMinimumSize(QtCore.QSize(0, 0))
        self.label_5.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 7, 0, 1, 1)
        self.idcard = QtGui.QLineEdit(self.groupBox_2)
        self.idcard.setEnabled(True)
        self.idcard.setMinimumSize(QtCore.QSize(120, 20))
        self.idcard.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.idcard.setAutoFillBackground(False)
        self.idcard.setStyleSheet(_fromUtf8(""))
        self.idcard.setReadOnly(True)
        self.idcard.setObjectName(_fromUtf8("idcard"))
        self.gridLayout.addWidget(self.idcard, 7, 1, 1, 1)
        self.label_21 = QtGui.QLabel(self.groupBox_2)
        self.label_21.setMinimumSize(QtCore.QSize(0, 0))
        self.label_21.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label_21.setObjectName(_fromUtf8("label_21"))
        self.gridLayout.addWidget(self.label_21, 7, 2, 1, 1)
        self.carddate = QtGui.QLineEdit(self.groupBox_2)
        self.carddate.setEnabled(True)
        self.carddate.setMinimumSize(QtCore.QSize(0, 20))
        self.carddate.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.carddate.setAutoFillBackground(False)
        self.carddate.setStyleSheet(_fromUtf8(""))
        self.carddate.setText(_fromUtf8(""))
        self.carddate.setReadOnly(True)
        self.carddate.setObjectName(_fromUtf8("carddate"))
        self.gridLayout.addWidget(self.carddate, 7, 3, 1, 1)
        self.label_19 = QtGui.QLabel(self.groupBox_2)
        self.label_19.setMinimumSize(QtCore.QSize(0, 0))
        self.label_19.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label_19.setObjectName(_fromUtf8("label_19"))
        self.gridLayout.addWidget(self.label_19, 8, 0, 1, 1)
        self.ugroup = QtGui.QLineEdit(self.groupBox_2)
        self.ugroup.setEnabled(True)
        self.ugroup.setMinimumSize(QtCore.QSize(0, 20))
        self.ugroup.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.ugroup.setAutoFillBackground(False)
        self.ugroup.setStyleSheet(_fromUtf8(""))
        self.ugroup.setText(_fromUtf8(""))
        self.ugroup.setReadOnly(True)
        self.ugroup.setObjectName(_fromUtf8("ugroup"))
        self.gridLayout.addWidget(self.ugroup, 8, 1, 1, 1)
        self.label_20 = QtGui.QLabel(self.groupBox_2)
        self.label_20.setMinimumSize(QtCore.QSize(0, 0))
        self.label_20.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label_20.setObjectName(_fromUtf8("label_20"))
        self.gridLayout.addWidget(self.label_20, 8, 2, 1, 1)
        self.store = QtGui.QLineEdit(self.groupBox_2)
        self.store.setEnabled(True)
        self.store.setMinimumSize(QtCore.QSize(0, 20))
        self.store.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.store.setAutoFillBackground(False)
        self.store.setStyleSheet(_fromUtf8(""))
        self.store.setText(_fromUtf8(""))
        self.store.setReadOnly(True)
        self.store.setObjectName(_fromUtf8("store"))
        self.gridLayout.addWidget(self.store, 8, 3, 1, 1)
        self.label_8 = QtGui.QLabel(self.groupBox_2)
        self.label_8.setMinimumSize(QtCore.QSize(0, 0))
        self.label_8.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.gridLayout.addWidget(self.label_8, 9, 0, 1, 1)
        self.adduser = QtGui.QLineEdit(self.groupBox_2)
        self.adduser.setEnabled(True)
        self.adduser.setMinimumSize(QtCore.QSize(0, 20))
        self.adduser.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.adduser.setAutoFillBackground(False)
        self.adduser.setStyleSheet(_fromUtf8(""))
        self.adduser.setText(_fromUtf8(""))
        self.adduser.setReadOnly(True)
        self.adduser.setObjectName(_fromUtf8("adduser"))
        self.gridLayout.addWidget(self.adduser, 9, 1, 1, 1)
        self.label_9 = QtGui.QLabel(self.groupBox_2)
        self.label_9.setMinimumSize(QtCore.QSize(0, 0))
        self.label_9.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.gridLayout.addWidget(self.label_9, 9, 2, 1, 1)
        self.cdate = QtGui.QLineEdit(self.groupBox_2)
        self.cdate.setEnabled(True)
        self.cdate.setMinimumSize(QtCore.QSize(120, 20))
        self.cdate.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.cdate.setAutoFillBackground(False)
        self.cdate.setStyleSheet(_fromUtf8(""))
        self.cdate.setReadOnly(True)
        self.cdate.setObjectName(_fromUtf8("cdate"))
        self.gridLayout.addWidget(self.cdate, 9, 3, 1, 1)
        self.label_15 = QtGui.QLabel(self.groupBox_2)
        self.label_15.setMinimumSize(QtCore.QSize(0, 0))
        self.label_15.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label_15.setObjectName(_fromUtf8("label_15"))
        self.gridLayout.addWidget(self.label_15, 10, 0, 1, 1)
        self.bankname = QtGui.QLineEdit(self.groupBox_2)
        self.bankname.setEnabled(True)
        self.bankname.setMinimumSize(QtCore.QSize(0, 20))
        self.bankname.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.bankname.setAutoFillBackground(False)
        self.bankname.setStyleSheet(_fromUtf8(""))
        self.bankname.setText(_fromUtf8(""))
        self.bankname.setReadOnly(True)
        self.bankname.setObjectName(_fromUtf8("bankname"))
        self.gridLayout.addWidget(self.bankname, 10, 1, 1, 1)
        self.label_18 = QtGui.QLabel(self.groupBox_2)
        self.label_18.setMinimumSize(QtCore.QSize(0, 0))
        self.label_18.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label_18.setObjectName(_fromUtf8("label_18"))
        self.gridLayout.addWidget(self.label_18, 10, 2, 1, 1)
        self.bankusername = QtGui.QLineEdit(self.groupBox_2)
        self.bankusername.setEnabled(True)
        self.bankusername.setMinimumSize(QtCore.QSize(0, 20))
        self.bankusername.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.bankusername.setAutoFillBackground(False)
        self.bankusername.setStyleSheet(_fromUtf8(""))
        self.bankusername.setText(_fromUtf8(""))
        self.bankusername.setReadOnly(True)
        self.bankusername.setObjectName(_fromUtf8("bankusername"))
        self.gridLayout.addWidget(self.bankusername, 10, 3, 1, 1)
        self.label_16 = QtGui.QLabel(self.groupBox_2)
        self.label_16.setMinimumSize(QtCore.QSize(0, 0))
        self.label_16.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label_16.setObjectName(_fromUtf8("label_16"))
        self.gridLayout.addWidget(self.label_16, 11, 0, 1, 1)
        self.bankcard = QtGui.QLineEdit(self.groupBox_2)
        self.bankcard.setEnabled(True)
        self.bankcard.setMinimumSize(QtCore.QSize(150, 20))
        self.bankcard.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.bankcard.setAutoFillBackground(False)
        self.bankcard.setStyleSheet(_fromUtf8(""))
        self.bankcard.setReadOnly(True)
        self.bankcard.setObjectName(_fromUtf8("bankcard"))
        self.gridLayout.addWidget(self.bankcard, 11, 1, 1, 1)
        self.label_17 = QtGui.QLabel(self.groupBox_2)
        self.label_17.setMinimumSize(QtCore.QSize(0, 0))
        self.label_17.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label_17.setObjectName(_fromUtf8("label_17"))
        self.gridLayout.addWidget(self.label_17, 11, 2, 1, 1)
        self.bankadder = QtGui.QLineEdit(self.groupBox_2)
        self.bankadder.setEnabled(True)
        self.bankadder.setMinimumSize(QtCore.QSize(0, 20))
        self.bankadder.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.bankadder.setAutoFillBackground(False)
        self.bankadder.setStyleSheet(_fromUtf8(""))
        self.bankadder.setText(_fromUtf8(""))
        self.bankadder.setReadOnly(True)
        self.bankadder.setObjectName(_fromUtf8("bankadder"))
        self.gridLayout.addWidget(self.bankadder, 11, 3, 1, 1)
        self.tabWidget = QtGui.QTabWidget(self.groupBox_2)
        self.tabWidget.setMinimumSize(QtCore.QSize(268, 194))
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.tab)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.shenfenzhengimage = QtGui.QWidget(self.tab)
        self.shenfenzhengimage.setMinimumSize(QtCore.QSize(238, 150))
        self.shenfenzhengimage.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.shenfenzhengimage.setObjectName(_fromUtf8("shenfenzhengimage"))
        self.horizontalLayout_2.addWidget(self.shenfenzhengimage)
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout(self.tab_2)
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.shenfenzhengimage_t = QtGui.QWidget(self.tab_2)
        self.shenfenzhengimage_t.setObjectName(_fromUtf8("shenfenzhengimage_t"))
        self.horizontalLayout_4.addWidget(self.shenfenzhengimage_t)
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))
        self.gridLayout.addWidget(self.tabWidget, 12, 0, 1, 4)
        self.getcard = QtGui.QPushButton(self.groupBox_2)
        self.getcard.setEnabled(False)
        self.getcard.setMinimumSize(QtCore.QSize(0, 20))
        self.getcard.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.getcard.setObjectName(_fromUtf8("getcard"))
        self.gridLayout.addWidget(self.getcard, 1, 0, 1, 1)
        self.pushButton_6 = QtGui.QPushButton(self.groupBox_2)
        self.pushButton_6.setEnabled(False)
        self.pushButton_6.setObjectName(_fromUtf8("pushButton_6"))
        self.gridLayout.addWidget(self.pushButton_6, 1, 1, 1, 1)
        self.gridLayout_2.addWidget(self.groupBox_2, 0, 3, 3, 1)
        self.tableWidget = QtGui.QTableWidget(Dialog)
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
        self.gridLayout_2.addWidget(self.tableWidget, 1, 0, 1, 3)
        self.pushButton_3 = QtGui.QPushButton(Dialog)
        self.pushButton_3.setMinimumSize(QtCore.QSize(60, 30))
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.gridLayout_2.addWidget(self.pushButton_3, 2, 0, 1, 1)
        self.pushButton_4 = QtGui.QPushButton(Dialog)
        self.pushButton_4.setMinimumSize(QtCore.QSize(60, 30))
        self.pushButton_4.setObjectName(_fromUtf8("pushButton_4"))
        self.gridLayout_2.addWidget(self.pushButton_4, 2, 1, 1, 1)
        self.pushButton_2 = QtGui.QPushButton(Dialog)
        self.pushButton_2.setMinimumSize(QtCore.QSize(0, 30))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.gridLayout_2.addWidget(self.pushButton_2, 2, 2, 1, 1)

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "客户查询", None))
        self.groupBox.setTitle(_translate("Dialog", "查询", None))
        self.label.setText(_translate("Dialog", "客户名：", None))
        self.label_4.setText(_translate("Dialog", "手机号：", None))
        self.label_3.setText(_translate("Dialog", " 身份证：", None))
        self.pushButton.setText(_translate("Dialog", "查询", None))
        self.pushButton_5.setText(_translate("Dialog", "高级查询", None))
        self.groupBox_2.setTitle(_translate("Dialog", "客户详情", None))
        self.label_11.setText(_translate("Dialog", "性    别：", None))
        self.label_10.setText(_translate("Dialog", "客户名称：", None))
        self.groupBox_4.setTitle(_translate("Dialog", "照片", None))
        self.sex.setItemText(0, _translate("Dialog", "女", None))
        self.sex.setItemText(1, _translate("Dialog", "男", None))
        self.label_12.setText(_translate("Dialog", "民    族：", None))
        self.label_13.setText(_translate("Dialog", "联系电话：", None))
        self.label_6.setText(_translate("Dialog", "余    额：", None))
        self.label_7.setText(_translate("Dialog", "状    态：", None))
        self.label_14.setText(_translate("Dialog", "联系地址：", None))
        self.label_5.setText(_translate("Dialog", "身 份 证：", None))
        self.idcard.setText(_translate("Dialog", "123456200101011234", None))
        self.label_21.setText(_translate("Dialog", "身份证有效期：", None))
        self.label_19.setText(_translate("Dialog", "客户类型：", None))
        self.label_20.setText(_translate("Dialog", "仓    位：", None))
        self.label_8.setText(_translate("Dialog", "开卡员工：", None))
        self.label_9.setText(_translate("Dialog", "开户日期：", None))
        self.cdate.setText(_translate("Dialog", "2000-10-20 05:20:30", None))
        self.label_15.setText(_translate("Dialog", "开 户 行：", None))
        self.label_18.setText(_translate("Dialog", "开 户 人：", None))
        self.label_16.setText(_translate("Dialog", "银行卡号：", None))
        self.bankcard.setText(_translate("Dialog", "1234 5678 9012 3456 789", None))
        self.label_17.setText(_translate("Dialog", "开 户 点：", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Dialog", "身份证正面", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Dialog", "身份证反面", None))
        self.getcard.setText(_translate("Dialog", "获取卡号", None))
        self.pushButton_6.setText(_translate("Dialog", "资金明细", None))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "id", None))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "客户姓名", None))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Dialog", "金荣卡号", None))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("Dialog", "余额", None))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("Dialog", "状态", None))
        self.pushButton_3.setText(_translate("Dialog", "打印", None))
        self.pushButton_4.setText(_translate("Dialog", "预览", None))
        self.pushButton_2.setText(_translate("Dialog", "导出客户列表", None))
