# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'zhuanzhang.ui'
#
# Created: Fri May 08 13:54:30 2015
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
        Dialog.resize(1082, 631)
        self.line = QtGui.QFrame(Dialog)
        self.line.setGeometry(QtCore.QRect(0, 320, 1071, 16))
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.label = QtGui.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(20, 28, 81, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.inputzccardid = QtGui.QLineEdit(Dialog)
        self.inputzccardid.setGeometry(QtCore.QRect(103, 19, 221, 31))
        self.inputzccardid.setText(_fromUtf8(""))
        self.inputzccardid.setObjectName(_fromUtf8("inputzccardid"))
        self.label_4 = QtGui.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(349, 25, 81, 16))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.inputzrcardid = QtGui.QLineEdit(Dialog)
        self.inputzrcardid.setGeometry(QtCore.QRect(432, 17, 221, 31))
        self.inputzrcardid.setText(_fromUtf8(""))
        self.inputzrcardid.setObjectName(_fromUtf8("inputzrcardid"))
        self.line_2 = QtGui.QFrame(Dialog)
        self.line_2.setGeometry(QtCore.QRect(0, 50, 1071, 16))
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.money = QtGui.QLineEdit(Dialog)
        self.money.setGeometry(QtCore.QRect(740, 17, 131, 31))
        self.money.setText(_fromUtf8(""))
        self.money.setObjectName(_fromUtf8("money"))
        self.label_10 = QtGui.QLabel(Dialog)
        self.label_10.setGeometry(QtCore.QRect(670, 25, 61, 16))
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.commandLinkButton_2 = QtGui.QCommandLinkButton(Dialog)
        self.commandLinkButton_2.setEnabled(True)
        self.commandLinkButton_2.setGeometry(QtCore.QRect(910, 10, 121, 41))
        self.commandLinkButton_2.setObjectName(_fromUtf8("commandLinkButton_2"))
        self.frame_2 = QtGui.QFrame(Dialog)
        self.frame_2.setGeometry(QtCore.QRect(0, 340, 1071, 281))
        self.frame_2.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_2.setObjectName(_fromUtf8("frame_2"))
        self.groupBox_2 = QtGui.QGroupBox(self.frame_2)
        self.groupBox_2.setGeometry(QtCore.QRect(600, 50, 461, 191))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.gridLayout_2 = QtGui.QGridLayout(self.groupBox_2)
        self.gridLayout_2.setMargin(3)
        self.gridLayout_2.setSpacing(3)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.label_21 = QtGui.QLabel(self.groupBox_2)
        self.label_21.setMinimumSize(QtCore.QSize(0, 30))
        self.label_21.setObjectName(_fromUtf8("label_21"))
        self.gridLayout_2.addWidget(self.label_21, 0, 2, 1, 1)
        self.membername_2 = QtGui.QLineEdit(self.groupBox_2)
        self.membername_2.setEnabled(True)
        self.membername_2.setMinimumSize(QtCore.QSize(0, 30))
        self.membername_2.setReadOnly(True)
        self.membername_2.setObjectName(_fromUtf8("membername_2"))
        self.gridLayout_2.addWidget(self.membername_2, 0, 1, 1, 1)
        self.adder_2 = QtGui.QLineEdit(self.groupBox_2)
        self.adder_2.setEnabled(True)
        self.adder_2.setMinimumSize(QtCore.QSize(0, 30))
        self.adder_2.setReadOnly(True)
        self.adder_2.setObjectName(_fromUtf8("adder_2"))
        self.gridLayout_2.addWidget(self.adder_2, 3, 3, 1, 1)
        self.amount_2 = QtGui.QLineEdit(self.groupBox_2)
        self.amount_2.setEnabled(True)
        self.amount_2.setMinimumSize(QtCore.QSize(0, 30))
        self.amount_2.setReadOnly(True)
        self.amount_2.setObjectName(_fromUtf8("amount_2"))
        self.gridLayout_2.addWidget(self.amount_2, 3, 1, 1, 1)
        self.label_15 = QtGui.QLabel(self.groupBox_2)
        self.label_15.setMinimumSize(QtCore.QSize(0, 30))
        self.label_15.setObjectName(_fromUtf8("label_15"))
        self.gridLayout_2.addWidget(self.label_15, 1, 0, 1, 1)
        self.label_20 = QtGui.QLabel(self.groupBox_2)
        self.label_20.setMinimumSize(QtCore.QSize(0, 30))
        self.label_20.setObjectName(_fromUtf8("label_20"))
        self.gridLayout_2.addWidget(self.label_20, 3, 0, 1, 1)
        self.nation_2 = QtGui.QLineEdit(self.groupBox_2)
        self.nation_2.setEnabled(True)
        self.nation_2.setMinimumSize(QtCore.QSize(0, 30))
        self.nation_2.setReadOnly(True)
        self.nation_2.setObjectName(_fromUtf8("nation_2"))
        self.gridLayout_2.addWidget(self.nation_2, 2, 1, 1, 1)
        self.sex_2 = QtGui.QComboBox(self.groupBox_2)
        self.sex_2.setEnabled(True)
        self.sex_2.setMinimumSize(QtCore.QSize(0, 30))
        self.sex_2.setEditable(True)
        self.sex_2.setDuplicatesEnabled(False)
        self.sex_2.setObjectName(_fromUtf8("sex_2"))
        self.sex_2.addItem(_fromUtf8(""))
        self.sex_2.addItem(_fromUtf8(""))
        self.sex_2.addItem(_fromUtf8(""))
        self.sex_2.setItemText(2, _fromUtf8(""))
        self.gridLayout_2.addWidget(self.sex_2, 1, 1, 1, 1)
        self.label_19 = QtGui.QLabel(self.groupBox_2)
        self.label_19.setMinimumSize(QtCore.QSize(0, 30))
        self.label_19.setObjectName(_fromUtf8("label_19"))
        self.gridLayout_2.addWidget(self.label_19, 3, 2, 1, 1)
        self.cardid_2 = QtGui.QLineEdit(self.groupBox_2)
        self.cardid_2.setEnabled(True)
        self.cardid_2.setMinimumSize(QtCore.QSize(0, 30))
        self.cardid_2.setReadOnly(True)
        self.cardid_2.setObjectName(_fromUtf8("cardid_2"))
        self.gridLayout_2.addWidget(self.cardid_2, 0, 3, 1, 1)
        self.label_16 = QtGui.QLabel(self.groupBox_2)
        self.label_16.setMinimumSize(QtCore.QSize(0, 30))
        self.label_16.setObjectName(_fromUtf8("label_16"))
        self.gridLayout_2.addWidget(self.label_16, 1, 2, 1, 1)
        self.tel_2 = QtGui.QLineEdit(self.groupBox_2)
        self.tel_2.setEnabled(True)
        self.tel_2.setMinimumSize(QtCore.QSize(0, 30))
        self.tel_2.setReadOnly(True)
        self.tel_2.setObjectName(_fromUtf8("tel_2"))
        self.gridLayout_2.addWidget(self.tel_2, 1, 3, 1, 1)
        self.label_13 = QtGui.QLabel(self.groupBox_2)
        self.label_13.setMinimumSize(QtCore.QSize(0, 30))
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.gridLayout_2.addWidget(self.label_13, 0, 0, 1, 1)
        self.label_18 = QtGui.QLabel(self.groupBox_2)
        self.label_18.setMinimumSize(QtCore.QSize(0, 30))
        self.label_18.setObjectName(_fromUtf8("label_18"))
        self.gridLayout_2.addWidget(self.label_18, 2, 2, 1, 1)
        self.idcard_2 = QtGui.QLineEdit(self.groupBox_2)
        self.idcard_2.setEnabled(True)
        self.idcard_2.setMinimumSize(QtCore.QSize(0, 30))
        self.idcard_2.setReadOnly(True)
        self.idcard_2.setObjectName(_fromUtf8("idcard_2"))
        self.gridLayout_2.addWidget(self.idcard_2, 2, 3, 1, 1)
        self.label_17 = QtGui.QLabel(self.groupBox_2)
        self.label_17.setMinimumSize(QtCore.QSize(0, 30))
        self.label_17.setObjectName(_fromUtf8("label_17"))
        self.gridLayout_2.addWidget(self.label_17, 2, 0, 1, 1)
        self.label_23 = QtGui.QLabel(self.groupBox_2)
        self.label_23.setMinimumSize(QtCore.QSize(0, 30))
        self.label_23.setObjectName(_fromUtf8("label_23"))
        self.gridLayout_2.addWidget(self.label_23, 4, 0, 1, 1)
        self.lineEdit_2 = QtGui.QLineEdit(self.groupBox_2)
        self.lineEdit_2.setMinimumSize(QtCore.QSize(0, 30))
        self.lineEdit_2.setObjectName(_fromUtf8("lineEdit_2"))
        self.gridLayout_2.addWidget(self.lineEdit_2, 4, 1, 1, 1)
        self.label_12 = QtGui.QLabel(self.frame_2)
        self.label_12.setGeometry(QtCore.QRect(20, 10, 101, 31))
        self.label_12.setStyleSheet(_fromUtf8("font: 75 12pt \"黑体\";"))
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.groupBox_6 = QtGui.QGroupBox(self.frame_2)
        self.groupBox_6.setGeometry(QtCore.QRect(20, 50, 211, 191))
        self.groupBox_6.setObjectName(_fromUtf8("groupBox_6"))
        self.widget_2 = QtGui.QWidget(self.groupBox_6)
        self.widget_2.setGeometry(QtCore.QRect(20, 20, 171, 161))
        self.widget_2.setObjectName(_fromUtf8("widget_2"))
        self.groupBox_5 = QtGui.QGroupBox(self.frame_2)
        self.groupBox_5.setGeometry(QtCore.QRect(240, 50, 351, 191))
        self.groupBox_5.setObjectName(_fromUtf8("groupBox_5"))
        self.frame_1 = QtGui.QFrame(Dialog)
        self.frame_1.setGeometry(QtCore.QRect(0, 70, 1071, 241))
        self.frame_1.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_1.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_1.setObjectName(_fromUtf8("frame_1"))
        self.groupBox = QtGui.QGroupBox(self.frame_1)
        self.groupBox.setGeometry(QtCore.QRect(603, 40, 461, 191))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout = QtGui.QGridLayout(self.groupBox)
        self.gridLayout.setMargin(3)
        self.gridLayout.setSpacing(3)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.sex = QtGui.QComboBox(self.groupBox)
        self.sex.setEnabled(True)
        self.sex.setMinimumSize(QtCore.QSize(0, 30))
        self.sex.setEditable(True)
        self.sex.setDuplicatesEnabled(False)
        self.sex.setObjectName(_fromUtf8("sex"))
        self.sex.addItem(_fromUtf8(""))
        self.sex.addItem(_fromUtf8(""))
        self.sex.addItem(_fromUtf8(""))
        self.sex.setItemText(2, _fromUtf8(""))
        self.gridLayout.addWidget(self.sex, 1, 1, 1, 1)
        self.label_14 = QtGui.QLabel(self.groupBox)
        self.label_14.setMinimumSize(QtCore.QSize(0, 30))
        self.label_14.setObjectName(_fromUtf8("label_14"))
        self.gridLayout.addWidget(self.label_14, 0, 2, 1, 1)
        self.cardid = QtGui.QLineEdit(self.groupBox)
        self.cardid.setEnabled(True)
        self.cardid.setMinimumSize(QtCore.QSize(0, 30))
        self.cardid.setReadOnly(True)
        self.cardid.setObjectName(_fromUtf8("cardid"))
        self.gridLayout.addWidget(self.cardid, 0, 3, 1, 1)
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setMinimumSize(QtCore.QSize(0, 30))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.label_3 = QtGui.QLabel(self.groupBox)
        self.label_3.setMinimumSize(QtCore.QSize(0, 30))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.label_5 = QtGui.QLabel(self.groupBox)
        self.label_5.setMinimumSize(QtCore.QSize(0, 30))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 1, 2, 1, 1)
        self.membername = QtGui.QLineEdit(self.groupBox)
        self.membername.setEnabled(True)
        self.membername.setMinimumSize(QtCore.QSize(0, 30))
        self.membername.setReadOnly(True)
        self.membername.setObjectName(_fromUtf8("membername"))
        self.gridLayout.addWidget(self.membername, 0, 1, 1, 1)
        self.label_6 = QtGui.QLabel(self.groupBox)
        self.label_6.setMinimumSize(QtCore.QSize(0, 30))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout.addWidget(self.label_6, 2, 0, 1, 1)
        self.tel = QtGui.QLineEdit(self.groupBox)
        self.tel.setEnabled(True)
        self.tel.setMinimumSize(QtCore.QSize(0, 30))
        self.tel.setReadOnly(True)
        self.tel.setObjectName(_fromUtf8("tel"))
        self.gridLayout.addWidget(self.tel, 1, 3, 1, 1)
        self.nation = QtGui.QLineEdit(self.groupBox)
        self.nation.setEnabled(True)
        self.nation.setMinimumSize(QtCore.QSize(0, 30))
        self.nation.setReadOnly(True)
        self.nation.setObjectName(_fromUtf8("nation"))
        self.gridLayout.addWidget(self.nation, 2, 1, 1, 1)
        self.label_7 = QtGui.QLabel(self.groupBox)
        self.label_7.setMinimumSize(QtCore.QSize(0, 30))
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout.addWidget(self.label_7, 2, 2, 1, 1)
        self.idcard = QtGui.QLineEdit(self.groupBox)
        self.idcard.setEnabled(True)
        self.idcard.setMinimumSize(QtCore.QSize(0, 30))
        self.idcard.setReadOnly(True)
        self.idcard.setObjectName(_fromUtf8("idcard"))
        self.gridLayout.addWidget(self.idcard, 2, 3, 1, 1)
        self.label_9 = QtGui.QLabel(self.groupBox)
        self.label_9.setMinimumSize(QtCore.QSize(0, 30))
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.gridLayout.addWidget(self.label_9, 3, 0, 1, 1)
        self.amount = QtGui.QLineEdit(self.groupBox)
        self.amount.setEnabled(True)
        self.amount.setMinimumSize(QtCore.QSize(0, 30))
        self.amount.setReadOnly(True)
        self.amount.setObjectName(_fromUtf8("amount"))
        self.gridLayout.addWidget(self.amount, 3, 1, 1, 1)
        self.label_8 = QtGui.QLabel(self.groupBox)
        self.label_8.setMinimumSize(QtCore.QSize(0, 30))
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.gridLayout.addWidget(self.label_8, 3, 2, 1, 1)
        self.adder = QtGui.QLineEdit(self.groupBox)
        self.adder.setEnabled(True)
        self.adder.setMinimumSize(QtCore.QSize(0, 30))
        self.adder.setReadOnly(True)
        self.adder.setObjectName(_fromUtf8("adder"))
        self.gridLayout.addWidget(self.adder, 3, 3, 1, 1)
        self.label_22 = QtGui.QLabel(self.groupBox)
        self.label_22.setMinimumSize(QtCore.QSize(0, 30))
        self.label_22.setObjectName(_fromUtf8("label_22"))
        self.gridLayout.addWidget(self.label_22, 4, 0, 1, 1)
        self.lineEdit = QtGui.QLineEdit(self.groupBox)
        self.lineEdit.setMinimumSize(QtCore.QSize(0, 30))
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.gridLayout.addWidget(self.lineEdit, 4, 1, 1, 1)
        self.label_11 = QtGui.QLabel(self.frame_1)
        self.label_11.setGeometry(QtCore.QRect(23, 0, 101, 31))
        self.label_11.setStyleSheet(_fromUtf8("font: 75 12pt \"黑体\";"))
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.groupBox_4 = QtGui.QGroupBox(self.frame_1)
        self.groupBox_4.setGeometry(QtCore.QRect(243, 40, 351, 191))
        self.groupBox_4.setObjectName(_fromUtf8("groupBox_4"))
        self.groupBox_3 = QtGui.QGroupBox(self.frame_1)
        self.groupBox_3.setGeometry(QtCore.QRect(23, 40, 211, 191))
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.widget = QtGui.QWidget(self.groupBox_3)
        self.widget.setGeometry(QtCore.QRect(20, 20, 171, 161))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.webView = QtWebKit.QWebView(Dialog)
        self.webView.setGeometry(QtCore.QRect(441, 6, 0, 0))
        self.webView.setMaximumSize(QtCore.QSize(0, 0))
        self.webView.setUrl(QtCore.QUrl(_fromUtf8("about:blank")))
        self.webView.setObjectName(_fromUtf8("webView"))

        self.retranslateUi(Dialog)
        self.sex_2.setCurrentIndex(2)
        self.sex.setCurrentIndex(2)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "转账", None))
        self.label.setText(_translate("Dialog", "转出会员卡号：", None))
        self.label_4.setText(_translate("Dialog", "转入会员卡号：", None))
        self.label_10.setText(_translate("Dialog", "转账金额：", None))
        self.commandLinkButton_2.setText(_translate("Dialog", "转账下一步", None))
        self.groupBox_2.setTitle(_translate("Dialog", "基本资料", None))
        self.label_21.setText(_translate("Dialog", "会员卡号：", None))
        self.label_15.setText(_translate("Dialog", "性    别：", None))
        self.label_20.setText(_translate("Dialog", "可用余额：", None))
        self.sex_2.setItemText(0, _translate("Dialog", "女", None))
        self.sex_2.setItemText(1, _translate("Dialog", "男", None))
        self.label_19.setText(_translate("Dialog", "联系地址：", None))
        self.label_16.setText(_translate("Dialog", "联系电话：", None))
        self.label_13.setText(_translate("Dialog", "客户姓名：", None))
        self.label_18.setText(_translate("Dialog", "身 份 证：", None))
        self.label_17.setText(_translate("Dialog", "民    族：", None))
        self.label_23.setText(_translate("Dialog", "冻结余额：", None))
        self.label_12.setText(_translate("Dialog", "转入人信息", None))
        self.groupBox_6.setTitle(_translate("Dialog", "照片", None))
        self.groupBox_5.setTitle(_translate("Dialog", "身份证扫描件", None))
        self.groupBox.setTitle(_translate("Dialog", "基本资料", None))
        self.sex.setItemText(0, _translate("Dialog", "女", None))
        self.sex.setItemText(1, _translate("Dialog", "男", None))
        self.label_14.setText(_translate("Dialog", "会员卡号：", None))
        self.label_2.setText(_translate("Dialog", "客户姓名：", None))
        self.label_3.setText(_translate("Dialog", "性    别：", None))
        self.label_5.setText(_translate("Dialog", "联系电话：", None))
        self.label_6.setText(_translate("Dialog", "民    族：", None))
        self.label_7.setText(_translate("Dialog", "身 份 证：", None))
        self.label_9.setText(_translate("Dialog", "可用余额：", None))
        self.label_8.setText(_translate("Dialog", "联系地址：", None))
        self.label_22.setText(_translate("Dialog", "冻结余额：", None))
        self.label_11.setText(_translate("Dialog", "转出人信息", None))
        self.groupBox_4.setTitle(_translate("Dialog", "身份证扫描件", None))
        self.groupBox_3.setTitle(_translate("Dialog", "照片", None))

from PyQt4 import QtWebKit
